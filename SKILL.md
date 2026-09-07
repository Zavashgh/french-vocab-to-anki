---
name: french-vocab-to-anki
description: >-
  Create or revise French Anki vocabulary cards with explanatory grammar details,
  English and Farsi meanings, examples, and optional illustrations. Deliver APKG
  packages, TSV exports, or paste-ready card text as requested. Use for French
  vocabulary lists intended for Anki, illustrated batches, and edits to French
  cards. In an established Anki workflow, treat a new vocabulary list as the next
  batch. For explicitly requested raw lexicon entries, use french-vocab-entries.
---

# French Vocabulary → Anki Cards

## Saved preferences

These are Zavosh's established preferences, not universal requirements for other
users. Apply them without asking again unless the current request changes them.

- New vocabulary batches: deliver an illustrated **APKG**, with **new cards** that
  can be added to the existing **French Vocabulary** deck. Use compatible **Basic**
  Front/Back fields where the existing note type supports them.
- Include English and **natural Farsi** in Meaning and both example translations.
  Choose the closest contextual meaning, not a word-for-word approximation.
- Include one relevant image per card on the **back, below Meaning and above
  Example 1**.
- Keep Grammar / Details tags first, then add **2–4 explanatory sentences**.
- The user normally generates audio with AwesomeTTS/Microsoft. Do not generate
  audio by default. Preserve available audio when editing cards.
- Merge exact duplicates within a batch and report the merge. Keep distinct items
  such as a base verb and an expression using it as separate cards.
- A separate test deck or an update of old cards is a different mode; follow the
  user's choice rather than treating every package as new cards.

## Match the requested output

- **New list in the established workflow:** complete the next illustrated APKG
  batch without merely offering to make it or repeating preference questions.
- **Paste-ready correction:** return the revised card directly using the requested
  labels and paragraph breaks. No file or image generation is needed unless asked.
  Preserve supplied media references when relevant; flag existing audio that may
  no longer match changed text rather than silently replacing it.
- **Text-only or TSV request:** deliver TSV through the bundled converter.
  TSV alone does not embed images.
- **Explicit raw entries request:** use french-vocab-entries.
- **Existing-card update:** follow the identity/progress rules below.

Creating a package does not authorize importing into or modifying live Anki.
Work on copies of exports unless live changes are requested.

## Card content

Cover every unique requested item. Correct obvious spelling errors, normalize base
forms, and split accidentally joined independent expressions. Report material
corrections or ambiguous interpretations. Do not silently omit difficult grammar
patterns or add unsolicited vocabulary cards.

### French expression / Front

Use infinitives for verbs, singular nouns with articles, and standard idiom forms.
Capitalize the first letter. Keep grammar tags out of Front. Put argument patterns
in Details when normalizing Front, but preserve enough wording to distinguish the
requested construction from other cards. Fixed sentence formulas may remain
sentences rather than being reduced to an uninformative base verb.

### Grammar / Details

Start with applicable tags, in the established order, separated by semicolons:
part of speech; gender/plural; pronominal flag; IPA; transitivity; register;
passé composé auxiliary; fixed formula/syntactic pattern; relevant notes.
For an idiom or proverb, give literal English and Farsi meanings here.
Do not call a whole construction "invariable" just because it is a fixed phrase.

After the tags, write **2–4 short explanatory sentences**:

- Identify the base verb and break down compound, pronominal, or idiomatic parts.
- Explain what pronouns refer to and why the preposition or construction is used.
- Teach reusable patterns, not only the translation of a single collocation.
- Explain useful contrasts with similar-looking words or near-synonyms where
  relevant. Do not invent contrasts just to fill space.
- Describe tone and real usage contexts when useful; avoid unsupported frequency
  claims. Explain grammatical triggers rather than only naming a mood.

For a complicated item, add a brief, natural Farsi clarification at the end of
Details, above Meaning. Keep it distinct from the translation.

### Meaning

Give the natural contextual English meaning, followed by an en dash and the closest
natural Farsi equivalent. Use a brief paraphrase if no exact equivalent exists.
Prioritize the intended sense over unrelated dictionary senses.

For idioms/proverbs, explain the practical message or idiomatic meaning rather than
only repeating the literal translation. Do not invent a figurative meaning because
the user finds a literal translation unhelpful. Verify uncertain usage with reliable
dictionaries or other primary language references.

### Two examples

Give two full, natural French sentences in different contexts, each followed by
idiomatic English and natural Farsi translations. Both must use the target
expression and demonstrate the taught sense. Prefer one example echoing the source
dialogue when available. Let the situation clarify an idiom's intended meaning.
Grammar explanations can extend beyond the book; do not turn extra illustrative
vocabulary into unsolicited cards.

## Back layout

Keep these exact visible labels and this order. For paste-ready text, use bold
labels with paragraph breaks. Images can be embedded in the individual Back field;
a separate Image field is not required for this user's Basic cards.

