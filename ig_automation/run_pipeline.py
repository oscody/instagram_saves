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
import fcntl
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from describe import CLAUDE_LIMIT_EXIT, needs_description, written_by_hailo
from download import CAP_RETRY_FILE, DEFAULT_JSON, IG_DIR, LOGGED_OUT_EXIT, LOGGED_OUT_FILE, needs_download
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
LOCK_FILE = HERE / "output" / "pipeline.lock"
HEALTH_FILE = HERE / "output" / "pipeline_health.json"
FINISH_LINE = "Pipeline ran"
BATCH_LINE = "=== Batch"


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
        "--export-every",
        type=float,
        default=6.0,
        help="Read the chat only when the last export is at least this many hours old. 0 reads it every batch. Default: 6",
    )
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
    """Move the last run's log to pipeline-<date>-part<N>.log; also say whether it ended with its finish line.

    A log from today whose run finished stays in place, and the next run appends to it.
    """
    if not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0:
        return None
    # A Ctrl+C or a traceback can follow the finish line, so look for it anywhere in the log.
    # A log holding only describe.py runs by hand never had a pipeline run to finish.
    text = LOG_FILE.read_text(errors="replace")
    finished = FINISH_LINE in text or BATCH_LINE not in text
    day = time.strftime("%Y-%m-%d", time.localtime(LOG_FILE.stat().st_mtime))
    # The timer starts a short run every 2 hours; finished runs from today share one log instead of a file each.
    if finished and day == time.strftime("%Y-%m-%d"):
        return None
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
    # IG_PIPELINE tells describe.py its output is already in the pipeline log, also with --foreground.
    result = subprocess.run(
        [sys.executable, str(HERE / script), "--limit", str(batch), *extra],
        cwd=HERE,
        env={**os.environ, "IG_PIPELINE": "1"},
    )
    name = " ".join((script,) + extra)
    logger.info(f"  {name} finished in {(time.monotonic() - started) / 60:.1f} min (exit code {result.returncode})")
    return result.returncode


def hours_since_export() -> float:
    """Hours since the export file's `exported_at`; very large when it is missing or unreadable."""
    try:
        exported = datetime.fromisoformat(json.loads(DEFAULT_JSON.read_text())["exported_at"])
        return (datetime.now(timezone.utc) - exported).total_seconds() / 3600
    except (OSError, ValueError, KeyError, TypeError):
        return float("inf")


def export(backfill_pages: int) -> bool:
    """Pick up new posts from the chat; a failure is only logged, the batch goes on without them."""
    started = time.monotonic()
    attempted_at = datetime.now().astimezone().isoformat(timespec="seconds")
    state = load_health_state()
    state["last_chat_sync_attempt"] = attempted_at
    try:
        result = subprocess.run(
            [sys.executable, str(HERE / "export_chat_links.py"), "--backfill-pages", str(backfill_pages)], cwd=HERE
        )
        success = result.returncode == 0
        state["last_chat_sync_result"] = "success" if success else "failed"
        state["last_chat_sync_error"] = None if success else f"export_chat_links.py exited with code {result.returncode}"
        if success:
            state["last_chat_sync_success"] = datetime.now().astimezone().isoformat(timespec="seconds")
    except OSError as e:
        success = False
        state["last_chat_sync_result"] = "failed"
        state["last_chat_sync_error"] = str(e)
        logger.exception("Could not start chat exporter")
    save_health_state(state)
    if 'result' in locals():
        logger.info(f"  export_chat_links.py finished in {(time.monotonic() - started) / 60:.1f} min (exit code {result.returncode})")
    else:
        logger.info(f"  export_chat_links.py could not start after {(time.monotonic() - started) / 60:.1f} min")
    if not success:
        logger.warning("  EXPORT FAILED: no new posts from the chat this batch. The error is just above.")
    return success


def load_health_state() -> dict:
    try:
        return json.loads(HEALTH_FILE.read_text())
    except (OSError, ValueError):
        return {}


def save_health_state(state: dict) -> None:
    HEALTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = HEALTH_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2) + "\n")
    tmp.replace(HEALTH_FILE)


def next_regular_timer_start(now: datetime | None = None) -> datetime:
    """Next nominal run from ig-pipeline.timer, which adds up to 20 minutes of jitter."""
    now = now or datetime.now().astimezone()
    candidates = []
    for day_offset in (0, 1):
        day = (now + timedelta(days=day_offset)).date()
        candidates.extend(
            datetime.combine(day, datetime.min.time(), tzinfo=now.tzinfo).replace(hour=hour)
            for hour in range(8, 23, 2)
        )
    return next(candidate for candidate in candidates if candidate > now)


