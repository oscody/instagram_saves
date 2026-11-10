---
shortcode: "Deo8i2rEQi5"
url: "https://instagram.com/reel/Deo8i2rEQi5/"
type: "Reel"
author: "jackroberts___"
shared: "Oct 28, 2026, 08:09 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-28"
---

# Two Claude Code mods to stop losing work

The post introduces two Claude Code mods that keep long sessions from losing details when Claude compacts its context. It shows the auto-handoff workflow on screen: a brief is written at about 80k context, and a fresh session reads it and continues (71k to 31k).

Written by claude-haiku-5-5.

## What it teaches

1. Turn on "You Should Know", which is built into Claude Code: a second AI watches the session and flags anything you or Claude missed.
2. Use auto-handoff near the context limit, before Claude compacts itself, so details are not squashed.
3. Auto-handoff writes a brief of the session right before compacting.
4. It then starts a fresh session that reads the brief and continues the work from where it left off.

## Source

* Link: github.com/alexknowshtml/claude-auto-handoff
* How to get it: Full setup for both mods is sent by comment: comment "MODS" on the post.

## Caption

Comment "MODS" and I'll send you the setup for both.

Long sessions don't break at the start.

They break near the end.

That's when Claude Code compacts itself.

And the details you needed get squashed.

Mod one is You Should Know.

It's built right in.

A second AI watches the session.

It flags what you or Claude missed.

Mod two is auto-handoff.

It's free on GitHub.

Right before compacting, it writes a brief.

Then hands it to a fresh session.

Like a shift change at a hospital.

The next nurse gets the full chart.

So your work keeps moving.

And nothing important gets dropped.

#claudecode #claudemods #claude #aiagent #aicoding

## Research

* Verdict: Valid. The auto-handoff repo exists and matches the post. It writes a brief and starts a fresh session. "You Should Know" is only confirmed by one secondary write-up. The "comment MODS" setup is a lead-in, since the repo is public.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [claude-auto-handoff (github.com)](https://github.com/alexknowshtml/claude-auto-handoff): repo, in the post, verified, high confidence. Opened the repo. It is a Claude Code mod that writes a Haiku handoff brief near the context limit, runs /clear, and seeds a fresh session with the brief.
* [Watcher Side Agents (describes the built-in 'You Should Know' mod) (agentpatterns.ai)](https://agentpatterns.ai/patterns/agent-design/watcher-side-agents/): page, found by search, not opened, low confidence. The search summary says this page describes the built-in mod, enabled with /plugin enable cc-plugin-you-should-know@builtin. I did not open the page and found no Anthropic doc for it.

### Key steps

1. Needs a Claude Code build that supports mods (function-hook plugins).
2. Clone: git clone https://github.com/alexknowshtml/claude-auto-handoff.git ~/claude-auto-handoff
3. Load for one session: claude --plugin-dir ~/claude-auto-handoff
4. To load it in every session, set CLAUDE_CODE_PLUGIN_DIRS to that folder, in your shell or in the env block of ~/.claude/settings.json.
5. The mod checks context size each turn. Past the threshold (default 160k tokens) it has Haiku write a brief to ~/.claude/state/auto-handoff/<session-id>.md, runs /clear, and points the new session at the brief.
6. Change threshold, maxConsecutiveHandoffs, ignoreFiles and viewer under auto-handoff in /config. The post shows about 80k, so you may want a lower threshold.
7. Edit your copies of brief.md and instructions.md in ~/.claude/auto-handoff/ so git pull doesn't overwrite them.
8. Test with AUTO_HANDOFF_TOKENS to set the threshold for one run. Use AUTO_HANDOFF_DISABLE=1 to turn the mod off.
9. For 'You Should Know', one secondary source gives: /plugin enable cc-plugin-you-should-know@builtin. This is unconfirmed.

### Not found

I found no official Anthropic documentation for the built-in "You Should Know" mod, only one secondary write-up that I did not open. I did not check the creator's DM/comment setup, but the repo is public.
