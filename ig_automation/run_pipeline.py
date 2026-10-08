#!/usr/bin/env python3
"""Run download, transcribe and describe in batches until every post is done.

Each batch takes the newest N posts that still need a stage through all three stages, so
finished posts appear early and hailo-ollama is back between batches. The scripts run one
after another, never at the same time, because they all write the export file.

After describe, each batch also upgrades up to --upgrade-batch posts that Qwen described to
Claude (describe.py --upgrade). Upgrades pause while Claude is at its usage limit, and start again
once a later describe step gets through Claude without hitting it.

Each batch starts with export_chat_links.py, so posts shared in the chat since the last run are
picked up (newest first, so they go into that batch). It reads every new message, then at most
--backfill-pages pages of older history, so the rest of the chat comes in a slice per batch.
A failed export is logged as a warning; the batch carries on with the posts already in the file.

Stop cleanly after the current batch by creating output/STOP (it is removed on exit).

By default it starts itself in the background and returns: it refuses to start if another
run_pipeline.py is running, checks that the export file is valid JSON, moves the last run's
output/pipeline.log to pipeline-<date>-part<N>.log, and notes in the new log when the last run
ended without its finish line (a power cut or a kill). --foreground runs it in this terminal
instead, with no log file.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

from describe import CLAUDE_LIMIT_EXIT, needs_description, written_by_hailo
from download import DEFAULT_JSON, IG_DIR, needs_download
from transcribe import needs_transcript

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_pipeline")

HERE = Path(__file__).resolve().parent
STOP_FILE = HERE / "output" / "STOP"
LOG_FILE = HERE / "output" / "pipeline.log"
FINISH_LINE = "Pipeline ran"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", type=int, default=100, help="Posts per stage per batch. Default: 100")
    parser.add_argument("--max-batches", type=int, default=None, help="Stop after this many batches.")
    parser.add_argument(
        "--upgrade-batch",
        type=int,
        default=20,
        help="Qwen posts to upgrade to Claude per batch, after describe. 0 turns upgrades off. Default: 20",
    )
    parser.add_argument(
        "--backfill-pages",
        type=int,
        default=50,
        help="Pages of older chat history (50 messages each) to read per batch. Default: 50",
    )
    parser.add_argument("--no-export", action="store_true", help="Do not run the exporter at the start of each batch.")
    parser.add_argument(
        "--foreground", action="store_true", help="Run in this terminal instead of starting in the background."
    )
    return parser.parse_args()


def pending() -> dict:
    links = json.loads(DEFAULT_JSON.read_text())["links"]
    return {
        "download": sum(needs_download(r, IG_DIR, False) for r in links),
        "transcribe": sum(needs_transcript(r, IG_DIR, False) for r in links),
        "describe": sum(bool(needs_description(r, False, False)) for r in links),
        "qwen": sum(written_by_hailo(r) for r in links),
        "errors": sum(bool(r.get("error")) for r in links),
    }


def pi_status() -> str:
    """Temperature and throttle flags, so a crash or slowdown can be matched to the heat."""
    try:
        temp = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True).stdout.strip()
        throttled = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True, text=True).stdout.strip()
        return f"{temp}, {throttled}"
    except OSError:
        return "vcgencmd not available"


def other_runner() -> int | None:
    """PID of another run_pipeline.py, if one is running."""
    skip = {os.getpid(), os.getppid()}
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit() or int(proc.name) in skip:
            continue
        try:
            cmdline = (proc / "cmdline").read_bytes().split(b"\0")
        except OSError:
            continue
        # Only Python running the script counts, not an editor or tail with the file open.
        if Path(cmdline[0].decode(errors="replace")).name.startswith("python") and any(
            arg.endswith(b"run_pipeline.py") for arg in cmdline
        ):
            return int(proc.name)
    return None


def archive_log() -> tuple[Path, bool] | None:
    """Move the last run's log to pipeline-<date>-part<N>.log; also say whether it ended with its finish line."""
    if not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0:
        return None
    # A Ctrl+C or a traceback can follow the finish line, so look for it anywhere in the log.
    finished = FINISH_LINE in LOG_FILE.read_text(errors="replace")
    day = time.strftime("%Y-%m-%d", time.localtime(LOG_FILE.stat().st_mtime))
    part = 1
    while (dest := LOG_FILE.with_name(f"pipeline-{day}-part{part}.log")).exists():
        part += 1
    LOG_FILE.rename(dest)
    return dest, finished


