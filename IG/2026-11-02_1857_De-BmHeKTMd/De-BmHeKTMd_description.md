---
shortcode: "De-BmHeKTMd"
url: "https://instagram.com/reel/De-BmHeKTMd/"
type: "Reel"
author: "j.t.rivard"
shared: "Nov 02, 2026, 06:57 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Running REA via Pi harness on OpenRouter

The creator says Claude Code began blocking people who use the REA reverse-engineering engine, so they ran it through the Pi harness with DeepSeek Flash V4.1 on OpenRouter for 37 cents. The run reverse-engineered a $50 PDF open-and-edit app.

Written by claude-haiku-5-5.

## What it teaches

1. Use a different harness than Claude Code, such as the Pi harness.
2. Go to openrouter.com and get an API key.
3. Use the key to run other models, such as DeepSeek Flash V4.1, with the harness.

## Source

* Link: openrouter.com
* How to get it: The full step-by-step setup is sent by DM after commenting GUIDE (the post asks viewers to follow first).

## Caption

Comment GUIDE and I’ll DM you the step-by-step setup. Follow first so I can send it.

Claude Code started blocking people trying to use REA, the Reverse Engineer Anything engine that blew up on GitHub. So I ran it from the Pi harness instead, on OpenRouter with DeepSeek Flash V4.1. It cost me 37 cents, and it reverse engineered a $50 app for opening and editing PDFs.

Who would pay $50 for that?

#claudecode #reverseengineering #openrouter #deepseek #aiagents

## Research

* Verdict: Partly valid. REA and the Pi harness are real, and Pi supports OpenRouter, so the workaround is plausible. But there is no confirmed targeted Claude Code ban on REA, only user reports of false-positive cyber blocks. The guide is DM-only, and I didn't verify the 37-cent cost or the DeepSeek model name.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [REA (Reverse Engineer Anything) (github.com)](https://github.com/morluto/rea): repo, found by search, verified, high confidence. Opened the repo. It is an MIT-licensed MCP server and CLI for agent-driven reverse engineering, with about 450k stars.
* [Pi coding agent (pi-mono) (pi.dev)](https://pi.dev): tool, found by search, not opened, medium confidence. Search results describe Pi as a minimal terminal coding harness by Mario Zechner. Its README lists OpenRouter as a provider. I did not open the page.
* [OpenRouter (openrouter.ai)](https://openrouter.ai): product, in the post, not opened, medium confidence. The post names openrouter.com for getting an API key. I did not open it.
* [Is Claude Blocking Reverse Engineering, or Is This a Misunderstanding? (pbxscience.com)](https://pbxscience.com/?p=24564): page, found by search, not opened, medium confidence. Search summary says there is no confirmed targeted ban, only broad cyber safeguards that cause some false positives.

### Already in the vault

* Vault: `ZAIHub/claude - SkillSpector scan of REA skill 2026-10-11.md`: Scan of the REA skill (rea-agents 6.4.0); links to a vault repo note on REA.
* Vault: `ZAIHub/Testing SLM models on the PI v3.md`: Mentions Pi. I did not read it, so it may be about a Raspberry Pi instead.

### Already in IG saves

* Similar: Web: [Run Claude Code for free with a local proxy (instagram.com)](https://instagram.com/p/DXmWHzIExeq/) (`DXmWHzIExeq`). Runs Claude Code through a proxy to other model backends, including OpenRouter, as a workaround.

### Key steps

1. Install REA: run `npx rea-agents setup` (needs Node 22+), choose your agents, approve the changes, then restart the agent.
2. Install the Pi harness with npm (package @earendil-works/pi-coding-agent, formerly @mariozechner/pi-coding-agent).
3. Create an OpenRouter API key at openrouter.ai and give it to Pi as the OpenRouter provider key.
4. Pick a DeepSeek model on OpenRouter and run REA from Pi against the target app.

### Not found

The creator's DM guide is not public. I did not open the Pi or OpenRouter pages, so I have no exact Pi-with-OpenRouter setup commands. I could not verify the "DeepSeek Flash V4.1" model name or the 37-cent cost.
