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
import gzip
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
HISTORY_FILE = OUTPUT_DIR / "history.jsonl"
BACKTEST_DIR = OUTPUT_DIR / "backtest"
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
MAX_ITEMS = 300
SEARCH_REPOS_PER_QUERY = 5
SEEN_KEEP_DAYS = 60
ARCHIVE_PAUSE = 4  # seconds between Wayback Machine requests; faster gets HTTP 429
ARCHIVE_CACHE_DIR = OUTPUT_DIR / "cache" / "archive"
PAGE_SNAPSHOT_DIR = OUTPUT_DIR / "cache" / "pages"
AWESOME_KEEP = 25  # newest additions kept per awesome list
REPO_LINK_RE = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
TRENDING_SNAPSHOT_DAYS = 3  # how far an archived trending page may be from the backtest date
GITHUB_PAUSE = 7  # seconds between searches; GitHub allows 10 a minute without a login
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
    headers = {"User-Agent": USER_AGENT, **({"Accept": accept} if accept else {})}
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"  # 30 searches a minute instead of 10
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
        data = response.read()
    return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data  # the Wayback Machine sends raw pages gzipped


def link_key(url: str) -> str:
    """One id per thing, so the same repo, paper or model matches across sites and link styles."""
    parsed = urllib.parse.urlparse(url.strip())
    host = parsed.netloc.lower().removeprefix("www.").removeprefix("m.")
    parts = [x for x in parsed.path.split("/") if x]
    if host == "github.com" and len(parts) >= 2:
        return f"github:{parts[0].lower()}/{parts[1].lower().removesuffix('.git')}"
    if host == "arxiv.org" and len(parts) >= 2:
        return "arxiv:" + re.sub(r"v\d+$", "", parts[1].removesuffix(".pdf"))
    if host == "huggingface.co" and parts:
        parts = parts[1:] if parts[0] in ("spaces", "datasets") else parts
        return "hf:" + "/".join(parts[:2]).lower()
    if host in ("x.com", "twitter.com") and "status" in parts:
        return "x:" + parts[parts.index("status") + 1]
    if host == "news.ycombinator.com":
        return "hn:" + urllib.parse.parse_qs(parsed.query).get("id", [""])[0]
    return host + "/" + "/".join(parts).lower()


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


def github_releases(repo: str, since, until) -> list:
    items = atom_items(f"https://github.com/{repo}/releases.atom", f"GitHub release, {repo}")
    return [{**i, "update": True} for i in items if not PRERELEASE_RE.search(i["title"])]


def github_commits(repo: str, since, until) -> list:
    return atom_items(f"https://github.com/{repo}/commits.atom", f"GitHub commit, {repo}")


def reddit(sub: str, since, until) -> list:
    time.sleep(REDDIT_PAUSE)
    try:
        return atom_items(f"https://www.reddit.com/r/{sub}/top/.rss?t=week", f"Reddit top of the week, r/{sub}")
    except urllib.error.HTTPError:  # the top listing is refused more often than the front page
        time.sleep(REDDIT_PAUSE)
        return atom_items(f"https://www.reddit.com/r/{sub}/.rss", f"Reddit, r/{sub}")


def github_search(query: str, since, until) -> list:
    time.sleep(GITHUB_PAUSE)
    q = f"{query} created:{since.date().isoformat()}..{until.date().isoformat()} stars:>=10"
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


def hackernews(query: str, since, until) -> list:
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": f'"{query}"', "advancedSyntax": "true", "typoTolerance": "false", "tags": "story",
         "restrictSearchableAttributes": "title", "numericFilters": f"created_at_i>{int(since.timestamp())},created_at_i<{int(until.timestamp())},points>20"})
    data = json.loads(get(url))
    return [{
        "id": f"hn-{hit['objectID']}",
        "source": f"Hacker News, search '{query}' ({hit.get('points', 0)} points)",
        "title": plain(hit.get("title") or ""),
        "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
        "published": hit.get("created_at") or "",
        "snippet": f"Discussion: https://news.ycombinator.com/item?id={hit['objectID']}",
    } for hit in data.get("hits", [])]


def is_past(when) -> bool:
    return when < datetime.now(timezone.utc) - timedelta(days=1)


