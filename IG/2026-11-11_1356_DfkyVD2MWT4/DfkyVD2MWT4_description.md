---
shortcode: "DfkyVD2MWT4"
url: "https://instagram.com/reel/DfkyVD2MWT4/"
type: "Reel"
author: "sheni_icg"
shared: "Nov 11, 2026, 01:56 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-11"
---

# Five Claude Code refactor tips with Fable

A creator walks through five ways to clean up a Claude Code setup using the Fable 5.2 model, covering skills, conflicting instructions, hard rules and large task prompts. The prompt he used is offered to viewers who comment for it.

Written by claude-haiku-5-5.

## What it teaches

1. Refactor the whole codebase so skills and rules are split by department and loaded only when needed, using progressive disclosure: always-loaded files like CLAUDE.md, files loaded when a folder is opened, and content found by search.
2. Run /insights to get a report on the last three months of conversations, showing what is going wrong and suggesting CLAUDE.md additions, new skills, hooks and features. Feed the full report back to Claude, do the recommended changes, then work through the 'horizon' items in a second pass.
3. Audit conflicting files, since a refactor exposes differences between CLAUDE.md, skills and notes, so you settle on one set of instructions.
4. Loosen hard rules. Many strict rules inside skills signal weak spots, so look for better tools or repos or better ways to explain the task. Rules in CLAUDE.md that conflict should be fixed.
5. Give Fable one large task written as user stories that describe the experience and end result in detail, without telling it how to do the work.

## Source

* How to get it: Comment "FABLE" to receive the prompt

## Caption

Comment “FABLE” for the prompt I used to do this

## Research

* Verdict: Partly valid. The tips are sound general Claude Code practice, and /insights is a real command. The creator's exact prompt is only sent to people who comment "FABLE", and I found no public copy. I did not check the "Fable 5.2" model or the "better than 99%" and speed claims.
* Checked: 2026-11-11 by claude-sonnet-5-5

### Resources

* [Claude Code /insights: Your Personalized AI Usage Report (blog.vincentqiao.com)](https://blog.vincentqiao.com/en/posts/claude-code-insights/): guide, found by search, not opened, medium confidence. The search result describes /insights as a built-in command that generates a usage report with CLAUDE.md suggestions. I did not open the page. Other sources give a 30-day window, not the post's three months.

### Key steps

1. Run /insights in Claude Code to generate the usage report.
2. Give the whole report back to Claude and have it apply the recommended CLAUDE.md additions, skills and hooks.
3. Do a second pass on the 'horizon' items.
4. Split skills and rules into department folders so they load only when needed. Keep only essentials in CLAUDE.md.
5. Ask Claude to audit CLAUDE.md, skills and notes for conflicting instructions, then settle on one answer for each.
6. Count the hard rules (words like 'always' and 'never'). Where they cluster in skills, look for better tools or a clearer task description. Fix any in CLAUDE.md.
7. For big tasks, write user stories describing the end result in detail and leave out how to do the work.

### Not found

The creator's "FABLE" prompt is only sent after a comment, and I found no public copy. I did not verify the "Fable 5.2" model or the claimed speedup (90 seconds down to 30). I did not open the /insights guide. The post names hyperframes as a repo, but I did not look for it.
