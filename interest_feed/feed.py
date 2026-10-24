#!/usr/bin/env python3
"""Weekly interest digest: check trusted sources for the Focus topics and keep only the few items worth acting on.

Version 1 of the information gathering plan (vault note `claude - What to do with the knowledge libraries`).
`profile.json` holds the Focus topics (keywords to search for and avoid, items per week) and the sources:
GitHub releases and commits, new GitHub repos by keyword, subreddits and Hacker News. All of them are free feeds.

New items since the last run go to one headless Claude call (`claude -p`, on the Claude subscription, no tools),
which matches each item to a topic, drops promos and scores the rest. The top items per topic become a digest in
`output/digests/`, and with `--vault` also a note in the vault's `ZAIHub/Interest digest/` folder.

Runs on the Mac and on the Pi. It needs only Python 3 and the logged in Claude CLI.
"""

import argparse
import html
import json
import logging
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROFILE_FILE = HERE / "profile.json"
OUTPUT_DIR = HERE / "output"
DIGEST_DIR = OUTPUT_DIR / "digests"
SEEN_FILE = OUTPUT_DIR / "seen.json"
LOG_FILE = OUTPUT_DIR / "feed.log"
IG_DIR = HERE.parent / "IG"
TOPICS_FILE = HERE.parent / "knowledge_library" / "topics.json"
TASTE_PER_TOPIC = 15

VAULT_GUESSES = [Path.home() / "Dev/obsidian/Bogle", Path.home() / "Work/obsidian/Bogle", Path.home() / "obsidian/Bogle"]
VAULT_DIGEST_DIR = Path("ZAIHub/Interest digest")
FOCUS_NOTE = "claude - Focus topics - coding agents and agent skills"

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/130 Safari/537.36")  # Reddit refuses non browser agents
FETCH_TIMEOUT = 30
SNIPPET_CHARS = 400
MAX_ITEMS = 200
SEARCH_REPOS_PER_QUERY = 5
SEEN_KEEP_DAYS = 60
REDDIT_PAUSE = 5  # seconds between subreddits; back to back requests get HTTP 429
PRERELEASE_RE = re.compile(r"-(alpha|beta|rc)\b", re.I)
ATOM = "{http://www.w3.org/2005/Atom}"

CLAUDE_TIMEOUT = 600
CLAUDE_LIMIT_RE = re.compile(r"usage limit|rate limit|limit reached|out of extra usage|hit your limit", re.I)

CLAUDE_SYSTEM = """You pick finds for one person who builds software and wants to get better at it.
You are given posts they saved on Instagram and found worth it. Judge each new item by one question: would this
person have saved this? They save discoveries: a new tool or repo that does something useful or impressive, a demo,
a method or workflow they can try. They do not save changelogs, version bumps, minor fixes, news with nothing to try,
promos, teasers or giveaways. Match each pick to one of their Focus topics and skip anything on the avoid lists.
Items marked [update] are releases of tools they already use: never make them picks; list one only if the release has
a change they would notice, as a single short line. Never invent items or links; use the item numbers given."""

CLAUDE_SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "picks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {"type": "integer", "description": "the item number from the list"},
                    "topic": {"type": "string", "description": "the Focus topic slug"},
                    "score": {"type": "integer", "minimum": 1, "maximum": 5, "description": "5 = they would save it for sure"},
                    "name": {"type": "string", "description": "short name of the tool, repo or idea"},
                    "what": {"type": "string", "description": "one plain sentence: what it does"},
                    "why": {"type": "string", "description": "one plain sentence: why this person would care, tied to what they save"},
                },
                "required": ["item", "topic", "score", "name", "what", "why"],
            },
        },
        "updates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {"type": "integer"},
                    "line": {"type": "string", "description": "one short line: the change they would notice"},
                },
                "required": ["item", "line"],
            },
        },
    },
    "required": ["picks", "updates"],
})

logger = logging.getLogger("interest_feed")


class ClaudeLimit(Exception):
    """The Claude subscription's usage limit was hit; try again after it resets."""


# ---------------------------------------------------------------- fetching


def get(url: str, accept: str = "") -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **({"Accept": accept} if accept else {})})
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
        return response.read()


