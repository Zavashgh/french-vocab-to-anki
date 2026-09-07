---
name: french-vocab-to-anki
description: >-
  Turn a list of French words, idioms, or expressions into detailed Anki
  flashcards (grammar, meaning, explanatory notes, two example sentences,
  translations) and export them as an Anki-importable TSV file. Use this skill
  whenever the user gives you a list of French words, idioms, expressions, or
  vocab and asks for Anki cards, flashcards, a vocab file, a vocabulary list,
  a lexicon, a word list, study cards, or spaced-repetition material. Trigger
  on phrasings like "make anki cards for this", "convert this list", "give me
  a vocab file", "make flashcards for these words", "turn this into a study
  deck", "add this to Anki", or simply a pasted/typed list of French words
  with no explicit request -- if it looks like a vocabulary list, offer to
  turn it into cards. Also trigger if they mention studying French vocabulary,
  building a French lexicon or glossary, or preparing words for spaced
  repetition. For explicitly requested raw lexicon entries (no Anki
  conversion), use the french-vocab-entries skill instead.
---

# French Vocabulary → Anki Cards

Converts a list of French words/expressions into rich, structured Anki
flashcards. Two-step pipeline: (1) generate detailed lexical entries in a
fixed intermediate format (kept internally, not shown to the user unless the
`french-vocab-entries` skill is what was actually asked for), (2) run the
bundled script to turn that into an Anki-ready TSV and report success/skip
counts.

## Session preferences

The first time this skill is used with a given user, ask:

> "Want translations in just English, or should I add a second language too
> (e.g. Spanish, Farsi, German)?"

