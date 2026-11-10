---
shortcode: "DfFB8PUv-ch"
url: "https://instagram.com/reel/DfFB8PUv-ch/"
type: "Reel"
author: "raycfu"
shared: "Oct 29, 2026, 05:31 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-30"
---

# Adding Jev to an AI agent: three steps

The post shows how to bring Jev, a fast decision model from TypeSafe, into an AI agent so that small decisions and command-safety checks no longer go to a large, expensive model. On-screen examples show routing a request to the fast model and asking Jev whether a curl-to-shell command is risky.

Written by claude-haiku-5-5.

## What it teaches

1. Step 1: Get an API key from TypeSafe, then tell the agent to send its small decision questions (such as whether a task is urgent or which model to use next) to Jev, which returns answers with a probability.
2. Step 2: Add a model router, for example with LangChain, that has two choices. Send direct lookup, extraction and small changes to the fast model. Send architecture and high-stakes decisions to the powerful model.
3. Step 2: Give the router the instruction to choose the least costly model that can complete the task, so only the requests that need it reach the big model.
4. Step 3: Add a safety guard by setting up auto-mode middleware and listing the tools to watch, such as the bash tool that runs terminal commands.
5. Step 3: Before the agent runs a command, have Jev check whether it is risky and block it if so.

## Source

* How to get it: The post says to comment "JET" to receive a detailed step-by-step guide

## Caption

How to build an agent harness with jev #ai #tech

## Research

* Verdict: Partly valid. Jev is real and works as the post describes (fast typed yes/no, choice and score answers with probabilities, very low price). The "400x cheaper" figure isn't on TypeSafe's docs page, and the detailed guide is only sent after a "JET" comment.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [TypeSafe Jev docs (models/API) (docs.typesafe.ai)](https://docs.typesafe.ai/models): page, in the vault, verified, high confidence. Opened it. It describes Jev as TypeSafe's System One model, called via POST api.typesafe.ai/v1/systemone with a Bearer key, at $0.042 per Mtok input and free output.
* [Jev on OpenRouter (openrouter.ai)](https://openrouter.ai/docs/guides/community/jev): guide, found by search, not opened, medium confidence. Search result says Jev is available through OpenRouter as typesafe/jev-1.13 or ~typesafe/jev-latest. I did not open the page.
* [AI/ML API Jev reference (docs.aimlapi.com)](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev): page, found by search, not opened, medium confidence. Search result lists a /v1/decisions endpoint with model typesafe/jev. I did not open the page.

### Already in the vault

* Vault: `ZAIHub/Jarvis_Custom_Instructions_Prompts.md`: Jev setup: TypeSafe, OpenRouter and Vercel access, the Claude Code plugin (typesafe-ai/skills), the jev-mcp-server MCP command, a note that signups were paused Sept 22, and a boss/worker pattern.
* Vault: `ZAIHub/search - claudex-loop - similar ai agent workflows.md`: Lists raycfu as the creator. Only a weak match for this post.

### Already in IG saves

* Similar: Web: [Effortless: Claude Code mod that picks effort level (instagram.com)](https://instagram.com/p/Debf2CdhWCE/) (`Debf2CdhWCE`). Effortless mod that uses a cheap model as the router for effort levels. Its step 6 also suggests Jev as a faster judge.

### Key steps

1. Get a Jev key from TypeSafe (console.typesafe.ai) or through OpenRouter. The vault note says TypeSafe signups were paused on Sept 22, so OpenRouter may be the only route.
2. Call POST https://api.typesafe.ai/v1/systemone with a Bearer key. Set model to jev-latest and send state plus a questions list (yes/no, choice or score).
3. Move small decisions to Jev, such as urgency or which model to use next. Read the returned probability.
4. Add a LangChain router with a fast model (lookup, extraction, small edits) and a strong model (architecture, high-stakes calls). Tell it to pick the cheapest model that can do the task.
5. Add middleware on risky tools such as bash. Before each command, ask Jev 'Is this command risky?' and block it above a confidence threshold.
6. Optional for Claude Code: claude plugin marketplace add typesafe-ai/skills, then claude plugin install typesafe@typesafe-ai.

### Not found

The creator's "JET" step-by-step guide is sent only after a comment or DM and I found no public copy. I could not confirm the "400x cheaper" claim from TypeSafe. I did not find the "auto-mode middleware" naming in any public docs.
