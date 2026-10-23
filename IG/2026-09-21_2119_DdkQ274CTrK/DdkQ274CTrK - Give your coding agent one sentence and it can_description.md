---
shortcode: "DdkQ274CTrK"
url: "https://instagram.com/reel/DdkQ274CTrK/"
type: "Reel"
author: "githubsignals"
shared: "Sep 21, 2026, 09:19 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Build World: prompt-to-playable 3D worlds with AI

The post shows the GitHub README for Build World, an open-source AI skill that links a coding agent to the Thrixel service to turn a one-sentence prompt into an interactive 3D world. Example screenshots show a playable underwater submarine game.

Written by claude-haiku-5-5.

## What it teaches

1. Install Claude Code and uv, then check each with `claude --version` and `uv --version`. If both print a version, skip to step 2.
2. Steps 1 and 2 are one-time setup per machine. After that, starting a new game is step 3 (the post does not show step 3's details).
3. Using Codex or Gemini CLI instead: each installs Thrixel its own way, and the linked installation page covers both.
4. Describe the experience in one plain-English sentence or prompt.
5. The agent calls Thrixel to generate and refine the 3D assets, while the agent handles the logic, interactions and scene setup.
6. The agent repeatedly builds, evaluates and improves the world, including its gameplay, interactions and assets.
7. Refine the result with simple follow-up prompts.

## Source

* Link: github.com/thrixel/build-world

## Caption

Give your coding agent one sentence, and it can turn it into a playable 3D world. 

Build World is the AI skill that turns plain English prompts into playable 3D worlds without writing code. It connects your favorite coding agent to Thrixel, a service that generates high-quality 3D assets while your agent handles the logic and interactions. The result is a full interactive experience like a submarine game or historical simulation, built from a single sentence. This workflow works across major engines like Three.js and Unity, letting you vibe out complex scenes and refine them with simple follow-up requests. It is a surprisingly easy way to go from idea to a live, shareable 3D experience in your browser.

Open source: thrixel/build-world

Follow for more open source project drops.

#AIGameDev #VibeCoding #GameDevTok #ThreeJS

## Research

* Verdict: Valid. The repo thrixel/build-world exists and matches the post: an agent plugin that uses Thrixel for 3D assets and supports Three.js, Roblox, Unity and Unreal. Whether the results are "high-quality" or playable from one sentence wasn't tested.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [thrixel/build-world (github.com)](https://github.com/thrixel/build-world): repo, in the post, verified, high confidence. README describes the Build World plugin linking a coding agent to Thrixel, with Three.js, Unity and other engines, and a submarine game example.

### Key steps

1. Install Claude Code and uv. Check them with `claude --version` and `uv --version`. If a command isn't found, open a new terminal.
2. Log in to Thrixel (once per machine): `uvx thrixel-mcp@latest login`, then approve the code in your browser.
3. Add the plugin marketplace: `claude plugin marketplace add thrixel/build-world`.
4. Install the plugin: `claude plugin install thrixel@thrixel`.
5. Check the install: `claude plugin list` should show it enabled, and `claude mcp list` should show Connected.
6. From your projects folder, run `claude --permission-mode auto`.
7. Type `/thrixel:build-world` followed by the game and engine, for example a submarine exploration game in three.js with coral and fish. The README recommends a top-tier model with high effort.
8. Refine the game with plain-English follow-up requests. For Codex or Gemini CLI, use the install page at thrixel.com/docs/build-world.

### Not found

The Codex and Gemini CLI install steps weren't checked. The README only points to thrixel.com/docs/build-world, which I didn't open.
