---
shortcode: "Deb3ZCdgFjW"
url: "https://instagram.com/reel/Deb3ZCdgFjW/"
type: "Reel"
author: "realrileybrown"
shared: "Oct 13, 2026, 09:37 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Giving Claude Code a phone number

A creator uses Claude Code to call him by phone and request landing page changes, then shows the Bland API setup that gives Claude Code a phone number. The video also shows a daily 9 a.m. automation that calls if a tool check fails.

Written by claude-haiku-5-5.

## What it teaches

1. Have a Claude Code subscription and a Bland API key.
2. Paste a prompt into Claude Code with your phone number and Bland API key.
3. Wait about 30 seconds; Claude Code calls you to test that the setup works.
4. Let Claude Code set up a skill so it can call any number on command.
5. Optionally, create an automation, such as a daily 9 a.m. check of your tools (GitHub, Slack, Linear, email) that calls you if something goes wrong.

## Source

* How to get it: Comment "Phone" on the post to receive the full guide and skill

## Caption

Comment "Phone" if you want to give Claude Code a phone.

You can set this up in about five minutes with a Bland API key. Your agent can call you when it needs a decision, then keep working with your answer. I’ll send you the full guide and the skill so you can try it yourself.

## Research

* Verdict: Partly valid. The idea works: Bland's API can place outbound calls, and public Claude Code skills already do this. The creator's own guide and skill are only sent after a comment ("Phone"), so I found no public copy.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Bland phone-calls skill (Sundial awesome skills) (openskillindex.com)](https://openskillindex.com/skills/sundial-org-awesome-openclaw-skills-phone-calls): tool, found by search, not opened, medium confidence. The search snippet describes a skill that takes a phone number and a task and uses Bland AI with BLAND_API_KEY to place the call. This is similar to the post's setup but is not the creator's own skill. I did not open the page.
* [Bland CLI skill (dvcrn) (skillsdirectory.com)](https://www.skillsdirectory.com/skills/dvcrn-bland): tool, found by search, not opened, low confidence. The search snippet says it wraps the Bland API for placing calls and fetching transcripts. It is an alternative and I did not open the page.

### Key steps

1. Get a Bland API key from bland.ai and add credit, since calls cost money.
2. Give Claude Code your phone number in E.164 format (for example +1...) and the Bland API key, as the post's prompt does.
3. Ask Claude Code to make a test call to you and wait about 30 seconds.
4. Ask it to save a skill that calls any number on command, using a skill file in ~/.claude/skills/.
5. Optionally add a scheduled daily 9am check of GitHub, Slack, Linear and email that calls you if a check fails.

### Not found

The creator's exact guide and skill, which are sent only after commenting "Phone". I did not open any of the third-party skill pages, and I did not check Bland pricing.
