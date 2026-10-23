---
shortcode: "DbQ9SdYqoNk"
url: "https://instagram.com/reel/DbQ9SdYqoNk/"
type: "Reel"
author: "codeandcomplexity"
shared: "Jul 29, 2026, 12:18 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-07"
---

# Antigravity Awesome Skills: 978+ agent skills repo

A POV-style reel showing the README of the "Antigravity Awesome Skills" GitHub repo, a library of 978+ agentic skills for coding assistants such as Claude Code, Gemini CLI, Codex CLI, Kiro, Cursor and Copilot. The caption offers the link to viewers who comment "link".

Written by claude-haiku-5-5.

## What it teaches

1. Install the skills into your assistant, then find the skill folder for your tool: .claude/skills/ for Claude Code, .gemini/skills/ for Gemini CLI, .codex/skills/ for Codex CLI, and for Kiro either ~/.kiro/skills/ (global) or .kiro/skills/ (workspace).
2. Pick a starting bundle by use case: Web Dev starts with Web Wizard, Security starts with Security Engineer, and general use starts with Essentials.
3. Once installed, ask your agent in plain language and name the skill, for example: Use the @brainstorming skill to help me plan a SaaS.
4. Invoke skills per tool: in Claude Code type /skill-name followed by your request; in Gemini CLI and Codex CLI write a prompt like 'Use skill-name...'; Kiro loads skills on demand automatically.
5. All skills use the universal SKILL.md format, so they are meant to work with any AI coding assistant that supports agentic skills.

## Source

* Link: Antigravity Awesome Skills
* How to get it: Comment "link" on the post to get the link

## Caption

Commen “link” to get it.

## Research

* Verdict: Valid. The repo is public and matches the post. It has grown and been renamed since the reel, so some install details have changed.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [sickn33/antigravity-awesome-skills (now agentic-awesome-skills) (github.com)](https://github.com/sickn33/antigravity-awesome-skills): repo, found by search, verified, high confidence. README describes a SKILL.md skill library with bundles such as Web Wizard and Security Engineer, for Claude Code, Gemini, Codex, Kiro, Cursor and Copilot. It now lists 2,600+ skills against the reel's 978+.

### Already in the vault

* Vault: `3. Resources/0. Daily/2026-02-15.md`: Daily note mentioning the antigravity-awesome-skills repo
* Vault: `ZAIHub/claude - Claude and Codex Skills Index.md`: Links to the 2026-02-15 daily note about the repo

### Key steps

1. Open github.com/sickn33/antigravity-awesome-skills; the README is the current install guide.
2. Preview an install first: npm exec --yes --ignore-scripts --package=agentic-awesome-skills@<version> -- agentic-awesome-skills --release <version> --path .agents/skills --skills brainstorming,systematic-debugging --dry-run. The README pins version 19.15.0. Remove --dry-run to apply.
3. Or use a per-tool shortcut: npx agentic-awesome-skills --cursor, --gemini, --codex, --kiro or --agy.
4. Claude Code: use AAS Core local MCP (aas mcp configure --host claude), a direct install, or the Claude plugin marketplace.
5. Pick skills by bundle (Web Wizard, Security Engineer, Essentials). Bundles only guide which skills to choose and are not separate packages.
6. Invoke by name: Cursor '@brainstorming help me plan a feature'; Gemini CLI 'Use brainstorming to plan a feature'; Kiro IDE 'Use @brainstorming ...'.

### Not found

The post's exact folder paths (.claude/skills, .gemini/skills, .codex/skills) were not confirmed on the current README. It lists explicit paths only for Kiro (~/.kiro/skills), OpenCode, Autohand and AdaL. I read only the first 100,000 of about 145,000 characters of the page. The repo has been renamed and the commands have changed since the reel, so the post's /skill-name syntax for Claude Code may be out of date. The current README says to ask the agent to compose skills through AAS Core.
