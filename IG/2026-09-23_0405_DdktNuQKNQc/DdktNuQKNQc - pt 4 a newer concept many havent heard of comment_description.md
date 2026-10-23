---
shortcode: "DdktNuQKNQc"
url: "https://instagram.com/reel/DdktNuQKNQc/"
type: "Reel"
author: "vardy.mov"
shared: "Sep 23, 2026, 04:05 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Agent graphs: building multi-agent workflows with nodes

A creator introduces the "agent graph" concept, where separate workers (nodes) pass information to each other instead of relying on one agent. The post is part four of a series and says the full guide is sent to people who comment "graph".

Written by claude-haiku-5-5.

## What it teaches

1. Build a system as an agent graph: each node does a specific piece of work, and each edge carries information from one node to the next.
2. Structure the graph so a failure stays contained to one node, since failures are easier to isolate from the rest of the system.
3. Don't make every node non-deterministic (LLM-based). Use normal functions for some nodes, such as a graph search, to reduce failure points.
4. Let graphs loop from node to node so the system can improve itself.
5. Add a parent orchestrator model on top of the graph that tweaks each node's performance.

## Source

* How to get it: Comment "graph" on the post to get the guide

## Caption

pt 4: a newer concept many haven’t heard of (comment “graph” for guide)

## Research

* Verdict: Unresolved. The guide is only sent to people who comment "graph", and I found no public copy. The concept itself (nodes, edges, loops, deterministic nodes) is real and standard in LangGraph-style frameworks.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Graph Multi-Agent Pattern (Strands Agents docs) (vnext-docs-preview.strandsagents.com)](https://vnext-docs-preview.strandsagents.com/docs/user-guide/concepts/multi-agent/graph): guide, found by search, not opened, low confidence. Public doc on the same concept (graphs of agent nodes, DAG or cyclic with feedback loops). It is not the creator's guide and I did not open it.

### Not found

The creator's "graph" guide (DM or comment-gated). No vault note covers it. Vault grep hits for "vardy" or "agent graph" were unrelated notes, such as the LocAgent note.
