---
shortcode: "DalUVOBjD00"
url: "https://instagram.com/p/DalUVOBjD00/"
type: "Carousel"
author: "theaifield"
shared: "Jul 10, 2026, 02:53 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Claude's Image Token Pricing Loophole: pxpipe

The carousel describes pxpipe, an open-source local proxy that renders bulky Claude context as PNG images to cut token costs, citing a 59-70% lower bill in Claude Code sessions. It also warns that the image compression is lossy and can silently corrupt exact details like hex strings.

Written by claude-haiku-5-5.

## What it teaches

1. Claude prices image input by pixel dimensions, not by how much readable text the image contains.
2. Dense text such as code, JSON, or tool output can be packed into a fixed-size image at roughly 3.1 characters per image token, versus about 1 character per text token.
3. pxpipe runs locally and rewrites bulky parts of each request (older context, system prompt, tool docs, history) into compact PNGs before the request reaches Anthropic's servers.
4. To judge real savings, compare each request's token count against a free count_tokens counterfactual, logged in ~/.pxpipe/events.jsonl, since prices change and workloads differ.
5. Do not rely on image-rendered context for IDs, hashes, secrets, or anything needing perfect recall, because the compression is lossy and errors can happen silently (one test: Fable 5 recalled 12-character hex strings 13 of 15 times, Opus 0 of 15).

## Source

* Link: teamchong/pxpipe

## Caption

Claude May Have a Strange Pricing Loophole

A developer created an open-source proxy called pxpipe that claims it can dramatically reduce Claude API costs by converting large text-heavy context into PNG images.

The trick comes from how image tokens are priced. Instead of charging based on how much readable text is inside the image, the cost depends on pixel size. According to the project, one dense 1928×1928 image can fit around 92,000 characters while costing roughly 4,761 vision tokens.

That creates an unusual workaround. In one production example, pxpipe says the bill dropped from $100 to about $41 by turning older context, tool documentation, and system prompts into images before sending them to Claude.

But there is a major tradeoff: accuracy.

The compression is lossy, and mistakes can happen silently. In one dense-render test, Fable 5 correctly recalled exact 12-character hex strings in 13 out of 15 attempts, while Opus failed all 15.

So pxpipe could be useful for bulky background context, but it is risky for IDs, hashes, secrets, or anything that requires perfect recall.

Would you trust this for real coding work?

Source: GitHub, teamchong/pxpipe

➡️ Want to stay ahead in the world of AI? Grab your coffee, relax, and let our newsletter deliver the biggest updates straight to your inbox.

## On screen text

SOMEONE DISCOVERED
HOW TO CUT CLAUDEAI
COSTS BY 70% AND ITS
EMBARRASSINGLY SIMPLE
SWIPE
@digimaga
in Fable5 lololol
not the amountof textinthe mage
N
2
For details
U
57 wer cndtend
.
O.
Anthropic's servers.
pxpipe
fraction of the tokens.
SHARE
EEVERV
W
HAPPENING
NTHE
WORLDFAI
