#!/usr/bin/env python3
"""Write a compact daily health report for the Instagram saves pipeline."""

import json
import os
import subprocess
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from describe import needs_description, written_by_hailo
from download import BLOCKED_FILE, DEFAULT_JSON, IG_DIR, LOGGED_OUT_FILE, blocked_until, needs_download
from transcribe import needs_transcript

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
HEALTH_FILE = OUTPUT_DIR / "pipeline_health.json"
REPORT_FILE = OUTPUT_DIR / "daily_status.md"
CAP_RETRY_FILE = OUTPUT_DIR / "download_cap_retry.json"
HERMES_SEND = os.environ.get("HERMES_SEND_BIN", "/home/homepi/.local/bin/hermes")
HERMES_STATUS_TARGET = os.environ.get("HERMES_STATUS_TARGET", "telegram")


def read_json(path: Path, fallback: dict) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return fallback


def local_timestamp(value: str | None) -> str:
    if not value:
        return "not recorded"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone().strftime("%b %-d, %Y %I:%M %p %Z")
    except ValueError:
        return value


def next_run_window(now: datetime) -> str:
    """Mirror ig-pipeline.timer: even hours from 08:00 through 22:00, plus up to 20 min."""
    if (OUTPUT_DIR / "PAUSED").exists():
        return "Paused (output/PAUSED)"
    if until := blocked_until():
        return f"Cooldown until {until.strftime('%a %b %-d, %-I:%M %p %Z')} (output/BLOCKED)"
    candidates = []
    for day_offset in (0, 1):
        day = (now + timedelta(days=day_offset)).date()
        candidates.extend(datetime.combine(day, datetime.min.time(), tzinfo=now.tzinfo).replace(hour=h)
                          for h in range(8, 23, 2))
    next_start = next(candidate for candidate in candidates if candidate > now)
    try:
        retry_at = datetime.fromisoformat(read_json(CAP_RETRY_FILE, {}).get("next_attempt_at", ""))
        if retry_at.tzinfo is None:
            retry_at = retry_at.astimezone()
        if now < retry_at < next_start:
            return f"{retry_at.strftime('%a %b %-d, %-I:%M %p %Z')} (download cap retry)"
    except ValueError:
        pass
    return f"{next_start.strftime('%a %b %-d, %-I:%M %p')}–{(next_start + timedelta(minutes=20)).strftime('%-I:%M %p %Z')}"


