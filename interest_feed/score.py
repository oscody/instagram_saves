#!/usr/bin/env python3
"""Score the interest digest against what you actually saved: recall (did it find your saves first) and precision
(were its picks any good).

Recall: every Instagram save in a Focus topic is traced to its original (the links in the note's `## Research`
section, from research.py) and sorted into a bucket:
* hit: a digest picked it on or before the week you saved it
* seen, not picked: the fetcher found it but the filter dropped it (fix the filter)
* never seen: no source had it (fix the sources)
* no original: research found no link behind the post, so it cannot be scored
* repeat: you had already saved the same original before, so the digest rightly skips it

Precision: a pick counts as good when you ticked it in the vault digest, when its link shows up in another vault note
(you acted on it), or when you saved it on Instagram too.

Reads `output/history.jsonl` from feed.py (`--backtest` reads `output/backtest/history.jsonl`) and writes
`scoreboard.md` next to it, and with `--vault` also a note in the vault's `ZAIHub/Interest digest/`.
"""

import argparse
import json
import re
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import feed

SAVE_TOPICS_FILE = feed.OUTPUT_DIR / "save_topics.json"
RESEARCH_RE = re.compile(r"^## Research\n(.*?)(?=^## |\Z)", re.M | re.S)
LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)")
TICKED_RE = re.compile(r"^\* \[[xX]\] ")
SKIP_VAULT_DIRS = ("ZAIHub/Interest digest/", "ZAIHub/Vault knowledge library/", "Media/")

LABEL_SYSTEM = """You sort saved Instagram posts into Focus topics. For each post give the topic slug it belongs to,
or "none" if it fits no topic. Use the item numbers given."""

LABEL_SCHEMA = json.dumps({
    "type": "object",
    "properties": {"labels": {"type": "array", "items": {
        "type": "object",
        "properties": {"item": {"type": "integer"}, "topic": {"type": "string"}},
        "required": ["item", "topic"],
    }}},
    "required": ["labels"],
})


# ---------------------------------------------------------------- inputs


def load_runs(path: Path) -> list:
    if not path.exists():
        raise SystemExit(f"No history yet at {path}. Run feed.py first.")
    runs = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entry = json.loads(line)
            runs[entry["run_date"]] = entry  # a rerun of the same date replaces the earlier one
    return [runs[d] for d in sorted(runs)]


def load_saves() -> list:
    saves = []
    for folder in sorted(feed.IG_DIR.iterdir()):
        if not folder.is_dir() or folder.name.startswith("0_"):
            continue
        for note in folder.glob("*_description.md"):
            text = note.read_text(encoding="utf-8")
            research = RESEARCH_RE.search(text)
            links = [u for u in LINK_RE.findall(research.group(1)) if "instagram.com" not in u] if research else []
            title = re.search(r"^# (.+)", text, re.M)
            saves.append({
                "code": folder.name.split("_", 2)[-1],
                "date": folder.name[:10],
                "title": title.group(1) if title else note.stem,
                "links": links,
                "keys": {feed.link_key(u) for u in links},
            })
    return saves


def focus_topics(saves: list, profile: dict, model: str, timeout: int) -> dict:
    """Shortcode to Focus topic slug ("none" when it fits none). Grouped posts use topics.json; newer posts are
    labelled once by Claude and cached."""
    library = {t["slug"]: set(t["sources"]) for t in json.loads(feed.TOPICS_FILE.read_text())["topics"]}
    grouped = set().union(*library.values())
    labels = json.loads(SAVE_TOPICS_FILE.read_text()) if SAVE_TOPICS_FILE.exists() else {}
    for topic in profile["topics"]:
        for slug in topic.get("library_topics", []):
            for code in library.get(slug, ()):
                labels.setdefault(code, topic["slug"])
    for code in grouped:
        labels.setdefault(code, "none")
    todo = [s for s in saves if s["code"] not in labels]
    if todo:
        topics = "\n".join(f"* {t['slug']}: {t['name']} ({', '.join(t['search'])})" for t in profile["topics"])
        listing = "\n".join(f"[{n}] {s['title']}" for n, s in enumerate(todo))
        answer = feed.ask_claude(f"Focus topics:\n{topics}\n\nPosts:\n{listing}", model, timeout,
                                 system=LABEL_SYSTEM, schema=LABEL_SCHEMA)
        for label in answer.get("labels", []):
            if 0 <= label["item"] < len(todo):
                labels[todo[label["item"]]["code"]] = label["topic"]
        SAVE_TOPICS_FILE.write_text(json.dumps(labels, indent=1))
    return labels


