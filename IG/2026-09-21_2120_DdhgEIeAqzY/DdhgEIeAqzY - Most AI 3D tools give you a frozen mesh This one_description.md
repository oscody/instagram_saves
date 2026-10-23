---
shortcode: "DdhgEIeAqzY"
url: "https://instagram.com/reel/DdhgEIeAqzY/"
type: "Reel"
author: "githubsignals"
shared: "Sep 21, 2026, 09:20 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Procedura: open-source text-to-editable-3D model tool

A showcase of Procedura, an open-source tool that turns a text prompt into a parametric 3D program with named parts, materials and moving joints. The video walks through the project's README install section and configuration variables on screen.

Written by claude-haiku-5-5.

## What it teaches

1. Clone the repo with git clone git@github.com:SpatiaOS/Procedura.git, then cd into Procedura.
2. Run bash scripts/install-deps.sh to install Bun, the packages, a Manifold-capable OpenSCAD, Blender and a starter .env.
3. Re-run the script safely; it leaves working parts alone, and bash scripts/install-deps.sh --check reports what is missing without installing.
4. Use --no-blender to skip the roughly 350 MB Blender download, or set PREFIX=/opt to install binaries somewhere else.
5. Make sure OpenSCAD has the Manifold backend, since a pre-Manifold build falls back to CGAL and runs far slower; the installer checks for --backend.
6. Copy .env.example to .env in the repo root and add your endpoint and key.
7. Set OPENAI_BASE_URL (for example https://api.openai.com/v1) and the key variable to choose the endpoint, or use GEMINI_API_KEY and GEMINI_BASE_URL with a gemini: model id for Gemini's native path.
8. Pick any model id your endpoint serves with PROCEDURA_MODEL, for example gpt-5.2 or gemini:gemini-3-pro-preview.

## Source

* Link: spatiaos/procedura

## Caption

Most AI 3D tools give you a frozen mesh. This one gives you the actual code behind the model. 

Generate 3D models from a simple text prompt that you can actually edit like code. Procedura solves the frustrating problem where AI usually spits out a frozen block of geometry that you cannot change without starting over. This tool uses an AI agent to write a parametric program, meaning every part is a named variable you can adjust, scale, or move later. It also adds realistic materials and moving joints, so your model isn’t just a static statue. The coolest part is that it’s not a black box; you get the actual source file to tweak.

Open source: spatiaos/procedura

Follow for more open source project drops.

#3DDesign #CreativeCoding #GenerativeAI #AICoding #Procedural3D

## Research

* Verdict: Valid. The repo exists and matches the post: text or image to editable parametric OpenSCAD with per-part materials and articulation. The current README leads with a different install route (MCP) than the one shown in the video.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [SpatiaOS/Procedura (github.com)](https://github.com/SpatiaOS/Procedura): repo, in the post, verified, high confidence. Opened the repo. It is MIT-licensed and turns a prompt into editable final.scad with materials and USD/URDF motion output.

### Key steps

1. Current README route (MCP): needs Git, curl, Python 3.11+ and a signed-in Codex or Claude Code. Linux x86_64 only.
2. Run the install script with --agent both (or codex / claude). For an existing clone, run bash scripts/install-mcp.sh --agent both.
3. Open the agent in ~/.local/share/Procedura and restart it if it was already open.
4. Ask for a build with an absolute PNG path, or use $procedura (Codex) or /procedura (Claude Code).
5. API route shown in the video: git clone git@github.com:SpatiaOS/Procedura.git, then bash scripts/install-deps.sh (use --check to inspect, --no-blender to skip Blender).
6. Copy .env.example to .env, then set OPENAI_BASE_URL plus the key, or GEMINI_API_KEY and GEMINI_BASE_URL. Set PROCEDURA_MODEL to a model id your endpoint serves.

### Not found

I did not check the install-deps.sh or .env details from the video against the repo files. The README page I opened does not list the .env variables. The vault notes returned only matched on "gpt-5.2" and ".env.example" and are unrelated.
