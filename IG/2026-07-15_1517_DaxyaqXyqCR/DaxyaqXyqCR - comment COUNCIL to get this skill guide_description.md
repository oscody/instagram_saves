---
shortcode: "DaxyaqXyqCR"
url: "https://instagram.com/reel/DaxyaqXyqCR/"
type: "Reel"
author: "felixleezd"
shared: "Jul 15, 2026, 03:17 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# The LLM Council: five-advisor prompt for Claude

A creator describes a multi-advisor setup, based on a multi-model "LLM Council," that runs five perspectives and a chairman's verdict inside a single Claude chat to test a decision. The full prompt is only sent by comment.

Written by claude-haiku-5-5.

## What it teaches

1. Ask Claude a real decision question.
2. Have five advisors answer it from different angles: a contrarian who focuses on what could go wrong, a first-principles thinker who breaks down your assumptions, an expansionist who looks for upside you may be missing, an outsider who knows nothing about your industry, and an executor who focuses on what you would actually do on Monday morning.
3. Have each advisor review the others' answers without knowing who wrote which one.
4. Have a chairman review everything and give one final verdict and the next step.

## Source

* How to get it: Comment "COUNCIL" to get the prompt, which is sent by comment.

## Caption

comment “COUNCIL” to get this skill guide. 

Claude will gaslight you, until you install this skill.

It’s called The LLM Council.

You ask a question. 5 advisors attack it from different angles. Then they peer-review each other before giving you the verdict.

How it works:

1. You ask a real decision question.
2. 5 advisors attack it from different angles.
3. They grade each other’s work anonymously.
4. Chairman synthesises one verdict and the next step.

Go try it today, it’s brilliant!

#claudeai #figma #vibecoding #ai #cursor

## Research

* Verdict: Valid. Public Claude skills implement exactly this five-advisor, anonymous peer-review and chairman design, so the comment-only prompt isn't needed. The creator's own prompt wasn't seen, and the "Claude will gaslight you" line is just hype for sycophancy.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [tenfoldmarc/llm-council-skill (github.com)](https://github.com/tenfoldmarc/llm-council-skill): repo, found by search, verified, medium confidence. Repo has the same five advisors (Contrarian, First Principles, Expansionist, Outsider, Executor), anonymous peer review and a chairman verdict with a next step. It isn't confirmed as the creator's exact source.
* [karpathy/llm-council (github.com)](https://github.com/karpathy/llm-council): repo, in the vault, not opened, medium confidence. Original multi-model LLM Council that the post's setup is based on. It is listed in the vault note 'follow - karpathy', and I did not open it.
* [LLM Council single-chat prompt (Mika Reyes) (mikareyes.com)](https://mikareyes.com/ai/how-to-run-llm-council-in-claude.md): guide, found by search, not opened, low confidence. Search result describes a copy-paste single-chat version of the same idea. I did not open it.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/follow - karpathy.md`: Link to karpathy/llm-council, the original multi-model version.

### Key steps

1. Install the skill: git clone https://github.com/tenfoldmarc/llm-council-skill ~/.claude/skills/llm-council, then start Claude Code with `claude`. You can instead put SKILL.md in ~/.claude/skills/llm-council/ and restart.
2. Trigger it with a phrase plus your question: "council this", "run the council", "pressure-test this", "stress-test this", "war room this" or "debate this".
3. Give plenty of context about the decision, because richer input gives sharper output.
4. Five advisors answer in parallel: Contrarian, First Principles, Expansionist, Outsider and Executor.
5. Their answers are anonymized and each advisor reviews the others.
6. The chairman gives agreements, clashes, blind spots, a recommendation and one next step. The skill also writes an HTML report and a markdown transcript. A run takes about 4 minutes.

### Not found

The creator's exact prompt, which is only sent by comment on "COUNCIL". I found no public copy of it.
