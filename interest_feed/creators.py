#!/usr/bin/env python3
"""Find where Instagram creators post outside Instagram (newsletter, YouTube, blog, Bluesky), find a feed for each, and
check how much of what you saved from them also appeared in that feed, and how many days earlier.

Claude with web search finds the channels (about 5 cents a creator, cached in `output/creators.json`). Python then
finds the feeds: YouTube channel feeds, Substack and blog feeds by autodiscovery, Bluesky profile feeds. X has no
free feed. The report goes to `output/creators.md`; feeds worth following can be added to `profile.json`.
"""

import argparse
import json
import re
import urllib.parse

import feed
import score

CACHE_FILE = feed.OUTPUT_DIR / "creators.json"
OUT_FILE = feed.OUTPUT_DIR / "creators.md"
AUTHOR_RE = re.compile(r'^author:\s*"?([^"\n]*)"?\s*$', re.M)
TOOLS = "WebSearch,WebFetch"

SYSTEM = """You find where an Instagram creator also publishes, outside Instagram: their newsletter, YouTube channel,
blog or website, Bluesky, X, TikTok, LinkedIn. Only list channels you saw in search results or on a page you opened,
and only ones that clearly belong to the same person (same name, links back to the Instagram account, or the
Instagram bio links to it). Never guess URLs. Stop after a few searches."""

SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "the person or brand behind the account"},
        "channels": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "platform": {"type": "string", "enum": ["Newsletter", "YouTube", "Blog or website", "Bluesky", "X",
                                                         "TikTok", "LinkedIn", "Other"]},
                "url": {"type": "string"},
                "evidence": {"type": "string", "description": "how you know it is the same person"},
            },
            "required": ["platform", "url", "evidence"],
        }},
    },
    "required": ["name", "channels"],
})


def find_channels(handle: str, model: str, timeout: int) -> dict:
    prompt = f"Instagram account: @{handle} (https://instagram.com/{handle}/). Where else does this creator publish?"
    answer = feed.ask_claude(prompt, model, timeout, system=SYSTEM, schema=SCHEMA, tools=TOOLS)
    return {"name": answer.get("name", ""), "channels": answer.get("channels", []), "cost_usd": answer.get("cost_usd")}


def feed_for(channel: dict) -> str:
    """A feed URL for a channel, or "" when there is none a script can read."""
    url = channel["url"] if "://" in channel["url"] else "https://" + channel["url"]
    host = urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    try:
        if host in ("youtube.com", "m.youtube.com"):
            page = feed.get(url).decode("utf-8", errors="ignore")
            found = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{22})"', page)
            return f"https://www.youtube.com/feeds/videos.xml?channel_id={found.group(1)}" if found else ""
        if host == "bsky.app":
            return url.rstrip("/") + "/rss"
        if host.endswith("substack.com"):
            return f"https://{host}/feed"
        if host in ("x.com", "twitter.com", "tiktok.com", "linkedin.com", "instagram.com", "linktr.ee"):
            return ""
        page = feed.get(url).decode("utf-8", errors="ignore")
        for tag in re.findall(r"<link[^>]+>", page):
            if re.search(r"application/(rss|atom)\+xml", tag):
                href = re.search(r'href="([^"]+)"', tag)
                if href:
                    return urllib.parse.urljoin(url, href.group(1))
        for guess in ("/feed", "/rss", "/rss.xml", "/feed.xml", "/atom.xml"):  # common spots when not advertised
            try:
                text = feed.get(urllib.parse.urljoin(url, guess))[:400].decode("utf-8", errors="ignore")
                if "<rss" in text or "<feed" in text:
                    return urllib.parse.urljoin(url, guess)
            except Exception:
                continue
    except Exception:
        return ""
    return ""


def overlap(handle: str, feed_items: list, saves: list, authors: dict) -> list:
    """Your saves from this creator that also appear in their feed, matched by original links, with days earlier."""
    mine = [s for s in saves if authors.get(s["code"], "").lower() == handle.lower()]
    found = []
    for s in mine:
        for item in feed_items:
            keys = {feed.link_key(item["url"])} | {feed.link_key(u) for u in item.get("links", [])}
            if s["keys"] & keys:
                posted = (feed.parse_time(item["published"]) or None)
                days = (feed.datetime.fromisoformat(s["date"]).date() - posted.date()).days if posted else None
                found.append((s, item, days))
                break
    return mine, found


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("handles", nargs="+", help="Instagram handles, without @")
    p.add_argument("--model", default="sonnet")
    p.add_argument("--timeout", type=int, default=420)
    p.add_argument("--redo", action="store_true", help="search again even if cached")
    args = p.parse_args()

    cache = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    saves = score.load_saves()
    authors = {}
    for note in feed.IG_DIR.glob("*/*_description.md"):
        found = AUTHOR_RE.search(note.read_text(encoding="utf-8"))
        authors[note.parent.name.split("_", 2)[-1]] = found.group(1).strip() if found else ""

    lines = ["# Creators outside Instagram", "",
             "| Account | Name | Channel | Feed | Your saves from them | Also in that feed | Median days earlier |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for handle in args.handles:
        if args.redo or handle not in cache:
            print(f"searching @{handle}")
            cache[handle] = find_channels(handle, args.model, args.timeout)
        entry = cache[handle]
        for channel in entry["channels"]:
            channel.setdefault("feed", feed_for(channel))
        CACHE_FILE.write_text(json.dumps(cache, indent=1))
        if not entry["channels"]:
            lines.append(f"| {handle} | {entry['name']} | none found | | | | |")
        for channel in entry["channels"]:
            items = []
            if channel["feed"]:
                try:
                    items = feed.atom_items(channel["feed"], channel["platform"])
                except Exception as error:
                    channel["feed_error"] = str(error)[:120]
            mine, hits = overlap(handle, items, saves, authors)
            days = sorted(d for _, _, d in hits if d is not None)
            median = days[len(days) // 2] if days else ""
            lines.append(f"| {handle} | {entry['name']} | {channel['platform']}: {channel['url']} | "
                         f"{channel['feed'] or 'no feed'}{' (' + str(len(items)) + ' entries)' if items else ''} | "
                         f"{len(mine)} | {len(hits)} | {median} |")
    CACHE_FILE.write_text(json.dumps(cache, indent=1))
    OUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT_FILE.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