def cancel_cap_retry() -> None:
    """Cancel a previously scheduled one-shot retry, if any."""
    try:
        subprocess.run(
            ["systemctl", "--user", "stop", "ig-pipeline-cap-retry.timer"],
            capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        pass


def schedule_cap_retry() -> None:
    """Add a one-shot user timer when a cap slot opens before the next regular run."""
    if not CAP_RETRY_FILE.exists():
        cancel_cap_retry()
        return
    try:
        retry = datetime.fromisoformat(json.loads(CAP_RETRY_FILE.read_text())["next_attempt_at"])
    except (OSError, ValueError, KeyError, TypeError) as e:
        logger.warning(f"Could not read the download cap retry time: {e}")
        return
    now = datetime.now().astimezone()
    if retry.tzinfo is None:
        retry = retry.astimezone()
    if retry <= now or LOGGED_OUT_FILE.exists():
        CAP_RETRY_FILE.unlink(missing_ok=True)
        cancel_cap_retry()
        return
    # A normal run will try first if it starts in the same timer window, or before the cap reopens.
    if retry >= next_regular_timer_start(now):
        cancel_cap_retry()
        logger.info(f"Periodic timer will check downloads before the cap slot reopens at {retry:%a %H:%M}")
        return

    cancel_cap_retry()
    calendar_time = retry.strftime("%Y-%m-%d %H:%M:%S")
    wait_for_pipeline = (
        "while systemctl --user is-active --quiet ig-pipeline.service; do sleep 15; done; "
        "exec systemctl --user start ig-pipeline.service"
    )
    try:
        result = subprocess.run(
            [
                "systemd-run", "--user", "--quiet", "--collect", "--unit=ig-pipeline-cap-retry",
                f"--on-calendar={calendar_time}", "--timer-property=AccuracySec=1s",
                "--timer-property=RandomizedDelaySec=0", "/bin/bash", "-lc", wait_for_pipeline,
            ],
            capture_output=True, text=True, timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        logger.warning(f"Could not schedule the download cap retry; the regular timer remains active: {e}")
        return
    if result.returncode == 0:
        logger.info(f"Scheduled a download cap retry for {retry:%a %b %d %H:%M}")
    else:
        detail = (result.stderr or result.stdout).strip()
        logger.warning(f"Could not schedule the download cap retry; the regular timer remains active: {detail}")


def main() -> int:
    args = parse_args()
    if not args.foreground:
        return start_background(sys.argv[1:])
    if pid := other_runner():
        logger.error(f"run_pipeline.py is already running (PID {pid})")
        return 1
    # Also protects against maintenance jobs in a different process namespace.
    lock = LOCK_FILE.open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        logger.info("Pipeline state is locked by another run or maintenance job; waiting for the next scheduled run")
        return 0
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
            # Every request to Instagram waits while the session is logged out.
            if LOGGED_OUT_FILE.exists():
                logger.error(f"Logged out of Instagram, stopping: {LOGGED_OUT_FILE.read_text().strip()}")
                break
            # Export first, so a restart with an empty backlog still picks up new posts. Reading the chat every
            # batch looked like a bot, so it waits --export-every hours between reads.
            if not args.no_export:
                age = hours_since_export()
                if age >= args.export_every:
                    export(args.backfill_pages)
                else:
                    logger.info(f"  Chat read {age:.1f} h ago, next read after {args.export_every:g} h")
            before = pending()
            logger.info(f"Pending: {before}")
            if not any(before[k] for k in work):
                logger.info("Nothing left to do")
                break
            batch_no += 1
            logger.info(f"{BATCH_LINE} {batch_no} === ({pi_status()})")
            describe_hit_limit = False
            for script, key in (("download.py", "download"), ("transcribe.py", "transcribe"), ("describe.py", "describe")):
                if pending()[key]:
                    code = run_stage(script, args.batch)
                    if script == "download.py" and code == LOGGED_OUT_EXIT:
                        logger.error(f"  LOGGED OUT: Instagram logged the session out, see {LOGGED_OUT_FILE}")
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
        try:
            from status_report import post_daily_status, write_daily_status

            schedule_cap_retry()
            report_path, snapshot = write_daily_status()
            logger.info(f"Daily status snapshot appended to {report_path}")
            posted = post_daily_status(snapshot)
            if posted:
                logger.info("This run's status snapshot posted to the configured Hermes chat")
            else:
                logger.error("Could not post this run's status snapshot to Hermes; see the delivery error")
        except Exception:
            logger.exception("Could not update the daily status report")
        lock.close()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; posts finished so far are saved")
        sys.exit(130)
