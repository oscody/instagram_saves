---
shortcode: "DeON0MOB5oi"
url: "https://instagram.com/reel/DeON0MOB5oi/"
type: "Reel"
author: "charles.zhengg"
shared: "Oct 12, 2026, 02:16 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Turning websites into agent APIs via reverse engineering

The creator says a repo can turn any website into an API for AI agents by reverse engineering its network traffic, so paid APIs such as LinkedIn or Reddit are not needed. On screen are a "Browser access" toggle switched on and a LinkedIn connect-button mockup.

Written by claude-haiku-5-5.

## What it teaches

1. Enable browser access for your agent before reverse engineering anything.
2. Give your agent the repo's prompt and name the website whose API you want to reverse engineer.
3. Use this for automated workflows where the agent already uses the browser, since browser actions become API calls.
4. Expect, per the creator's claim, about 50% less time and 50% lower cost on a task.

## Caption

This is how I made my agents native browser use so fast and efficient

## Research

* Verdict: Partly valid. Open-source repos that reverse engineer site traffic into APIs for agents do exist, but the post never names its repo, so I can't confirm which one the creator used. The "50% less time and cost" figure has no source.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Unbrowse (unbrowse-ai/unbrowse) (github.com)](https://github.com/unbrowse-ai/unbrowse): repo, found by search, verified, medium confidence. It reverse engineers sites so agents call first-party APIs instead of driving a browser, which fits the post's idea. The README claims 50-100x faster and 95% cheaper, not the creator's 50%.
* [Reverse API Engineer (kalil0321) (github.com)](https://github.com/kalil0321/reverse-api-engineer): repo, found by search, verified, medium confidence. Its agent mode records browser traffic to a HAR file and has the model generate an API client, which also fits the post.

### Key steps

1. Unbrowse: install the skill with `npx skills add unbrowse-ai/unbrowse --skill unbrowse`.
2. Unbrowse: or connect over MCP with `claude mcp add --transport http unbrowse https://unbrowse.ai/mcp`.
3. Unbrowse: sign in with `npx unbrowse login`.
4. Unbrowse: run a task, e.g. `npx unbrowse run 'top stories on hacker news'`. If no learned capability matches, it records the site in a cloud browser and compiles the requests into a reusable one.
5. Reverse API Engineer: install with `uv tool install reverse-api-engineer`, then run `reverse-api-engineer`.
6. Reverse API Engineer: state your goal and switch to agent mode so an AI agent browses the site.
7. Reverse API Engineer: it captures traffic to a HAR file and writes a typed client to `./scripts/{name}/`. Review the generated code before running it.

### Not found

The creator's exact repo and prompt are not in the post or the vault. I didn't open the creator's Instagram profile. I found no source for the 50% time and cost claim. The Unbrowse speed and cost claims are the project's own and come with no benchmarks. Sites like LinkedIn restrict automated access in their terms and may block it.
