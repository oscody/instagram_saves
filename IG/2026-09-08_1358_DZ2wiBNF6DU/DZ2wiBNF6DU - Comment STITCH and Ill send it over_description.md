---
shortcode: "DZ2wiBNF6DU"
url: "https://instagram.com/reel/DZ2wiBNF6DU/"
type: "Reel"
author: "nateherkai"
shared: "Sep 08, 2026, 01:58 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Google Stitch designs into Claude Code workflow

A short reel showing how to take a UI design made in Google Stitch and export it to Claude Code through MCP, so Claude builds the front end from that design system.

Written by claude-haiku-5-5.

## What it teaches

1. Open Google Stitch (stitch.withgoogle.com) and describe your app idea in plain English.
2. Optionally add reference images from Pinterest or Dribbble so Stitch generates a UI system with screens, layouts and colors.
3. Export the design using the MCP option in Stitch's Export menu.
4. Connect the Stitch MCP server to Claude Code so Claude can access your designs while it builds.
5. Prompt Claude Code to connect the screens, add animations, make the app responsive and clean up the code.

## Source

* Link: stitch.withgoogle.com
* How to get it: Comment 'STITCH' on the post; the setup is sent by the account after the comment

## Caption

Comment 'STITCH' and I'll send it over.

## Research

* Verdict: Partly valid. Stitch is a real Google tool and its MCP/Claude Code workflow is described by third parties. The creator's own setup is only sent via comment, and I couldn't open an official Google setup doc to confirm the Export menu step.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Google Stitch (stitch.withgoogle.com)](https://stitch.withgoogle.com): product, in the post, verified, medium confidence. Page opened with title 'Stitch - Design with AI', but it showed no detail on MCP export.
* [Claude Stitch MCP (community server, Glama listing) (glama.ai)](https://glama.ai/mcp/servers/gjurjy7c9u): tool, found by search, not opened, low confidence. Community wrapper for connecting Stitch to Claude. Its instructions target Claude Desktop, not Claude Code, so it is not necessarily the creator's setup.
* [Google Stitch MCP: From Design to Code with Claude Code in 23 Minutes (pasqualepillitteri.it)](https://pasqualepillitteri.it/en/news/647/google-stitch-mcp-export-claude-code-design-to-code): guide, found by search, not opened, low confidence. Third-party guide on the same workflow. The page failed to load, and the search summary called it promotional.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/stitch.md`: Stitch links only, with MCP-token URLs. No steps.
* Vault: `3. Resources/0. note idea draft/Learning - AI UI design.md`: One-line description of Stitch with its link. No steps.

### Key steps

1. Open stitch.withgoogle.com and describe your app. Optionally add reference images from Pinterest or Dribbble.
2. Generate the screens, then use Export and pick the MCP option, as the reel shows.
3. Authenticate: create a Stitch API key under Settings → API Keys, or use gcloud ADC (`gcloud auth application-default login`). Google's official endpoint is stitch.googleapis.com/mcp, which Claude Code can't use directly because of its auth type.
4. Either use a community wrapper such as the Glama-listed Claude Stitch MCP (clone, `npm install`, `npm run build`, run the installer), or use the setup the creator sends.
5. Restart Claude Code and confirm the Stitch tools show up.
6. Prompt Claude to build from the Stitch screens: connect the screens, add animations, make the app responsive and clean up the code.

### Not found

The creator's own 'STITCH' setup, which is sent after a comment. No official Google doc for the Stitch MCP export or a `claude mcp add` command. The Italian guide page failed to load.
