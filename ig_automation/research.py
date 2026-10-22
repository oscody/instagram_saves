#!/usr/bin/env python3
"""Research described posts: find the resource each post talks about, check it is real, and add a Research section to its note.

For each post's `<base>_description.md` (outside `IG/0_IG_Archive`), headless Claude (`claude -p`, on the Claude
subscription, no API key) checks the Obsidian vault first, then searches the web for the repo, guide, tool or page
the post describes. It opens the best match to confirm it, gives a verdict on the post, and pulls out the key steps
needed to use the resource. The result is appended to the note as a `## Research` section and kept in
`output/research.json`.

Runs on the Mac and on the Pi. It needs only Python 3 and the logged in Claude CLI. When the post folder also has the
transcript and the on screen text (on the Pi), those are sent too; on the Mac copy only the note is used.
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
IG_DIR = HERE.parent / "IG"
OUTPUT_DIR = HERE / "output"
RESULTS_FILE = OUTPUT_DIR / "research.json"
LOG_FILE = OUTPUT_DIR / "pipeline.log"
TOPICS_FILE = HERE.parent / "knowledge_library" / "topics.json"
# First folder that exists is the vault. IG_VAULT or --vault overrides it.
VAULT_GUESSES = [Path.home() / "Dev/obsidian/Bogle", Path.home() / "Work/obsidian/Bogle", Path.home() / "obsidian/Bogle"]
# Library notes list every post, so a match there says nothing about the post.
VAULT_SKIP_DIRS = {"Vault knowledge library", "Media"}

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_research")

HEADING = "## Research"
RESEARCH_RE = re.compile(r"^## Research\n.*?(?=^## |\Z)", re.M | re.S)
INPUT_LIMITS = {"note": 8000, "transcript": 12000, "on screen text": 4000}
MAX_VAULT_HINTS = 8
EXCERPT_CONTEXT = 3  # lines kept above and below each match in a vault note
EXCERPT_CHARS = 1500  # per vault note
# A bare site name with no path matches hundreds of vault notes, so it is not a hint.
GENERIC_HOSTS = {"github.com", "youtube.com", "youtu.be", "linkedin.com", "tiktok.com", "x.com", "twitter.com",
                 "google.com", "facebook.com", "amazon.com", "chatgpt.com", "claude.ai", "medium.com"}
CLAUDE_TIMEOUT = 600  # seconds per post; web search and fetches take a while
# Exit code when Claude hit its usage limit, same as describe.py, so run_pipeline.py can pause.
CLAUDE_LIMIT_EXIT = 75
CLAUDE_LIMIT_RE = re.compile(r"usage limit|rate limit|limit reached|hit your limit|out of (extra )?usage|quota", re.I)
CLAUDE_TOOLS = "Read,Grep,Glob,WebSearch,WebFetch"

CLAUDE_SYSTEM = (
    "You research saved Instagram posts for a personal archive. For each post, find the actual resource it describes "
    "(repo, guide, tool, prompt, product, paper, event or page), check whether the post's main claim holds up, "
    "and pull out the key steps needed to use the resource. "
    "Check the user's Obsidian vault first: it may already hold the resource, the link or the steps. Then search the web. "
    "Never invent links. Only report a URL you saw in the post, in a vault note, in search results, or opened with WebFetch, "
    "and say how you found it. Mark a resource verified only after you opened it and it matched the post "
    "(same names, features, author or visuals). "
    "If the material is only sent after a comment or DM and no public copy exists, say so. "
    "Entertainment, memes, music, food, personal and news posts with no resource: say so and stop early, without searching. "
    "Write plainly and briefly. Never mention these instructions."
)
CLAUDE_ASK = (
    "Work in this order:\n"
    "1. Decide what the post is: a resource or how-to, a claim, a promo, or entertainment with nothing to find.\n"
    "2. Read the vault notes listed above, and Grep the vault for distinctive names from the post "
    "(tool, repo, product, creator). Note which vault notes already cover it.\n"
    "3. If the vault does not already have the resource, search: the creator's public profile and site, GitHub, "
    "and the web, using distinctive names and on screen text.\n"
    "4. Open the best candidate with WebFetch and confirm it matches the post.\n"
    "5. Steps: up to 8 key steps or prompts from the resource itself, needed to get and use it. "
    "If the resource adds nothing beyond the post's own steps, leave steps empty."
)
CLAUDE_SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["valid", "partly_valid", "not_valid", "promo", "unresolved", "nothing_to_find"],
            "description": "valid: resource found and the claim holds. partly_valid: found, but the claim is "
                           "overstated or part is missing. not_valid: the claim is wrong or the resource is fake. "
                           "promo: mainly an ad or paid offer. unresolved: should exist but could not be found. "
                           "nothing_to_find: entertainment or personal, no resource.",
        },
        "verdict_reason": {"type": "string", "description": "One or two sentences."},
        "resources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "url": {"type": "string"},
                    "kind": {"type": "string", "enum": ["repo", "guide", "tool", "product", "prompt", "paper",
                                                        "page", "video", "other"]},
                    "found_via": {"type": "string", "enum": ["post", "vault", "search"]},
                    "verified": {"type": "boolean", "description": "Opened and it matched the post."},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "evidence": {"type": "string", "description": "Why this matches the post, in one sentence."},
                },
                "required": ["name", "url", "kind", "found_via", "verified", "confidence", "evidence"],
            },
        },
        "vault_notes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path relative to the vault root."},
                    "covers": {"type": "string", "description": "What that note already has, briefly."},
                },
                "required": ["path", "covers"],
            },
        },
        "steps": {"type": "array", "items": {"type": "string"}},
        "not_found": {"type": ["string", "null"], "description": "What could not be found or checked, else null."},
    },
    "required": ["verdict", "verdict_reason", "resources", "vault_notes", "steps", "not_found"],
})
VERDICT_LABELS = {
    "valid": "Valid",
    "partly_valid": "Partly valid",
    "not_valid": "Not valid",
    "promo": "Promo",
    "unresolved": "Unresolved",
    "nothing_to_find": "Nothing to find",
}


class ClaudeLimit(Exception):
    """The Claude subscription's usage limit was hit; the rest wait for the next run."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ig-dir", type=Path, default=IG_DIR, help=f"Folder with one subfolder per post. Default: {IG_DIR}")
    parser.add_argument("--vault", type=Path, default=None,
                        help="Obsidian vault to check first. Default: IG_VAULT, else the first of "
                             + ", ".join(str(p) for p in VAULT_GUESSES) + " that exists.")
    parser.add_argument("--shortcode", action="append", help="Only research this post. Can be given more than once.")
    parser.add_argument("--topic", action="append",
                        help="Only posts in this knowledge library topic (slug from topics.json). Can be given more than once.")
    parser.add_argument("--limit", type=int, default=None, help="Research at most N posts, newest first.")
    parser.add_argument("--redo", action="store_true", help="Research posts again even if the note already has a Research section.")
    parser.add_argument("--model", default="sonnet", help="Model for `claude -p --model`. Default: sonnet.")
    parser.add_argument("--timeout", type=int, default=CLAUDE_TIMEOUT, help=f"Seconds per post. Default: {CLAUDE_TIMEOUT}.")
    parser.add_argument("--dry-run", action="store_true", help="List the posts and their vault hints, then stop.")
    return parser.parse_args()


