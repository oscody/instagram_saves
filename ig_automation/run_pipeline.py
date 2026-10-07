#!/usr/bin/env python3
"""Run download, transcribe and describe in batches until every post is done.

Each batch takes the newest N posts that still need a stage through all three stages, so
finished posts appear early and hailo-ollama is back between batches. The scripts run one
after another, never at the same time, because they all write the export file.

Stop cleanly after the current batch by creating output/STOP (it is removed on exit).
"""

import argparse
import json
import logging
import subprocess
import sys
import time
from pathlib import Path

from describe import needs_description
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", type=int, default=100, help="Posts per stage per batch. Default: 100")
    parser.add_argument("--max-batches", type=int, default=None, help="Stop after this many batches.")
    return parser.parse_args()


def pending() -> dict:
    links = json.loads(DEFAULT_JSON.read_text())["links"]
    return {
        "download": sum(needs_download(r, IG_DIR, False) for r in links),
        "transcribe": sum(needs_transcript(r, IG_DIR, False) for r in links),
        "describe": sum(bool(needs_description(r, False, False)) for r in links),
        "errors": sum(bool(r.get("error")) for r in links),
    }


def run_stage(script: str, batch: int) -> None:
    """Run one stage; a failed post is recorded in the export file, so a non zero exit is only logged."""
    started = time.monotonic()
    result = subprocess.run([sys.executable, str(HERE / script), "--limit", str(batch)], cwd=HERE)
    logger.info(f"  {script} finished in {(time.monotonic() - started) / 60:.1f} min (exit code {result.returncode})")


def main() -> int:
    args = parse_args()
    STOP_FILE.unlink(missing_ok=True)
    run_started = time.monotonic()
    batch_no = 0
    try:
        while True:
            before = pending()
            logger.info(f"Pending: {before}")
            if not (before["download"] or before["transcribe"] or before["describe"]):
                logger.info("Nothing left to do")
                break
            if args.max_batches and batch_no >= args.max_batches:
                logger.info(f"Stopping after {batch_no} batches (--max-batches)")
                break
            if STOP_FILE.exists():
                logger.info("Stop file found, stopping")
                break
            batch_no += 1
            logger.info(f"=== Batch {batch_no} ===")
            for script, key in (("download.py", "download"), ("transcribe.py", "transcribe"), ("describe.py", "describe")):
                if pending()[key]:
                    run_stage(script, args.batch)
            after = pending()
            if all(after[k] >= before[k] for k in ("download", "transcribe", "describe")):
                logger.warning(f"Batch {batch_no} made no progress, stopping: {after}")
                break
    finally:
        STOP_FILE.unlink(missing_ok=True)
        logger.info(f"Pipeline ran {batch_no} batches in {(time.monotonic() - run_started) / 3600:.1f} h")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; posts finished so far are saved")
        sys.exit(130)
