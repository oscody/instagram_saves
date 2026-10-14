#!/usr/bin/env python3
"""Remove the `## Transcript` section from the posts' `_description.md` notes, and nothing else.

Since 2026-10-14 describe.py writes notes without the transcript; it stays in `<audio>_transcript.txt`. This
cleans notes written before that, or restored from a backup. Dry run unless --apply.

A section is only removed when its text matches one of the post's `_transcript.txt` files exactly, so a note
that was edited by hand is left alone and listed.
"""

import argparse
import sys
from pathlib import Path

from download import IG_DIR

HEADING = "\n## Transcript\n"


def strip(text: str, transcripts: list) -> str | None:
    """The note without its transcript section, or None when there is none or it does not match a transcript."""
    start = text.find(HEADING)
    if start < 0:
        return None
    body_start = start + len(HEADING)
    nxt = text.find("\n## ", body_start)
    end = nxt if nxt >= 0 else len(text.rstrip("\n"))
    if text[body_start:end].strip() not in transcripts:
        return None
    return text[:start] + (text[end:] if nxt >= 0 else "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ig-dir", type=Path, default=IG_DIR, help=f"Folder with one subfolder per post. Default: {IG_DIR}")
    parser.add_argument("--apply", action="store_true", help="Change the notes. Without it, only count them.")
    args = parser.parse_args()

    notes = sorted(args.ig_dir.glob("*/*_description.md"))
    with_section = stripped = 0
    mismatched = []
    for note in notes:
        text = note.read_text(encoding="utf-8")
        if HEADING not in text:
            continue
        with_section += 1
        transcripts = [t.read_text(encoding="utf-8").strip() for t in note.parent.glob("*_transcript.txt")]
        new = strip(text, transcripts)
        if new is None:
            mismatched.append(note)
            continue
        stripped += 1
        if args.apply:
            note.write_text(new, encoding="utf-8")

    action = "Removed" if args.apply else "Would remove (dry run, add --apply)"
    print(f"Notes: {len(notes)} | with a transcript section: {with_section} | {action}: {stripped}")
    for note in mismatched:
        print(f"  left alone, section does not match a transcript file: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