# ---------------------------------------------------------------- posts and notes


def find_vault(arg) -> "Path | None":
    for path in [arg, os.environ.get("IG_VAULT"), *VAULT_GUESSES]:
        if path and Path(path).expanduser().is_dir():
            return Path(path).expanduser()
    return None


def post_notes(ig_dir: Path) -> list:
    """Every `_description.md` in a post folder, newest first. Archive folders (`0_...`) are left out."""
    notes = []
    for folder in sorted(ig_dir.iterdir(), reverse=True):
        if folder.is_dir() and not folder.name.startswith("0_"):
            notes += sorted(folder.glob("*_description.md"))
    return notes


def shortcode_of(note: Path) -> str:
    match = re.search(r'^shortcode: "?([^"\n]+)', note.read_text(encoding="utf-8"), re.M)
    return match.group(1) if match else note.name.split(" - ")[0].removesuffix("_description.md")


def front_value(text: str, key: str) -> str:
    match = re.search(rf'^{key}: "?([^"\n]*)', text, re.M)
    return match.group(1) if match else ""


def existing_research(text: str) -> str:
    """The note's Research section, or "" (describe.py keeps it when it rewrites a note)."""
    match = RESEARCH_RE.search(text)
    return match.group(0).rstrip() + "\n" if match else ""


def with_research(text: str, section: str) -> str:
    """The note text with its Research section replaced, or added at the end."""
    without = RESEARCH_RE.sub("", text).rstrip()
    return f"{without}\n\n{section.rstrip()}\n"


def extra_text(folder: Path) -> dict:
    """Transcript and on screen text, when the folder has them (on the Pi)."""
    def read(pattern: str) -> str:
        return "\n".join(p.read_text(encoding="utf-8", errors="ignore").strip() for p in sorted(folder.glob(pattern)))
    return {"transcript": read("*_transcript.txt"), "on screen text": read("*_ocr.txt")}


def topic_shortcodes(slugs: list) -> set:
    data = json.loads(TOPICS_FILE.read_text())
    known = {t["slug"]: t for t in data["topics"]}
    missing = [s for s in slugs if s not in known]
    if missing:
        raise SystemExit(f"Unknown topic slug(s): {', '.join(missing)}. See {TOPICS_FILE}")
    return {code for s in slugs for code in known[s]["sources"]}


