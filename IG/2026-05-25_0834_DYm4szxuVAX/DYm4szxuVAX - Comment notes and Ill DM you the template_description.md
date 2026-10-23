---
shortcode: "DYm4szxuVAX"
url: "https://instagram.com/reel/DYm4szxuVAX/"
type: "Reel"
author: "keshavsuki"
shared: "May 25, 2026, 08:34 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Claude Code prompt: running implementation-notes HTML log

A reel describing a Claude Code prompt attributed to an Anthropic engineer: have Claude keep a running implementation-notes.html file of every decision it made beyond the spec. The creator argues this turns the model into an engineer who explains its choices and gives an audit trail against vibe coding.

Written by claude-haiku-5-5.

## What it teaches

1. Give Claude your spec and tell it to implement it while keeping a running implementation-notes.html file.
2. Have Claude log every decision it had to make that the spec did not cover, along with its reasoning.
3. Use HTML rather than markdown for the notes so they open in any browser with headers, links, collapsible sections and embedded screenshots.
4. Treat the decision log as the documentation and the audit trail, so you can review what the model decided and avoid vibe coding.

## Source

* How to get it: Comment "notes" on the post to get the template (sent by DM)

## Caption

Comment “notes” and I’ll DM you the template👇

The engineer behind Claude Code just posted a single prompt that replaced two of my custom commands.

His name is Thariq Shihipar. He works on Claude Code at Anthropic. The prompt: tell Claude to implement your spec, and while it does, keep a running implementation-notes.html file with every decision it had to make that wasn’t in the spec.

That one line turns Claude from a code generator into an engineer who explains himself.

Here’s why it works:

The HTML file becomes the agent’s working memory. Every time Claude hits a fork the spec didn’t cover, the choice goes into the file with the reasoning. The decision log IS the documentation.

HTML, not markdown. Thariq also posted that HTML continues to be undefeated. Open the file in any browser — you get headers, links, collapsible sections, embedded screenshots. The lightest possible CMS for one agent’s brain.

The non-obvious part: this is how you escape vibe coding. Vibe coding fails because you can’t audit what the model decided. A running implementation notes file is the audit trail.

I rebuilt three prompts in my own setup this morning. Replaced two custom Claude commands.

Comment “notes” for the template plus the three places to plug it in 👇

## Research

* Verdict: Valid. Thariq Shihipar did post this prompt on X in May 2026, and it is short and public, so the DM template isn't needed. The reel's claims about replacing commands and escaping vibe coding are the creator's opinion.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Thariq (@trq212) original X post (x.com)](https://x.com/trq212/status/2056415973125796184): page, found by search, not opened, medium confidence. The link comes from the abmedia article, which says it is Thariq's prompt post. I did not open it on X.
* [abmedia: Thariq's implementation-notes prompt (abmedia.io)](https://abmedia.io/thariq-anthropic-claude-code-prompt-implementation-notes-may-2026): page, found by search, verified, high confidence. I opened it. It quotes the prompt 'implement <SPEC> and while you do, keep a running implementation-notes.html file (or markdown)' and lists the kinds of notes to keep.
* [mer.vin: implementation notes prompt template (mer.vin)](https://mer.vin/2026/05/implementation-notes-prompt-track-agent-decisions-whilst-shipping-a-spec/): guide, found by search, verified, medium confidence. I opened it. It is a third-party tightened version of the prompt with its own suggested sections, not Thariq's text.

### Key steps

1. Paste this prompt: "implement <SPEC> and while you do, keep a running implementation-notes.html file (or markdown)".
2. Ask it to record decisions the spec didn't cover, changes it made to the spec, tradeoffs it accepted, and anything else you should know.
3. Optional structure from mer.vin, not Thariq's: Assumptions, Spec deltas, Trade-offs, Risks and follow-ups.
4. When it finishes, open the HTML file in a browser and review the decisions.

### Not found

I could not open the original X post. The exact full wording comes only from the abmedia quote, and the DM template was not checked.
