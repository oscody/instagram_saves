---
shortcode: "DVHiGM5DJRn"
url: "https://instagram.com/p/DVHiGM5DJRn/"
type: "Carousel"
author: "theaifield"
shared: "Feb 26, 2026, 03:34 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Boris Cherny's CLAUDE.md workflow template

A three-slide carousel that shows a CLAUDE.md template of workflow rules attributed to Boris Cherny, the creator of Claude Code. The caption frames the template as a way to make Claude behave like a team of senior engineers on your project.

Written by claude-haiku-5-5.

## What it teaches

1. Plan Node Default: enter plan mode for any non-trivial task (3+ steps or architectural decisions); if something goes sideways, stop and re-plan immediately; use plan mode for verification steps, not just building; write detailed specs upfront to reduce ambiguity.
2. Subagent Strategy: use subagents liberally to keep the main context window clean; offload research, exploration, and parallel analysis to subagents; for complex problems, throw more compute at it via subagents; give each subagent one task for focused execution.
3. Self-Improvement Loop: after any correction from the user, update tasks/lessons.md with the pattern; write rules for yourself that prevent the same mistake; iterate on these lessons until the mistake rate drops; review lessons at session start for the relevant project.
4. Verification Before Done: never mark a task complete without proving it works; diff behavior between main and your changes when relevant; ask whether a staff engineer would approve this; run tests, check logs, and demonstrate correctness.
5. Demand Elegance (Balanced): for non-trivial changes, pause and ask whether there is a more elegant way; if a fix feels hacky, implement the elegant solution knowing everything you know now; skip this for simple, obvious fixes so you don't over-engineer; challenge your own work before presenting it.
6. Autonomous Bug Fixing: when given a bug report, just fix it without asking for hand-holding; point at logs, errors, and failing tests, then resolve them; require zero context switching from the user; go fix failing CI tests without being told how.
7. Task Management: write the plan to tasks/todo.md with checkable items; check in on the plan before starting implementation; mark items complete as you go; give a high-level summary of changes at each step; add a review section to tasks/todo.md to document results; update tasks/lessons.md after corrections.
8. Core Principles: simplicity first (make every change as simple as possible, impact minimal code); no laziness (find root causes, no temporary fixes, senior developer standards); minimal impact (touch only what's necessary and avoid introducing bugs).

## Caption

The guy who BUILT Claude Code just shared his actual workflow.

Boris Cherny runs 10–15 Claude sessions in parallel every single day.

5 in the terminal. 5–10 on the web. All shipping code at the same time.

But the real weapon isn’t the sessions, it’s his CLAUDE.md file.

Every time Claude makes a mistake, the team adds a rule so it never happens again. Boris literally told people to end every correction with: “Update your CLAUDE.md so you don’t make that mistake again.”
Claude writes rules for itself. The longer you use it, the smarter it gets on your specific codebase.

One more detail: he hasn’t written a single line of SQL in over 6 months. Claude pulls BigQuery data directly through the CLI.

Claude Code now makes up 4% of all public GitHub commits.

This CLAUDE.md template turns AI from a chatbot into a fleet of senior engineers working in parallel on your project.

➡️ Want to stay ahead in the world of AI? Grab your coffee, relax, and let our newsletter deliver the biggest updates straight to your inbox.
