---
shortcode: "DW5bfmLt4bS"
url: "https://instagram.com/reel/DW5bfmLt4bS/"
type: "Reel"
author: "chase.h.ai"
shared: "Apr 10, 2026, 12:55 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Career Ops: Claude Code job search tool

The reel recommends Career-Ops, an open-source GitHub repo that uses Claude Code and Playwright as a multi-agent job search system to filter listings and create job-specific resumes. On-screen README frames show its setup steps, usage commands and usage rules.

Written by claude-haiku-5-5.

## What it teaches

1. Configure: copy config/profile.example.yml to config/profile.yml and templates/portals.example.yml to portals.yml, then edit them with your details and the companies you want.
2. Add your CV as cv.md in the project root, written in markdown.
3. Run claude in that directory and ask Claude to adapt the system, for example changing archetypes, translating modes, adding companies to portals.yml, or updating your profile with a pasted CV.
4. Start by pasting a job URL or running /career-ops.
5. Usage: /career-ops with no arguments shows all commands, and /career-ops with a job description runs the full auto-pipeline (evaluate, PDF, tracker entry).
6. Treat it as a filter, not a spray-and-pray tool, and review every application before submitting.
7. Don't apply to anything scoring below 4.0, per the README.
8. Expect weak first evaluations and feed it your career story, proof points, preferences and what to avoid so it improves.

## Source

* Link: github.com/santifer/career-ops

## Caption

Comment “agent” for my Claude code guides

## Research

* Verdict: Valid. The repo exists, is MIT-licensed, and matches the post: a Claude Code job-search tool with /career-ops commands and the "don't apply below 4.0" rule. Setup has changed slightly since the reel.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [santifer/career-ops (github.com)](https://github.com/santifer/career-ops): repo, in the post, verified, high confidence. Opened the repo. It describes a local AI-CLI job search tool with /career-ops commands, PDF generation, a tracker, and the 4.0/5 guidance.

### Key steps

1. Quick setup: run `npx @santifer/career-ops init`. Or clone the repo, run `npm install`, then `npx playwright install chromium` (needed for PDF generation).
2. Open Claude Code (or another supported AI CLI) in the project folder. The first run walks you through setup by chat.
3. Add your CV (cv.md) and profile. Per the reel, copy config/profile.example.yml to config/profile.yml and templates/portals.example.yml to portals.yml, then edit them. The current README may have changed this flow.
4. Paste a job URL or description with `/career-ops {JD}`. It evaluates the job and produces a report, a PDF and a tracker entry.
5. Other commands: `/career-ops scan` (find new offers), `pipeline`, `pdf`, `tracker` and `batch`.
6. Review every output yourself. It never submits for you, and it advises against applying to roles scored below 4.0/5.

### Not found

The reel itself wasn't checked. The "agent" comment guides are a lead-gen offer and weren't needed.