def vault_text(vault) -> str:
    """All vault notes outside the digest and library folders, lowercased, for the "acted on it" check."""
    if not vault:
        return ""
    parts = []
    for note in vault.rglob("*.md"):
        rel = note.relative_to(vault).as_posix()
        if not rel.startswith(SKIP_VAULT_DIRS) and not rel.startswith("."):
            parts.append(note.read_text(encoding="utf-8", errors="ignore").lower())
    return "\n".join(parts)


def ticked_urls(vault, run_date: str) -> set:
    """Links of the picks you ticked in that week's vault digest."""
    if not vault:
        return set()
    note = vault / feed.VAULT_DIGEST_DIR / f"claude - interest digest {run_date}.md"
    if not note.exists():
        return set()
    urls, ticked = set(), False
    for line in note.read_text(encoding="utf-8").splitlines():
        if line.startswith("* ["):
            ticked = bool(TICKED_RE.match(line))
        elif ticked:
            urls.update(LINK_RE.findall(line))
    return urls


# ---------------------------------------------------------------- scoring


def score_week(run: dict, runs: list, saves: list, labels: dict, profile: dict, vault, vault_lower: str,
               saved_keys: set) -> dict:
    end = date.fromisoformat(run["run_date"])
    start = end - timedelta(days=7)
    earlier = [r for r in runs if r["run_date"] <= run["run_date"]]
    picked = {i["key"]: r["run_date"] for r in earlier for i in r["items"] if i["picked"] and not i["update"]}
    seen = {i["key"]: i["title"] for r in earlier for i in r["items"] if not i["update"]}
    slugs = {t["slug"] for t in profile["topics"]}
    earlier_keys = set().union(set(), *(s["keys"] for s in saves if s["date"] < start.isoformat()))

    buckets, misses = Counter(), []
    for s in saves:
        if not (start.isoformat() <= s["date"] < end.isoformat()) or labels.get(s["code"]) not in slugs:
            continue
        if not s["keys"]:
            buckets["no original"] += 1
            continue
        if s["keys"] <= earlier_keys:
            buckets["repeat"] += 1
            continue
        if s["keys"] & picked.keys():
            buckets["hit"] += 1
        elif s["keys"] & seen.keys():
            buckets["seen, not picked"] += 1
            misses.append((s, "seen, not picked: " + seen[next(iter(s["keys"] & seen.keys()))]))
        else:
            buckets["never seen"] += 1
            misses.append((s, "never seen: original is " + ", ".join(sorted(s["keys"]))[:120]))

    ticks = ticked_urls(vault, run["run_date"])
    picks = [i for i in run["items"] if i["picked"] and not i["update"]]
    good = Counter()
    for i in picks:
        repo = i["key"].removeprefix("github:")
        if i["url"] in ticks:
            good["ticked"] += 1
        elif vault_lower and (i["url"].lower() in vault_lower or (i["key"].startswith("github:") and f"github.com/{repo}" in vault_lower)):
            good["acted"] += 1
        elif i["key"] in saved_keys:
            good["saved"] += 1

    scored = buckets["hit"] + buckets["seen, not picked"] + buckets["never seen"]
    return {
        "week": f"{start.isoformat()} to {(end - timedelta(days=1)).isoformat()}",
        "run_date": run["run_date"],
        "buckets": buckets,
        "recall": buckets["hit"] / scored if scored else None,
        "picks": len(picks),
        "good": good,
        "precision": sum(good.values()) / len(picks) if picks else None,
        "misses": misses,
    }


