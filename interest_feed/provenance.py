#!/usr/bin/env python3
"""Where do your saves come from? Tally the originals behind every Instagram save by source type and topic, and how
old each GitHub repo was when you saved it. Use it to choose the fetcher's sources from data instead of guesses.

Reads the links in each post note's `## Research` section (written by research.py, tracked in git, so it runs on the
Pi too) and `knowledge_library/topics.json`. Writes `output/provenance.md`. The repo age check needs GITHUB_TOKEN.
"""

import argparse
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import feed

RESEARCH_RE = re.compile(r"^## Research\n(.*?)(?=^## |\Z)", re.M | re.S)
VERDICT_RE = re.compile(r"^\* Verdict: ([^.\n]+)", re.M)
RESOURCE_RE = re.compile(r"^\* \[[^\]]*\]\((https?://[^)\s]+)\): (\w+), ([^,.]+)", re.M)
OUT_FILE = feed.OUTPUT_DIR / "provenance.md"

SOCIAL = {"x.com": "X", "twitter.com": "X", "youtube.com": "YouTube", "youtu.be": "YouTube",
          "instagram.com": "Instagram", "reddit.com": "Reddit", "linkedin.com": "LinkedIn", "tiktok.com": "TikTok",
          "threads.net": "Threads", "bsky.app": "Bluesky"}
PAPER_HOSTS = ("arxiv.org", "openreview.net", "aclanthology.org", "paperswithcode.com", "semanticscholar.org")
DOCS_RE = re.compile(r"^(docs|developers?|platform|help|support|learn)\.|^code\.claude\.com$|^docs?\.")
BLOG_RE = re.compile(r"substack\.com$|medium\.com$|dev\.to$|hashnode|\.blog$|^blog\.")


def source_type(url: str, kind: str) -> str:
    """One source type per link, which maps to the kind of feed that could catch it."""
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.").removeprefix("m.")
    path = parsed.path.lower()
    if host in ("github.com", "gist.github.com"):
        return "GitHub repo"
    if host.endswith(".github.io"):
        return "Project page (github.io)"
    if host == "huggingface.co":
        return "Hugging Face"
    if host.endswith(PAPER_HOSTS) or kind == "paper":
        return "Paper"
    if host in SOCIAL:
        return SOCIAL[host]
    if DOCS_RE.search(host) or "/docs" in path:
        return "Official docs"
    if BLOG_RE.search(host) or "/blog" in path or kind == "guide":
        return "Blog or guide"
    if host.endswith("wikipedia.org"):
        return "Wikipedia"
    if kind in ("product", "tool"):
        return "Product or tool site"
    return "Other web page (news, events, listings)"


