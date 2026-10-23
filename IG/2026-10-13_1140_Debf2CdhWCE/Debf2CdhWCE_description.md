---
shortcode: "Debf2CdhWCE"
url: "https://instagram.com/reel/Debf2CdhWCE/"
type: "Reel"
author: "nocodealex"
shared: "Oct 13, 2026, 11:40 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Effortless: Claude Code mod that picks effort level

The post promotes Effortless, a free Claude Code mod that uses Haiku 5.5 to set the effort level for each prompt. It claims up to 42% lower Opus 5.5 costs on four mostly easy coding tasks, with all 12 answers still correct.

Written by claude-haiku-5-5.

## What it teaches

1. Install in Claude Code by pasting the link into Claude Code, or by running /plugin marketplace add HeyCubit/effortless and then /plugin install effortless@effortless.
2. Effortless reads each prompt with Haiku 5.5 and sets Low effort for quick questions and High effort for hard jobs.
3. Lower effort saves usage because every request rereads the whole chat, and at lower effort the model makes fewer requests.
4. Savings are smaller on hard work, since the reported tests were mostly easy tasks.

## Source

* Link: HeyCubit/effortless
* How to get it: Comment "SAVE" and the link is sent by DM (the post says to follow so the DM arrives)

## Caption

Comment “SAVE” and I’ll DM you the link to this free mod that cuts what Claude costs you. Follow so the DM lands 📩

👇 READ BELOW: a free Claude Code mod called Effortless picks the effort level for every prompt.

1. A quick question gets the same deep thinking as building a whole app, and it all comes out of your limit.

2. Effortless reads each prompt with Haiku 5.5 (about a second, on your own Claude login, no key) and sets Low for quick questions and High for hard jobs.

3. On four real coding tasks it cut Opus 5.5 costs by up to 42% against xhigh (21% against medium, 29% against high), with 12 of 12 answers still right.

4. Why it saves: every request rereads the whole chat, and at a lower effort the model makes fewer requests.

5. Setup takes a minute: paste the link into Claude Code, or type /plugin marketplace add HeyCubit/effortless and then /plugin install effortless@effortless.

The catch: that was four mostly easy tasks, so the savings are smaller on hard work.

Save this one for later.

Comment “SAVE” for the link.

#claudeai #claudecode #claude #claudetips

## Research

* Verdict: Partly valid. The repo exists and matches the post's install steps and benchmark numbers. The 42% saving is the best case: it compares against xhigh effort, uses only four mostly easy tasks, and ran on fresh API chats. The README says this itself.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [HeyCubit/effortless (github.com)](https://github.com/HeyCubit/effortless): repo, in the post, verified, high confidence. README describes a free MIT Claude Code plugin whose Haiku 5.5 judge picks the effort level, with the same install commands and the 21/29/42% savings and 12/12 correct answers.

### Key steps

1. In Claude Code, run: /plugin marketplace add HeyCubit/effortless
2. Run: /plugin install effortless@effortless
3. Run /reload-plugins or restart Claude Code
4. Complete the short setup that appears above the prompt. The default judge uses your Claude login, so no API key is needed.
5. Read the hooks/ folder before installing, because the mod runs code on your machine.
6. Optional: add TypeSafe's Jev as a faster judge.
7. Optional: the experimental cheaper-model routing switch is off by default.

### Not found

The comment-for-DM link isn't needed. The repo is public, and the post's own text gives the name HeyCubit/effortless.
