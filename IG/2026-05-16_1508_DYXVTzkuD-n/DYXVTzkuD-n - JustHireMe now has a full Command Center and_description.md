---
shortcode: "DYXVTzkuD-n"
url: "https://instagram.com/reel/DYXVTzkuD-n/"
type: "Reel"
author: "marc.kaz"
shared: "May 16, 2026, 03:08 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# JustHireMe AI job search agent update

A demo of JustHireMe, an open-source AI job search agent, showing its Command Center screens: job pipeline, discarded jobs, a knowledge graph, and a generated resume and cold email. The caption lists the features and the post links the GitHub repo.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/vasu-devs/JustHireMe

## Caption

JustHireMe now has a full Command Center and pro-level features.

Ships with:
• Real-time dashboard (active leads, scores, agent status)
• Paste any job URL → instant tailored resume + cover letter
• Outreach generator (DMs, LinkedIn notes, cold emails in your voice)
• Rebuilt 3D Knowledge Graph + Job Pipeline CRM
• Live Activity Stream + built-in AI assistant
• Modular agents you can configure yourself

Still 100% local, private, open source & free.

👉 https://github.com/vasu-devs/JustHireMe

## Research

* Verdict: Valid. The GitHub repo exists and matches the post: local-first, open source, with scraping, ranking, a knowledge graph, tailored resume and cover letter, and outreach drafts. The page doesn't use the name "Command Center", and it describes the license as AGPL-3.0 with commercial licenses offered separately, so "free" holds for self-use.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [JustHireMe (github.com)](https://github.com/vasu-devs/JustHireMe): repo, in the post, verified, high confidence. README describes a local desktop job-search app with lead scraping, fit ranking, a Kùzu knowledge graph, a CRM pipeline, and resume, cover letter and outreach generation.

### Key steps

1. Easiest: download the installer for your OS from the repo's GitHub Releases page (.exe, .dmg for Apple Silicon, .deb or AppImage).
2. On macOS the app isn't notarized, so allow it in System Settings > Privacy & Security.
3. The first launch downloads a one-time runtime pack (browser, vector libraries, embedding model).
4. Pick a model backend: local Ollama, an existing Claude Code or Codex CLI subscription, or an optional API key.
5. To run from source, clone the repo and run `npm ci`.
6. Then run `cd backend && uv sync --dev`.
7. Start it with `npm run tauri dev`. This needs Node 24, Python 3.13+, Rust and uv.

### Not found

I didn't check the "Paste any job URL" feature, the built-in AI assistant or the Activity Stream. The README summary didn't mention them. Browser auto-apply is experimental and off by default.