def plain(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    return re.sub(r"\s+", " ", text).strip()[:SNIPPET_CHARS]


def parse_time(value: str):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def atom_items(url: str, source: str) -> list:
    root = ET.fromstring(get(url))
    items = []
    for entry in root.iter(f"{ATOM}entry"):
        link = entry.find(f"{ATOM}link")
        body = entry.find(f"{ATOM}content")
        if body is None:
            body = entry.find(f"{ATOM}summary")
        items.append({
            "id": entry.findtext(f"{ATOM}id") or (link.get("href") if link is not None else ""),
            "source": source,
            "title": plain(entry.findtext(f"{ATOM}title") or ""),
            "url": link.get("href") if link is not None else "",
            "published": entry.findtext(f"{ATOM}updated") or entry.findtext(f"{ATOM}published") or "",
            "snippet": plain(body.text if body is not None else ""),
        })
    return items


def github_releases(repo: str, since) -> list:
    items = atom_items(f"https://github.com/{repo}/releases.atom", f"GitHub release, {repo}")
    return [{**i, "update": True} for i in items if not PRERELEASE_RE.search(i["title"])]


def github_commits(repo: str, since) -> list:
    return atom_items(f"https://github.com/{repo}/commits.atom", f"GitHub commit, {repo}")


def reddit(sub: str, since) -> list:
    time.sleep(REDDIT_PAUSE)
    try:
        return atom_items(f"https://www.reddit.com/r/{sub}/top/.rss?t=week", f"Reddit top of the week, r/{sub}")
    except urllib.error.HTTPError:  # the top listing is refused more often than the front page
        time.sleep(REDDIT_PAUSE)
        return atom_items(f"https://www.reddit.com/r/{sub}/.rss", f"Reddit, r/{sub}")


def github_search(query: str, since) -> list:
    q = f"{query} created:>{since.date().isoformat()} stars:>=10"
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q, "sort": "stars", "order": "desc", "per_page": SEARCH_REPOS_PER_QUERY})
    data = json.loads(get(url, "application/vnd.github+json"))
    return [{
        "id": repo["html_url"],
        "source": f"New GitHub repo, search '{query}'",
        "title": f"{repo['full_name']} ({repo['stargazers_count']} stars)",
        "url": repo["html_url"],
        "published": repo["created_at"],
        "snippet": plain(repo.get("description") or ""),
    } for repo in data.get("items", [])]


def hackernews(query: str, since) -> list:
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": f'"{query}"', "advancedSyntax": "true", "typoTolerance": "false", "tags": "story",
         "restrictSearchableAttributes": "title", "numericFilters": f"created_at_i>{int(since.timestamp())},points>20"})
    data = json.loads(get(url))
    return [{
        "id": f"hn-{hit['objectID']}",
        "source": f"Hacker News, search '{query}' ({hit.get('points', 0)} points)",
        "title": plain(hit.get("title") or ""),
        "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
        "published": hit.get("created_at") or "",
        "snippet": f"Discussion: https://news.ycombinator.com/item?id={hit['objectID']}",
    } for hit in data.get("hits", [])]


def show_hn(query: str, since) -> list:
    """Show HN posts: people sharing something they built."""
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": f'"{query}"', "advancedSyntax": "true", "typoTolerance": "false", "tags": "show_hn",
         "restrictSearchableAttributes": "title", "numericFilters": f"created_at_i>{int(since.timestamp())},points>5"})
    data = json.loads(get(url))
    return [{
        "id": f"hn-{hit['objectID']}",
        "source": f"Show HN, search '{query}' ({hit.get('points', 0)} points)",
        "title": plain(hit.get("title") or ""),
        "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
        "published": hit.get("created_at") or "",
        "snippet": f"Discussion: https://news.ycombinator.com/item?id={hit['objectID']}",
    } for hit in data.get("hits", [])]


FETCHERS = {
    "github_releases": github_releases,
    "github_commits": github_commits,
    "github_search": github_search,
    "reddit": reddit,
    "hackernews": hackernews,
    "show_hn": show_hn,
}


def fetch_all(sources: dict, since) -> list:
    items, ids = [], set()
    for kind, names in sources.items():
        fetcher = FETCHERS.get(kind)
        if not fetcher:
            logger.warning(f"  unknown source type '{kind}' in profile.json, skipped")
            continue
        for name in names:
            try:
                found = fetcher(name, since)
            except Exception as error:  # one dead feed should not stop the digest
                logger.warning(f"  ✗ {kind} {name}: {error}")
                continue
            fresh = [i for i in found if i["id"] not in ids and (parse_time(i["published"]) or since) >= since]
            ids.update(i["id"] for i in fresh)
            items += fresh
            logger.info(f"  {kind} {name}: {len(fresh)} new this window")
    return items


# ---------------------------------------------------------------- filtering