def pct(value) -> str:
    return "" if value is None else f"{round(value * 100)}%"


def render(weeks: list, backtest: bool, today: str, for_vault: bool) -> str:
    lines = []
    if for_vault:
        name = f"claude - interest digest {'backtest' if backtest else 'scoreboard'}"
        lines += ["---", f"name: {name}", f"created: {today}", "---", "", "#interest-digest #aiplan", "",
                  "## Prompt", "", f"Weekly score from Outside vault: `{Path(__file__).resolve()}`, defined in "
                  "[[claude - Deeper version of the information gathering system]].", "",
                  f"## Response (Claude, {today})", ""]
    else:
        lines += [f"# Interest digest {'backtest' if backtest else 'scoreboard'}", ""]
    if backtest:
        lines += ["Backtest: the fetcher was run as of each past week, with only the sources that can search the past "
                  "(GitHub search, Hacker News, Show HN), and taste examples from before that week.", ""]
    lines += [
        "* **Recall:** of your saves in the Focus topics that have a known original, how many a digest showed first.",
        "* **Precision:** of the picks, how many you ticked, acted on in the vault, or saved on Instagram too.", "",
        "| Week | Focus saves | Hit | Seen, not picked | Never seen | No original | Repeat | Recall | Picks | Good picks | Precision |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for w in weeks:
        b, g = w["buckets"], w["good"]
        good = ", ".join(f"{n} {k}" for k, n in g.items()) or "0"
        lines.append(f"| {w['week']} | {sum(b.values())} | {b['hit']} | {b['seen, not picked']} | {b['never seen']} "
                     f"| {b['no original']} | {b['repeat']} | {pct(w['recall'])} | {w['picks']} | {good} | {pct(w['precision'])} |")
    total = Counter()
    for w in weeks:
        total.update(w["buckets"])
    scored = total["hit"] + total["seen, not picked"] + total["never seen"]
    picks = sum(w["picks"] for w in weeks)
    good = sum(sum(w["good"].values()) for w in weeks)
    lines += ["", f"**All weeks:** recall {pct(total['hit'] / scored if scored else None)} ({total['hit']} of {scored}), "
              f"precision {pct(good / picks if picks else None)} ({good} of {picks}).", "", "### Misses", ""]
    for w in weeks:
        for s, why in w["misses"]:
            lines.append(f"* {s['date']} {s['title']}: {why}")
    lines += [""]
    return "\n".join(lines)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--backtest", action="store_true", help="score the backtest runs from feed.py --as-of")
    p.add_argument("--weeks", type=int, default=4, help="how many of the latest runs to score (default 4)")
    p.add_argument("--vault", nargs="?", const="", default=None, help="also write the scoreboard into the vault")
    p.add_argument("--model", default="haiku", help="model for labelling new saves (default haiku)")
    p.add_argument("--timeout", type=int, default=feed.CLAUDE_TIMEOUT)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = feed.BACKTEST_DIR if args.backtest else feed.OUTPUT_DIR
    profile = json.loads(feed.PROFILE_FILE.read_text())
    runs = load_runs(out_dir / feed.HISTORY_FILE.name)
    saves = load_saves()
    labels = focus_topics(saves, profile, args.model, args.timeout)
    vault = feed.find_vault(args.vault or None)
    lower = vault_text(vault)
    saved_keys = set().union(*(s["keys"] for s in saves))

    weeks = [score_week(r, runs, saves, labels, profile, vault, lower, saved_keys) for r in runs[-args.weeks:]]
    today = date.today().isoformat()
    board = out_dir / "scoreboard.md"
    board.write_text(render(weeks, args.backtest, today, for_vault=False), encoding="utf-8")
    print(board.read_text(encoding="utf-8"))
    if args.vault is not None and vault:
        name = f"claude - interest digest {'backtest' if args.backtest else 'scoreboard'}.md"
        note = vault / feed.VAULT_DIGEST_DIR / name
        note.parent.mkdir(exist_ok=True)
        note.write_text(render(weeks, args.backtest, today, for_vault=True), encoding="utf-8")
        print(f"Vault note: {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