def archived_text(page: str, when) -> str:
    """The Wayback Machine copy of a page nearest to `when` (within TRENDING_SNAPSHOT_DAYS), cached on disk."""
    lookup = "https://archive.org/wayback/available?" + urllib.parse.urlencode(
        {"url": page.removeprefix("https://"), "timestamp": when.strftime("%Y%m%d")})
    snap = {}
    for _ in range(3):  # the lookup sometimes comes back empty or offline; asking again usually works
        time.sleep(ARCHIVE_PAUSE)
        try:
            snap = json.loads(get(lookup)).get("archived_snapshots", {}).get("closest", {})
        except (json.JSONDecodeError, urllib.error.URLError):
            snap = {}
        if snap.get("timestamp"):
            break
        time.sleep(5)
    if not snap.get("timestamp"):  # fall back to letting the archive redirect to its nearest copy
        request = urllib.request.Request(f"https://web.archive.org/web/{when:%Y%m%d}id_/{page}",
                                         headers={"User-Agent": USER_AGENT}, method="HEAD")
        with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
            found = re.search(r"/web/(\d{14})", response.geturl())
        snap = {"timestamp": found.group(1)} if found else {}
    if not snap.get("timestamp"):
        raise RuntimeError(f"no archived copy of {page}")
    taken = datetime.strptime(snap["timestamp"], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    if abs(taken - when) > timedelta(days=TRENDING_SNAPSHOT_DAYS):
        raise RuntimeError(f"no archived copy within {TRENDING_SNAPSHOT_DAYS} days of {when.date()}")
    cache = ARCHIVE_CACHE_DIR / (re.sub(r"[^A-Za-z0-9]+", "_", page)[:120] + f"-{snap['timestamp']}.html")
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    time.sleep(ARCHIVE_PAUSE)
    text = get(f"https://web.archive.org/web/{snap['timestamp']}id_/{page}").decode("utf-8", errors="ignore")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(text, encoding="utf-8")
    return text


def github_trending(language: str, since, until) -> list:
    """GitHub trending for the week (all languages when blank). A backtest reads the Wayback Machine copy of the page
    from that date, since GitHub keeps no trending history."""
    page = f"https://github.com/trending{'/' + language if language else ''}?since=weekly"
    text = archived_text(page, until) if is_past(until) else get(page).decode("utf-8", errors="ignore")
    items = []
    for block in text.split('<article class="Box-row">')[1:]:
        name = re.search(r'<h2[^>]*>.*?href="(?:https://github\.com)?/([^"/]+/[^"/]+)"', block, re.S)
        if not name:
            continue
        about = re.search(r'<p class="col-9[^"]*">(.*?)</p>', block, re.S)
        stars = re.search(r"([\d,]+) stars this week", block)
        repo = name.group(1)
        items.append({
            "id": f"https://github.com/{repo}",
            "source": f"GitHub trending this week{', ' + language if language else ''}",
            "title": f"{repo} (+{stars.group(1) if stars else '?'} stars this week)",
            "url": f"https://github.com/{repo}",
            "published": (until - timedelta(seconds=1)).isoformat(),
            "snippet": plain(about.group(1) if about else ""),
        })
    return items


def awesome_list(repo: str, since, until) -> list:
    """Repos added to an awesome list's README during the window: older repos that just caught on."""
    repo, _, path = repo.partition(":")
    path = path or "README.md"

    def sha_at(when):
        url = f"https://api.github.com/repos/{repo}/commits?" + urllib.parse.urlencode(
            {"path": path, "until": when.isoformat()[:19] + "Z", "per_page": 1})
        commits = json.loads(get(url, "application/vnd.github+json"))
        return commits[0]["sha"] if commits else ""

    def repo_lines(sha):
        if not sha:
            return {}
        text = get(f"https://raw.githubusercontent.com/{repo}/{sha}/{path}").decode("utf-8", errors="ignore")
        lines = {}
        for line in text.splitlines():
            for name in REPO_LINK_RE.findall(line):
                name = name.removesuffix(".git").rstrip(".")
                if name.lower() != repo.lower() and "/" in name:
                    lines.setdefault(name.lower(), (name, line))
        return lines

    before, after = sha_at(since), sha_at(until)
    if not after or before == after:
        return []
    old, new = repo_lines(before), repo_lines(after)
    added = [new[k] for k in new if k not in old][-AWESOME_KEEP:]
    return [{
        "id": f"https://github.com/{name}",
        "source": f"Added to {repo}",
        "title": f"{name} (added to {repo.split('/')[-1]})",
        "url": f"https://github.com/{name}",
        "published": (until - timedelta(seconds=1)).isoformat(),
        "snippet": plain(line),
    } for name, line in added]


def hn_github(query: str, since, until) -> list:
    """GitHub repos of any age that people posted to Hacker News in the window."""
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": query or "github.com", "restrictSearchableAttributes": "url", "tags": "story", "hitsPerPage": 100,
         "numericFilters": f"created_at_i>{int(since.timestamp())},created_at_i<{int(until.timestamp())},points>10"})
    items = []
    for hit in json.loads(get(url)).get("hits", []):
        found = REPO_LINK_RE.search(hit.get("url") or "")
        if not found:
            continue
        name = "/".join(found.group(1).split("/")[:2])
        items.append({
            "id": f"https://github.com/{name}",
            "source": f"GitHub repo on Hacker News ({hit.get('points', 0)} points)",
            "title": f"{name}: {plain(hit.get('title') or '')}",
            "url": f"https://github.com/{name}",
            "published": hit.get("created_at") or "",
            "snippet": f"Discussion: https://news.ycombinator.com/item?id={hit['objectID']}",
        })
    return items


