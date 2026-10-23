---
shortcode: "DcT55p0Rnhn"
url: "https://instagram.com/reel/DcT55p0Rnhn/"
type: "Reel"
author: "charlieautomates"
shared: "Sep 19, 2026, 08:26 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Base: knowledge graph for Claude rules

Shows Base, a GitHub tool that builds a knowledge graph of Claude Code rules, behaviors and projects, so domain rules load only when their keywords come up instead of a static CLAUDE.md. The repo link is offered to viewers who comment the keyword.

Written by claude-haiku-5-5.

## Source

* Link: Base
* How to get it: Comment "Base" on the post

## Caption

Comment “Base” for the GitHub repo link

Your claude.md is static.

Rules go stale. The whole file dumps into context every session, burning tokens on rules you didn’t need.

Here’s the thing. Base builds a knowledge graph of your rules, behaviors, and projects.

Domain rules fire on keywords. Nothing else loads.

Boot a session and Claude already knows what you’re building.

Consistency up 90%.

#ClaudeCode
#AItools
#AIWorkflow
#Automation
#DevTools

## Research

* Verdict: Partly valid. The repo is public and does what the post says: it graphs rules and projects and injects domain rules on keyword match. The "consistency up 90%" figure has no support in the README.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [ChristopherKahler/base (BASE: Builder's Automated State Engine) (github.com)](https://github.com/ChristopherKahler/base): repo, found by search, verified, high confidence. README describes a Rust binary that builds a knowledge graph and hooks into Claude Code, with domain rules triggered by keywords, as in the reel.
* [Claude Code Memory: BASE vs Graphify (charlieautomates.com)](https://www.charlieautomates.com/blog/claude-code-memory-base-vs-graphify/): page, found by search, not opened, medium confidence. The post author's own write-up on BASE; seen in search results only, not opened.

### Key steps

1. Install Claude Code first, because BASE writes its hooks into ~/.claude.
2. Run: curl -fsSL https://raw.githubusercontent.com/ChristopherKahler/base/main/install.sh | sh (on Windows, use install.ps1 via irm | iex).
3. The installer puts the binary at ~/.local/bin/base, writes config to ~/.base-gbl/ and adds hooks to ~/.claude/settings.json.
4. In your workspace, run: base scaffold
5. Register a project: base p a -n "My App" -p "src"
6. Optionally map the code: base sync --ast --target src
7. Add a domain rule: base rule add --domain myapp --text "Migrations always run through the CLI, never raw SQL"
8. Query the graph: base a q -c "auth"

### Not found

The "90% consistency" figure has no source in the README. I did not confirm that the repo is the one the creator links in comments, though the creator's blog covers the same tool. I did not open the blog post.
