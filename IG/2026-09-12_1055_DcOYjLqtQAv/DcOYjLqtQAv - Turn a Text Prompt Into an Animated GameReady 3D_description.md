---
shortcode: "DcOYjLqtQAv"
url: "https://instagram.com/reel/DcOYjLqtQAv/"
type: "Reel"
author: "githubsignals"
shared: "Sep 12, 2026, 10:55 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# AnyCreature: text-to-3D creature generator from a JSON spec

A reel promoting the open-source AnyCreature project, which compiles an animated, game-ready 3D creature from one JSON spec or a text prompt. The video shows a flying creature model and the project's README, with its quick start, knob table and folder layout.

Written by claude-haiku-5-5.

## What it teaches

1. Run `bash setup.sh` to install dependencies and the red/green ruler checks.
2. Confirm setup.sh prints `calibrate OK` before trusting any other output.
3. Generate a model with `node engine/cli.js example/wolf.json out/wolf.glb`.
4. For a full text-to-creature session, point an agent at MANUAL.md and have it read cards/ in order: 00_START, 01_LOW, 02_MID, 03_HIGH, 04_SHIP.
5. Tune smooth_angle (default 50) in the spec root or per volume/part: higher gives a smoother body, lower gives more facets.
6. Set shading in the spec root to control the vertical colour gradient and grain.
7. Use build: "rigid" in the spec root only for robots and crystals, since it is the only way to get a fully faceted body past the checker.
8. Set ao to false in the spec root to skip the ambient occlusion bake.
9. Pick a QC role preset (minion.json, npc.json, boss.json) in harness/presets/ for different budgets and thresholds.

## Source

* Link: ariescar/anycreature

## Caption

Turn a Text Prompt Into an Animated, Game-Ready 3D Creature

AnyCreature is the text-to-3D pipeline that turns a simple written order into a fully animated, game-ready model. This is the creature generator that actually works, solving the nightmare of hand-sculpting every asset from scratch. Instead of downloading generic packs or wrestling with complex software, you just type a prompt like "menacing mountain giant." The system handles the heavy lifting, asking only a couple of clarifying questions before it builds the shape, colors, and animations itself. The coolest part is its strict quality control, where a separate AI agent acts as a blind judge to ensure the final model actually looks good, not just technically correct.

Open source: ariescar/anycreature
Spotted on Hacker News.

Follow for more open source project drops.

#3DGeneration #GameDev #GenerativeAI #AiAgents #aitools
