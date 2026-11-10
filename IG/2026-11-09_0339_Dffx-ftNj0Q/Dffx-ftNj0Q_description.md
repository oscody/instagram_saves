---
shortcode: "Dffx-ftNj0Q"
url: "https://instagram.com/reel/Dffx-ftNj0Q/"
type: "Reel"
author: null
shared: "Nov 09, 2026, 03:39 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-09"
---

# Four ways to keep Claude Code working

Explains four modes Anthropic describes for running Claude Code without being told each next step, with a diagram of how a goal-based loop works. The full setup for all four is sent by comment.

Written by claude-haiku-5-5.

## What it teaches

1. Pick the mode by what you are handing off. Turn-based: give Claude a task; it works, checks the result, and stops when it thinks it is done or needs your input.
2. Goal-based: define a measurable finish line (example: get the homepage Lighthouse score to 90 or above) and set a limit on attempts (example: stop after 5 tries). Use it for tasks with verifiable exit criteria.
3. Goal-based loop mechanics: Claude works on the task, an evaluator model checks your condition, and if it is not met the work goes back to Claude. The loop ends when the goal is met or the turn limit is reached.
4. Time-based: use a timer for something you keep checking yourself (example: every 30 minutes, check customer reviews and surface complaints).
5. Proactive: set up a cloud workflow that runs even when your laptop is closed (example: one agent picks up bug reports, another fixes them, another reviews the changes, and you approve what ships).
6. Starting point: pick one task you are tired of checking on, give it a clear finish line, and set a limit on how long it keeps trying.

## Source

* How to get it: Comment "autopilot" to receive the step-by-step setup for all four modes

## Caption

comment “autopilot” and I’ll send you the step-by-step to set up all four ⚡

if you’re still typing “keep going” to Claude, you’re the bottleneck.

Anthropic laid out 4 ways to keep Claude Code working on its own:
1. turn-based
2. goal-based
3. time-based
4. proactive

start with one task you’re tired of checking on. give it a clear finish line and a limit on how long to keep trying.

#claudecode #aiagents #aiautomation #claudeai #aitools

## Research

* Verdict: Valid. Anthropic's "Getting started with loops" article describes exactly these four loop types, and the vault already holds a rebuilt step-by-step guide.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Loop engineering: Getting started with loops (Anthropic) (claude.com)](https://claude.com/blog/getting-started-with-loops): guide, in the vault, verified, high confidence. Opened it; it covers turn-based, goal-based (/goal with Lighthouse 90, 5 tries), time-based (/loop) and proactive (/schedule) loops, as in the reel.
* [anthropics/cwc-long-running-agents (github.com)](https://github.com/anthropics/cwc-long-running-agents): repo, in the vault, not opened, medium confidence. Linked in the vault note as a related harness; not opened.

### Already in the vault

* Vault: `ZAIHub/claude - Four ways to keep Claude Code working 2026-11-10.md`: Full step-by-step setup for all four loop types, rebuilt from Anthropic's article and docs (/goal, /loop, routines).
* Vault: `3. Resources/0. Daily/2026-11-09.md`: Daily note linking the reel, the article, the cwc-long-running-agents repo and the guide.

### Key steps

1. Turn-based: write a specific prompt. Add a verification skill (SKILL.md) so Claude can check its own work, for example by starting the dev server and checking the browser console.
2. Goal-based: type `/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.` Run `/goal` with no arguments to see turns and token use.
3. Time-based: `/loop 5m check my PR, address review comments, and fix failing CI` re-runs a prompt on an interval on your computer. It stops if you shut the machine off.
4. Time-based in the cloud: use `/schedule` to move the loop to a cloud routine.
5. Proactive: use `/schedule` with a prompt that combines a schedule, a `/goal` and a workflow, such as handling bug reports. Dynamic workflows (research preview) can coordinate several agents.
6. Turn on auto mode so the routine doesn't pause for permission.
7. Send routine work to smaller, faster models. Keep the most capable model for judgment calls.

### Not found

The comment-only \"autopilot\" guide has no public copy, but Anthropic's article covers the same content. I didn't open the docs pages or the GitHub repo. I did a quick check of other saved posts but didn't confirm any as the same or similar.
