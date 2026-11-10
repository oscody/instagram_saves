---
shortcode: "DfSKSKUNroJ"
url: "https://instagram.com/reel/DfSKSKUNroJ/"
type: "Reel"
author: "pathionai"
shared: "Nov 04, 2026, 04:26 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-04"
---

# Five Claude connectors to add before using Claude

A man in a black shirt, shown against 3D renders of a Claude-branded airship, lists five connectors to add to Claude and what each one does. Playwright's section is shown with a sign-up form test.

Written by claude-haiku-5-5.

## What it teaches

1. Before using Claude, add the Perplexity connector to give Claude real-time research on any topic.
2. Add the Firecrawl connector so Claude can scrape any website, pull brand assets, and research competitors.
3. Add the Playwright connector to give Claude its own browser for opening pages, testing buttons, filling out forms, and testing what it built.
4. Add the PostHog connector so Claude can see how users behave on your website, including sign-ups and errors.
5. Add the Composio connector to reach multiple apps such as Gmail and Slack without setting up each one separately.

## Source

* How to get it: Comment CONNECT (the full guide is sent by comment)

## Caption

Comment CONNECT and I will send you the Full Guide

## Research

* Verdict: Partly valid. All five tools are real and work with Claude, but the "full guide" is only sent by comment and has no public copy. The "don't use Claude before adding these" framing is hype, since they are optional.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Firecrawl in Claude.ai (official docs) (docs.firecrawl.dev)](https://docs.firecrawl.dev/developer-guides/mcp-setup-guides/claude-ai): guide, found by search, verified, high confidence. Opened it. It covers adding the native Firecrawl connector in Claude.ai, matching item 2.
* [Composio connect guide for PostHog MCP in Claude (composio.dev)](https://composio.dev/toolkits/posthog_mcp/framework/claude-cowork): guide, found by search, not opened, medium confidence. Search result only, not opened. Describes connecting PostHog (and via Composio, other apps) to Claude.
* [Claude connectors overview (official) (claude.com)](https://claude.com/docs/connectors/overview): page, found by search, not opened, medium confidence. Search result only, not opened. Official page on adding connectors in Claude.

### Already in IG saves

* Same: Web: [Audit of five scraping frameworks before deploying (instagram.com)](https://instagram.com/p/DY2Cf2jks2a/) (`DY2Cf2jks2a`). Covers Firecrawl and Playwright as scraping tools for agents.
* Same: Web: [Two app habits: session replays and review prompts (instagram.com)](https://instagram.com/p/DcUy9rhR0Uo/) (`DcUy9rhR0Uo`). Covers PostHog session replays, with a verified docs link.
* Similar: Web: [Five Claude Code plugins for better website design (instagram.com)](https://instagram.com/p/DcWQCQdN28T/) (`DcWQCQdN28T`). Lists Playwright CLI as a Claude plugin for letting Claude open and test websites.

### Key steps

1. Perplexity: in Claude Code, a third-party guide gives the hosted MCP URL https://api.perplexity.ai/mcp. It needs a Perplexity API key, which is billed by usage. I did not verify this.
2. Firecrawl: open the Firecrawl connector in Claude.ai, sign in, pick a team and approve access. Then in a chat open + > Connectors and enable it.
3. Playwright: in Claude Code run `claude mcp add playwright npx @playwright/mcp@latest` (from a third-party guide, not opened).
4. PostHog and Composio: in Claude Desktop go to Customize > Connectors > + and add https://connect.composio.dev/mcp (from a search summary, not opened). Then link each app at connect.composio.dev and authorize your PostHog account.
5. If a connector shows as connected but Claude ignores it, re-enable it from the + menu in the chat.

### Not found

The creator's "Full Guide" (sent after commenting CONNECT) has no public copy that I found. I did not open the Perplexity, Playwright or Composio setup pages, so their commands come from search summaries.
