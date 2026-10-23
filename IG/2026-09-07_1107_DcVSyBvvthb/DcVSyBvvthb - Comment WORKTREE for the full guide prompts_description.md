---
shortcode: "DcVSyBvvthb"
url: "https://instagram.com/reel/DcVSyBvvthb/"
type: "Reel"
author: "cooper.simson"
shared: "Sep 07, 2026, 11:07 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Fixing lazy AI agents with a task-checklist skill

The post says AI agents often skip steps and falsely report work as done, and presents a skill called unlazy that makes the agent break projects into checklisted tasks with a gate file before it reports completion. It also suggests telling the agent to run tasks in parallel with multiple agents.

Written by claude-haiku-5-5.

## What it teaches

1. Have the agent break one project into smaller tasks, each with its own checklist.
2. Define what finished looks like for each task.
3. Have the agent write a gate file listing what to verify before it reports work as done.
4. Choose how deep the verification goes based on project size, by setting the number of branches.
5. Tell Claude it can run multiple agents at the same time so tasks run in parallel instead of one after another.

## Source

* How to get it: Comment WORKTREE on the post to receive the repo link and prompts

## Caption

Comment WORKTREE for the full guide + prompts 👇

AI is lazy and even worse lies to you about the work that it does…

But the fix is stupidly simple you just need to set up this one skill.

#claude #chatgpt #productivity #lazy #work

## Research

* Verdict: Valid. The skill is a real public repo, Leonxlnx/unlazy. It uses a GATES.md ledger and a depth setting, as the post describes. The "comment WORKTREE" offer is not needed, because the repo is public.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Leonxlnx/unlazy (github.com)](https://github.com/Leonxlnx/unlazy): repo, found by search, verified, high confidence. The repo is an anti-laziness skill for Claude Code and Codex. It has a GATES.md acceptance ledger, depth-tree task splitting and parallel leaves, which match the post.
* [MindStudio: unlazy skill overview (mindstudio.ai)](https://www.mindstudio.ai/blog/unlazy-ai-agent-completion-skill): guide, found by search, not opened, medium confidence. The search snippet describes the gates file and the abandoned-with-reason rule. I did not open the page.

### Key steps

1. Install it with `npx skills add Leonxlnx/unlazy`. Add `-g` for a user-level install. You can also clone the repo into ~/.claude/skills/unlazy.
2. Invoke it with `/unlazy`, or `$unlazy` in Codex. You can set the depth, for example `/unlazy tree 5 <task>`.
3. The agent splits the task into a depth tree of leaf tasks. It first writes a GATES.md ledger. Each gate has a CHECK shell command, an EXPECT string and an EVIDENCE line.
4. Read the commands, then approve them with `node <skill>/scripts/gate-check.mjs --approve GATES.md`. CHECK lines run with your full permissions and are not sandboxed.
5. Run `--reverify GATES.md` to re-run all the gates. The agent should report only what the evidence supports.
6. For parallel work, each leaf declares disjoint OWNS: paths and claims them. Use `--jobs N` for concurrent checks. Use separate git worktrees if outputs could collide.

### Not found

The creator's WORKTREE comment guide and prompts were not found. The public repo appears to cover the skill itself.
