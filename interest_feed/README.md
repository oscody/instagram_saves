# interest_feed

A weekly scout for the Focus topics: it checks free sources, keeps only what you would likely have saved on
Instagram, and writes a short digest. It also measures itself against what you actually save.

Plan and findings live in the vault: `ZAIHub/Vault knowledge library/claude - Deeper version of the information gathering system.md`.
Focus topics: `ZAIHub/Vault knowledge library/claude - Focus topics - coding agents and agent skills.md`.

Needs only Python 3 and the logged in Claude CLI. No packages. Runs on the Mac and on the Pi.

## Scripts

| Script | What it does | Claude cost |
| --- | --- | --- |
| `feed.py` | Fetches the sources, drops what you already have, asks Haiku to pick, writes the digest | About a cent a run |
| `score.py` | Recall and precision of the digest against your Instagram saves | Only to label new saves (Haiku) |
| `provenance.py` | Where your saves come from: source types per topic, and how old repos were when saved | None |
| `who_posted.py` | For each Focus topic save, who wrote about it before you saved it (Claude with web search) | About 5 cents a save, cached |

## Run

```bash
cd interest_feed
export GITHUB_TOKEN=$(gh auth token)   # optional: more GitHub API calls (search, awesome lists)

python3 feed.py --dry-run              # list this week's new items, no Claude call, nothing saved
python3 feed.py                        # digest in output/digests/YYYY-MM-DD.md
python3 feed.py --vault                # also write it to the vault's ZAIHub/Interest digest/
python3 score.py --vault               # weekly scoreboard from the live history

# Backtest: replay past weeks, then score them
for d in 2026-09-26 2026-10-03 2026-10-10 2026-10-17; do python3 feed.py --as-of $d; done
python3 score.py --backtest --vault

python3 provenance.py                  # output/provenance.md
python3 who_posted.py --limit 5        # output/who_posted.md (rerun to continue; results are cached)
```

On a Claude usage limit `feed.py` stops with exit code 75 and nothing is marked as seen, so the next run retries.

## profile.json

* `topics`: each Focus topic has `per_week` (picks), `library_topics` (knowledge_library slugs whose Valid saves teach
  the filter your taste), `search` (what it is about) and `avoid`.
* `sources`: lists per source type.

| Source type | Entries | Backtest |
| --- | --- | --- |
| `awesome_list` | `owner/repo` (or `owner/repo:path`): repos added to the list's README during the week | Yes, through the GitHub commit history |
| `hn_github` | Query for GitHub links posted to Hacker News (`github.com` for all) | Yes |
| `page_links` | `URL \| link prefix`: new links on a page, such as the Claude Code docs index | Yes, through the Wayback Machine. Live runs compare with the copy saved last time; the first run only saves it |
| `feeds` | Atom or RSS feed URLs. Links inside each post also count when scoring | Only as far back as the feed's last entries |
| `github_trending` | Language, or blank for all | Yes, through the Wayback Machine (the main page is archived; language pages usually are not) |
| `github_search` | Keywords: new repos created this week with 10 or more stars | Yes |
| `show_hn`, `hackernews` | Title phrases | Yes |
| `reddit` | Subreddit names (top of the week) | No |
| `github_releases` | `owner/repo`: releases of tools you use, shown as one line under "Tools you use", never as picks | No |

Each source gives at most 30 items a run (`PER_SOURCE_MAX`), and a run sends at most 300 items to Claude.

## How the digest is picked

1. Fetch every source for the last 7 days (or the week before `--as-of`).
2. Drop what you have already: the originals of earlier saves (from each note's `## Research` section) and links in
   vault notes changed before that week.
3. Drop items seen in earlier live runs (`output/seen.json`).
4. One Haiku call gets your Valid saves in each Focus topic as examples of your taste and picks what you would have
   saved, up to `per_week` per topic. Releases get one line each.
5. Write the digest. Each pick is a checkbox: tick it if you would have saved it.
6. Log every item looked at, picked or not, to `output/history.jsonl` for scoring.

## How the score works

* Every link becomes one id per thing (`github:owner/repo`, `arxiv:2603.16021`, `hf:owner/name`, `x:123`), so the
  same repo matches across link styles.
* Each Instagram save in a Focus topic is traced to its originals (the links in its Research section) and put in one
  bucket: **hit** (picked on or before the week you saved it), **seen, not picked** (fix the filter), **never seen**
  (fix the sources), **repeat** (you had saved it before; not counted) or **no original** (not counted).
* Recall = hits / (hits + seen, not picked + never seen).
* Precision = good picks / picks. A pick is good if you ticked it in the vault digest, its link appears in another
  vault note, or you saved it on Instagram too.
* New saves without a topic yet are labelled once by Haiku and cached in `output/save_topics.json`.

Limits: it only matches by link (a tip with no link behind it lands in "no original"), only Focus topics count, and
precision needs your ticks.

## Output (not in git)

`output/`: `digests/`, `history.jsonl`, `seen.json`, `scoreboard.md`, `backtest/`, `provenance.md`, `who_posted.json`,
`who_posted.md`, `save_topics.json`, `feed.log`, and `cache/` (Wayback copies and page snapshots).

## Findings so far (2026-10-24)

* In the Focus topics, 58% and 93% of saves are GitHub repos, but the median repo was about 6 months old when saved.
* Those repos rarely appear in awesome lists or on Hacker News; they spread through short videos and X.
* 46% of saves had a blog post about them first, but scattered across many blogs.
* Backtest recall stayed at 0 across every source change, so live runs with ticks are the real test.
