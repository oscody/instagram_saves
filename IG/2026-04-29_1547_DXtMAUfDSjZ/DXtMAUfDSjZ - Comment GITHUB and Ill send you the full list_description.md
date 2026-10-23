---
shortcode: "DXtMAUfDSjZ"
url: "https://instagram.com/p/DXtMAUfDSjZ/"
type: "Carousel"
author: "anubhavhingg"
shared: "Apr 29, 2026, 03:47 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Trending GitHub repos list teaser for Claude Code

The post is a teaser for a list of trending GitHub repos related to Claude Code and AI tools. It shows the top two entries (forrestchang/andrej-karpathy-skills and thedotmack/claude-mem) and says the full top 10 list is sent only by comment or DM.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment GITHUB (per the caption) or REPO (per the on-image text) to get the full top 10 list by DM

## Caption

Comment GITHUB and I’ll send you the full list.

The #1 trending repo on GitHub today?A single file that makes Claude Code 10x smarter.Based on Andrej Karpathy’s observations. 9,000+ stars in one day.And that’s just #1.There’s an AI hedge fund, a voice studio, a memory plugin for Claude, a financial markets foundation model  all blowing up today.

Comment GITHUB and I’ll DM you the full top 10 list.

## Research

* Verdict: Partly valid. The two repos shown are real and match the post. The "10x smarter" claim is hype for what is a behavior-guidelines CLAUDE.md. The full top-10 list is only sent by DM, and I found no public copy.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [forrestchang/andrej-karpathy-skills (github.com)](https://github.com/forrestchang/andrej-karpathy-skills): repo, in the post, verified, high confidence. A single CLAUDE.md based on Karpathy's observations about LLM coding mistakes, as the post describes; the repo has about 222k stars now.
* [thedotmack/claude-mem (github.com)](https://github.com/thedotmack/claude-mem): repo, in the post, verified, high confidence. A memory plugin for Claude Code that keeps context across sessions, matching the post's 'memory plugin for Claude'.

### Key steps

1. Karpathy skills, as a plugin: in Claude Code run `/plugin marketplace add forrestchang/andrej-karpathy-skills`, then `/plugin install andrej-karpathy-skills@karpathy-skills`.
2. Karpathy skills, as a file: curl the repo's CLAUDE.md into your project, or append it to your existing CLAUDE.md.
3. Cursor users can use the repo's `.cursor/rules/karpathy-guidelines.mdc`.
4. Claude-mem: run `npx claude-mem install` and sign in through the browser. Or in Claude Code run `/plugin marketplace add thedotmack/claude-mem`, then `/plugin install claude-mem`.
5. Restart Claude Code. It needs Node.js 20 or higher. Don't use `npm install -g claude-mem`, which doesn't register the plugin hooks.
6. Past context is injected automatically. You can search it with the `search`, `timeline` and `get_observations` MCP tools.

### Not found

The full top-10 list (AI hedge fund, voice studio, financial markets foundation model and the rest) is only sent by DM after a comment. I didn't find a public copy and didn't check GitHub trending for that day. I didn't verify the '9,000+ stars in one day' claim.
