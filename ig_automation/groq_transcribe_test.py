#!/usr/bin/env python3
"""Test Groq's hosted Whisper on reels that already have a local faster-whisper transcript.

Read only: it never writes iambogle.json or the IG/ folders, so it is safe while the pipeline runs.
Groq's transcripts go to output/groq_test/<shortcode>_groq.txt, next to a copy of the local one,
and each reel logs the time taken and how closely the two transcripts match.

The API key comes from GROQ_API_KEY, or the `groq=` line in ig_automation/.env.
"""

import argparse
import difflib
import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

from download import DEFAULT_JSON, IG_DIR, post_dir
from export_chat_links import SENT_AT_FORMAT
from transcribe import GROQ_MAX_UPLOAD, audio_name, groq_key, groq_transcribe, transcript_path

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_groq_test")

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "output" / "groq_test"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help=f"Export file to read. Default: {DEFAULT_JSON}")
    parser.add_argument("--ig-dir", type=Path, default=IG_DIR, help=f"Folder with one subfolder per post. Default: {IG_DIR}")
    parser.add_argument("--limit", type=int, default=5, help="Test at most N reels, newest first. Default: 5")
    parser.add_argument("--shortcode", action="append", help="Only test this reel. Can be given more than once.")
    parser.add_argument(
        "--model",
        default="whisper-large-v3-turbo",
        help="Groq model: whisper-large-v3-turbo (faster) or whisper-large-v3. Default: whisper-large-v3-turbo",
    )
    parser.add_argument("--language", default=None, help="Force a language code (e.g. en). Default: auto-detect.")
    return parser.parse_args()


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def main() -> int:
    args = parse_args()
    key = groq_key()
    if not key:
        raise RuntimeError("No Groq API key: set GROQ_API_KEY or add groq=<key> to ig_automation/.env")
    records = sorted(
        json.loads(args.json.read_text())["links"],
        key=lambda r: datetime.strptime(r["sent_at"], SENT_AT_FORMAT),
        reverse=True,
    )
    if args.shortcode:
        records = [r for r in records if r["shortcode"] in args.shortcode]
    # Only reels with a local transcript, so there is something to compare with.
    todo = [r for r in records if r.get("transcribed") and audio_name(r) and transcript_path(r, args.ig_dir).exists()]
    todo = todo[:args.limit]
    logger.info(f"{len(todo)} reels to test with Groq {args.model}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    audio_total = groq_total = 0.0
    scores = []
    failed = 0
    for index, record in enumerate(todo, start=1):
        code = record["shortcode"]
        audio = post_dir(args.ig_dir, record) / audio_name(record)
        local = transcript_path(record, args.ig_dir).read_text(encoding="utf-8").strip()
        logger.info(f"[{index}/{len(todo)}] {code} ({audio.stat().st_size / 1e6:.1f} MB)")
        if audio.stat().st_size > GROQ_MAX_UPLOAD:
            logger.warning("  ✗ over Groq's 25 MB upload limit, skipped")
            failed += 1
            continue
        try:
            started = time.monotonic()
            result, _ = groq_transcribe(key, audio, args.model, args.language)
            took = time.monotonic() - started
        except (RuntimeError, requests.RequestException) as exc:
            logger.warning(f"  ✗ {exc}")
            failed += 1
            continue
        text = (result.get("text") or "").strip()
        (OUT_DIR / f"{code}_groq.txt").write_text(text + "\n" if text else "", encoding="utf-8")
        (OUT_DIR / f"{code}_local.txt").write_text(local + "\n" if local else "", encoding="utf-8")
        duration = float(result.get("duration") or 0)
        audio_total += duration
        groq_total += took
        if local or text:
            score = difflib.SequenceMatcher(None, words(local), words(text)).ratio()
            scores.append(score)
            match = f"{score:.0%} word match"
        else:
            match = "no speech in either"
        logger.info(
            f"  ✓ {len(text.split())} words ({len(local.split())} local), {result.get('language')}, "
            f"{duration:.0f}s of audio in {took:.1f}s, {match}"
        )

    if scores:
        logger.info(
            f"Done. Tested: {len(todo) - failed} | Failed: {failed} | {audio_total / 60:.1f} min of audio in "
            f"{groq_total:.0f}s | average word match {sum(scores) / len(scores):.0%} | files in {OUT_DIR}"
        )
    else:
        logger.info(f"Done. Tested: {len(todo) - failed} | Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(130)
    except RuntimeError as e:
        logger.error(str(e))
        sys.exit(1)
