#!/usr/bin/env python3
"""Who posted about the things you saved, before you saved them? Rank the channels that keep coming up, to choose
which creators the fetcher should follow.

For each save in a Focus topic that has an original (from research.py), headless Claude with web search looks for
YouTube videos, X posts, newsletters, blogs, Reddit and other posts about that tool, with dates. Posts from before your
save date count toward a channel's score. Results are cached per save in `output/who_posted.json`, so a rerun only
asks about new saves. The ranking goes to `output/who_posted.md`.
"""

import argparse
import json
import re
import urllib.parse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import feed
import score

CACHE_FILE = feed.OUTPUT_DIR / "who_posted.json"
OUT_FILE = feed.OUTPUT_DIR / "who_posted.md"
AUTHOR_RE = re.compile(r'^author:\s*"?([^"\n]*)"?\s*$', re.M)
TOOLS = "WebSearch,WebFetch"

SYSTEM = """You trace where a tool or idea was talked about online before a given date. Search the web (YouTube,
X, Reddit, Hacker News, LinkedIn, newsletters, blogs, Bluesky, TikTok) for posts about it. Report only posts you
actually saw in search results or opened, with the date shown there. Never invent posts, people, links or dates.
If a date is not visible, leave it empty. Include the maker's own announcement if you find it. Stop after a few
searches; this is a quick scan, not a deep investigation."""

SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "posts": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "platform": {"type": "string", "enum": ["YouTube", "X", "Reddit", "Hacker News", "LinkedIn", "Blog",
                                                         "Newsletter", "Bluesky", "TikTok", "Instagram", "Other"]},
                "who": {"type": "string", "description": "channel, account or site name"},
                "who_url": {"type": "string", "description": "the channel or profile page, not the single post"},
                "post_url": {"type": "string"},
                "posted": {"type": "string", "description": "YYYY-MM-DD, or empty if not shown"},
            },
            "required": ["platform", "who", "who_url", "post_url", "posted"],
        }},
    },
    "required": ["posts"],
})


def focus_saves(profile: dict, model: str, timeout: int) -> list:
    saves = score.load_saves()
    labels = score.focus_topics(saves, profile, model, timeout)
    slugs = {t["slug"] for t in profile["topics"]}
    authors = {}
    for note in feed.IG_DIR.glob("*/*_description.md"):
        found = AUTHOR_RE.search(note.read_text(encoding="utf-8"))
        authors[note.parent.name.split("_", 2)[-1]] = found.group(1).strip() if found else ""
    chosen = []
    for s in saves:
        if labels.get(s["code"]) in slugs and s["links"]:
            chosen.append({**s, "author": authors.get(s["code"], ""), "keys": sorted(s["keys"])})
    return chosen


def ask(save: dict, model: str, timeout: int) -> dict:
    prompt = (f"Tool or idea: {save['title']}\n"
              f"Its original links: {', '.join(save['links'][:4])}\n"
              f"I saved an Instagram post about it from @{save['author'] or 'unknown'} on {save['date']}.\n\n"
              f"Who else posted about it, especially before {save['date']}? List each post with its channel and date.")
    answer = feed.ask_claude(prompt, model, timeout, system=SYSTEM, schema=SCHEMA, tools=TOOLS)
    return {"posts": answer.get("posts", []), "cost_usd": answer.get("cost_usd"), "model": answer.get("model")}


def channel_key(post: dict) -> str:
    """One id per channel or account, so the same creator matches across posts."""
    url = post.get("who_url") or post.get("post_url") or ""
    parsed = urllib.parse.urlparse(url if "://" in url else "https://" + url)
    host = parsed.netloc.lower().removeprefix("www.").removeprefix("m.")
    parts = [p for p in parsed.path.split("/") if p]
    if host in ("youtube.com", "x.com", "twitter.com", "instagram.com", "tiktok.com", "bsky.app", "linkedin.com",
                "reddit.com", "github.com") and parts:
        keep = parts[:2] if parts[0] in ("channel", "c", "user", "in", "r", "u", "profile") else parts[:1]
        return f"{post['platform']}: {host}/{'/'.join(keep).lower()}"
    return f"{post['platform']}: {host or post.get('who', '').lower()}"


