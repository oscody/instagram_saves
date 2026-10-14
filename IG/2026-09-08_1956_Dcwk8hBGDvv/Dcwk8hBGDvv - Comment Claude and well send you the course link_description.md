---
shortcode: "Dcwk8hBGDvv"
url: "https://instagram.com/p/Dcwk8hBGDvv/"
type: "Carousel"
author: "evolvingfrontier"
shared: "Sep 08, 2026, 07:56 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Boris Cherny's Claude Code tips from his talk

A carousel recapping tips Boris Cherny gave on stage at Anthropic's first developer conference, noting which ones have since become built-in Claude Code features. It covers codebase Q&A, CLAUDE.md, planning, feedback loops and memory.

Written by claude-haiku-5-5.

## What it teaches

1. Ask Claude Code questions about your codebase directly; no command is needed. The speaker said this cut Anthropic's technical onboarding from two or three weeks to two or three days.
2. Keep one CLAUDE.md in the project root, written by hand and checked into git. Use /init to generate one from the codebase, /context to confirm it loaded, and /doctor to propose cuts once it passes about 200 lines.
3. Plan before coding: ask Claude to make a plan, or press Shift+Tab until plan mode is on, then Ctrl+G to edit the plan before Claude runs it.
4. Give Claude a feedback loop, such as a unit test or a screenshot to check its work against. The speaker said two or three iterations gets it almost perfect. Stop hooks can enforce this by blocking the turn from ending until the check passes.
5. Run several sessions at once with /batch.
6. Use /context to see which memory files are loaded, and /memory to view and edit auto memory, where Claude saves notes on your corrections and reloads them at the start of every session.

## Source

* How to get it: Comment "Claude" on the post to receive the course link

## Caption

Comment: “Claude” and we’ll send you the course link

Boris Cherny wrote Anthropic’s Claude Code best practices guide and took it on stage at the company’s first developer conference a month later. Clips from that talk still circulate as eight tips, and six of them have since been built into the tool: `/init` and `/doctor` for CLAUDE.md, plan mode for thinking first, Stop hooks for verification, `/batch` for running several sessions at once. He told the room they were actively working on that last one, and it shipped.

The one worth knowing about is `/memory`. On stage it listed the memory files being pulled into context; `/context` does that now, and `/memory` fronts auto memory, where Claude writes its own notes on your corrections and reloads them every session. Two of the eight never became commands at all, because codebase questions and git history need no special prompting. He rated codebase Q&A above every other tip on the list, and said it took technical onboarding at Anthropic from two or three weeks down to two or three days.

Follow @evolving.qc for the AI shifts that actually change how you work.

#AI #claudecode #anthropic #coding #aiagents
