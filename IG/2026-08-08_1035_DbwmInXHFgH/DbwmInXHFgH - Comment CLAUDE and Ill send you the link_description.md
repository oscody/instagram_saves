---
shortcode: "DbwmInXHFgH"
url: "https://instagram.com/p/DbwmInXHFgH/"
type: "Carousel"
author: "godofprompt"
shared: "Aug 08, 2026, 10:35 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Claude Code setup and workflow tips carousel

A six-slide carousel relaying setup and workflow tips from a talk by the Claude Code creator, covering setup commands, planning, layered CLAUDE.md context, and the SDK. It ends with a call to comment a keyword.

Written by claude-haiku-5-5.

## What it teaches

1. Run /terminal-setup to get shift+enter for new lines instead of backslashes.
2. Use /theme to switch between light and dark mode.
3. Run /install-github-app so you can mention Claude on GitHub issues and pull requests.
4. Customize the allowed tools list so you are not prompted to approve the same actions every time.
5. On macOS, enable dictation in system settings under accessibility and dictate prompts instead of typing them.
6. Plan first: ask Claude to brainstorm or make a plan before it writes code, and give it enough context, since it makes better decisions with more.
7. Put a CLAUDE.md file in the project root with common bash commands, common MCP tools, and architecture notes; it is read automatically at the start of every session.
8. Check the project CLAUDE.md into source control so the team shares it, and use CLAUDE.local.md for personal notes that are not checked in.
9. Layer context: an enterprise root CLAUDE.md applies to all sessions, and ~/.claude/CLAUDE.md is shared across all your projects.
10. Automate with the Claude Code SDK: use claude -p with a prompt, allowed tools, and an output format such as JSON or streaming JSON, treating it like a Unix utility.
11. Scale automation once it works, for example in CI pipelines or incident response.

## Source

* How to get it: Comment the keyword CLAUDE on the post; the post says the link is sent after commenting.

## Caption

Comment “CLAUDE” and I’ll send you the link.

The engineer who created Claude Code just dropped a 28-minute video, and it’s a completely different level of insight than the generic prompts everyone recycles.

He walks through exactly how to get 300% more out of Claude: CLAUDE.md files, permanent memory across sessions, running multiple sessions in parallel, and prompting tricks nobody actually shares. $300 courses don’t cover in full what he explains in the first 10 minutes.

And it’s free.

Doesn’t matter if you’re just starting out or coding all day, after this, you’ll be using Claude in a way you didn’t know was possible.

## Research

* Verdict: Partly valid. The video is real and public: Boris Cherny's "Mastering Claude Code in 30 minutes" for Anthropic. The "300% more" and "$300 courses" lines are hype, and the "link" is just a comment-to-DM funnel for a public video.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Mastering Claude Code in 30 minutes (Boris Cherny, Anthropic) (youtube.com)](https://www.youtube.com/watch?v=6eBSHbLKuN0): video, found by search, not opened, medium confidence. The page title matches, but I couldn't confirm channel or length. I recalled the video ID from memory, and search results gave a runtime of about 28 min and Boris as speaker.

### Key steps

1. Watch the video on YouTube (search the exact title if the link is wrong).
2. Run /terminal-setup for shift+enter newlines.
3. Add a CLAUDE.md in the project root with bash commands, MCP tools and architecture notes.
4. Use CLAUDE.local.md for personal notes and ~/.claude/CLAUDE.md for global context.
5. Ask Claude to plan before coding.
6. Run /install-github-app and tune the allowed tools list.
7. Automate with claude -p, allowed tools and --output-format json.

### Not found

The official Anthropic upload page could not be confirmed. I didn't find godofprompt's DM link, which is probably just the YouTube video. The vault has no note on this resource.