def taste_examples(profile: dict) -> dict:
    """Topic slug to the titles and openings of saved posts that research.py marked Valid, newest first.

    Read from the post notes (tracked in git), so it works on the Pi too, where research.json is not synced."""
    if not TOPICS_FILE.exists() or not IG_DIR.is_dir():
        return {}
    library = {t["slug"]: set(t["sources"]) for t in json.loads(TOPICS_FILE.read_text())["topics"]}
    examples = {}
    for topic in profile["topics"]:
        codes = set().union(*(library.get(slug, set()) for slug in topic.get("library_topics", [])))
        found = []
        for folder in sorted(IG_DIR.iterdir(), reverse=True):
            code = folder.name.split("_", 2)[-1]
            if code not in codes or len(found) >= TASTE_PER_TOPIC:
                continue
            for note in folder.glob("*_description.md"):
                text = note.read_text(encoding="utf-8")
                if not re.search(r"^\* Verdict: Valid\b", text, re.M):
                    continue
                title = re.search(r"^# (.+)", text, re.M)
                body = text.split("\n# ", 1)[-1].split("\n\n", 2)
                opening = plain(body[1] if len(body) > 1 else "")[:200]
                found.append(f"{title.group(1) if title else code}: {opening}")
        examples[topic["slug"]] = found
    return examples


def claude_prompt(profile: dict, items: list, examples: dict) -> str:
    topics = "\n".join(
        f"* {t['slug']} ({t['name']}): about {', '.join(t['search'])}. Avoid {', '.join(t['avoid'])}."
        for t in profile["topics"])
    taste = "\n\n".join(
        f"{slug}:\n" + "\n".join(f"* {e}" for e in found) for slug, found in examples.items() if found)
    listing = "\n\n".join(
        f"[{n}]{' [update]' if i.get('update') else ''} {i['title']}\nSource: {i['source']}\nLink: {i['url']}\n{i['snippet']}"
        for n, i in enumerate(items))
    return (f"Focus topics:\n{topics}\n\n"
            f"Posts this person saved on Instagram and found worth it (this is their taste):\n\n{taste or 'none yet'}\n\n"
            f"Items found this week:\n\n{listing}\n\n"
            "Return the picks they would have saved, each with its topic slug and a score, and the few updates worth a line.")


def ask_claude(prompt: str, model: str, timeout: int) -> dict:
    """The picks, the model id and the cost, from one headless `claude -p` run on the subscription login."""
    cmd = [
        "claude", "-p", prompt,
        "--model", model,
        "--system-prompt", CLAUDE_SYSTEM,
        "--safe-mode", "--strict-mcp-config",  # no CLAUDE.md, hooks, plugins or MCP servers
        "--tools", "",
        "--no-session-persistence",
        "--output-format", "json",
        "--json-schema", CLAUDE_SCHEMA,
    ]
    out = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=timeout)
    try:
        result = json.loads(out.stdout)
    except json.JSONDecodeError:
        message = (out.stderr or out.stdout).strip()[:300] or f"exit code {out.returncode}"
        if CLAUDE_LIMIT_RE.search(message):
            raise ClaudeLimit(message)
        raise RuntimeError(f"claude gave no JSON: {message}")
    if result.get("is_error") or out.returncode != 0:
        message = str(result.get("result") or result.get("subtype") or f"exit code {out.returncode}")[:300]
        if result.get("api_error_status") == 429 or CLAUDE_LIMIT_RE.search(message):
            raise ClaudeLimit(message)
        raise RuntimeError(f"claude: {message}")
    answer = result.get("structured_output") or {}
    answer["model"] = next(iter(result.get("modelUsage") or {}), model)
    answer["cost_usd"] = result.get("total_cost_usd")
    return answer


def top_picks(answer: dict, items: list, profile: dict) -> dict:
    """Topic slug to its best picks, capped at the topic's `per_week`."""
    chosen = {t["slug"]: [] for t in profile["topics"]}
    seen = set()
    for pick in sorted(answer.get("picks", []), key=lambda p: -p["score"]):
        n, slug = pick["item"], pick["topic"]
        if slug not in chosen or not 0 <= n < len(items) or n in seen or items[n].get("update"):
            continue
        if len(chosen[slug]) < next(t["per_week"] for t in profile["topics"] if t["slug"] == slug):
            chosen[slug].append({**items[n], **pick})
            seen.add(n)
    return chosen


def notable_updates(answer: dict, items: list) -> list:
    """One line per release worth noticing, at most one per tool."""
    lines, tools = [], set()
    for update in answer.get("updates", []):
        n = update["item"]
        if 0 <= n < len(items) and items[n].get("update") and items[n]["source"] not in tools:
            tools.add(items[n]["source"])
            lines.append({**items[n], **update})
    return lines


# ---------------------------------------------------------------- digest


