---
shortcode: "Dcwk8hBGDvv"
url: "https://instagram.com/p/Dcwk8hBGDvv/"
type: "Carousel"
author: "evolvingfrontier"
shared: "Sep 08, 2026, 07:56 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Eight Claude Code tips from Boris Cherny's talk

A carousel recapping tips from Boris Cherny's talk on Claude Code best practices at Anthropic's developer conference, noting which tips have since become built-in commands. It has a comment-to-receive course offer in the caption.

Written by claude-haiku-5-5.

## What it teaches

1. Start with codebase Q&A: ask Claude Code questions about your codebase from day one instead of relying on other engineers or manual code reading.
2. Put a CLAUDE.md in the project root and check it into git so the team shares it; keep personal notes in CLAUDE.local.md, which is not checked in.
3. Keep CLAUDE.md under about 200 lines, since adherence drops past that; use /init to generate one, /context to confirm it loaded, and /doctor to propose cuts.
4. Before coding, ask Claude to make a plan first. Plan mode is optional: press Shift+Tab until plan mode shows in the status bar, then Ctrl+G to edit the plan before Claude runs it.
5. Give Claude a way to check its own work, such as a unit test or a screenshot, so it can iterate; two or three rounds often gets close to perfect. A Stop hook can stop the turn from ending until the check passes.
6. Use /context to see which memory files are loaded and /memory to open auto memory, where Claude saves notes on your corrections and reloads them at the start of every session.

## Source

* How to get it: Comment "Claude" on the post to receive the course link

## Caption

Comment: “Claude” and we’ll send you the course link

Boris Cherny wrote Anthropic’s Claude Code best practices guide and took it on stage at the company’s first developer conference a month later. Clips from that talk still circulate as eight tips, and six of them have since been built into the tool: `/init` and `/doctor` for CLAUDE.md, plan mode for thinking first, Stop hooks for verification, `/batch` for running several sessions at once. He told the room they were actively working on that last one, and it shipped.

The one worth knowing about is `/memory`. On stage it listed the memory files being pulled into context; `/context` does that now, and `/memory` fronts auto memory, where Claude writes its own notes on your corrections and reloads them every session. Two of the eight never became commands at all, because codebase questions and git history need no special prompting. He rated codebase Q&A above every other tip on the list, and said it took technical onboarding at Anthropic from two or three weeks down to two or three days.

Follow @evolving.qc for the AI shifts that actually change how you work.

#AI #claudecode #anthropic #coding #aiagents