def write_daily_status() -> tuple[Path, str]:
    data = read_json(DEFAULT_JSON, {"links": [], "scan": {}})
    health = read_json(HEALTH_FILE, {})
    records = data.get("links", [])
    now = datetime.now().astimezone()
    today = now.strftime("%Y-%m-%d")

    failed = [record for record in records if record.get("error")]
    pending_download = [r for r in records if needs_download(r, IG_DIR, False)]
    pending_transcribe = [r for r in records if needs_transcript(r, IG_DIR, False)]
    pending_describe = [r for r in records if needs_description(r, False, False)]
    pending_upgrade = [r for r in records if written_by_hailo(r) and not r.get("error")]
    completed = [
        r for r in records
        if not r.get("error")
        and not needs_download(r, IG_DIR, False)
        and not needs_transcript(r, IG_DIR, False)
        and not needs_description(r, False, False)
    ]
    completed_today = [r for r in completed if r.get("described_at") == today]
    repeated = Counter(str(r.get("error")).strip() for r in failed if r.get("error"))
    repeated = [(message, count) for message, count in repeated.most_common() if count >= 3]

    sync_success = health.get("last_chat_sync_success")
    sync_result = health.get("last_chat_sync_result")
    sync_error = health.get("last_chat_sync_error")
    sync_attempt = health.get("last_chat_sync_attempt")
    # Older runs predate explicit sync health tracking; exported_at is the best available record.
    if not sync_success:
        sync_success = data.get("exported_at")
        sync_label = " (from export file; success tracking starts with the next pipeline run)" if sync_success else ""
    else:
        sync_label = ""

    flags = []
    if LOGGED_OUT_FILE.exists():
        reason = LOGGED_OUT_FILE.read_text(errors="replace").strip()
        flags.append(f"Instagram login expired or challenged: {reason or 'see output/LOGGED_OUT'}")
    if blocked_until():
        try:
            reason = json.loads(BLOCKED_FILE.read_text()).get("reason")
        except (OSError, ValueError, AttributeError):
            reason = None
        flags.append(f"Instagram is likely blocking the account, downloads are cooling down: {reason or 'see output/BLOCKED'}")
    if sync_result == "failed":
        flags.append(f"Latest chat sync attempt failed: {sync_error or 'see pipeline.log'}")
    for message, count in repeated:
        flags.append(f"Repeated failure ({count} posts): {message}")
    if failed and not repeated:
        flags.append(f"{len(failed)} post(s) have recorded failures; review the failed posts below.")

    scan = data.get("scan", {})
    history = "complete" if scan.get("history_complete") else "backfill in progress"
    failed_lines = [f"* `{r.get('shortcode', 'unknown')}`: {str(r.get('error')).replace(chr(10), ' ')[:240]}" for r in failed[:20]]
    if len(failed) > 20:
        failed_lines.append(f"* ...and {len(failed) - 20} more")

    lines = [
        f"## Pipeline run: {now.strftime('%Y-%m-%d %I:%M:%S %p %Z')}",
        "",
        f"Updated: {now.strftime('%Y-%m-%d %I:%M:%S %p %Z')}",
        "",
        "### Posts",
        "",
        f"* Completed: {len(completed)} total, {len(completed_today)} completed today",
        f"* Backlog: {len(pending_download)} to download, {len(pending_transcribe)} to transcribe, {len(pending_describe)} to describe, {len(pending_upgrade)} Qwen descriptions eligible for Claude upgrade",
        f"* Failed: {len(failed)}",
        f"* Chat history scan: {history} ({scan.get('oldest_us') and 'oldest messages covered' or 'scan starting point not recorded'})",
        "",
        "### Chat sync",
        "",
        f"* Last successful chat sync: {local_timestamp(sync_success)}{sync_label}",
        f"* Latest sync attempt: {local_timestamp(sync_attempt)} ({sync_result or 'unknown'})",
        "",
        "### Schedule and health",
        "",
        f"* Next scheduled run window: {next_run_window(now)} local time",
        f"* Alerts: {'; '.join(flags) if flags else 'none'}",
    ]
    if failed_lines:
        lines.extend(["", "### Failed posts", "", *failed_lines])
    lines.append("")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = "\n".join(lines)
    separator = "\n\n---\n\n" if REPORT_FILE.exists() and REPORT_FILE.stat().st_size else ""
    with REPORT_FILE.open("a", encoding="utf-8") as report:
        report.write(separator + snapshot)
    return REPORT_FILE, snapshot


def send_hermes(text: str) -> tuple[bool, str | None]:
    """Send text to the Hermes chat; returns whether it was sent and the error if not."""
    try:
        result = subprocess.run(
            [HERMES_SEND, "send", "--to", HERMES_STATUS_TARGET, "--quiet"],
            capture_output=True,
            text=True,
            input=text,
            timeout=45,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    if result.returncode == 0:
        return True, None
    return False, (result.stderr or result.stdout or f"hermes send exited with code {result.returncode}").strip()


def post_daily_status(snapshot: str) -> bool:
    """Post the newest status snapshot to Hermes, without resending the accumulated local history."""
    health = read_json(HEALTH_FILE, {})
    today = datetime.now().astimezone().strftime("%Y-%m-%d")
    attempted_at = datetime.now().astimezone().isoformat(timespec="seconds")
    success, error = send_hermes(snapshot)

    health["last_status_post_attempt"] = attempted_at
    health["last_status_post_result"] = "sent" if success else "failed"
    health["last_status_post_error"] = error
    health["last_status_post_target"] = HERMES_STATUS_TARGET
    if success:
        health["last_status_post_date"] = today
    tmp = HEALTH_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(health, indent=2) + "\n")
    tmp.replace(HEALTH_FILE)
    return success


if __name__ == "__main__":
    report_path, _ = write_daily_status()
    print(report_path)