def web_link(title: str, url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.removeprefix("www.")
    title = title.replace("[", "(").replace("]", ")")
    return f"Web: [{title} ({host})]({url})" if host else title


def render_digest(chosen: dict, updates: list, profile: dict, today: str, checked: int, model: str,
                  for_vault: bool) -> str:
    lines = []
    if for_vault:
        lines += ["---", f"name: claude - interest digest {today}", f"created: {today}", "---", "",
                  "#interest-digest #aiplan", "", "## Prompt", "",
                  f"Weekly digest from Outside vault: `{HERE / 'feed.py'}`, using the Focus topics in [[{FOCUS_NOTE}]].",
                  "", f"## Response (Claude, {today})", ""]
    else:
        lines += [f"# Interest digest {today}", ""]
    lines += [f"Checked {checked} new items from the sources in `profile.json`. Picked by {model}.", ""]
    for topic in profile["topics"]:
        lines += [f"### {topic['name']}", ""]
        picks = chosen.get(topic["slug"]) or []
        if not picks:
            lines += ["Nothing you would have saved this week.", ""]
        for p in picks:
            lines += [f"* **{p['name']}**: {p['what']}", f"\t* Why you would care: {p['why']}",
                      f"\t* {web_link(p['title'], p['url'])}", f"\t* Found via {p['source']}", ""]
    if updates:
        lines += ["### Tools you use", ""]
        lines += [f"* {u['source'].split(', ', 1)[-1]}: {u['line']} {web_link(u['title'], u['url'])}" for u in updates]
        lines += [""]
    lines += ["### Feedback", "", "* Useful:", "* Not useful:", ""]
    return "\n".join(lines)


def find_vault(arg):
    for candidate in [arg, os.environ.get("IG_VAULT"), *VAULT_GUESSES]:
        if candidate and (Path(candidate) / "ZAIHub").is_dir():
            return Path(candidate)
    return None


# ---------------------------------------------------------------- state


def load_seen() -> dict:
    return json.loads(SEEN_FILE.read_text()) if SEEN_FILE.exists() else {}


def save_seen(seen: dict, items: list, now) -> None:
    cutoff = (now - timedelta(days=SEEN_KEEP_DAYS)).isoformat()
    seen = {k: v for k, v in seen.items() if v >= cutoff}
    seen.update({i["id"]: now.isoformat() for i in items})
    tmp = SEEN_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(seen, indent=1))
    tmp.replace(SEEN_FILE)


# ---------------------------------------------------------------- main


def parse_args():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--days", type=int, default=7, help="how far back to look (default 7)")
    p.add_argument("--vault", nargs="?", const="", default=None,
                   help="also write the digest into the vault's ZAIHub/Interest digest/ (optionally give the vault path)")
    p.add_argument("--model", default="haiku", help="model for claude -p (default haiku)")
    p.add_argument("--timeout", type=int, default=CLAUDE_TIMEOUT, help="seconds for the Claude call")
    p.add_argument("--dry-run", action="store_true", help="fetch and list the new items, no Claude call, nothing saved")
    p.add_argument("--all", action="store_true", help="include items already seen in earlier runs")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    OUTPUT_DIR.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    file_log = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_log.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_log)

    profile = json.loads(PROFILE_FILE.read_text())
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=args.days)
    logger.info(f"=== feed.py (last {args.days} days, model {args.model})")

    seen = load_seen()
    items = fetch_all(profile["sources"], since)
    if not args.all:
        items = [i for i in items if i["id"] not in seen]
    items = sorted(items, key=lambda i: i["published"], reverse=True)[:MAX_ITEMS]
    logger.info(f"{len(items)} new items to filter")

    if args.dry_run:
        for i in items:
            print(f"* {i['source']}: {i['title']}\n  {i['url']}")
        return 0
    if not items:
        logger.info("Nothing new. No digest written.")
        return 0

    try:
        answer = ask_claude(claude_prompt(profile, items, taste_examples(profile)), args.model, args.timeout)
    except ClaudeLimit as error:
        logger.warning(f"Claude usage limit: {error}")
        return 75
    chosen = top_picks(answer, items, profile)
    updates = notable_updates(answer, items)
    today = datetime.now().date().isoformat()
    model = answer["model"]

    DIGEST_DIR.mkdir(exist_ok=True)
    digest = DIGEST_DIR / f"{today}.md"
    digest.write_text(render_digest(chosen, updates, profile, today, len(items), model, for_vault=False), encoding="utf-8")
    logger.info(f"Digest: {digest}")
    if args.vault is not None:
        vault = find_vault(args.vault or None)
        if not vault:
            logger.warning("No vault found. Give the path with --vault DIR or IG_VAULT.")
        else:
            note = vault / VAULT_DIGEST_DIR / f"claude - interest digest {today}.md"
            note.parent.mkdir(exist_ok=True)
            note.write_text(render_digest(chosen, updates, profile, today, len(items), model, for_vault=True), encoding="utf-8")
            logger.info(f"Vault note: {note}")

    save_seen(seen, items, now)
    picked = sum(len(v) for v in chosen.values())
    logger.info(f"Done. Picked {picked} of {len(items)} | Cost reported by Claude: ${answer.get('cost_usd') or 0:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
