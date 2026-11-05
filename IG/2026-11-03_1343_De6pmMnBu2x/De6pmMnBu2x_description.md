---
shortcode: "De6pmMnBu2x"
url: "https://instagram.com/reel/De6pmMnBu2x/"
type: "Reel"
author: "pragmaticcoder.ai"
shared: "Nov 03, 2026, 01:43 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# MCP Problems and Code Mode Explained

A short explainer contrasting direct MCP tool calling with "Code Mode," where the AI writes one script that runs in a sandbox and returns only the result. It uses Cloudflare's MCP server and token counts as examples.

Written by claude-haiku-5-5.

## What it teaches

1. Let the AI write one script that covers the whole task, instead of making a separate tool call for each step.
2. Run that script once in a sandbox so all the individual calls happen inside it.
3. Send only the final answer back into the AI's context, not every intermediate result.
4. Cloudflare's example: expose a small MCP server with just two tools, search and execute, which the post says cost about 1,000 tokens.

## Source

* How to get it: comment CODE, setup sent by DM

## Caption

RIP MCP? Cloudflare says we’ve all been using it wrong. Here’s why 🤯

Cloudflare, Anthropic and Block now let the AI write code instead of calling tools one by one. The code runs once, in a sandbox, and only the answer comes back. It’s called Code Mode.

The problem with MCP as we know it:
01 · Every tool’s manual loads into the AI’s memory before it does anything (5 apps ≈ 55,000 tokens)
02 · Cloudflare’s 2,500+ endpoints would take 1.17 million tokens as MCP tools
03 · Every single step goes back through the AI

Why Code Mode works:
04 · The AI writes one script, not 40 separate tool calls
05 · All the calls happen inside the sandbox; only the answer lands in its memory
06 · AI grew up reading code, not tool calls

Cloudflare’s own MCP server is now just 2 tools, search and execute: about 1,000 tokens.

MCP isn’t dead. Direct tool calling is.

💬 Comment CODE and I’ll DM you the setup
➡️ Send this to the friend who still wires 40 tools into one agent
📌 Save it for your next agent build

Sources: Cloudflare blog (Sep 26, 2025 · Feb 20, 2026) · Anthropic (Nov 4 & Nov 24, 2025) · goose (Dec 15, 2025)

#AIagents #MCP #ClaudeAI #Cloudflare #AItools
