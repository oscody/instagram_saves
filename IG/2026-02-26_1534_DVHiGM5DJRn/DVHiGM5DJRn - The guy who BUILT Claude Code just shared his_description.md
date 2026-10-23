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

## Research

* Verdict: Partly valid. The template exists publicly and matches the slides. The attribution to Boris Cherny looks secondhand: it appears to be a community file built from his posts, and I found no source from him.
* Checked: 2026-10-23 by claude-sonnet-5-5

### Resources

* [Boris Cherny's CLAUDE.md (gist by hqman) (gist.github.com)](https://gist.github.com/hqman/e29cb6386c539d795767e8c3fd2c959b): page, found by search, verified, medium confidence. Its headings match the carousel exactly: Plan Node Default, Subagent Strategy, Self-Improvement Loop, Verification Before Done, Demand Elegance, Autonomous Bug Fixing, Task Management, Core Principles. The gist has no author byline tying it to Cherny.
* [Claude Code creator workflow CLAUDE.md (MindWired AI deep dive) (mindwiredai.com)](https://mindwiredai.com/2026/03/25/claude-code-creator-workflow-claudemd/): guide, found by search, not opened, low confidence. A secondary blog post that treats the file as Cherny's. I only saw it in search results and did not open it.

### Key steps

1. Copy the gist's contents into a CLAUDE.md at your project root, or into ~/.claude/CLAUDE.md to apply it everywhere.
2. Create a tasks/ folder with todo.md and lessons.md. The template tells Claude to write plans and lessons there.
3. After each correction, tell Claude: "Update your CLAUDE.md so you don't make that mistake again." The template itself routes lessons to tasks/lessons.md.
4. Edit the file to fit your project. Treat it as a starting point, not an official Anthropic file.

### Not found

I found no first-party post from Boris Cherny publishing this exact file. I did not check the caption's other claims: 10–15 parallel sessions, no SQL in 6 months, and 4% of GitHub commits. The vault has no note on this resource.
