---
shortcode: "DXrgzklgLqN"
url: "https://instagram.com/reel/DXrgzklgLqN/"
type: "Reel"
author: "wassimyounes_"
shared: "May 05, 2026, 05:13 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# High-speed web scraper for AI agents

A creator shows a fast web scraper for AI agents on Claude Code, shared as a GitHub repo, and says he runs it overnight to collect web data for his AI. He offers the tool to anyone who comments.

Written by claude-haiku-5-5.

## Source

* Link: 0xMassi/webclaw
* How to get it: Comment "web" on the post; the creator says he will send it over

## Caption

Comment “Web” ⬇️for web scrapping agent on Claude code

## Research

* Verdict: Valid. The webclaw repo is public and matches the post: a fast Rust web scraper with an MCP server for Claude Code. You don't need the comment-for-link step because the GitHub repo is open.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [0xMassi/webclaw (github.com)](https://github.com/0xMassi/webclaw): repo, in the post, verified, high confidence. The repo name matches the post's source. It is a Rust web extractor (CLI and MCP server) that works with Claude Code and outputs LLM-ready markdown.

### Key steps

1. Easiest setup: run `npx create-webclaw`. It detects supported AI clients, including Claude Code, and configures them.
2. Or install with Homebrew: `brew tap 0xMassi/webclaw && brew install webclaw`. You can also use a prebuilt binary or Docker.
3. To use it with Claude Code via MCP, set the server command to `npx -y @webclaw/mcp`.
4. Optionally add the agent skill: `npx skills add 0xMassi/webclaw-skill`.
5. Scrape one page: `webclaw https://example.com --format llm`.
6. Crawl a site: `webclaw https://docs.rust-lang.org --crawl --depth 2 --max-pages 50`.
7. Search and research tools, and the `--cloud` option, need the hosted API and a `WEBCLAW_API_KEY`.
8. The license is AGPL-3.0, so check it before using the tool commercially.

### Not found

I didn't verify the creator's overnight-scraping workflow or his speed claims. The repo's own benchmarks cover browser-profile runs only. No vault note covers webclaw.