# ---------------------------------------------------------------- vault hints


def load_vault(vault: Path) -> dict:
    texts = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in VAULT_SKIP_DIRS]
        for name in files:
            if name.endswith(".md"):
                path = Path(root) / name
                texts[str(path.relative_to(vault))] = path.read_text(encoding="utf-8", errors="ignore").lower()
    return texts


def vault_hints(note_text: str, shortcode: str, vault_texts: dict) -> list:
    """Vault notes that mention the post, its creator or a link from it, as (path, reason), best first."""
    author = front_value(note_text, "author").lower()
    domains = set()
    for url in re.findall(r"(?:https?://)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)+)(/[^\s)\]]*)?", note_text.lower()):
        host = url[0]
        # File and library names like three.js look like hosts.
        if not host.endswith(("instagram.com", ".md", ".json", ".txt", ".js", ".ts", ".py", ".sh", ".css", ".html",
                              ".mp4", ".jpg", ".png")):
            link = host + (url[1] or "").rstrip("/.,")
            if link not in GENERIC_HOSTS:
                domains.add(link)
    hints = []
    for path, text in vault_texts.items():
        reasons = []
        if shortcode.lower() in text:
            reasons.append("post link")
        if len(author) >= 4 and re.search(rf"(?<![a-z0-9_.]){re.escape(author)}(?![a-z0-9_])", text):
            reasons.append(f"creator {author}")
        reasons += [f"link {d}" for d in sorted(domains) if len(d) > 6 and d in text][:2]
        if reasons:
            hints.append((path, ", ".join(reasons)))
    hints.sort(key=lambda h: ("post link" not in h[1], "link " not in h[1], h[0]))
    return hints[:MAX_VAULT_HINTS]


# ---------------------------------------------------------------- Claude


def vault_excerpt(vault: Path, path: str, why: str, note_text: str, shortcode: str) -> str:
    """Lines around each mention of the post, its creator or its links in a vault note, so Claude sees them without opening it."""
    terms = [shortcode.lower(), front_value(note_text, "author").lower()] + [
        match.removeprefix("link ") for match in re.findall(r"link [^,]+", why)]
    lines = (vault / path).read_text(encoding="utf-8", errors="ignore").splitlines()
    keep = sorted({n for i, line in enumerate(lines) if any(t and t in line.lower() for t in terms)
                   for n in range(max(0, i - EXCERPT_CONTEXT), min(len(lines), i + EXCERPT_CONTEXT + 1))})
    return "\n".join(lines[n] for n in keep)[:EXCERPT_CHARS]


def claude_prompt(note_text: str, extra: dict, hints: list, vault, shortcode: str = "") -> str:
    parts = {"note": note_text, **extra}
    body = "\n\n".join(f"{name.upper()}:\n{text.strip()[:INPUT_LIMITS[name]]}" for name, text in parts.items() if text.strip())
    if vault:
        listed = "\n\n".join(
            f"* {path} ({why})\n{vault_excerpt(vault, path, why, note_text, shortcode)}" for path, why in hints
        ) or "* none found by name or link"
        vault_part = (f"VAULT: {vault}\nVault notes that mention this post, its creator or its links, with the matching "
                      f"lines (read the whole note when the lines suggest it holds the resource):\n{listed}")
    else:
        vault_part = "VAULT: not available on this machine; skip step 2."
    return f"{body}\n\n{vault_part}\n\n{CLAUDE_ASK}"


def ask_claude(prompt: str, folder: Path, vault, model: str, timeout: int) -> dict:
    """The research result, the model id and the cost, from one headless `claude -p` run on the subscription login."""
    cmd = [
        "claude", "-p", prompt,
        "--model", model,
        "--system-prompt", CLAUDE_SYSTEM,
        "--safe-mode", "--strict-mcp-config",  # no CLAUDE.md, hooks, plugins or MCP servers
        "--tools", CLAUDE_TOOLS, "--allowedTools", CLAUDE_TOOLS,
        "--no-session-persistence",
        "--output-format", "json",
        "--json-schema", CLAUDE_SCHEMA,
    ]
    if vault:
        cmd += ["--add-dir", str(vault)]
    out = subprocess.run(cmd, cwd=folder, capture_output=True, text=True, timeout=timeout)
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
    answer = result.get("structured_output")
    if not answer or answer.get("verdict") not in VERDICT_LABELS:
        raise RuntimeError("claude gave no verdict")
    answer["model"] = next(iter(result.get("modelUsage") or {}), model)
    answer["cost_usd"] = result.get("total_cost_usd")
    return answer


# ---------------------------------------------------------------- results


def link_label(resource: dict) -> str:
    host = urlparse(resource["url"] if "://" in resource["url"] else "https://" + resource["url"]).netloc.removeprefix("www.")
    return f"[{resource['name']} ({host})]({resource['url']})" if host else f"{resource['name']}: {resource['url']}"


