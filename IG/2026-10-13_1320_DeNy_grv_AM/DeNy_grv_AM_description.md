---
shortcode: "DeNy_grv_AM"
url: "https://instagram.com/reel/DeNy_grv_AM/"
type: "Reel"
author: "benkimball.ai"
shared: "Oct 13, 2026, 01:20 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Five Claude plugins to upgrade your workflow

A reel introducing five Claude Code plugins: CloudCode Setup, OmniRoute, FindSkills, Strix, and Agent Reach, each with a short description of what it does. The post asks viewers to comment "Claude" to get links to them.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment the word "Claude" to receive the links

## Caption

Wait until the end 👀 These 5 Claude plugins can seriously upgrade your workflow! #Claude #ClaudeAI #ClaudePlugins #AI #AITools AITips Productivity AIWorkflow ClaudeTips AIForCreators TechTok AITok

## Research

* Verdict: Partly valid. Three of the five tools (OmniRoute, Strix, Agent Reach) are real public GitHub repos that match the post's descriptions. They are standalone tools, not Claude plugins as the post calls them. I couldn't identify "CloudCode Setup" or "FindSkills" without the creator's links.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [OmniRoute (github.com)](https://github.com/diegosouzapw/OmniRoute): repo, found by search, verified, medium confidence. An MIT AI gateway with one endpoint for many providers, with Claude Code integration; I couldn't confirm it's the exact one the creator showed.
* [Strix (github.com)](https://github.com/usestrix/strix): repo, found by search, verified, medium confidence. An open-source AI pentesting agent tool; the opened README matches the name, though the reel's exact visuals weren't checked.
* [Agent Reach (github.com)](https://github.com/Panniantong/Agent-Reach): repo, found by search, verified, medium confidence. A CLI that gives AI agents access to Twitter, Reddit, YouTube and other platforms, and it works with Claude Code.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Mentions Agent Reach only, as a link to another reel (heystevetan).

### Key steps

1. OmniRoute: install via the npm package `omniroute` or the Docker image, then connect a provider with your own account or API key.
2. OmniRoute: point your tool at localhost:20128/v1 with the key from Dashboard → Endpoints and model `auto`.
3. OmniRoute: run `omniroute run claude --model <provider/model>`, or run `omniroute configure claude` to write Claude Code's config.
4. Strix: have Docker running and set STRIX_LLM and LLM_API_KEY.
5. Strix: install with `curl -sSL https://strix.ai/install | bash`, then run `strix --target ./app` or `strix --target https://your-app.com`. Only scan systems you own or have permission to test.
6. Agent Reach: paste the install.md URL from the README into your agent, or run `agent-reach install --env=auto --dry-run`, then `agent-reach doctor`. Don't install the same-named PyPI package.

### Not found

The creator's link list is sent only by comment or DM, and I found no public copy. I did not find repos for "CloudCode Setup" or "FindSkills" (possibly a skills finder), so both are unverified.
