---
shortcode: "DV8qasfDWXx"
url: "https://instagram.com/p/DV8qasfDWXx/"
type: "Carousel"
author: "leadgenman"
shared: "Mar 20, 2026, 06:31 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Boris Cherny's CLAUDE.md File Rules

A five-slide carousel listing the sections of a CLAUDE.md config file attributed to Claude Code's founder, covering workflow orchestration, task management and core principles. The final slide asks viewers to comment for the full file.

Written by claude-haiku-5-5.

## What it teaches

1. Plan mode: enter plan mode for any non-trivial task (3+ steps or architectural decisions).
2. If something goes sideways, stop and re-plan immediately.
3. Use plan mode for verification steps, not just building.
4. Write detailed specs upfront to reduce ambiguity.
5. Use subagents liberally to keep the main context window clean.
6. Offload research, exploration, and parallel analysis to subagents.
7. For complex problems, throw more compute at it via subagents.
8. Give each subagent one task for focused execution.
9. After any correction from the user, update tasks/lessons.md with the pattern.
10. Write rules for yourself that prevent the same mistake.
11. Ruthlessly iterate on these lessons until the mistake rate drops.
12. Review lessons at session start for the relevant project.
13. Never mark a task complete without proving it works.
14. Diff behavior between main and your changes when relevant.
15. Ask yourself: would a staff engineer approve this?
16. Run tests, check logs, and demonstrate correctness.
17. For non-trivial changes, pause and ask whether there is a more elegant way.
18. If a fix feels hacky, implement the elegant solution knowing everything you know now.
19. Skip this for simple, obvious fixes; don't over-engineer.
20. Challenge your own work before presenting it.
21. When given a bug report, just fix it without asking for hand-holding.
22. Point at logs, errors, and failing tests, then resolve them.
23. Require zero context switching from the user.
24. Fix failing CI tests without being told how.
25. Plan first: write the plan to tasks/todo.md with checkable items.
26. Verify plan: check in before starting implementation.
27. Track progress: mark items complete as you go.
28. Explain changes: give a high-level summary at each step.
29. Document results: add a review section to tasks/todo.md.
30. Capture lessons: update tasks/lessons.md after corrections.
31. Simplicity first: make every change as simple as possible and impact minimal code.
32. No laziness: find root causes, no temporary fixes, senior developer standards.
33. Minimal impact: only touch what's necessary, with no side effects or new bugs.

## Source

* How to get it: Comment "MD" to get the full file

## Caption

The founder of Claude Code, Boris Cherny, shared his personal CLAUDE. md file — the config that controls how Claude Code thinks in your repo. @boris_cherny 

Drop this file in your project root:

- Plans before writing a single line
- Spins up subagents for parallel work
- Logs its own mistakes and never repeats them
- Refuses to mark tasks done without proof

3 sections. 33 rules. Zero hand-holding.
This is how top engineers ship 10x faster from the terminal.

Comment “MD” to get the full file.

## Research

* Verdict: Partly valid. A public copy of this CLAUDE.md exists, but it's a third-party reconstruction, not a file Boris Cherny published. The post's "his personal file" framing is overstated, and the comment-for-file gate isn't needed.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Claude Code creator workflow CLAUDE.md (MindWired AI) (mindwiredai.com)](https://mindwiredai.com/2026/03/25/claude-code-creator-workflow-claudemd/): guide, found by search, verified, medium confidence. Page shows a CLAUDE.md with Workflow Orchestration, Task Management and Core Principles (Simplicity First, No Laziness, Minimal Impact), labelled 'reconstructed from his public sharing'.
* [InfoQ: Claude Code creator workflow (infoq.com)](https://infoq.com/news/2026/01/claude-code-creator-workflow/): page, found by search, not opened, medium confidence. Search snippet says Cherny describes teams keeping a CLAUDE.md in git to log mistakes (about 2.5k tokens); it did not confirm the wording of this file. I did not open it.

### Key steps

1. Create CLAUDE.md in your project root.
2. Add a Workflow Orchestration section: plan mode for tasks of 3+ steps, subagents for research, a self-improvement loop, verify before done, demand elegance, and autonomous bug fixing.
3. Add a Task Management section: write the plan to tasks/todo.md, check in before starting, track progress, summarize changes, add a review section, and update tasks/lessons.md after corrections.
4. Add Core Principles: Simplicity First, No Laziness (find root causes), Minimal Impact.
5. Create the tasks/ folder with todo.md and lessons.md, and have Claude review lessons.md at session start.
6. Edit the rules to fit your repo. Anthropic's own advice is to keep CLAUDE.md short.

### Not found

I did not find Boris Cherny's original Threads or X post, and nothing confirms the 33-rule file is his verbatim file. The MindWired text may differ from the carousel's wording.