def start_background(argv: list[str]) -> int:
    """Check, archive the old log, then start the runner detached with its output in output/pipeline.log."""
    if pid := other_runner():
        logger.error(f"run_pipeline.py is already running (PID {pid}). Stop it first: touch {STOP_FILE}")
        return 1
    try:
        json.loads(DEFAULT_JSON.read_text())
    except (OSError, ValueError) as e:
        logger.error(f"{DEFAULT_JSON} is not readable JSON, not starting: {e}")
        return 1
    archived = archive_log()
    with LOG_FILE.open("a") as log:
        file_log = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_log.setFormatter(logging.getLogger().handlers[0].formatter)
        logger.addHandler(file_log)
        if archived:
            dest, finished = archived
            logger.info(f"Last run's log moved to {dest.name}")
            if not finished:
                logger.warning(f"The last run ended without its finish line (power cut or killed?), see {dest.name}")
        logger.info(f"Starting: {pi_status()}")
        logger.removeHandler(file_log)
        file_log.close()
        child = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), *argv, "--foreground"],
            cwd=HERE,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    logger.info(f"Pipeline started in the background (PID {child.pid})")
    logger.info(f"Follow it: tail -f {LOG_FILE}")
    logger.info(f"Stop after the current batch: touch {STOP_FILE}")
    return 0


def run_stage(script: str, batch: int, *extra: str) -> int:
    """Run one stage; a failed post is recorded in the export file, so a non zero exit is only logged."""
    started = time.monotonic()
    result = subprocess.run([sys.executable, str(HERE / script), "--limit", str(batch), *extra], cwd=HERE)
    name = " ".join((script,) + extra)
    logger.info(f"  {name} finished in {(time.monotonic() - started) / 60:.1f} min (exit code {result.returncode})")
    return result.returncode


def export(backfill_pages: int) -> None:
    """Pick up new posts from the chat; a failure is only logged, the batch goes on without them."""
    started = time.monotonic()
    result = subprocess.run(
        [sys.executable, str(HERE / "export_chat_links.py"), "--backfill-pages", str(backfill_pages)], cwd=HERE
    )
    logger.info(f"  export_chat_links.py finished in {(time.monotonic() - started) / 60:.1f} min (exit code {result.returncode})")
    if result.returncode != 0:
        logger.warning("  EXPORT FAILED: no new posts from the chat this batch. The error is just above.")


def main() -> int:
    args = parse_args()
    if not args.foreground:
        return start_background(sys.argv[1:])
    if pid := other_runner():
        logger.error(f"run_pipeline.py is already running (PID {pid})")
        return 1
    STOP_FILE.unlink(missing_ok=True)
    run_started = time.monotonic()
    batch_no = 0
    # Qwen posts count as work left only while upgrades are on.
    work = ("download", "transcribe", "describe") + (("qwen",) if args.upgrade_batch else ())
    try:
        while True:
            if args.max_batches and batch_no >= args.max_batches:
                logger.info(f"Stopping after {batch_no} batches (--max-batches)")
                break
            if STOP_FILE.exists():
                logger.info("Stop file found, stopping")
                break
            # Export first, so a restart with an empty backlog still picks up new posts.
            if not args.no_export:
                export(args.backfill_pages)
            before = pending()
            logger.info(f"Pending: {before}")
            if not any(before[k] for k in work):
                logger.info("Nothing left to do")
                break
            batch_no += 1
            logger.info(f"=== Batch {batch_no} === ({pi_status()})")
            describe_hit_limit = False
            for script, key in (("download.py", "download"), ("transcribe.py", "transcribe"), ("describe.py", "describe")):
                if pending()[key]:
                    code = run_stage(script, args.batch)
                    if script == "describe.py" and code == CLAUDE_LIMIT_EXIT:
                        describe_hit_limit = True
                        logger.info("  Claude hit its usage limit during describe, the Hailo did the rest")
            # Each batch tries again, so upgrades start again on their own once the limit resets.
            if args.upgrade_batch and pending()["qwen"]:
                if describe_hit_limit:
                    logger.info("  Upgrade skipped this batch: Claude is at its usage limit")
                elif run_stage("describe.py", args.upgrade_batch, "--upgrade") == CLAUDE_LIMIT_EXIT:
                    logger.info("  Upgrade stopped: Claude is at its usage limit")
            after = pending()
            if all(after[k] >= before[k] for k in work):
                logger.warning(f"Batch {batch_no} made no progress, stopping: {after}")
                break
    finally:
        STOP_FILE.unlink(missing_ok=True)
        logger.info(f"{FINISH_LINE} {batch_no} batches in {(time.monotonic() - run_started) / 3600:.1f} h")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; posts finished so far are saved")
        sys.exit(130)
