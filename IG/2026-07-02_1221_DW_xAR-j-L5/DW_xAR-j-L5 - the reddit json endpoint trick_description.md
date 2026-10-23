---
shortcode: "DW_xAR-j-L5"
url: "https://instagram.com/reel/DW_xAR-j-L5/"
type: "Reel"
author: "zchangd"
shared: "Jul 02, 2026, 12:21 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Scraping Reddit via the .json endpoint trick

A creator shows how Reddit's unofficial .json endpoints return structured post and comment data without an API key. The reel shows a Python scraper built with Claude Code, then a summary of Claude Code feature feedback pulled from r/ClaudeCode.

Written by claude-haiku-5-5.

## What it teaches

1. Add .json to the end of any Reddit URL to get its raw data, with no authentication or API keys needed.
2. Ask Claude Code to build a Python scrape function that calls these endpoints with the requests library.
3. Set a custom User-Agent and wait about 1.1 seconds between requests to stay under Reddit's rate limit, as the on-screen script does.
4. Add retries with exponential backoff for failed requests, as the on-screen script does.
5. Point the scraper at a subreddit and ask Claude to list the top-voted new features, plus what people like and dislike about each.

## Caption

the reddit json endpoint trick.

## Research

* Verdict: Partly valid. Adding .json to Reddit URLs does return data, and a custom User-Agent avoids 429s. The "no auth, works reliably" claim is shaky: 2025–26 reports say anonymous access is often blocked (403) or rate-limited.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Scraping Reddit via their JSON API (Simon Willison TIL) (til.simonwillison.net)](https://til.simonwillison.net/reddit/scraping-reddit-json): guide, found by search, verified, medium confidence. Documents the same .json trick and the custom User-Agent fix for 429 errors; it is not the reel's own script.
* [Reddit JSON endpoint dead 2026 (redditapis.com) (redditapis.com)](https://www.redditapis.com/blogs/reddit-json-endpoint-dead-2026): page, found by search, not opened, low confidence. Search snippet says the endpoints are rate-limited and unreliable at volume. It is a vendor blog and I did not open it.

### Key steps

1. Append .json to a Reddit URL, e.g. https://www.reddit.com/r/ClaudeCode/top.json?t=month
2. Send a descriptive custom User-Agent header; the default requests/curl agent gets 429.
3. Read posts from data.children[].data. For comments, request the post permalink plus .json.
4. Wait about 1.1 seconds between requests and retry with exponential backoff on 429 or 5xx.
5. If you get 403s, use Reddit's official OAuth API with a registered app instead.
6. Feed the collected posts to Claude and ask for the top-voted features, plus what people like and dislike about each.

### Not found

The creator's actual script was not published anywhere I could find. I did not open the redditapis.com article.