def rank(saves: list, cache: dict) -> list:
    channels = defaultdict(lambda: {"saves": set(), "early": set(), "leads": [], "who": "", "url": ""})
    for s in saves:
        result = cache.get(s["code"])
        if not result:
            continue
        for post in result["posts"]:
            if post["platform"] == "Instagram" and s["author"] and s["author"].lower() in post["who_url"].lower():
                continue  # the account you saw it from
            c = channels[channel_key(post)]
            c["who"] = c["who"] or post["who"]
            c["url"] = c["url"] or post["who_url"]
            c["saves"].add(s["code"])
            if post["posted"] and post["posted"] < s["date"]:
                c["early"].add(s["code"])
                c["leads"].append((date.fromisoformat(s["date"]) - date.fromisoformat(post["posted"])).days
                                  if re.match(r"\d{4}-\d{2}-\d{2}$", post["posted"]) else 0)
    rows = [{"key": k, **v} for k, v in channels.items()]
    rows.sort(key=lambda r: (-len(r["early"]), -len(r["saves"]), r["key"]))
    return rows


def render(saves: list, cache: dict, rows: list) -> str:
    done = [s for s in saves if s["code"] in cache]
    platforms = defaultdict(set)
    for s in done:
        for post in cache[s["code"]]["posts"]:
            if post["posted"] and post["posted"] < s["date"]:
                platforms[post["platform"]].add(s["code"])
    cost = sum(cache[s["code"]].get("cost_usd") or 0 for s in done)
    out = ["# Who posted about your saves first", "",
           f"{len(done)} Focus topic saves checked (cost about ${cost:.2f}). A channel counts as early for a save when it "
           "posted before you saved it.", "",
           "## Platforms that had it first", "", "| Platform | Saves it had before you |", "| --- | --- |",
           *[f"| {p} | {len(c)} of {len(done)} |" for p, c in sorted(platforms.items(), key=lambda x: -len(x[1]))], "",
           "## Channels that keep coming up", "",
           "| Channel | Platform link | Saves covered early | Saves covered at all | Median days ahead |",
           "| --- | --- | --- | --- | --- |"]
    for r in rows:
        if len(r["saves"]) < 2 and len(r["early"]) < 1:
            continue
        leads = sorted(r["leads"])
        median = leads[len(leads) // 2] if leads else ""
        out.append(f"| {r['who']} | {r['url']} | {len(r['early'])} | {len(r['saves'])} | {median} |")
    out += ["", "## Per save", ""]
    for s in done:
        early = [p for p in cache[s["code"]]["posts"] if p["posted"] and p["posted"] < s["date"]]
        out.append(f"* {s['date']} {s['title']} (@{s['author']}): {len(early)} earlier posts" +
                   (": " + "; ".join(f"{p['who']} ({p['platform']}, {p['posted']})" for p in early[:4]) if early else ""))
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model", default="sonnet", help="model for the searches (default sonnet)")
    p.add_argument("--workers", type=int, default=4, help="searches run at the same time (default 4)")
    p.add_argument("--limit", type=int, help="only check this many saves (newest first)")
    p.add_argument("--timeout", type=int, default=420)
    args = p.parse_args()
    profile = json.loads(feed.PROFILE_FILE.read_text())
    saves = sorted(focus_saves(profile, "haiku", args.timeout), key=lambda s: s["date"], reverse=True)
    cache = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    todo = [s for s in saves if s["code"] not in cache][:args.limit]
    print(f"{len(saves)} Focus topic saves with an original, {len(todo)} to check")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(ask, s, args.model, args.timeout): s for s in todo}
        for job in as_completed(jobs):
            s = jobs[job]
            try:
                cache[s["code"]] = job.result()
                print(f"  {s['date']} {s['title'][:60]}: {len(cache[s['code']]['posts'])} posts")
            except feed.ClaudeLimit as error:
                print(f"  usage limit: {error}")
                break
            except Exception as error:  # one failed search should not lose the others
                print(f"  ✗ {s['code']}: {error}")
            CACHE_FILE.write_text(json.dumps(cache, indent=1))
    OUT_FILE.write_text(render(saves, cache, rank(saves, cache)), encoding="utf-8")
    print(OUT_FILE.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