```html
<b>Grammar / Details:</b><br>
[tags, explanation, optional Farsi clarification]<br><br>
<b>Meaning:</b><br>
[English – Farsi]<br><br>
[illustration, when included]<br><br>
<b>Example 1:</b><br>
[French]<br>
[English – Farsi]<br><br>
<b>Example 2:</b><br>
[French]<br>
[English – Farsi]
```

Use responsive image sizing and preserve aspect ratio. Embed images in the selected
notes so the change need not affect other decks sharing the same Basic note type.

## Images

- Depict the contextual meaning clearly. For abstract expressions, show a concrete
  situation. Avoid misleading literal pictures of idioms.
- Generated illustrations are accepted. Suitable internet images are also accepted
  to save time/cost, with generation for difficult concepts. Choose efficiently
  without asking for the same preference on every batch.
- Use the available image-generation skill/tool when generating. Prefer reusable/
  licensed sources for downloaded images and keep source/license records internally.
  Download actual image assets; do not depend on remote hotlinks.
- Contact sheets can reduce generation overhead when supported. Maintain an ordered
  item-to-cell mapping, inspect the sheet, crop into individual assets, and verify
  every crop matches its card and contains no neighboring panel.
- Bundle media inside APKG with unique filenames and valid references. Check visual
  quality and semantic relevance, not just file existence. Repair missing or
  mismatched images or clearly disclose unresolved limitations.
- Reuse existing images for layout/text-only updates. Moving images below Meaning
  does not require regeneration or new card identities.

## File workflow

For a batch, create an internal UTF-8 entries file. Each entry is one line with
seven double-quoted fields separated by ` ; `, with a blank line between entries:

```text
"French expression" ; "Grammar / Details" ; "Meaning" ; "French example 1" ; "English – Farsi translation 1" ; "French example 2" ; "English – Farsi translation 2"
```

Run the bundled converter relative to this skill directory:

```text
python scripts/convert_to_anki.py <entries.txt> <output_prefix>
```

It produces `<output_prefix>_anki_basic.tsv` and a skipped-lines report. Repair
malformed entries and rerun before treating them as skipped. Keep the entries and
intermediate TSV internal when the final deliverable is APKG.

For APKG, use a compatible Anki package library or inspect and reuse existing local
resources where available. Previous implementations are in
`C:/Users/Zavosh/Documents/Codex/2026-08-03/yes/`:

- `build_illustrated_anki_new_cards.py`: new-card builder accepting template APKG,
  two-column TSV, numbered JPG directory, output APKG, media prefix, and deck name.
- `verify_batch2_apkg.py`: checks text, media, placement, and new-card identities.

These are optional local resources, not portable dependencies. Inspect before reuse:
the builder expects a specific legacy export structure, and the verifier has
user-specific hard-coded identities. Do not assume any APKG matches them. Use an
appropriate implementation when unavailable/incompatible. These helpers must not
be used unmodified to update reviewed cards.

## New cards versus updates

**New cards:** fresh note GUIDs and note/card IDs, with no review history. Use the
intended deck and compatible note type from an inspected template when available.
Matching display names alone do not guarantee matching identities. New-card
scheduling is expected only for genuinely new cards.

**Separate test deck:** explicitly distinct deck name/identity and fresh notes/cards.
Explain that test copies start as new cards.

**Existing-card updates:** use the actual source export or an authorized, inspected
live connection. Preserve note GUIDs, note/card IDs, note-type identity, scheduling
state, and review logs. Modify only requested content, media, or layout in a copy.
Never clear review tables or regenerate identities. Request a missing source if
needed rather than claiming to preserve unavailable history.

Import behavior depends on Anki version, matching, modification dates, and update
options. Verify current behavior before prescribing settings. Distinguish retaining
history in an export from verified retention in live Anki. Avoid overwriting newer
live progress with stale exported scheduling or replacing deck presets unnecessarily.
A filename such as UPDATE_EXISTING does not guarantee correct matching.

Preserve available audio/media during updates. If the source excludes media, explain
the limitation. The user has accepted regenerating audio, but do not silently
discard available media.

## Verification and handoff

- Reconcile input count, duplicate merges, unique entries, cards, and illustrations.
- Check French accuracy, natural Farsi, complete fields, useful examples, and the
  explanatory layer. Verify package/database integrity, media references, and
  placement. Inspect representative rendered backs.
- For new packages, verify fresh identities and new-card scheduling. For updates,
  compare identities, scheduling, and review records with the source.
- Deliver only the requested final APKG, TSV, or paste-ready card text. Do not expose
  internal entries/build scripts/intermediates unless requested.
- For file batches, report created/updated count, image count, duplicate merges,
  skipped count, and material limitations. Link a skipped report only if unresolved
  skipped entries remain. Clearly distinguish new cards from updates.
- Give import instructions only when needed. Do not claim a live import or live
  history preservation was tested unless it actually was.
