---
shortcode: "DYtCoIJxH8M"
url: "https://instagram.com/reel/DYtCoIJxH8M/"
type: "Reel"
author: "aimindscope"
shared: "Jul 02, 2026, 12:20 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# GitNexus: codebase dependency graph for AI coding agents

A reel promoting GitNexus, an open-source tool that maps functions, dependencies and call chains in a repo so AI coding agents like Claude Code, Cursor and Windsurf can see what a change affects. It lists the tool's features and closes with a one-line setup command.

Written by claude-haiku-5-5.

## What it teaches

1. Set up GitNexus in your repo by running: npx gitnexus analyze

## Source

* Link: GitNexus

## Caption

Your AI coding agent has been editing your codebase blind. GitNexus just exposed it — and fixed it in one command. 💀🧠

Every time Claude Code, Cursor, or Windsurf edits a function —
it has zero idea what depends on it.

47 functions relying on that return type?
12 services breaking from that one change?
It doesn’t know. It just ships. And hopes. 👀

GitNexus fixes that. Here’s what it does 👇
🔵 Maps every function, dependency & call chain in your repo
🔵 Blast radius analysis before you touch a single line
🔵 Full MCP integration with Claude Code, Cursor & Windsurf
🔵 Answers “what depends on this?” in 1 query instead of 10
🔵 Even GPT-4o-mini stops breaking call chains

Setup: npx gitnexus analyze

One command. Done. 9.4K stars. 100% open source.

The bottleneck was never model intelligence.
It was always context. 💀

Save this — every dev using AI in production needs this. 🔖

Follow for more.

#GitNexus #ClaudeCode #Cursor #OpenSource #AIEngineering DeveloperTools MCP CodeIntelligence SoftwareDev TechNews

## Research

* Verdict: Partly valid. GitNexus is real and does what the post says (graph, blast-radius, MCP). But it is not "100% open source": the license is PolyForm Noncommercial, and the star count is now ~48k, not 9.4K. `analyze` only indexes; you also need `setup` or an MCP add for the agent to use it.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [GitNexus (abhigyanpatwari/GitNexus) (github.com)](https://github.com/abhigyanpatwari/GitNexus): repo, found by search, verified, high confidence. README describes a codebase knowledge graph of dependencies and call chains exposed to agents via MCP, with `npx gitnexus analyze` setup.

### Key steps

1. From the repo root run: npx gitnexus analyze (builds the graph in .gitnexus/, may add AGENTS.md/CLAUDE.md and skills).
2. Run: npx gitnexus setup (auto-detects Claude Code, Cursor, etc. and writes the MCP config). Optionally install globally first: npm i -g gitnexus, to avoid slow npx startup.
3. Or add manually for Claude Code: claude mcp add gitnexus -- npx -y gitnexus@latest mcp
4. For Cursor, add to ~/.cursor/mcp.json: {"mcpServers":{"gitnexus":{"command":"npx","args":["-y","gitnexus@latest","mcp"]}}}
5. Ask your agent to use the MCP tools such as query, context, impact (blast radius) and detect_changes before editing.
6. Check the PolyForm Noncommercial license before using it in commercial work.

### Not found

Did not read the last ~20k characters of the README. No Windsurf manual config snippet seen. The claim that GPT-4o-mini stops breaking call chains was not checked.