def page_links(spec: str, since, until) -> list:
    """New links on a page since the last check, as "URL | link prefix". Live runs compare with the copy saved last
    time (the first run only saves it); backtests compare the Wayback Machine copies from the start and end of the
    window."""
    page, _, prefix = (x.strip() for x in spec.partition("|"))
    link_re = re.compile(r"\[([^\]]+)\]\((" + re.escape(prefix) + r"[^)\s]*)\)|href=\"(" + re.escape(prefix) + r"[^\"]*)\"")

    def links(text):
        found = {}
        for label, md_url, html_url in link_re.findall(text):
            found.setdefault(md_url or html_url, plain(label) or (md_url or html_url).rstrip("/").split("/")[-1])
        return found

    if is_past(until):
        old, new = links(archived_text(page, since)), links(archived_text(page, until))
    else:
        snapshot = PAGE_SNAPSHOT_DIR / (re.sub(r"[^A-Za-z0-9]+", "_", page)[:120] + ".json")
        new = links(get(page).decode("utf-8", errors="ignore"))
        old = json.loads(snapshot.read_text()) if snapshot.exists() else None
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_text(json.dumps(new, indent=1))
        if old is None:
            logger.info(f"  first check of {page}: saved {len(new)} links to compare next time")
            return []
    host = urllib.parse.urlparse(page).netloc
    return [{
        "id": url,
        "source": f"New on {host}",
        "title": label,
        "url": url,
        "published": (until - timedelta(seconds=1)).isoformat(),
        "snippet": f"New link on {page}",
    } for url, label in new.items() if url not in old]


def feeds(url: str, since, until) -> list:
    """Any Atom feed, such as a blog."""
    return atom_items(url, f"Blog, {urllib.parse.urlparse(url).netloc.removeprefix('www.')}")


def show_hn(query: str, since, until) -> list:
    """Show HN posts: people sharing something they built."""
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": f'"{query}"', "advancedSyntax": "true", "typoTolerance": "false", "tags": "show_hn",
         "restrictSearchableAttributes": "title", "numericFilters": f"created_at_i>{int(since.timestamp())},created_at_i<{int(until.timestamp())},points>5"})
    data = json.loads(get(url))
    return [{
        "id": f"hn-{hit['objectID']}",
        "source": f"Show HN, search '{query}' ({hit.get('points', 0)} points)",
        "title": plain(hit.get("title") or ""),
        "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
        "published": hit.get("created_at") or "",
        "snippet": f"Discussion: https://news.ycombinator.com/item?id={hit['objectID']}",
    } for hit in data.get("hits", [])]


BACKDATABLE = {"github_search", "github_trending", "hackernews", "show_hn", "awesome_list", "hn_github", "page_links"}  # sources that can search a past window, for --as-of

