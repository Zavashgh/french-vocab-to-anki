# french-vocab-to-anki

A Claude skill that turns a list of French words, idioms, or expressions into rich, structured Anki flashcards — grammar details, IPA, register, an explanatory teaching layer, meaning, and two example sentences per word — and exports them as an Anki-importable file.

## What it does

Give Claude a list of French vocabulary (single words, idioms, fixed expressions — anything), and this skill will:

1. Generate a detailed entry for each item: part of speech, IPA pronunciation, register (formal/informal/slang), auxiliary verb for passé composé, fixed grammatical patterns, **2–4 sentences explaining the pattern/reasoning (not just labeling it)**, meaning, and two natural example sentences with translations.
2. Convert that into a ready-to-import Anki `.tsv` file (Basic note type: Front = French expression, Back = full formatted entry).
3. Report how many cards were created successfully and how many were skipped (with a skipped-lines file attached only if something was actually skipped).

By default translations are in English only. You can ask for a second language too (e.g. Spanish, German, Farsi) — Claude will ask once per conversation and remember your preference for that session. If you tell Claude a standing preference (e.g. "always include Farsi for me"), it can carry that forward without asking each time — but that's *your* preference, not a default baked into the skill for everyone.

> The intermediate plain-text entries (the raw `"field" ; "field" ; ...` format) are generated internally but not handed to you by this skill — that's the job of the separate [`french-vocab-entries`](https://github.com/Zavashgh/french-vocab-entries) skill, for people who want the raw lexicon file on its own.

## Optional: illustrated Anki packages (APKG)

If you ask for it, Claude can also produce an illustrated `.apkg` deck (one image per card) instead of a plain TSV. This isn't the default — a plain TSV has no dependency on image generation and works everywhere. If you want illustrations, say so explicitly, or tell Claude it's your standing preference for a given deck.

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

The first time in a conversation, Claude will ask whether you want a second language included alongside English. After that it won't ask again in that session.

### Importing into Anki

1. Anki → **File → Import** → select the `.tsv` file
2. Note type: **Basic**
3. Field 1 → **Front**, Field 2 → **Back**
4. Import

## Repo structure

```
french-vocab-to-anki/
├── LICENSE
├── README.md
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

## A note on personalizing this for yourself

The skill instructions here are written to work for anyone. If you have your own standing preferences (a specific deck name, always wanting a second language, always wanting illustrated APKGs, a personal image-generation pipeline you already have set up), keep those as your own local notes/instructions layered on top rather than editing the shared SKILL.md to hardcode them — that keeps this repo usable for other people who install it too.

## License

MIT — do whatever you want with it.
