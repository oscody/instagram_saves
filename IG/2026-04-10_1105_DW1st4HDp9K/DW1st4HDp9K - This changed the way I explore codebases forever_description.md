---
shortcode: "DW1st4HDp9K"
url: "https://instagram.com/reel/DW1st4HDp9K/"
type: "Reel"
author: "marc.kaz"
shared: "Apr 10, 2026, 11:05 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Graphify: open-source folder-to-knowledge-graph tool

A reel presenting Graphify, an open-source tool that builds a knowledge graph, Obsidian vault, and wiki from a folder of code, notes, PDFs, or images, with the GitHub repo page shown on screen. The post claims it was built in 48 hours after Karpathy asked for it and cuts tokens per query by 71.5x.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/safishamsi/graphify

## Caption

This changed the way I explore codebases forever.

Before: Scattered folders, massive token burn, and zero visibility into real connections. 
After: One command → full knowledge graph with Obsidian vault, interactive wiki, and plain-English answers like “What calls this function?” 
The bridge? **Graphify** — built in 48 hours after Karpathy asked for it. Handles code, PDFs, images. 71.5x fewer tokens per query.

Open source. Zero setup.

Save this if you build or research!

👉 https://github.com/safishamsi/graphify

#Graphify #KnowledgeGraph #AICoding #DevTools #OpenSourceAI

## Research

* Verdict: Partly valid. The Graphify repo is real and does turn code, docs and PDFs into a queryable knowledge graph. The repo page I opened doesn't mention the 71.5x token figure, Karpathy, the 48-hour build or Obsidian output.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [safishamsi/graphify (github.com)](https://github.com/safishamsi/graphify): repo, in the post, verified, high confidence. The repo page describes a /graphify skill that builds a knowledge graph from code, docs and PDFs, with a --wiki option for a markdown wiki.

### Key steps

1. Install the CLI. The PyPI package name is graphifyy, with two y's: `uv tool install graphifyy` (or `pipx install graphifyy`).
2. Run `graphify install` to register the skill with your AI assistant (Claude Code, Cursor, Codex or Gemini CLI).
3. In the assistant, run `/graphify .` in your folder. Codex uses `$graphify`.
4. Open the output in graphify-out/: graph.html, GRAPH_REPORT.md and graph.json.
5. Query the graph with `graphify query "<question>"`, `graphify path A B` or `graphify explain <name>`.
6. Add the `--wiki` option to build a markdown wiki from the graph.

### Not found

I found no source for the 71.5x token claim, the Karpathy request or the 48-hour build on the repo page. I didn't search elsewhere for them. The repo page doesn't name Obsidian output either, though the --wiki option produces markdown. The vault has no note on Graphify itself.
