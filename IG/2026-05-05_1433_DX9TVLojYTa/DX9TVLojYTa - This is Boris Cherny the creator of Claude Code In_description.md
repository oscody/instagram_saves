---
shortcode: "DX9TVLojYTa"
url: "https://instagram.com/p/DX9TVLojYTa/"
type: "Carousel"
author: "evolving.ai"
shared: "May 05, 2026, 02:33 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Boris Cherny's 8 tips for mastering Claude Code

A carousel by Evolving AI summarizing talk by Boris Cherny, creator of Claude Code, on eight practices for getting more out of it. Each slide gives one tip with a short explanation and stills from the talk.

Written by claude-haiku-5-5.

## What it teaches

1. Start with codebase Q&A: ask Claude questions about your codebase so it explores the files itself, which Anthropic uses for new-hire technical onboarding.
2. Ask about git history to understand the why behind changes, such as who introduced arguments and which GitHub issues the commits link to.
3. Create a CLAUDE.md file in the project root to store architecture notes, style rules, and key build commands; it is read at the start of every session. CLAUDE.md is checked into source control to share with the team, while CLAUDE.local.md is not checked in and is for you alone.
4. Plan before coding: ask Claude to brainstorm and make a plan, then approve the approach before it executes or writes code.
5. Enable feedback loops by giving Claude a way to check its own work, such as unit tests, screenshots, or visual output, so it can iterate and fix mistakes.
6. Run /memory to see which memory files Claude pulls into a session, and edit them to correct wrong context or add project-specific rules.
7. Automate with the Claude Code SDK by piping logs, git status, or Sentry data into Claude, treating it like a Unix utility that outputs JSON or streaming JSON.
8. Scale with multiple Claude instances in parallel, using separate checkouts in terminal tabs, git worktrees for branch isolation, or SSH and tmux sessions, with each instance working on a different part of the codebase.

## Caption

🤖⚡ This is Boris Cherny, the creator of Claude Code. In just a couple of minutes, he explains how to actually master Claude Code.

Save this before you forget it.

Here are the 8 tips:

1. Start with codebase Q&A so Claude explores the project on its own.

2. Ask about git history to understand why changes were made, not just what changed.

3. Add a CLAUDE.md file to your project root so context loads at the start of every session.

4. Plan before coding. Ask Claude to brainstorm an approach and approve it before execution.

5. Enable feedback loops with tests or screenshots so Claude can check its own work.

6. Use /memory to see and edit exactly what context Claude pulls into a session.

7. Automate with the SDK by piping logs, git status, or Sentry data straight into Claude.

8. Run multi-Claude in parallel with git worktrees or tmux to scale across the codebase.

These tips will change the way you use Claude forever.

What are your thoughts on this? 🤔💬 
—

➡️ If you want to keep up with all the AI news, useful tips, and important developments, join 100k+ subscribers reading our free newsletter

#ai #artificialintelligence #technology

## Research

* Verdict: Partly valid. The tips match known Claude Code practices and Boris Cherny's public talks. I couldn't open the original talk the carousel draws from, and no source I opened confirms the full list of 8 tips.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Anthropic's official Claude Code masterclass (write-up with video link) (opinionai.substack.com)](https://opinionai.substack.com/p/anthropics-official-claude-code-masterclass): guide, found by search, verified, low confidence. I opened it. It covers a newer Boris Cherny talk (memory files, parallel agents, verification), not the talk the carousel's 8 tips come from.
* [Boris Cherny talk video (YouTube live) (youtube.com)](https://www.youtube.com/live/GMIWm5y90xA?si=YxEAHacMAA9Kdpbx): video, found by search, not opened, low confidence. The link comes from the write-up above. I didn't open it, and it appears to be a newer talk than the one the carousel describes.

### Not found

I didn't find the original "Mastering Claude Code in 30 minutes" talk on an official Anthropic page. I opened no source that lists all 8 tips, and I couldn't confirm that tips 1 and 2 (codebase Q&A, git history) come from that talk. The vault has nothing on this post. The only vault match is an unrelated evolving.ai note.
