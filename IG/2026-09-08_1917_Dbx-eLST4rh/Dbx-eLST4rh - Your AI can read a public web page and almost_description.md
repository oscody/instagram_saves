---
shortcode: "Dbx-eLST4rh"
url: "https://instagram.com/reel/Dbx-eLST4rh/"
type: "Reel"
author: "heystevetan"
shared: "Sep 08, 2026, 07:17 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Agent Reach: giving Claude live platform access

The post presents Agent Reach, a free MIT-licensed open-source tool that gives Claude live access to platforms such as YouTube, GitHub, Reddit, LinkedIn, Twitter and Chinese sites without separate paid API keys. On screen it shows the pip install commands and the install variants.

Written by claude-haiku-5-5.

## What it teaches

1. Install the package with: pip install agent-reach
2. Run the setup command: agent-reach install
3. Or ask Claude in plain English to run the install for you
4. Once installed, the agent can call commands such as reach_twitter, reach_reddit and reach_youtube
5. Pick an installation variant: Skill mode (recommended for Claude Code, OpenClaw or Cursor), MCP Server mode, or Standalone CLI for scripting

## Source

* Link: https://github.com/Panniantong/Agent-Reach
* How to get it: Caption says to comment "REACH" for the repo plus setup; the GitHub URL is also shown on screen

## Caption

Your AI can read a public web page and almost nothing beyond that. Everything genuinely useful sits behind an API key someone wants paying for.

Agent Reach hands Claude live access to all of it through a single free tool. YouTube transcripts pulled in full, GitHub repositories searched, Reddit threads read, LinkedIn profiles, Twitter posts, podcasts, and Chinese platforms most tools ignore entirely.

Sixty two thousand stars and an MIT license, so it stays free. Several platforms work the second you install it, and the install is one line you can just ask Claude to run.
Comment "REACH" for the repo plus the setup.

[Agent Reach, Claude, Claude Code, Anthropic, Claude skills, AI agents, web scraping, MCP, open source, GitHub, AI automation, Cursor, Codex, AI developer tools, YouTube transcript, Reddit, LinkedIn, AI research, agent skills, free AI tools]

## Research

* Verdict: Partly valid. The repo is real, MIT-licensed and free, but several claims are off. The README warns against the same-named PyPI package, and logged-in platforms need cookies, not just an install. The star count is about 101k, not 62k.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Agent-Reach (github.com)](https://github.com/Panniantong/Agent-Reach): repo, in the post, verified, high confidence. The repo is an MIT CLI that gives agents access to YouTube, GitHub, Reddit, Twitter, LinkedIn, and Chinese platforms like Bilibili and Xiaohongshu.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Lists the Agent Reach reel under safety habits and warnings, with the note that it installs via pip.

### Key steps

1. Ask your agent "帮我安装 Agent Reach" with the repo's install.md link, or install it yourself from the GitHub repo.
2. Run `agent-reach install --env=auto`. This is a read-only check that lists missing items.
3. Use `--dry-run` to preview changes. Use `--system` only if you allow it to install dependencies and write config.
4. Run `agent-reach doctor` to see the status of each channel.
5. YouTube subtitles, web pages (Jina Reader), RSS, and public GitHub work without setup.
6. Twitter, Reddit, LinkedIn, Instagram, and similar sites need cookies or a login. Use a secondary account because of ban risk.
7. Remove it with `agent-reach uninstall` and `pip uninstall agent-reach`.

### Not found

I did not check the PyPI package or the post's commands (`reach_twitter` and others, Skill/MCP/CLI variants) against the README. The README says not to install the same-named PyPI package, so `pip install agent-reach` as shown in the post may be wrong. Install from the GitHub repo instead.