Remember the answer for the rest of the conversation — don't ask again in the
same session. If the user has stated a standing preference before (e.g. "I
always want Farsi included," "always give me a TSV, never an APKG"), honor it
without re-asking, but don't assume any specific language, deck name, or
output format as a universal default for people who haven't said so — those
are per-user preferences, not skill defaults.

## Card content

Cover every unique requested item. Correct obvious spelling errors, normalize
base forms, and split accidentally joined independent expressions. Mention
any material corrections you made. Don't silently skip a difficult
grammar/idiom item, and don't add extra vocabulary cards nobody asked for.

### French expression / Front

- Verbs → infinitive. Nouns → singular with article (`un garçon`). Idioms →
  standard form.
- Capitalize the first letter.
- Keep grammar tags and pattern markers out of this field — if the input
  includes something like "suivre + nom", strip the pattern out of the front
  and fold it into Grammar/Details instead.
- Fixed sentence-formulas (e.g. a whole proverb) can stay as full sentences
  rather than being reduced to an uninformative base verb.

### Grammar / Details

Start with tags, in this order, semicolon-separated, including only the ones
that apply:
- Part of speech
- Gender / plural note (nouns)
- Pronominal-verb flag
- IPA pronunciation
- Transitive / intransitive / reflexive
- Register (formal / informal / neutral / slang)
- Passé composé auxiliary (avoir / être)
- Fixed formula or syntactic pattern (e.g. `avoir besoin de`, `suivre + nom`,
  `il n'est pas exclu que + subjonctif`)
- For an idiom/proverb, also give the **literal** meaning here (the natural
  meaning belongs in the Meaning field, not here).

**After the tags, add 2–4 short explanatory sentences.** This is the part
that makes these cards actually teach the pattern, not just label it:
- Identify the base verb and break down compound/pronominal/idiomatic parts.
- Explain what any pronoun refers to and *why* that preposition/construction
  is used — the reasoning, not just the rule.
- Point out a genuinely useful contrast with a similar-looking word or
  near-synonym when one exists. Don't invent a contrast just to fill space.
- Note real-world register/usage context when it's actually informative
  (e.g. "extremely common for confusing paperwork/bureaucracy") — don't make
  up frequency claims you can't support.

If a second language was requested and the item is genuinely tricky, a short
clarification in that language can go at the end of Details, above Meaning —
kept distinct from the Meaning field's translation, not a duplicate of it.

### Meaning

Natural, contextual meaning in English. If a second language was requested,
append it after an en dash: `"English meaning – [second language] meaning"`.
Use the closest natural equivalent, not a word-for-word gloss — paraphrase if
there's no exact match. For idioms/proverbs, give the practical/idiomatic
message, not just a repeat of the literal translation from Details.

### Two examples

Two full, natural French sentences in different contexts, each demonstrating
the taught sense, each with a translation matching the Meaning field's
language setup. If the word came from a dialogue/text the user shared earlier
in the conversation, prefer an example that echoes that context for at least
one of the two. Extra grammar explanation can go beyond a single textbook
page's material — but don't spin unrelated vocabulary from an example
sentence into new unsolicited cards.

## Back field layout

```html
<b>Grammar / Details:</b><br>
[tags + explanatory sentences]<br><br>
<b>Meaning:</b><br>
[Meaning]<br><br>
<b>Example 1:</b><br>
[Example 1 in French]<br>
[Translation of Example 1]<br><br>
<b>Example 2:</b><br>
[Example 2 in French]<br>
[Translation of Example 2]
```

Don't change this layout unless the user asks — it renders cleanly in Anki's
card viewer.

## File workflow

For a batch, build an internal entries file: one line per item, seven
double-quoted fields separated by ` ; `, one blank line between entries:

```
"French expression" ; "Grammar / Details" ; "Meaning" ; "Example 1 in French" ; "Translation of example 1" ; "Example 2 in French" ; "Translation of example 2"
```

This entries file is **internal working state**, not something to hand the
user — that's the separate `french-vocab-entries` skill's job if that's what
they actually asked for.

Run the bundled script, relative to this skill's own directory:

```bash
python scripts/convert_to_anki.py <entries.txt> <output_prefix>
```

This produces:
- `<output_prefix>_anki_basic.tsv` — import into Anki as note type **Basic**,
  Field 1 → Front, Field 2 → Back
- `<output_prefix>_skipped_lines.txt` — malformed-entry report (empty if
  none). If something was skipped, fix and rerun before treating it as final.

### What to present to the user

- **Only present the `.tsv` file** by default. Don't present the entries
  `.txt` — that's internal, unless the user explicitly asked for the raw
  entries too (in which case, consider whether they actually meant to invoke
  `french-vocab-entries` instead).
- **Always state, in your message, how many entries succeeded and how many
  were skipped.** e.g. "12 of 12 cards created successfully." or "10 of 12
  cards created — 2 were skipped, see below."
- **Only attach the skipped-lines file if the skipped count is > 0.** If
  nothing was skipped, just say "0 skipped" — don't mention or attach that
  file at all.
- If something was skipped, briefly say why in your message too, not just in
  the attached file.

## Optional: images and illustrated packages

Some users like an illustrated deck (one relevant image per card) delivered
as a full Anki `.apkg` package instead of a plain TSV. This is **not** the
default — only do it if the user asks for illustrations or an APKG package,
or has told you that's their standing preference for this deck.

If requested:
- Depict the contextual meaning clearly; for abstract expressions, illustrate
  a concrete situation rather than a misleading literal picture of an idiom.
- Use whatever image-generation or image-search tool is available in your
  current environment — don't assume a specific local script or file path
  exists. If you need to build or reuse an APKG-packaging script, write one
  fresh into this skill's own `scripts/` directory (or ask the user for
  their existing one if they say they have one) rather than assuming a path
  on their machine.
- When updating **existing** Anki cards rather than creating new ones,
  preserve note GUIDs, note/card IDs, note-type identity, scheduling state,
  and review logs — modify only the requested content/media/layout, and
  never regenerate identities or clear review history. If you don't have
  access to the actual source export, say so rather than claiming history
  was preserved.
- Report image count and any unresolved image/media issues alongside the
  normal success/skip counts.

## Verification before handoff

- Reconcile input count vs. entries generated vs. cards produced.
- Spot-check French accuracy and that the explanatory layer in Grammar/
  Details is actually explaining something, not just repeating tags.
- Deliver only what was asked for (TSV, or APKG if requested) — don't expose
  the internal entries file or build scripts unless asked.