def load(ig_dir: Path) -> list:
    topics = {}
    if feed.TOPICS_FILE.exists():
        for t in json.loads(feed.TOPICS_FILE.read_text())["topics"]:
            for code in t["sources"]:
                topics[code] = t["name"]
    saves = []
    for folder in sorted(ig_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith("0_"):
            continue
        for note in folder.glob("*_description.md"):
            text = note.read_text(encoding="utf-8")
            research = RESEARCH_RE.search(text)
            verdict = VERDICT_RE.search(text)
            links = []
            for url, kind, via in RESOURCE_RE.findall(research.group(1) if research else ""):
                if "instagram.com" in url:
                    continue  # the post itself, not its original
                links.append({"url": url, "kind": kind, "type": source_type(url, kind), "in_post": via == "in the post"})
            code = folder.name.split("_", 2)[-1]
            saves.append({"code": code, "date": folder.name[:10], "topic": topics.get(code, "(no topic)"),
                          "verdict": verdict.group(1).strip() if verdict else "Not researched", "links": links})
    return saves


def coverage(saves: list) -> list:
    """(source type, saves it could catch, share) for saves that have an original, biggest first."""
    with_links = [s for s in saves if s["links"]]
    counts = Counter(t for s in with_links for t in {l["type"] for l in s["links"]})
    return [(t, n, n / len(with_links)) for t, n in counts.most_common()] if with_links else []


def greedy_cover(saves: list) -> list:
    """Order source types by how many still uncaught saves each adds: the order to add feeds in."""
    left = [{l["type"] for l in s["links"]} for s in saves if s["links"]]
    total, order = len(left), []
    while left:
        counts = Counter(t for types in left for t in types)
        best, n = counts.most_common(1)[0]
        left = [types for types in left if best not in types]
        order.append((best, n, 1 - len(left) / total))
    return order


def repo_ages(saves: list) -> dict:
    """Days between each GitHub repo's creation and your save, per topic."""
    if not os.environ.get("GITHUB_TOKEN"):
        return {}
    created, ages = {}, defaultdict(list)
    for s in saves:
        for l in s["links"]:
            key = feed.link_key(l["url"])
            if not key.startswith("github:"):
                continue
            repo = key.removeprefix("github:")
            if repo not in created:
                try:
                    created[repo] = json.loads(feed.get(f"https://api.github.com/repos/{repo}"))["created_at"][:10]
                except Exception:
                    created[repo] = ""
            if created[repo]:
                ages[s["topic"]].append((date.fromisoformat(s["date"]) - date.fromisoformat(created[repo])).days)
    return ages


def pct(x: float) -> str:
    return f"{round(x * 100)}%"


def table(rows: list, header: str) -> list:
    lines = [f"| {header} | Saves it could catch | Share |", "| --- | --- | --- |"]
    return lines + [f"| {t} | {n} | {pct(share)} |" for t, n, share in rows]


def render(saves: list, focus: list, ages: dict) -> str:
    total = len(saves)
    with_links = [s for s in saves if s["links"]]
    out = ["# Where your saves come from", "",
           f"{total} saves; {len(with_links)} ({pct(len(with_links) / total)}) have an original link from research.py. "
           "A save can have links of several types, so shares add up to more than 100%.", "",
           "## All saves", "", *table(coverage(saves), "Source type"), "",
           "## Order to add sources (each row adds the saves not caught by the rows above)", "",
           "| Source type | New saves caught | Caught so far |", "| --- | --- | --- |",
           *[f"| {t} | {n} | {pct(c)} |" for t, n, c in greedy_cover(saves)], ""]
    for name in focus:
        group = [s for s in saves if s["topic"] == name]
        if not group:
            continue
        linked = [s for s in group if s["links"]]
        out += [f"## {name}", "", f"{len(group)} saves, {len(linked)} with an original link.", "",
                *table(coverage(group), "Source type"), "",
                "| Order to add | New saves caught | Caught so far |", "| --- | --- | --- |",
                *[f"| {t} | {n} | {pct(c)} |" for t, n, c in greedy_cover(group)], ""]
    by_topic = Counter()
    for s in with_links:
        by_topic[s["topic"]] += 1
    out += ["## Top source type per topic", "", "| Topic | Saves with a link | Top source types |", "| --- | --- | --- |"]
    for name, n in by_topic.most_common(25):
        top = ", ".join(f"{t} {pct(sh)}" for t, _, sh in coverage([s for s in saves if s["topic"] == name])[:3])
        out.append(f"| {name} | {n} | {top} |")
    out += [""]
    if ages:
        everything = [d for days in ages.values() for d in days]
        out += ["## How old GitHub repos were when you saved them", "",
                "| Topic | Repos | Median age in days | Saved within 7 days of creation | Within 30 days |",
                "| --- | --- | --- | --- | --- |"]
        rows = [("All topics", everything)] + sorted(((t, d) for t, d in ages.items() if len(d) >= 5),
                                                    key=lambda x: -len(x[1]))
        for name, days in rows:
            out.append(f"| {name} | {len(days)} | {round(statistics.median(days))} | "
                       f"{pct(sum(d <= 7 for d in days) / len(days))} | {pct(sum(d <= 30 for d in days) / len(days))} |")
        out += [""]
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--ig-dir", type=Path, default=feed.IG_DIR)
    args = p.parse_args()
    profile = json.loads(feed.PROFILE_FILE.read_text())
    library = {t["slug"]: t["name"] for t in json.loads(feed.TOPICS_FILE.read_text())["topics"]}
    focus = [library[s] for t in profile["topics"] for s in t.get("library_topics", []) if s in library]
    saves = load(args.ig_dir)
    feed.OUTPUT_DIR.mkdir(exist_ok=True)
    OUT_FILE.write_text(render(saves, focus, repo_ages(saves)), encoding="utf-8")
    print(OUT_FILE.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
