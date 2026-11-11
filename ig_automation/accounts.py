#!/usr/bin/env python3
"""Track which Instagram accounts you save the most posts from, and how useful those saves turn out to be.

Reads every post's `<base>_description.md` (outside `IG/0_IG_Archive`): the `author` from the frontmatter, the save
date from the folder name, the verdict from the `## Research` section (research.py) and the topic from
`knowledge_library/topics.json`. Writes `knowledge_library/Account index.md` and `knowledge_library/accounts.json`.

Useful counts only posts that had something to find: "Nothing to find" posts (music, comedy, personal) are counted
as fun, not as failures. Dead ends come from `output/dead_ends.json` (read only): posts that only send the resource
after a comment or DM, and posts research could not find. run_pipeline.py reruns this at the end of every run.

Runs on the Mac and on the Pi with only Python 3. No Claude calls, so it is free to rerun after every pipeline run.
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from research import post_notes

HERE = Path(__file__).resolve().parent
IG_DIR = HERE.parent / "IG"
LIBRARY_DIR = HERE.parent / "knowledge_library"
TOPICS_FILE = LIBRARY_DIR / "topics.json"
DEAD_ENDS_FILE = HERE / "output" / "dead_ends.json"
INDEX_FILE = LIBRARY_DIR / "Account index.md"
JSON_FILE = LIBRARY_DIR / "accounts.json"

AUTHOR_RE = re.compile(r'^author:\s*"?([^"\n]*)"?\s*$', re.M)
VERDICT_RE = re.compile(r"^\* Verdict: ([^.\n]+)", re.M)
FOLDER_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")

USEFUL = {"Valid", "Partly valid"}
NOISE = {"Promo", "Not valid"}
FUN = {"Nothing to find"}  # entertainment or personal: not a failure, so left out of Useful
RECENT_DAYS = 90


def dead_end_lists() -> dict:
    """shortcode -> list name ("comment_to_get" or "other") for open research dead ends. Empty if no file."""
    try:
        entries = json.loads(DEAD_ENDS_FILE.read_text())
    except (OSError, ValueError):
        return {}
    return {e["shortcode"]: e["list"] for e in entries
            if isinstance(e, dict) and e.get("stage") == "research" and e.get("status") not in ("resolved",)}


def topic_names() -> dict:
    if not TOPICS_FILE.exists():
        return {}
    data = json.loads(TOPICS_FILE.read_text())
    return {code: t["name"] for t in data["topics"] for code in t["sources"]}


def collect(ig_dir: Path) -> dict:
    topics = topic_names()
    dead = dead_end_lists()
    accounts = defaultdict(lambda: {"saves": [], "verdicts": Counter(), "topics": Counter(), "dead_ends": Counter()})
    for note in post_notes(ig_dir):
        text = note.read_text(encoding="utf-8")
        author = AUTHOR_RE.search(text)
        name = author.group(1).strip().lstrip("@") if author else ""
        if name in ("", "null", "None"):
            name = "(unknown)"
        match = FOLDER_DATE_RE.match(note.parent.name)
        saved = match.group(1) if match else ""
        code = note.parent.name.split("_", 2)[-1]
        verdict = VERDICT_RE.search(text)
        acc = accounts[name]
        acc["saves"].append({"shortcode": code, "saved": saved, "note": f"{note.parent.name}/{note.name}"})
        acc["verdicts"][verdict.group(1).strip() if verdict else "Not researched"] += 1
        if code in topics:
            acc["topics"][topics[code]] += 1
        if code in dead:
            acc["dead_ends"][dead[code]] += 1
    return accounts


def summarize(accounts: dict, today: date) -> list:
    cutoff = (today - timedelta(days=RECENT_DAYS)).isoformat()
    rows = []
    for name, acc in accounts.items():
        dates = sorted(s["saved"] for s in acc["saves"] if s["saved"])
        verdicts = acc["verdicts"]
        useful = sum(verdicts[v] for v in USEFUL)
        fun = sum(verdicts[v] for v in FUN)
        # Useful is out of the posts that had something to find, so fun posts do not count against an account.
        judged = sum(n for v, n in verdicts.items() if v != "Not researched" and v not in FUN)
        rows.append({
            "account": name,
            "saves": len(acc["saves"]),
            "recent": sum(1 for d in dates if d >= cutoff),
            "first_saved": dates[0] if dates else "",
            "last_saved": dates[-1] if dates else "",
            "valid": verdicts["Valid"],
            "useful": useful,
            "noise": sum(verdicts[v] for v in NOISE),
            "useful_share": round(useful / judged, 2) if judged else None,
            "fun": fun,
            "gated": acc["dead_ends"]["comment_to_get"],
            "not_found": acc["dead_ends"]["other"],
            "verdicts": dict(verdicts),
            "topics": [t for t, _ in acc["topics"].most_common()],
            "posts": sorted(acc["saves"], key=lambda s: s["saved"], reverse=True),
        })
    rows.sort(key=lambda r: (-r["saves"], -r["recent"], r["account"]))
    return rows


def account_link(name: str) -> str:
    if name == "(unknown)":
        return name
    return f"[{name}](https://instagram.com/{name}/)"


def percent(share) -> str:
    return "" if share is None else f"{round(share * 100)}%"


def table(rows: list, today: date) -> list:
    lines = [
        "| Account | Saves | Last 90 days | Useful | Valid | Promo or not valid | Comment to get it | Fun | Last saved | Main topics |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        topics = ", ".join(r["topics"][:2])
        lines.append(f"| {account_link(r['account'])} | {r['saves']} | {r['recent']} | {percent(r['useful_share'])} "
                     f"| {r['valid']} | {r['noise']} | {r['gated']} | {r['fun']} | {r['last_saved']} | {topics} |")
    return lines


def render(rows: list, today: date) -> str:
    repeat = [r for r in rows if r["saves"] >= 2]
    single = len(rows) - len(repeat)
    total = sum(r["saves"] for r in rows)
    best = sorted((r for r in repeat if r["useful_share"] is not None and r["saves"] >= 3),
                  key=lambda r: (-r["useful_share"], -r["valid"], -r["saves"]))[:10]
    rising = sorted((r for r in repeat if r["recent"] >= 2), key=lambda r: (-r["recent"], -r["saves"]))[:10]
    # Fun posts are left out here too: an account is noisy when half of what it promised did not hold up.
    noisy = sorted((r for r in repeat if r["saves"] > r["fun"] and r["noise"] * 2 >= r["saves"] - r["fun"]),
                   key=lambda r: (-r["noise"], -r["saves"]))
    baiting = sorted((r for r in repeat if r["gated"] >= 2 and r["gated"] * 2 >= r["saves"] - r["fun"]),
                     key=lambda r: (-r["gated"], -r["saves"]))
    fun = sorted((r for r in repeat if r["fun"] * 2 > r["saves"]), key=lambda r: (-r["fun"], -r["saves"]))

    out = [
        "# Account index",
        "",
        f"Built {today.isoformat()} by `ig_automation/accounts.py` from {total} posts across {len(rows)} accounts.",
        "",
        "* **Useful** is the share of researched posts with a Valid or Partly valid verdict, out of the posts that had "
        "something to find. **Fun** posts (verdict Nothing to find: music, comedy, personal) are not counted against it.",
        "* **Comment to get it** counts posts that only send the resource after a comment or DM, and that research "
        "could not find anywhere else (from `ig_automation/output/dead_ends.json`).",
        f"* **Last 90 days** counts saves since {(today - timedelta(days=RECENT_DAYS)).isoformat()}.",
        f"* {len(repeat)} accounts have 2 or more saves and are listed below. {single} accounts have a single save "
        "(see `accounts.json`).",
        "",
        "## Best sources",
        "",
        "Accounts with 3 or more saves, ranked by how often their posts held up.",
        "",
        *table(best, today),
        "",
        "## Saving more lately",
        "",
        "Accounts with 2 or more saves in the last 90 days.",
        "",
        *(table(rising, today) if rising else ["None yet."]),
        "",
        "## Mostly promo or not valid",
        "",
        "Half or more of their saves were promo or did not hold up. Candidates to stop saving from.",
        "",
        *(table(noisy, today) if noisy else ["None."]),
        "",
        "## Mostly comment to get it",
        "",
        "Half or more of their posts only send the resource after a comment or DM, and it was not found anywhere else. "
        "Saving these rarely gets you the thing. Candidates to stop saving from, or to comment on right away.",
        "",
        *(table(baiting, today) if baiting else ["None."]),
        "",
        "## Saved for fun",
        "",
        "Accounts where most saves were entertainment or personal, with nothing to find. Not a problem, just not learning "
        "sources.",
        "",
        *(table(fun, today) if fun else ["None."]),
        "",
        "## All accounts with 2 or more saves",
        "",
        *table(repeat, today),
        "",
    ]
    return "\n".join(out)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--ig-dir", type=Path, default=IG_DIR, help="folder of post folders (default: IG next to ig_automation)")
    p.add_argument("--print", action="store_true", help="print the top accounts instead of writing files")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    today = datetime.now().date()
    rows = summarize(collect(args.ig_dir), today)
    if args.print:
        for r in rows[:25]:
            print(f"{r['saves']:3}  {r['recent']:3} recent  {percent(r['useful_share']):>4} useful  {r['account']}")
        return 0
    INDEX_FILE.write_text(render(rows, today), encoding="utf-8")
    JSON_FILE.write_text(json.dumps({"built": today.isoformat(), "accounts": rows}, indent=1), encoding="utf-8")
    print(f"{len(rows)} accounts -> {INDEX_FILE.name}, {JSON_FILE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
