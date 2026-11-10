---
shortcode: "DfS0h0Nqyi4"
url: "https://instagram.com/reel/DfS0h0Nqyi4/"
type: "Reel"
author: "j.t.rivard"
shared: "Nov 04, 2026, 08:00 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-04"
---

# Five Claude Code features, countdown from #5

The creator lists five Claude Code features, including a 690-hour run that ended only because they had to reboot. The full list of commands is not in the post; it is sent by DM to people who comment LIST.

Written by claude-haiku-5-5.

## What it teaches

1. #5: Enable the plugin with /plugin enable cc-plugin-you-should-know@builtin. A second agent watches your agent's work and flags what it missed.
2. #4: Use /loop with no fixed interval for your task. The post gives no further detail.
3. #3: Lower the auto compact threshold with /autocompact, for example /autocompact 600000, from the default of a million to about two-thirds or half of the context window, to avoid context pollution on long runs.
4. #2: Use UltraCode, which runs custom JavaScript to coordinate dozens or hundreds of agents.
5. #1: Type ultrathink to force maximum reasoning effort for one turn only. Later turns go back to your normal effort level.

## Source

* How to get it: Comment LIST; the creator says they will DM all five commands. Follow the account first so the DM can be sent.

## Caption

Comment LIST and I’ll DM you all five commands. Follow first so I can send it.

I’ve had Claude Code run 690 hours straight, and it only stopped because I had to reboot my machine. That’s number four.

The other four: a plugin where a second agent checks your agent’s work, an auto compact setting that keeps Claude Code smarter on long runs, Ultracode for coordinating dozens or hundreds of agents, and my favorite at number one.

This is part one of a series. Which of these did you already know?

## Research

* Verdict: Partly valid. Ultrathink, /loop and Ultracode are real Claude Code features. I found no `/autocompact` command or `@builtin` plugin in the official changelog. The "690 hours" claim can't be checked, and the full list is only sent by DM.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Claude Code changelog (official) (code.claude.com)](https://code.claude.com/docs/en/changelog): page, found by search, verified, medium confidence. Opened it. v2.1.311 says ultrathink runs its turn at xhigh effort on Opus 5.5 and other 5.5 models, and v2.1.314 mentions Ultracode. It has no `/autocompact` command and no `@builtin` plugin syntax. The page was only read up to v2.1.311, so older entries may add more.
* [Claude Code commands reference (official) (code.claude.com)](https://code.claude.com/docs/en/commands): page, found by search, not opened, low confidence. Opened it, but it was too large to read fully. A grep showed matches for /loop and ultracode, and for autocompact (one match). I did not read the context of any of them.
* [just-every/plugin-ultracode (Codex plugin) (github.com)](https://github.com/just-every/plugin-ultracode): repo, in the vault, verified, low confidence. Your vault note 'repo - ultracode' links it. It coordinates many workers on one goal, but it is a Codex plugin and doesn't mention Claude Code. It is probably not the Ultracode in the reel.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/repo - ultracode.md`: Install commands and repo link for the just-every Ultracode plugin for Codex. Not the Claude Code Ultracode effort setting.
* Vault: `3. Resources/0. note idea draft/educative - Claude Code Workflows and Tools.md`: General notes on the think and ultrathink thinking-mode cues.

### Already in IG saves

* Same: Web: [Trim outdated CLAUDE.md rules with /doctor (instagram.com)](https://instagram.com/p/DefIicBgCiv/) (`DefIicBgCiv`). Same link: Claude Code commands reference (official).

### Key steps

1. Ultrathink: put the word 'ultrathink' in your prompt. Since v2.1.311 that turn runs at xhigh effort, and later turns go back to your normal effort. CLAUDE_CODE_DISABLE_ULTRATHINK (v2.1.316) turns the keyword off.
2. Ultracode: per the changelog it is an /effort toggle (reported from v2.1.284). Claude orchestrates dynamic workflows at that setting, so check /effort in your version.
3. Auto compact: I found no `/autocompact` command. The documented control is the CLAUDE_CODE_AUTO_COMPACT_WINDOW environment variable, which in v2.1.304 accepts k and M suffixes (e.g. 600k). Set it to roughly half to two-thirds of the context window.
4. /loop: run /loop with your task. Leave out the interval and Claude picks the timing. Loops are tied to the open session.
5. Second-agent plugin: the post gives `/plugin enable cc-plugin-you-should-know@builtin`. I could not verify that name or the `@builtin` syntax, so check /plugin in your own install first.

### Not found

The creator's full command list is sent by DM after you comment LIST, and no public copy was found. I could not verify the plugin 'cc-plugin-you-should-know@builtin' or a `/autocompact` command. The 690-hour run is unverifiable. I read only the first part of the changelog page, up to v2.1.311.
