---
shortcode: "DaswYSQuDL6"
url: "https://instagram.com/reel/DaswYSQuDL6/"
type: "Reel"
author: "wutronicai"
shared: "Sep 06, 2026, 10:37 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Open-source AI-driven 2.5D game engine showcase

The reel promotes an open-source 2.5D game engine built for AI agent-driven game development, showing a Claude Code session that generates a farming sim with maps, assets, and crop systems. It also highlights a built-in server SDK for accounts, cloud saves, and multiplayer, plus baked-in Claude Code and Codex agent setups.

Written by claude-haiku-5-5.

## Source

* Link: d-liya / capybara_2d_engine

## Caption

an open-source game engine built from the ground up for AI/agent-driven 2.5D game dev.

This is Claude Code building a full farming sim inside it, generating maps, assets, systems, and logic on the fly. Everything the agent needs lives in one small, predictable interface (`src/Game.ts`) plus a built-in server SDK for accounts/multiplayer.

Library: d-liya / capybara_2d_engine

## Research

* Verdict: Partly valid. The repo exists and matches the post (Game.ts interface, server SDK, Claude/Codex agent files, MIT license). However, the README says it is no longer maintained, and the post doesn't mention that.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [d-liya/capybara_2d_engine (github.com)](https://github.com/d-liya/capybara_2d_engine): repo, in the post, verified, high confidence. README describes an AI-agent-oriented 2.5D engine with src/Game.ts, src/sdk/ for accounts, saves and multiplayer, and CLAUDE.md/AGENTS.md.

### Key steps

1. Clone the repo, or export an HTML project from capybara.build (the zip includes a .env with an API key and the git history).
2. Run `npm install`.
3. Run `npm run dev`.
4. Open the project in Claude Code or Codex. It reads CLAUDE.md, AGENTS.md and .agents/skills/capybara-game-developer.
5. The agent works through the public API in src/Game.ts. The server SDK is in src/sdk/.
6. Optional cloud sync: `npm run pull`, `npm run push`, `npm run publish`.
7. Don't commit .env. If generated art looks wrong, check the original file in src/data before regenerating.
8. The older MCP-based setup is on the v1 branch.

### Not found

I didn't check the farming sim demo itself, or whether the capybara.build site still works.
