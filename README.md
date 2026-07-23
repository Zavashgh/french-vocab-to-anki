# french-vocab-to-anki

A Claude skill that turns a list of French words, idioms, or expressions into rich, structured Anki flashcards — grammar details, IPA, register, meaning, and two example sentences per word — and exports them as an Anki-importable file.

## What it does

Give Claude a list of French vocabulary (single words, idioms, fixed expressions — anything), and this skill will:

1. Generate a detailed entry for each item: part of speech, IPA pronunciation, register (formal/informal/slang), auxiliary verb for passé composé, fixed grammatical patterns, meaning, and two natural example sentences with translations.
2. Convert that into a ready-to-import Anki `.tsv` file (Basic note type: Front = French expression, Back = full formatted entry).
3. Report how many cards were created successfully and how many were skipped (with a skipped-lines file attached only if something was actually skipped).

By default translations are in English only. You can ask for a second language too (e.g. Spanish, German, Farsi) — Claude will ask once per conversation and remember your preference.

> The intermediate plain-text entries (the raw `"field" ; "field" ; ...` format) are generated internally but not handed to you by this skill — that's the job of a separate, upcoming `french-vocab-entries` skill for people who want the raw lexicon file on its own.

## Example

**Input:**
```
Se débrouiller
Avoir la flemme
```

**Output:** a ready-to-import `entries_anki_basic.tsv` file — a two-column TSV with a nicely formatted HTML back side (Grammar / Meaning / Example 1 / Example 2) — plus a chat message like:

> "2 of 2 cards created successfully, 0 skipped."

## Installation

### Claude.ai / Claude apps
Upload the `.skill` file (or this folder) and click **Save skill** to install it into your profile.

### Claude Code / Cowork
Drop this folder into your skills directory, or point Claude at it and ask it to use the `french-vocab-to-anki` skill.

## Usage

Just paste or type a list of French words/expressions and ask for Anki cards:

> "Make anki cards for this list: ..."
> "Convert this list to a vocab file"
> "Give me flashcards for these idioms"

The first time in a conversation, Claude will ask whether you want a second language included alongside English. After that it won't ask again.

### Importing into Anki

1. Anki → **File → Import** → select the `.tsv` file
2. Note type: **Basic**
3. Field 1 → **Front**, Field 2 → **Back**
4. Import

## Repo structure

```
french-vocab-to-anki/
├── SKILL.md                    # skill instructions (entry format, workflow)
└── scripts/
    └── convert_to_anki.py      # deterministic txt → Anki TSV converter
```

## Running the converter manually

You don't need Claude to run the conversion step — it's a plain Python script:

```bash
python scripts/convert_to_anki.py entries.txt output_prefix
```

Produces `output_prefix_anki_basic.tsv` and `output_prefix_skipped_lines.txt` (a report of any malformed entries).

## License

MIT — do whatever you want with it.
