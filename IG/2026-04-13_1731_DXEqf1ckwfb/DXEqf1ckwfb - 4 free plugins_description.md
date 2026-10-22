---
shortcode: "DXEqf1ckwfb"
url: "https://instagram.com/reel/DXEqf1ckwfb/"
type: "Reel"
author: "softgirlnocode"
shared: "Apr 13, 2026, 05:31 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Four free Claude Code plugins to save tokens

A reel of a woman at a laptop saying "Hi Claude," then hitting a "rate limit, please try again later" message, with an on-screen title "How I hacked Claude's rate limit." The caption lists four plugins said to reduce Claude Code token use and suggests switching to OpenAI Codex.

Written by claude-haiku-5-5.

## What it teaches

1. Install claude-mem so Claude Code keeps persistent memory and doesn't need the whole history or files every session, especially on ongoing projects.
2. Use the Context Manager plugin for rolling conversation compression: summarize older turns and keep recent ones verbatim in long coding chats.
3. Index your repo with Claude Context so Claude pulls only the specific functions or snippets it needs instead of whole files.
4. Turn long, reusable prompts (SEO systems, refactor recipes, content frameworks) into short commands or tasks with Superpowers-style plugins.

## Source

* How to get it: Comment "hack" to receive the links to all the plugins (the post says the links are sent after commenting)

## Caption

(4 free plugins) ⬇️
claude-mem (persistent memory)
Gives Claude Code persistent memory so it doesn’t need your whole history or files every session; used well on ongoing projects, it can realistically cut “rehashing context” input tokens by around 80–90% for you. 

The Context Manager plugin 
Does rolling conversation compression (summarizing older turns, keeping recent ones verbatim), which typically trims long coding chats by roughly 30–50% tokens while still feeling continuous. 

Claude Context (semantic code search)
Lets Claude pull only the specific functions or snippets it needs instead of whole files, so per‑request code tokens usually drop on the order of 40–70% once your repo is indexed. 

Superpowers‑style plugins
Turn your long, reusable prompts (SEO systems, refactor recipes, content frameworks) into short commands or tasks, which in everyday use often cuts 15–40% of tokens from each repeated workflow.

Comment “hack” I will send you the links to all the plugins. 

(Switch to Codex)
Speaking from my own experience, I recently ran an end-to-end lead automation inside codex sing only natural language prompting—it was very intuitive and easy to navigate. It continued running for over 5 hours without hitting any rate limits.
Codex also uses a different limiting model: instead of a small fixed token bucket, your main constraint is the “reasoning time” within that 5-hour window.
Across multiple benchmarks, Claude tends to use roughly 2–4× more tokens than Codex on identical coding tasks. This is largely because Claude “thinks out loud,” explains its reasoning, and often spins up more sub-agents.
So next time, instead of waiting for your tokens to reset, give @openai Codex a try!

#claude #aihacks #openai #automation #claudecode

## Research

* Verdict: Partly valid. Three of the four plugins are real, free and public: claude-mem, Claude Context and Superpowers. The "Context Manager" plugin is too vague to identify. The saving percentages are unsourced. The only measured figure I found is about 40% for Claude Context, and the 2-4x Codex claim has no citation.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [claude-mem (github.com)](https://github.com/thedotmack/claude-mem): repo, found by search, verified, high confidence. README describes persistent memory compression for Claude Code, matching the post's first plugin.
* [Claude Context (zilliztech) (github.com)](https://github.com/zilliztech/claude-context): repo, found by search, verified, high confidence. MCP semantic code search that returns only relevant code; the README claims about 40% token reduction, the low end of the post's 40-70%.
* [Superpowers (obra) (github.com)](https://github.com/obra/superpowers): repo, found by search, not opened, medium confidence. Search results show a popular skills plugin for Claude Code. It is a skills and workflow framework, not clearly a prompt-shortening tool. I did not open the repo.

### Key steps

1. claude-mem: run `npx claude-mem install`, or `/plugin marketplace add thedotmack/claude-mem` then `/plugin install claude-mem`, then restart Claude Code.
2. Claude Context: needs Node 20 or later (not Node 24), an OpenAI API key and a Zilliz Cloud endpoint and token.
3. Claude Context: run `claude mcp add claude-context -e OPENAI_API_KEY=... -e MILVUS_ADDRESS=... -e MILVUS_TOKEN=... -- npx @zilliz/claude-context-mcp@latest`.
4. Claude Context: ask Claude Code to index the codebase, then search in natural language.
5. Superpowers: run `/plugin marketplace add obra/superpowers-marketplace`, then `/plugin install superpowers@superpowers-marketplace`, then restart.

### Not found

The "Context Manager" plugin could not be identified. I found no source for the 80-90%, 30-50% and 15-40% savings figures or the 2-4x Codex comparison. I did not read the vault notes or grep the vault.
