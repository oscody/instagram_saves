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
