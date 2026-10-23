---
shortcode: "DXhIODkDqq2"
url: "https://instagram.com/reel/DXhIODkDqq2/"
type: "Reel"
author: "marc.kaz"
shared: "May 01, 2026, 01:21 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# 90% cheaper Claude Code tool open-sourced

The post presents an open-source tool that sits between an AI coding assistant and the shell and compresses command output before it reaches the context window. On-screen, a terminal "rtk gain" report shows 130.0M tokens saved (88.9%) across 15,720 commands.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/rtk-ai/rtk

## Caption

🚨 90% CHEAPER CLAUDE CODE JUST OPEN-SOURCED

Someone built a tool that sits between your AI and the shell and compresses every command output before it hits context.

Ships with:
• Auto-rewrites git push, cargo test, ls, grep, etc.
• Massive token savings on every run
• Works with Claude Code, Cursor, Gemini, Codex & Copilot
• 100% open source

Context limits and token bills just got destroyed.

👉 https://github.com/rtk-ai/rtk

Who’s slashing their Claude costs today? Drop a 🔥

## Research

* Verdict: Partly valid. The rtk repo exists and does what the post says: it compresses shell output for many agents. The "90% cheaper Claude Code" headline is overstated. The repo claims 60-90% savings on bash output only, not on your total bill.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [rtk (Rust Token Killer) (github.com)](https://github.com/rtk-ai/rtk): repo, in the post, verified, high confidence. The repo describes a Rust CLI proxy that compresses command output and has the `rtk gain` dashboard and multi-agent support shown in the post.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Lists the rtk reel as a one-line entry: sits between the agent and the shell and compresses output. It has no install steps.

### Key steps

1. Install: `brew install rtk` (macOS/Linux), `winget install rtk-ai.rtk` (Windows), or use the repo's install.sh script.
2. Check the install with `rtk gain`. It should show the savings dashboard. Another crate named rtk exists, so a "command not found" error means you may have the wrong one.
3. Claude Code: run `rtk init -g`, then restart Claude Code.
4. Other agents: Gemini `rtk init -g --gemini`, Codex `rtk init -g --codex`, Cursor `rtk init -g --agent cursor`, Windsurf `rtk init -g --agent windsurf`.
5. Test with `git status`. The hook rewrites it to `rtk git status`.
6. Only Bash tool calls are filtered. For file reads and searches, use `rtk read`, `rtk grep` or `rtk find` directly.
7. Use `rtk gain --graph` or `--history` for stats, `rtk discover` to find missed savings, and `rtk bypass <cmd>` to run a command unfiltered.

### Not found

I did not check the 130M tokens saved figure on screen. It is one user's own measurement, and the repo says token counts are estimated as bytes/4.
