---
shortcode: "DfdtpQmoFTs"
url: "https://instagram.com/p/DfdtpQmoFTs/"
type: "Carousel"
author: null
shared: "Nov 08, 2026, 03:32 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-08"
---

# Anthropic talk on shipping a first managed agent

Caption and slides describe a 37-minute Anthropic session by engineer Isabella He on shipping a first managed AI agent. The transcript covers only the opening remarks and agenda.

Written by claude-haiku-5-5.

## Source

* How to get it: comment "Guide", sent by DM

## Caption

Anthropic just released a 37-minute guide on how to build your first managed AI agent.

Throughout the guide, Isabella He skips the usual hype around “one-click automation replacing an entire company” and goes straight into the real engineering challenges.

She explains how Anthropic’s approach lets agents handle their own tool calls, manage tasks, and decide when they’re done, without developers having to manually manage every loop and interruption.

It’s completely free and comes straight from the engineers who built Claude.

Follow us @quantumfield.ai and comment “Guide”. We’ll DM you the link.

## Research

* Verdict: Valid. The session is real and public, so no DM is needed. The "37 minutes" and "free" details are unconfirmed. The caption's description of agents handling their own loops is loosely fair, but the talk is a hands-on incident-investigator workshop.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Ship your first Claude Managed Agent (webinar page) (claude.com)](https://claude.com/resources/webinars/ship-your-first-claude-managed-agent): video, found by search, verified, high confidence. Opened it: Isabella He (Applied AI, Anthropic) leads an on-demand build of an incident-investigator agent. A form is needed to watch.
* [Code with Claude London session page (claude.com)](https://claude.com/code-with-claude/session/ldn-ext-ship-your-first-managed-agent): page, found by search, not opened, medium confidence. Search result with the same title. Not opened.
* [Managed Agents quickstart docs (platform.claude.com)](https://platform.claude.com/docs/en/managed-agents/quickstart): guide, in the vault, not opened, medium confidence. Listed in an earlier saved-post note as the official quickstart. Not opened.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Mentions Claude Managed Agents only briefly. It has no link to this session and no steps.

### Already in IG saves

* Same: Web: [Anthropic 37-minute agent guide, comment TEACH (instagram.com)](https://instagram.com/p/DeET_LNFrz5/) (`DeET_LNFrz5`). Same link: Ship your first Claude Managed Agent (webinar page).
* Similar: Web: [Self-improving AI system with Claude Managed Agents (instagram.com)](https://instagram.com/p/DaiXvIEkrar/) (`DaiXvIEkrar`). Carousel on Claude Managed Agents covering agent, environment and session building blocks.

### Key steps

1. Open the webinar page and fill in the form to watch on demand.
2. Have an Anthropic API key ready. Managed Agents is in beta and needs the managed-agents-2026-04-01 header, which the SDK sets for you.
3. Clone the workshop repo (cwc-workshops) and cd into ship-your-first-managed-agent.
4. Define the three core resources: an Agent, an Environment and a Session.
5. Stream session events and add custom tools.
6. Build the incident-investigator agent in the workshop's six functions.
7. Use the server-side loop model and the production roadmap (subagents, vaults, memory) to move toward shipping.

### Not found

The workshop repo URL was not given in full, so I did not find it. I did not confirm the 37-minute length or that the video is free. I did not watch the recording.
