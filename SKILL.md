---
name: french-vocab-to-anki
description: >-
  Turn a list of French words, idioms, or expressions into detailed Anki flashcards
  (grammar, meaning, two example sentences, translations) and export them as an
  Anki-importable TSV file. Use this skill whenever the user gives you a list of
  French words, idioms, expressions, or vocab and asks for Anki cards, flashcards,
  a vocab file, a vocabulary list, a lexicon, a word list, study cards, or
  spaced-repetition material. Trigger on phrasings like "make anki cards for this",
  "convert this list", "give me a vocab file", "make flashcards for these words",
  "turn this into a study deck", "add this to Anki", or simply a pasted/typed list
  of French words with no explicit request -- if it looks like a vocabulary list,
  offer to turn it into cards. Also trigger if they mention studying French
  vocabulary, building a French lexicon or glossary, or preparing words for
  spaced repetition.
---

# French Vocabulary → Anki Cards

Converts a list of French words/expressions into rich, structured Anki flashcards. Two-step pipeline: (1) generate detailed lexical entries in a fixed intermediate format (kept internally, not shown to the user), (2) run the bundled script to turn that into an Anki-ready TSV and report success/skip counts.

## When to use this

Trigger whenever the user:
- Pastes or lists French words, idioms, expressions, or sentences and asks for Anki cards / flashcards
- Says something like "make anki cards for this", "convert this list", "give me a vocab file"
- Asks to review or extract vocabulary from a French text/dialogue and wants it turned into cards

## Step 1 — Ask about the second language (once per conversation)

By default, entries are **English-only**. The first time this skill triggers in a conversation, ask:

> "Want translations in just English, or should I add a second language too (e.g. Spanish, Farsi, German)?"

Remember the answer for the rest of the conversation — never ask again in the same session, even if the user sends more lists later. Just keep applying whatever they said the first time.

## Step 2 — Generate the entries file

For **every** item in the user's list, produce one entry using **exactly** this structure and punctuation. Each entry is a single line, fields separated by ` ; `, each field wrapped in double quotes. Leave one blank line between entries.

```
"French expression" ; "Grammar / Details" ; "Meaning" ; "Example 1 in French" ; "Translation of example 1" ; "Example 2 in French" ; "Translation of example 2"
```

### Field 1 — French expression
- Base form only: verbs → infinitive, nouns → singular with article (`un garçon`), idioms → standard form.
- Capitalize the first letter.
- Nothing else goes in this field — no grammar tags, no parenthetical notes. If the input includes a pattern marker like "suivre + nom", strip it out of field 1 and fold it into field 2 as the fixed formula instead.

### Field 2 — Grammar / Details
Pack in, in this order, whichever apply (semicolon-separated inside the field):
- Part of speech
- Gender (nouns) / plural note if relevant
- Pronominal form flag if reflexive
- IPA pronunciation
- Transitive/intransitive/reflexive
- Register (formal/informal/neutral/slang)
- Passé composé auxiliary (avoir/être)
- Fixed formula or syntactic pattern (e.g. `avoir besoin de`, `suivre + nom`, `il n'est pas exclu que + subjonctif`)
- Notes (figurative use, invariable, idiomatic literal meaning, etc.)
- If the entry is an idiom/proverb/fixed phrase, also give its **literal** meaning here (not the natural meaning — that belongs in field 3).

### Field 3 — Meaning
Natural, idiomatic meaning(s) in English. Format: `"meaning – meaning2"` if there are close synonyms worth listing.
If a second language was requested, append it after an en dash: `"English meaning – [second language] meaning"`.

### Fields 4–7 — Two full example sentences
- Field 4: French example sentence 1 (uses the expression naturally, ideally reflecting real usage/context if the word came from a specific dialogue).
- Field 5: its translation. English only, or `"English – [second language]"` if a second language was requested.
- Field 6: French example sentence 2 (different context from example 1).
- Field 7: its translation, same format as field 5.

### Rules
- Always try to reflect real, natural usage — if the word came from a dialogue/text the user shared earlier in the conversation, prefer an example that echoes that context for at least one of the two examples.
- Never skip a field. If something is genuinely inapplicable (e.g. no plural note needed), just omit that sub-item from field 2 rather than leaving a field empty.
- Save the entries as a working `.txt` file on disk (needed as input for Step 3), but this file is **internal only** — do not present it or link to it for the user to download. Only the final Anki TSV (and, if needed, the skipped-lines report) get shown to the user.

## Step 3 — Convert to Anki TSV

Run the bundled script on the entries file:

```bash
python scripts/convert_to_anki.py <entries.txt> <output_prefix>
```

This produces:
- `<output_prefix>_anki_basic.tsv` — import into Anki as note type **Basic**, Field 1 → Front, Field 2 → Back
- `<output_prefix>_skipped_lines.txt` — a report of any malformed entries (empty file if none)

### What to present to the user

- **Only present the `.tsv` file.** Do not present or link to the entries `.txt` file — that's an internal working file only (a future separate skill will handle giving the user the raw entries file).
- **Always state, in your message, how many entries succeeded and how many were skipped.** e.g. "12 of 12 cards created successfully." or "10 of 12 cards created — 2 were skipped, see below."
- **Only present the `_skipped_lines.txt` file if the skipped count is greater than 0.** If nothing was skipped, don't mention or attach that file at all — just report "0 skipped" in the message.
- If anything was skipped, briefly say why (from the skipped-lines report) in your message as well as attaching the file, rather than making the user open the file to find out.

## Step 4 — Anki import reminder (only needed once per user, skip if already told them)

1. Anki → File → Import → select the `.tsv`
2. Note type: **Basic**
3. Field 1 → Front, Field 2 → Back
4. Import

## Notes on the Back field format

The script wraps grammar/meaning/examples into this HTML layout for the Back field:

```html
<b>Grammar / Details:</b><br>
[Grammar / Details] <br><br>
<b>Meaning:</b><br>
[Meaning] <br><br>
<b>Example 1:</b><br>
[Example 1 in French]<br>
[Translation of Example 1] <br><br>
<b>Example 2:</b><br>
[Example 2 in French]<br>
[Translation of Example 2]
```

Don't change this layout unless the user asks — it's designed to render cleanly in Anki's card viewer.
