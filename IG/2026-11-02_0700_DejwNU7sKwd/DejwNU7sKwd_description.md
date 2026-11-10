---
shortcode: "DejwNU7sKwd"
url: "https://instagram.com/reel/DejwNU7sKwd/"
type: "Reel"
author: "sheni_icg"
shared: "Nov 02, 2026, 07:00 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Nine Claude Code tips for agent teams

A creator lists nine tips for running Claude Code with an agent team, covering the Superset or Orca environment, team roles, handoff documents, auto-compact, and overnight decisions. The on-screen list and transcript match.

Written by claude-haiku-5-5.

## What it teaches

1. Work in an agent development environment such as Superset or Orca instead of leaving Visual Studio Code.
2. Ask Claude to build an agent team that works in git worktrees of your project folder, with each agent getting its own copy so they don't overwrite each other.
3. Give each agent a human name, one job, and the ability to create its own sub-agents (for an app: CTO, database, UI, tester).
4. Only talk to one agent, and have the other agents send their information and questions through that agent.
5. Create an agent team skill that sets start and stop rules, decides how many agents a task needs, and includes a protocol covering who talks to whom, message flow, handoffs, scope, and how to check work.
6. Make sure every window opens in the same mode (for example bypass permissions or auto mode), since a mismatched agent can block messages.
7. Have every team member maintain a handoff.md with what's done, what's in progress, what's next, and the info needed for auto compaction.
8. Turn on auto compact and set it to about 400,000 tokens.
9. For overnight runs, have Claude front-load its questions, then say you're going to bed and keep all decisions in decisions.md to review in the morning.

## Source

* How to get it: Comment "SUPERSET" for the agent team setup guide (offered in the caption and on screen)

## Caption

Comment “Superset” for the setup guide

## Research

* Verdict: Partly valid. Superset is real (now renamed Paradev), and the tips are plausible workflow advice. The creator's "setup guide" is only sent by comment, and the 400k auto-compact figure and the "better than 99%" claim rest on personal anecdote.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Superset (now Paradev) – open-source worktree-based agent desktop app (github.com)](https://github.com/superset-sh/superset): repo, found by search, verified, high confidence. Repo page describes a desktop app that runs Claude Code and other CLI agents in parallel, each in its own git worktree, and says it was formerly named Superset.
* [Superset vs Orca comparison (paradev.com)](https://paradev.com/compare/superset-vs-orca): page, found by search, not opened, medium confidence. The old superset.sh comparison URL redirected here; I did not open the page itself. It covers the two tools the post names.

### Key steps

1. Install Git (gh CLI optional) and download the desktop app from the GitHub releases page (macOS primary, Linux experimental, no Windows).
2. Add or clone a repo and create a workspace; each workspace gets its own git worktree and branch.
3. Optional CLI: curl -fsSL https://paradev.com/cli/install.sh | sh, or brew install paradevai/tap/superset.
4. Run Claude Code in each workspace's terminal, with the same permission mode in every window.
5. Per the post: have each agent keep handoff.md, set auto-compact near 400k tokens, and keep overnight decisions in decisions.md.

### Not found

The creator's "SUPERSET" setup guide (sent by comment or DM) has no public copy that I found. I did not check Orca's own site. The auto-compact and token-saving numbers come from the creator and I could not verify them.
