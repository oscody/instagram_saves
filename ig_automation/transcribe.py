#!/usr/bin/env python3
"""Transcribe the downloaded reels in an export file.

Groq's hosted Whisper does the work while its free quota lasts. When Groq says the quota is used up
(a long Retry-After), the rest of the run uses faster-whisper on the CPU, with cooling pauses.
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

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

ENV_FILE = Path(__file__).resolve().parent / ".env"
GROQ_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_MAX_UPLOAD = 25 * 1024 * 1024  # Groq's free tier file size limit
GROQ_RETRIES = 3
# A rate limit with a longer wait than this means the hourly or daily quota is used up, not just a busy minute.
GROQ_MAX_WAIT = 60


class GroqQuota(RuntimeError):
    """Groq's free quota is used up for now."""


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
    parser.add_argument(
        "--backend",
        choices=("auto", "groq", "cpu"),
        default="auto",
        help="auto: Groq, then the CPU once Groq's quota is used up (or with no key). "
        "groq: Groq only, stop when the quota is used up. cpu: faster-whisper only. Default: auto",
    )
    parser.add_argument(
        "--groq-model",
        default="whisper-large-v3-turbo",
        help="Groq model: whisper-large-v3-turbo or whisper-large-v3. Default: whisper-large-v3-turbo",
    )
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


def groq_key() -> str | None:
    """GROQ_API_KEY, or the `groq=` line in ig_automation/.env."""
    if key := os.environ.get("GROQ_API_KEY"):
        return key
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            name, _, value = line.partition("=")
            if name.strip().lower() in ("groq", "groq_api_key") and value.strip():
                return value.strip().strip("'\"")
    return None


def groq_transcribe(key: str, audio: Path, model: str, language: str | None) -> tuple[dict, dict]:
    """One transcription; returns Groq's answer and its headers. Waits out a short rate limit, raises GroqQuota on a long one."""
    data = {"model": model, "response_format": "verbose_json", "temperature": "0"}
    if language:
        data["language"] = language
    for attempt in range(1, GROQ_RETRIES + 1):
        with audio.open("rb") as fh:
            resp = requests.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {key}"},
                data=data,
                files={"file": (audio.name, fh, "audio/mpeg")},
                timeout=120,
            )
        if resp.status_code == 429:
            wait = float(resp.headers.get("retry-after") or 20)
            if wait > GROQ_MAX_WAIT:
                raise GroqQuota(f"Groq quota used up, try again in {wait / 60:.0f} min")
            if attempt < GROQ_RETRIES:
                logger.info(f"  Groq rate limit, waiting {wait:.0f}s")
                time.sleep(wait)
                continue
            raise GroqQuota("Groq still rate limited after retries")
        if resp.status_code != 200:
            raise RuntimeError(f"Groq HTTP {resp.status_code}: {resp.text[:300]}")
        return resp.json(), resp.headers
    raise GroqQuota("Groq still rate limited after retries")


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

    key = groq_key() if args.backend != "cpu" else None
    if args.backend == "groq" and not key:
        logger.error(f"No Groq API key: set GROQ_API_KEY or add groq=<key> to {ENV_FILE}")
        return 1
    if args.backend == "auto" and not key:
        logger.info("No Groq API key, using the CPU")
    use_groq = bool(key)
    model = None
    groq_headers = {}

    done = failed = pauses = by_groq = 0
    paused = 0.0
    run_started = time.monotonic()
    for index, record in enumerate(todo, start=1):
        audio = post_dir(args.ig_dir, record) / audio_name(record)
        logger.info(f"[{index}/{len(todo)}] {record['shortcode']} (CPU {cpu_temp():.1f}C)")
        if not audio.exists():
            # The download stage fetches the post again on its next run.
            record["downloaded"] = False
            logger.warning("  ✗ audio file missing, marked for download again")
            save(data, args.json)
            continue
        started = time.monotonic()
        text = None
        if use_groq and audio.stat().st_size > GROQ_MAX_UPLOAD:
            logger.info("  over Groq's 25 MB upload limit, using the CPU")
        elif use_groq:
            try:
                result, groq_headers = groq_transcribe(key, audio, args.groq_model, args.language)
                text = (result.get("text") or "").strip()
                language, duration = result.get("language"), float(result.get("duration") or 0)
                record["transcribed_by"] = f"groq {args.groq_model}"
                by_groq += 1
            except GroqQuota as exc:
                if args.backend == "groq":
                    logger.warning(f"  {exc}; stopping (--backend groq)")
                    break
                logger.warning(f"  {exc}; the CPU does the rest of this run")
                use_groq = False
            except (RuntimeError, requests.RequestException) as exc:
                if args.backend == "groq":
                    failed += 1
                    record["error"] = short_error(exc)
                    logger.warning(f"  ✗ {record['error']}")
                    save(data, args.json)
                    continue
                logger.warning(f"  Groq failed ({short_error(exc)}), using the CPU for this reel")
        try:
            if text is None:
                waited = cool_down(args.max_temp, args.resume_temp, args.max_wait)
                if waited:
                    pauses += 1
                    paused += waited
                if model is None:
                    from faster_whisper import WhisperModel

                    logger.info(f"Loading faster-whisper '{args.model}' (cpu, int8)")
                    model = WhisperModel(args.model, device="cpu", compute_type="int8")
                started = time.monotonic()
                segments, info = model.transcribe(str(audio), language=args.language)
                text = "".join(segment.text for segment in segments).strip()
                language, duration = info.language, info.duration
                record["transcribed_by"] = f"faster-whisper {args.model}"
            # Reels with no speech get an empty transcript, so they are not retried every run.
            transcript_path(record, args.ig_dir).write_text(text + "\n" if text else "", encoding="utf-8")
            record["transcribed"] = True
            record["error"] = False
            done += 1
            summary = f"{len(text.split())} words, {language}" if text else "no speech"
            logger.info(
                f"  ✓ {record['transcribed_by']}: {summary}, {duration:.0f}s of audio in {time.monotonic() - started:.0f}s"
            )
        except Exception as exc:  # noqa: BLE001
            failed += 1
            record["error"] = short_error(exc)
            logger.warning(f"  ✗ {record['error']}")
        save(data, args.json)

    total = time.monotonic() - run_started
    quota = ""
    if left := groq_headers.get("x-ratelimit-remaining-requests"):
        quota = f" | Groq requests left today: {left}"
    logger.info(
        f"Done. Transcribed: {done} ({by_groq} by Groq) | Failed: {failed} | "
        f"Time: {total / 60:.1f} min, of which cooling {paused / 60:.1f} min in {pauses} pauses{quota}"
    )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; posts finished so far are saved")
        sys.exit(130)