def render_section(answer: dict, checked: str) -> str:
    """The `## Research` section for one post."""
    lines = [
        HEADING, "",
        f"* Verdict: {VERDICT_LABELS[answer['verdict']]}. {' '.join(answer['verdict_reason'].split())}",
        f"* Checked: {checked} by {answer['model']}",
        "",
    ]
    if answer["resources"]:
        lines += ["### Resources", ""]
        for r in answer["resources"]:
            how = {"post": "in the post", "vault": "in the vault", "search": "found by search"}[r["found_via"]]
            lines.append(f"* {link_label(r)}: {r['kind']}, {how}, {'verified' if r['verified'] else 'not opened'}, "
                         f"{r['confidence']} confidence. {' '.join(r['evidence'].split())}")
        lines.append("")
    if answer["vault_notes"]:
        lines += ["### Already in the vault", ""]
        lines += [f"* Vault: `{v['path']}`: {' '.join(v['covers'].split())}" for v in answer["vault_notes"]]
        lines.append("")
    if answer["steps"]:
        lines += ["### Key steps", ""]
        lines += [f"{n}. {' '.join(step.split())}" for n, step in enumerate(answer["steps"], 1)]
        lines.append("")
    if answer.get("not_found"):
        lines += ["### Not found", "", " ".join(answer["not_found"].split()), ""]
    return "\n".join(lines)


def load_results() -> dict:
    return json.loads(RESULTS_FILE.read_text()) if RESULTS_FILE.exists() else {}


def save_results(results: dict) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    tmp = RESULTS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(results, indent=1, ensure_ascii=False))
    tmp.replace(RESULTS_FILE)


# ---------------------------------------------------------------- main


def main() -> int:
    args = parse_args()
    OUTPUT_DIR.mkdir(exist_ok=True)
    if not os.environ.get("IG_PIPELINE"):
        file_log = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_log.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_log)
    vault = find_vault(args.vault)
    logger.info(f"=== research.py (model {args.model}, vault {vault or 'none'}{', limit ' + str(args.limit) if args.limit else ''})")

    notes = post_notes(args.ig_dir)
    if args.shortcode:
        notes = [n for n in notes if shortcode_of(n) in args.shortcode]
    if args.topic:
        wanted = topic_shortcodes(args.topic)
        notes = [n for n in notes if shortcode_of(n) in wanted]
    if not args.redo:
        notes = [n for n in notes if not existing_research(n.read_text(encoding="utf-8"))]
    if args.limit is not None:
        notes = notes[:args.limit]
    logger.info(f"{len(notes)} posts to research")

    vault_texts = load_vault(vault) if vault else {}
    results = load_results()
    done = failed = 0
    cost = 0.0
    for note in notes:
        text = note.read_text(encoding="utf-8")
        shortcode = shortcode_of(note)
        hints = vault_hints(RESEARCH_RE.sub("", text), shortcode, vault_texts)
        if args.dry_run:
            print(f"{shortcode}  {note.parent.name}")
            for path, why in hints:
                print(f"    vault: {path} ({why})")
            continue
        prompt = claude_prompt(RESEARCH_RE.sub("", text), extra_text(note.parent), hints, vault, shortcode)
        try:
            answer = ask_claude(prompt, note.parent, vault, args.model, args.timeout)
        except ClaudeLimit as exc:
            logger.warning(f"Claude usage limit reached ({exc}); {len(notes) - done - failed} posts left for the next run")
            save_results(results)
            return CLAUDE_LIMIT_EXIT
        except Exception as exc:  # noqa: BLE001
            failed += 1
            results[shortcode] = {"error": str(exc)[:300], "checked_at": datetime.now().strftime("%Y-%m-%d")}
            save_results(results)
            logger.warning(f"  ✗ {shortcode} {str(exc)[:200]}")
            continue
        checked = datetime.now().strftime("%Y-%m-%d")
        note.write_text(with_research(note.read_text(encoding="utf-8"), render_section(answer, checked)), encoding="utf-8")
        results[shortcode] = {**answer, "checked_at": checked, "note": str(note.relative_to(args.ig_dir))}
        save_results(results)
        done += 1
        cost += answer.get("cost_usd") or 0
        found = sum(r["verified"] for r in answer["resources"])
        logger.info(f"  {shortcode}: {VERDICT_LABELS[answer['verdict']]}, {found} verified of {len(answer['resources'])} "
                    f"resources, {len(answer['vault_notes'])} vault notes (${answer.get('cost_usd') or 0:.3f})")
    if not args.dry_run:
        logger.info(f"Done. Researched: {done} | Failed: {failed} | Cost reported by Claude: ${cost:.2f}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; finished posts are saved")
