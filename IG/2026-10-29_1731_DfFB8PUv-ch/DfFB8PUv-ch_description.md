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