FETCHERS = {
    "github_releases": github_releases,
    "github_commits": github_commits,
    "github_search": github_search,
    "reddit": reddit,
    "hackernews": hackernews,
    "show_hn": show_hn,
    "github_trending": github_trending,
    "awesome_list": awesome_list,
    "hn_github": hn_github,
    "page_links": page_links,
    "feeds": feeds,
}


def fetch_all(sources: dict, since, until, backtest: bool = False) -> list:
    items, ids = [], set()
    for kind, names in sources.items():
        fetcher = FETCHERS.get(kind)
        if not fetcher:
            logger.warning(f"  unknown source type '{kind}' in profile.json, skipped")
            continue
        if backtest and kind not in BACKDATABLE:
            logger.info(f"  {kind}: skipped, its feed only shows recent items")
            continue
        for name in names:
            try:
                found = fetcher(name, since, until)
            except Exception as error:  # one dead feed should not stop the digest
                logger.warning(f"  ✗ {kind} {name}: {error}")
                continue
            fresh = [i for i in found if i["id"] not in ids and since <= (parse_time(i["published"]) or since) <= until]
            ids.update(i["id"] for i in fresh)
            items += fresh
            logger.info(f"  {kind} {name}: {len(fresh)} new this window")
    return items


# ---------------------------------------------------------------- filtering


def taste_examples(profile: dict, before: str = "") -> dict:
    """Topic slug to the titles and openings of saved posts that research.py marked Valid, newest first.

    Read from the post notes (tracked in git), so it works on the Pi too, where research.json is not synced.
    `before` (YYYY-MM-DD) keeps out saves from that date on, so a backtest is not shown the answers."""
    if not TOPICS_FILE.exists() or not IG_DIR.is_dir():
        return {}
    library = {t["slug"]: set(t["sources"]) for t in json.loads(TOPICS_FILE.read_text())["topics"]}
    examples = {}
    for topic in profile["topics"]:
        codes = set().union(*(library.get(slug, set()) for slug in topic.get("library_topics", [])))
        found = []
        for folder in sorted(IG_DIR.iterdir(), reverse=True):
            code = folder.name.split("_", 2)[-1]
            if code not in codes or len(found) >= TASTE_PER_TOPIC or (before and folder.name[:10] >= before):
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


