#!/usr/bin/env python3
"""
Convert a semicolon-delimited French vocabulary entries file into:
  1. An Anki-importable TSV file (Basic note type: Front / Back)
  2. A skipped-lines report

Input format (one entry per paragraph, separated by a blank line):

"French Expression" ; "Grammar / Details" ; "Meaning" ; "Example 1 (FR)" ; "Example 1 translation" ; "Example 2 (FR)" ; "Example 2 translation"

Usage:
    python convert_to_anki.py <input.txt> [output_prefix]

If output_prefix is omitted, it defaults to the input filename (without extension).
Produces:
    <prefix>_anki_basic.tsv
    <prefix>_skipped_lines.txt
"""

import re
import sys
import os


def convert(input_path: str, output_prefix: str | None = None):
    if output_prefix is None:
        output_prefix = os.path.splitext(input_path)[0]

    output_tsv = f"{output_prefix}_anki_basic.tsv"
    output_skipped = f"{output_prefix}_skipped_lines.txt"

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    raw_entries = [e.strip() for e in re.split(r"\n\s*\n", content) if e.strip()]

    tsv_lines = []
    skipped = []

    for i, entry in enumerate(raw_entries, 1):
        fields = re.findall(r'"((?:[^"\\]|\\.)*)"', entry)

        if len(fields) != 7:
            skipped.append(
                f"Entry {i}: Expected 7 fields, found {len(fields)} — {entry[:80]}..."
            )
            continue

        french_expr, grammar, meaning, ex1_fr, ex1_trans, ex2_fr, ex2_trans = fields

        back = (
            f"<b>Grammar / Details:</b><br>{grammar}<br><br>"
            f"<b>Meaning:</b><br>{meaning}<br><br>"
            f"<b>Example 1:</b><br>{ex1_fr}<br>{ex1_trans}<br><br>"
            f"<b>Example 2:</b><br>{ex2_fr}<br>{ex2_trans}"
        )

        front = french_expr.replace("\t", " ")
        back = back.replace("\t", " ")
        tsv_lines.append(f"{front}\t{back}")

    with open(output_tsv, "w", encoding="utf-8") as f:
        f.write("\n".join(tsv_lines))

    with open(output_skipped, "w", encoding="utf-8") as f:
        if skipped:
            f.write("\n".join(skipped))
        else:
            f.write("No skipped lines — all entries processed successfully!")

    print(f"Done! {len(tsv_lines)} entries written to {output_tsv}.")
    print(f"Skipped: {len(skipped)} (see {output_skipped})")
    return output_tsv, output_skipped, len(tsv_lines), len(skipped)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_to_anki.py <input.txt> [output_prefix]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else None
    convert(input_path, output_prefix)
