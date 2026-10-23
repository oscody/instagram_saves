---
shortcode: "Dcw_ZgYSHuP"
url: "https://instagram.com/reel/Dcw_ZgYSHuP/"
type: "Reel"
author: "felixleezd"
shared: "Sep 03, 2026, 08:17 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# The LLM Council: five advisors and a chairman

A creator presents "The LLM Council," a way to get a Claude chat to answer a decision question from five advisor perspectives, have them review each other anonymously, and end with a chairman's verdict and next step. The post invites viewers to comment "STANFORD" to get the prompt.

Written by claude-haiku-5-5.

## What it teaches

1. Start with a real decision question you are facing.
2. Ask the chat to answer from five advisor perspectives: a contrarian who looks at what will fail, a first-principles thinker who challenges your assumptions, an expansionist who finds upside you are missing, an outsider who knows nothing about your industry, and an executor who focuses on what you actually do on Monday morning.
3. Have each advisor review the others' answers without knowing who wrote which one.
4. A chairman reviews everything and gives one final verdict and the next step.

## Source

* How to get it: Comment "STANFORD" on the post to get the skill guide (the post says the prompt is sent after commenting)

## Caption

comment “STANFORD” to get this skill guide.

Claude will gaslight you, until you install this skill.

It’s called The LLM Council. 🧠

You ask a question. 5 advisors attack it from different angles. Then they peer-review each other before giving you the verdict.

How it works:

1. You ask a real decision question.
2. 5 advisors attack it from different angles.
3. They grade each other’s work anonymously.
4. Chairman synthesises one verdict and the next step.

Go try it today, it’s genius!

#claudeai #figma #vibecoding #ai #cursor

## Research

* Verdict: Valid. The "LLM Council" is a real, public Claude skill with the same five advisors, anonymous peer review and chairman. The creator's exact guide is gated behind a comment, but a public copy exists. The Stanford claim about AI agreeing too much was not verified.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [tenfoldmarc/llm-council-skill (github.com)](https://github.com/tenfoldmarc/llm-council-skill): repo, found by search, verified, medium confidence. Opened it. It is a Claude Code skill with the same five advisors, anonymous peer review and chairman verdict as the post. I can't confirm it is the creator's exact guide.
* [automatorsplus/llm-council-skill (github.com)](https://github.com/automatorsplus/llm-council-skill): repo, found by search, not opened, low confidence. Appeared in search results as another packaging of the same idea. I did not open it.

### Key steps

1. Install: git clone the repo into ~/.claude/skills/llm-council, or create that folder and put SKILL.md in it, then restart Claude Code.
2. Run `claude` in Terminal.
3. Start your question with a trigger phrase such as 'council this', 'run the council', 'pressure-test this' or 'war room this'. Add plenty of context.
4. The skill scans your workspace (CLAUDE.md, memory files) and frames a neutral version of the question.
5. It runs five advisors in parallel: Contrarian, First Principles, Expansionist, Outsider, Executor.
6. It anonymizes their answers and has them peer-review each other.
7. The chairman gives the points of agreement and conflict, blind spots, a recommendation and one next step.
8. You also get an HTML report and a markdown transcript. A run takes about 4 minutes.

### Not found

The creator's own 'STANFORD' guide is sent only after a comment, and I found no public copy of it. The Stanford study the projects cite was not verified. The vault has no note on this post. One vault note, 'Openclaw hub skills', lists a different 'LLM Council' skill for multi-CLI planning.
