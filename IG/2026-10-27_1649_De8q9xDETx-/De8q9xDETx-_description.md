---
shortcode: "De8q9xDETx-"
url: "https://instagram.com/reel/De8q9xDETx-/"
type: "Reel"
author: "gittrend.io"
shared: "Oct 27, 2026, 04:49 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-01"
---

# 74 game-dev agent skills with one install

A reel promoting a free GitHub pack of 74 game-development skills for AI coding agents, with a router that loads the ones matching your engine and task. On-screen README pages show the install command and how the router chooses skills.

Written by claude-haiku-5-5.

## What it teaches

1. Install the pack in your project with: npx skills add gamedev-skills/awesome-gamedev-agent-skills (add --list to preview, -a <agent> such as -a cursor, -a claude-code or -a gemini-cli to target one tool, -g to install for every project).
2. Alternatively, install it as a Claude Code plugin: claude plugin marketplace add gamedev-skills/awesome-gamedev-agent-skills, then claude plugin install gamedev@awesome-gamedev-agent-skills.
3. For a single engine, install the smaller bundle: claude plugin install router@awesome-gamedev-agent-skills, then claude plugin install godot@awesome-gamedev-agent-skills (or the engine you use).
4. Describe what you are building in plain language to your agent; you never need to name skills yourself.
5. The router detects your engine from project files (project.godot means Godot, *.uproject means Unreal) and asks if it cannot tell.
6. The router reads the task (a concept, a genre, or a shipping step) and loads only the matching skills, engine basics first, then the concept, then genre skills, re-routing if you switch tasks.

## Source

* Link: gamedev-skills/awesome-gamedev-agent-skills

## Caption

This free pack gives your AI coding agent 74 game-dev skills and loads the right one for your engine. More like this → gittrend.io

#gamedev #aiagents #godot #unity #opensource #gamedevelopment #coding #github

## Research

* Verdict: Valid. The repo exists and matches the post: a router plus game-dev skills, Apache-2.0, with the same install commands. The repo now says 77 skills, not 74, so the count has grown since the reel.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [gamedev-skills/awesome-gamedev-agent-skills (github.com)](https://github.com/gamedev-skills/awesome-gamedev-agent-skills): repo, in the post, verified, high confidence. The README matches the post: a router that detects the engine from project.godot or *.uproject, the npx skills and claude plugin install commands, and Apache-2.0. It lists 77 skills across 12 engines.

### Already in IG saves

* Similar: Web: [Open-sourced Three.js game dev skills for isometric RPGs (instagram.com)](https://instagram.com/p/DbORY7-OLjT/) (`DbORY7-OLjT`). Open-sourced Three.js game-dev skills for agents, a narrower pack that does a similar job.

### Key steps

1. Needs Node.js 22.20 or later for the npx route.
2. Run: npx skills add gamedev-skills/awesome-gamedev-agent-skills (add --list to preview, -a <agent> to target one tool, -g for global).
3. Or in Claude Code: claude plugin marketplace add gamedev-skills/awesome-gamedev-agent-skills, then claude plugin install gamedev@awesome-gamedev-agent-skills.
4. For one engine only: install router@awesome-gamedev-agent-skills plus the engine bundle, e.g. godot@awesome-gamedev-agent-skills.
5. Describe your game task in plain language. The router detects the engine from project files and loads only the matching skills.
