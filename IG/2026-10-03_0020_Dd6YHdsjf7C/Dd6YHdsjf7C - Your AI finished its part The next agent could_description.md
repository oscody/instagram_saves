---
shortcode: "Dd6YHdsjf7C"
url: "https://instagram.com/reel/Dd6YHdsjf7C/"
type: "Reel"
author: "heystevetan"
shared: "Oct 03, 2026, 12:20 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Agent Tincan: relay for AI agent handoffs

The post introduces Agent Tincan, an open-source relay that lets connected AI agents send requests, replies and files to each other over a private Tailscale network. It walks through how a handoff works and lists setup needs and trust risks.

Written by claude-haiku-5-5.

## What it teaches

1. Ask your main agent to get help with a task so it sends a request and the relevant context to a connected agent.
2. The receiving agent works on the request with its own tools and permissions.
3. The receiving agent sends its result back through the relay.
4. Your main agent brings the result back to you for review.
5. Keep the relay online and make sure each receiving agent is running or has a supported way to wake up.
6. Connect each agent with the tools and access it needs; browser connections need a running, logged-in browser.
7. Connected agents trust each other by default, so be selective about what you connect.
8. Decide which handoffs need your confirmation, and which only need to pass a message along.

## Source

* How to get it: Comment TIN, and the link is sent by DM

## Caption

Your AI finished its part. The next agent could take over, but it’s waiting for you to copy the result into another app.

You’re moving files, repeating instructions and carrying answers back and forth between tools you got to save time. The agents have different abilities, but you’re still the connection between them.

Agent Tincan is an open-source relay that lets connected AI agents ask each other for help and send results back. It passes requests, replies and files through a private Tailscale network. Each agent uses the tools and access it already has.

In practice:
- You ask your main agent to help with a coding task
- It sends a request and the relevant context to a connected coding agent
- The coding agent works on the request using its existing tools and permissions
- It sends its result back through Tincan
- Your main agent brings the result back to you for review

Code handoffs. Research requests. Second opinions from different assistants. Without you having to copy every message between them and explain the same context again.

Two honest caveats. This needs setup and an available relay, and the receiving agents need to be running or have a supported way to wake up. Browser connections need a running, logged-in browser. The relay software is free, but hosting and the AI services can still cost money.

And connected agents trust each other by default. Tincan doesn’t add an approval step to every request or guarantee that a task gets done correctly. An agent that can reach a powerful teammate can also pass along a harmful request, so be careful about what you connect and which actions need your confirmation.

The useful shift is deciding which handoffs need your judgment and which only need you to move a message. You shouldn’t have to do both.

Comment "TIN" and I'll send you the link, and follow for more ideas that make your life easier.
.
.
.
.
.
[Agent Tincan, AI agents, agent communication, multi-agent workflows, AI collaboration, task handoffs, workflow automation, open source, self-hosted AI, Tailscale, Grok Bot, Muse, Instinct, Hermes, Claude Code, Codex, ChatGPT, Claude, AI permissions, founder productivity]
