---
shortcode: "DaojVuSNKno"
url: "https://instagram.com/reel/DaojVuSNKno/"
type: "Reel"
author: "cooper.simson"
shared: "Sep 18, 2026, 06:32 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Fable 5 orchestrates GPT-5.6 with a /route loop

The reel shows a /route loop in Claude Code where Fable 5 plans and reviews while GPT-5.6 builds and fixes, repeating until Fable approves. The setup prompts are not shown and are offered by comment.

Written by claude-haiku-5-5.

## What it teaches

1. Make sure you have an OpenAI account and install Codex.
2. Install the Codex plugin for Claude Code from GitHub.
3. Use the provided prompt to make sure Fable can call GPT-5.6.
4. Give the second prompt to Claude so it builds a /route skill that uses Fable as orchestrator and GPT-5.6 as worker.
5. Type /route. Fable 5 interviews you and builds the plan.
6. GPT-5.6 builds the project, Fable 5 reviews it, and the work goes back to GPT-5.6 until Fable approves.

## Source

* How to get it: Comment ROUTE on the post; the full from-scratch setup and exact prompts are sent by the account

## Caption

You can run the new OpenAI GPT 5.6 inside Claude code with Fable 5 to get 10 times the work done while saving on your usage limit.

Comment ROUTE and I’ll send you the exact from-scratch setup.

#fable5 #gpt5.6 #claude #chatgpt #teamwork

## Research

* Verdict: Partly valid. The plugin the reel relies on is real and public (openai/codex-plugin-cc), so a Claude-plans, Codex-builds loop is feasible. The /route prompts are comment-gated with no public copy, and the "10x work" and usage-savings claims are unproven.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [openai/codex-plugin-cc (github.com)](https://github.com/openai/codex-plugin-cc): repo, found by search, verified, medium confidence. The README matches the reel's "install Codex plugin for Claude Code from GitHub" step. The reel never names the repo, so the link is inferred.
* [Fable 5 /route reel (instagram.com)](https://instagram.com/reel/DaojVuSNKno/): other, in the vault, not opened, high confidence. This is the source post. Its setup prompts are sent only by comment (ROUTE).

### Already in the vault

* Vault: `ZAIHub/search - claudex-loop - similar ai agent workflows.md`: Lists this reel as a comment-gated lead with no public repo. Compares it with claudex-loop, a public plan/build/cross-review loop.

### Key steps

1. Have a ChatGPT subscription (the free tier works) or an OpenAI API key, and Node.js 18.18 or later.
2. In Claude Code run: /plugin marketplace add openai/codex-plugin-cc
3. Run: /plugin install codex@openai-codex
4. Run: /reload-plugins
5. Run: /codex:setup. If Codex is missing, install it with npm install -g @openai/codex, then run !codex login.
6. Check that the /codex:* commands and the codex:codex-rescue subagent show up in /agents.
7. Ask Claude to write a /route skill: the orchestrator model interviews you and plans, Codex builds, the orchestrator reviews, and the work loops until it approves. The author's exact prompts are comment-gated, so write your own.
8. Use /codex:review, /codex:rescue, /codex:status and /codex:result for the review and fix steps.

### Not found

The author's exact /route prompts and the from-scratch guide, which are sent only by comment. I found no public copy. I also did not check that GPT-5.6 or "Fable 5" can be selected through the plugin, or the "10x work" and usage-savings claims.
