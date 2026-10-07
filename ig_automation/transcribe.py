#!/usr/bin/env python3
"""Transcribe the downloaded reels in an export file with faster-whisper on the CPU."""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

from download import DEFAULT_JSON, IG_DIR, post_dir, save, short_error
from export_chat_links import SENT_AT_FORMAT

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_transcribe")

CPU_TEMP = Path("/sys/class/thermal/thermal_zone0/temp")  # thousandths of a degree C
COOL_CHECK_SECONDS = 15


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        type=Path,
        default=DEFAULT_JSON,
        help=f"Export file to read and update. Default: {DEFAULT_JSON}",
    )
    parser.add_argument(
        "--ig-dir",
        type=Path,
        default=IG_DIR,
        help=f"Folder that holds one subfolder per post. Default: {IG_DIR}",
    )
    parser.add_argument("--limit", type=int, default=None, help="Transcribe at most N posts, newest first.")
    parser.add_argument("--retry-failed", action="store_true", help="Also try posts whose error field is set.")
    parser.add_argument(
        "--shortcode",
        action="append",
        help="Only consider this post. Can be given more than once.",
    )
    parser.add_argument("--dry-run", action="store_true", help="List the posts that would be transcribed, then stop.")
    parser.add_argument("--model", default="base", help="faster-whisper model size. Default: base")
    parser.add_argument("--language", default=None, help="Force a language code (e.g. en). Default: auto-detect.")
    # The Pi 5 throttles at about 85 C. Without a fan, transcribing gets there in about 4 minutes.
    parser.add_argument(
        "--max-temp",
        type=float,
        default=80.0,
        help="Pause before the next reel when the CPU is at or above this, in C. Default: 80",
    )
    parser.add_argument(
        "--resume-temp",
        type=float,
        default=70.0,
        help="After a pause, continue once the CPU is down to this, in C. Default: 70",
    )
    parser.add_argument(
        "--max-wait",
        type=int,
        default=600,
        help="Longest single pause, in seconds; carries on after it even if still warm. Default: 600",
    )
    args = parser.parse_args()
    if args.resume_temp >= args.max_temp:
        parser.error("--resume-temp must be lower than --max-temp")
    return args


def cpu_temp() -> float:
    return int(CPU_TEMP.read_text()) / 1000


def cool_down(max_temp: float, resume_temp: float, max_wait: int) -> float:
    """Wait while the CPU is too hot. Returns the seconds spent waiting."""
    temp = cpu_temp()
    if temp < max_temp:
        return 0.0
    logger.info(f"  CPU at {temp:.1f}C, pausing until it is down to {resume_temp:.0f}C")
    started = time.monotonic()
    while temp > resume_temp:
        waited = time.monotonic() - started
        if waited >= max_wait:
            logger.warning(f"  still {temp:.1f}C after {waited:.0f}s, carrying on")
            return waited
        time.sleep(COOL_CHECK_SECONDS)
        temp = cpu_temp()
    waited = time.monotonic() - started
    logger.info(f"  cooled to {temp:.1f}C in {waited:.0f}s")
    return waited


def audio_name(record: dict) -> str | None:
    """The post's .mp3, if it has one. Photo and carousel posts do not."""
    return next((name for name in record.get("files") or [] if name.endswith(".mp3")), None)


def transcript_path(record: dict, ig_dir: Path) -> Path:
    return post_dir(ig_dir, record) / (Path(audio_name(record)).stem + "_transcript.txt")


def needs_transcript(record: dict, ig_dir: Path, retry_failed: bool) -> bool:
    if record.get("error") and not retry_failed:
        return False
    if not record.get("downloaded") or not audio_name(record):
        return False
    if not record.get("transcribed"):
        return True
    # Trust the folder: a transcript that was deleted is made again.
    return not transcript_path(record, ig_dir).exists()


def main() -> int:
    args = parse_args()
    data = json.loads(args.json.read_text())
    records = sorted(
        data["links"],
        key=lambda r: datetime.strptime(r["sent_at"], SENT_AT_FORMAT),
        reverse=True,
    )
    if args.shortcode:
        records = [r for r in records if r["shortcode"] in args.shortcode]
    todo = [r for r in records if needs_transcript(r, args.ig_dir, args.retry_failed)]
    if args.limit is not None:
        todo = todo[:args.limit]
    logger.info(f"{len(todo)} posts to transcribe")

    if args.dry_run:
        for record in todo:
            print(f"{record['sent_at']}  {record['shortcode']}  {audio_name(record)}")
        return 0
    if not todo:
        return 0

    from faster_whisper import WhisperModel

    logger.info(f"Loading faster-whisper '{args.model}' (cpu, int8)")
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    done = failed = pauses = 0
    paused = 0.0
    run_started = time.monotonic()
    for index, record in enumerate(todo, start=1):
        waited = cool_down(args.max_temp, args.resume_temp, args.max_wait)
        if waited:
            pauses += 1
            paused += waited
        audio = post_dir(args.ig_dir, record) / audio_name(record)
        logger.info(f"[{index}/{len(todo)}] {record['shortcode']} (CPU {cpu_temp():.1f}C)")
        if not audio.exists():
            # The download stage fetches the post again on its next run.
            record["downloaded"] = False
            logger.warning("  ✗ audio file missing, marked for download again")
            save(data, args.json)
            continue
        try:
            started = time.monotonic()
            segments, info = model.transcribe(str(audio), language=args.language)
            text = "".join(segment.text for segment in segments).strip()
            # Reels with no speech get an empty transcript, so they are not retried every run.
            transcript_path(record, args.ig_dir).write_text(text + "\n" if text else "", encoding="utf-8")
            record["transcribed"] = True
            record["error"] = False
            done += 1
            summary = f"{len(text.split())} words, {info.language}" if text else "no speech"
            logger.info(f"  ✓ {summary}, {info.duration:.0f}s of audio in {time.monotonic() - started:.0f}s")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            record["error"] = short_error(exc)
            logger.warning(f"  ✗ {record['error']}")
        save(data, args.json)

    total = time.monotonic() - run_started
    logger.info(
        f"Done. Transcribed: {done} | Failed: {failed} | "
        f"Time: {total / 60:.1f} min, of which cooling {paused / 60:.1f} min in {pauses} pauses"
    )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; posts finished so far are saved")
        sys.exit(130)
