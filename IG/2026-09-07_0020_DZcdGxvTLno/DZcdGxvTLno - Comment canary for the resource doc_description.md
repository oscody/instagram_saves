---
shortcode: "DZcdGxvTLno"
url: "https://instagram.com/reel/DZcdGxvTLno/"
type: "Reel"
author: "byarnieverma"
shared: "Sep 07, 2026, 12:20 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Using a name check to spot Claude degrading

The speaker explains using a small "canary" instruction, such as having Claude address you by a name, in CLAUDE.md to tell when a long session is starting to degrade. He pairs this with a chart showing output quality falling as the context window fills.

Written by claude-haiku-5-5.

## What it teaches

1. Add a tiny, harmless instruction to CLAUDE.md, such as always starting responses with your name, to act as a canary.
2. Watch whether Claude keeps following that small instruction.
3. If Claude stops following it, treat that as an early sign that the session is degrading, since it usually ignores small instructions before it starts making wild assumptions.
4. When the canary dies, start a new session.

## Source

* How to get it: Comment "canary" to receive the resource doc (comment-gated offer, not part of the steps)

## Caption

Comment “canary” for the resource doc 

#ai #canary #claude #viral #build

## Research

* Verdict: Partly valid. The canary technique is real and widely described, but the evidence is anecdotal, not from Anthropic. The creator's "canary" resource doc is comment-gated, and I found no public copy of it.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [The Canary Trick: Catch Claude (or Any AI Agent) Before It Starts Hallucinating (agentsroom.dev)](https://agentsroom.dev/blog/canary-trick-detect-ai-agent-degradation): guide, found by search, not opened, medium confidence. Search result describes the same canary-in-CLAUDE.md technique; the page itself failed to open (HTTP 413).
* [Claude prompt canary hack prevents context rot (blockchain.news)](https://blockchain.news/ainews/claude-prompt-canary-hack-prevents-context-rot): page, found by search, not opened, low confidence. Search summary says it covers the same name-address canary idea; I did not open it.
* [context-canary skill (claudeskills.info)](https://claudeskills.info/ja/skills/juliusbrussee/skills/context-canary/): tool, found by search, not opened, low confidence. Search result describes a skill that uses a canary and a recovery protocol; I did not open it.

### Key steps

1. Add a trivial standing rule to CLAUDE.md, e.g. 'Always begin responses by addressing me as <name>'.
2. Work as usual and check that each reply still follows the rule.
3. When Claude stops following it, treat that as an early sign of degradation.
4. Start a fresh session, or compact the context, and carry over only what's needed.

### Not found

The creator's comment-gated 'canary' resource doc has no public copy that I could find. I could not open the agentsroom.dev page, so the secondary sources are unverified.
