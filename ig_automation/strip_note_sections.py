#!/usr/bin/env python3
"""Remove the `## Transcript` and `## On screen text` sections from the posts' `_description.md` notes, and nothing else.

Since 2026-10-14 describe.py writes notes without them; the text stays in `<audio>_transcript.txt` and
`<base>_ocr.txt` next to the note. This cleans notes written before that, or restored from a backup.
Dry run unless --apply.

A section is only removed when its text matches the post's own file exactly, so a note that was edited by
hand is left alone and listed.
"""

import argparse
import sys
from pathlib import Path

from download import IG_DIR

# Heading, and the files in the post folder whose text the section must match.
SECTIONS = {"Transcript": "*_transcript.txt", "On screen text": "*_ocr.txt"}


def strip_section(text: str, heading: str, sources: list) -> tuple[str, str]:
    """The note without that section, and 'removed', 'none' or 'mismatch'.

    The heading plus a source file's exact text is removed, so text that itself holds a `## ` line (OCR of a
    slide with headings) is still removed whole.
    """
    marker = f"\n## {heading}\n"
    if marker not in text:
        return text, "none"
    for source in sources:
        block = f"{marker}\n{source}\n" if source else None
        if block and block in text:
            return text.replace(block, "", 1), "removed"
    return text, "mismatch"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ig-dir", type=Path, default=IG_DIR, help=f"Folder with one subfolder per post. Default: {IG_DIR}")
    parser.add_argument("--apply", action="store_true", help="Change the notes. Without it, only count them.")
    args = parser.parse_args()

    notes = sorted(args.ig_dir.glob("*/*_description.md"))
    removed = {heading: 0 for heading in SECTIONS}
    changed = 0
    mismatched = []
    for note in notes:
        text = new = note.read_text(encoding="utf-8")
        for heading, pattern in SECTIONS.items():
            sources = [f.read_text(encoding="utf-8").strip() for f in note.parent.glob(pattern)]
            new, result = strip_section(new, heading, sources)
            if result == "removed":
                removed[heading] += 1
            elif result == "mismatch":
                mismatched.append(f"{heading}: {note}")
        if new != text:
            changed += 1
            if args.apply:
                note.write_text(new, encoding="utf-8")

    action = "Changed" if args.apply else "Would change (dry run, add --apply)"
    counts = ", ".join(f"{heading} {n}" for heading, n in removed.items())
    print(f"Notes: {len(notes)} | sections removed: {counts} | {action}: {changed} notes")
    for line in mismatched:
        print(f"  left alone, section does not match its file: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