def ask_claude(prompt: str, model: str, timeout: int, system: str = CLAUDE_SYSTEM, schema: str = CLAUDE_SCHEMA,
               tools: str = "") -> dict:
    """The picks, the model id and the cost, from one headless `claude -p` run on the subscription login."""
    cmd = [
        "claude", "-p", prompt,
        "--model", model,
        "--system-prompt", system,
        "--safe-mode", "--strict-mcp-config",  # no CLAUDE.md, hooks, plugins or MCP servers
        "--tools", tools, *(["--allowedTools", tools] if tools else []),
        "--no-session-persistence",
        "--output-format", "json",
        "--json-schema", schema,
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
    lines += [f"Checked {checked} new items from the sources in `profile.json`. Picked by {model}.",
              "Tick a pick if you would have saved it. `score.py` reads the ticks.", ""]
    for topic in profile["topics"]:
        lines += [f"### {topic['name']}", ""]
        picks = chosen.get(topic["slug"]) or []
        if not picks:
            lines += ["Nothing you would have saved this week.", ""]
        for p in picks:
            lines += [f"* [ ] **{p['name']}**: {p['what']}", f"\t* Why you would care: {p['why']}",
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


# ---------------------------------------------------------------- already known


RESEARCH_SECTION_RE = re.compile(r"^## Research\n(.*?)(?=^## |\Z)", re.M | re.S)
MD_LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)")
BARE_LINK_RE = re.compile(r"https?://[^\s)\]>`\"']+")


def known_keys(before: str, vault) -> set:
    """Link ids of things you already have: the originals of saves made before `before` (YYYY-MM-DD), and links in
    vault notes last changed before then. Picks never repeat these."""
    keys = set()
    if IG_DIR.is_dir():
        for folder in IG_DIR.iterdir():
            if not folder.is_dir() or folder.name.startswith("0_") or folder.name[:10] >= before:
                continue
            for note in folder.glob("*_description.md"):
                research = RESEARCH_SECTION_RE.search(note.read_text(encoding="utf-8"))
                if research:
                    keys.update(link_key(u) for u in MD_LINK_RE.findall(research.group(1)) if "instagram.com" not in u)
    if vault:
        cutoff = datetime.fromisoformat(before).timestamp()
        for note in vault.rglob("*.md"):
            rel = note.relative_to(vault).as_posix()
            if rel.startswith((".", str(VAULT_DIGEST_DIR) + "/")) or note.stat().st_mtime >= cutoff:
                continue
            text = note.read_text(encoding="utf-8", errors="ignore")
            keys.update(link_key(u) for u in BARE_LINK_RE.findall(text) if "github.com/" in u or "huggingface.co/" in u)
    return keys


# ---------------------------------------------------------------- state


def log_history(path: Path, run_date: str, items: list, chosen: dict) -> None:
    """Every item looked at in this run, picked or not, for score.py."""
    picked = {p["id"]: slug for slug, picks in chosen.items() for p in picks}
    entry = {"run_date": run_date, "items": [{
        "key": link_key(i["url"]), "url": i["url"], "title": i["title"], "source": i["source"],
        "update": bool(i.get("update")), "picked": i["id"] in picked, "topic": picked.get(i["id"], ""),
    } for i in items]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


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
    p.add_argument("--as-of", metavar="YYYY-MM-DD",
                   help="backtest: run as if it were this date (only sources that can search the past). "
                        "Writes to output/backtest/ and leaves the seen list and the vault alone")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    OUTPUT_DIR.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    file_log = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_log.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_log)

    profile = json.loads(PROFILE_FILE.read_text())
    backtest = bool(args.as_of)
    now = datetime.fromisoformat(args.as_of).replace(tzinfo=timezone.utc) if backtest else datetime.now(timezone.utc)
    since = now - timedelta(days=args.days)
    logger.info(f"=== feed.py ({'backtest as of ' + args.as_of + ', ' if backtest else ''}last {args.days} days, model {args.model})")

    seen = {} if backtest else load_seen()
    items = fetch_all(profile["sources"], since, now, backtest)
    have = known_keys(since.date().isoformat(), find_vault(args.vault or None))
    before = len(items)
    items = [i for i in items if i.get("update") or link_key(i["url"]) not in have]
    logger.info(f"Dropped {before - len(items)} items you already saved or have in the vault")
    if not args.all and not backtest:
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
        examples = taste_examples(profile, before=since.date().isoformat())
        answer = ask_claude(claude_prompt(profile, items, examples), args.model, args.timeout)
    except ClaudeLimit as error:
        logger.warning(f"Claude usage limit: {error}")
        return 75
    chosen = top_picks(answer, items, profile)
    updates = notable_updates(answer, items)
    today = args.as_of if backtest else datetime.now().date().isoformat()
    model = answer["model"]
    out_dir = BACKTEST_DIR if backtest else OUTPUT_DIR
    log_history(out_dir / HISTORY_FILE.name if backtest else HISTORY_FILE, today, items, chosen)

    digest_dir = out_dir / "digests"
    digest_dir.mkdir(parents=True, exist_ok=True)
    digest = digest_dir / f"{today}.md"
    digest.write_text(render_digest(chosen, updates, profile, today, len(items), model, for_vault=False), encoding="utf-8")
    logger.info(f"Digest: {digest}")
    if args.vault is not None and not backtest:
        vault = find_vault(args.vault or None)
        if not vault:
            logger.warning("No vault found. Give the path with --vault DIR or IG_VAULT.")
        else:
            note = vault / VAULT_DIGEST_DIR / f"claude - interest digest {today}.md"
            note.parent.mkdir(exist_ok=True)
            note.write_text(render_digest(chosen, updates, profile, today, len(items), model, for_vault=True), encoding="utf-8")
            logger.info(f"Vault note: {note}")

    if not backtest:
        save_seen(seen, items, now)
    picked = sum(len(v) for v in chosen.values())
    logger.info(f"Done. Picked {picked} of {len(items)} | Cost reported by Claude: ${answer.get('cost_usd') or 0:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
