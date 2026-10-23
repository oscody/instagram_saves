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

## Research

* Verdict: Partly valid. The pxpipe repo exists and matches the post's claims about savings, how it works and the caveats. The post's "Opus 0 of 15" is slightly off: the README lists Opus 5 at 2/15 and the older Opus 4.8 at 0/15. The savings figures are the project's own and depend on workload.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [teamchong/pxpipe (github.com)](https://github.com/teamchong/pxpipe): repo, in the post, verified, high confidence. The README describes a local Claude Code proxy that renders old context as PNGs, with ~59–70% savings, ~3.1 chars per token, and the events.jsonl and count_tokens logging.

### Key steps

1. Run `npx pxpipe-proxy`. It listens on 127.0.0.1:47821.
2. Start Claude Code with `ANTHROPIC_BASE_URL=http://127.0.0.1:47821 claude`. Alternatively run `pxpipe warp -- claude`.
3. Open the dashboard at the same local address to see savings and conversions.
4. Run `pxpipe stats` to summarize ~/.pxpipe/events.jsonl. It compares billed usage with a free count_tokens counterfactual.
5. Keep IDs, hashes and secrets as plain text, because image rendering can silently swap characters.
6. Use `npx pxpipe-proxy export` to render files or diffs to PNG pages without running the proxy.

### Not found

I did not check the savings numbers independently. They come from the project's own traces.
