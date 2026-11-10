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

* Verdict: Partly valid. All five tools exist and roughly match the descriptions, but the post's wording is loose. Only the first is a real plugin, the others are standalone tools or skills. "No API key" for Agent Reach is overstated, because some platforms need cookies or a login. The links are only sent by comment, but public copies exist.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [claude-code-setup (claude-automation-recommender) (claude.com)](https://claude.com/plugins/claude-code-setup): tool, found by search, not opened, medium confidence. Search results describe an official Anthropic plugin that scans a codebase and recommends hooks, skills, MCP servers and subagents. Read-only, so it does not clear anything out as the post claims.
* [OmniRoute (github.com)](https://github.com/diegosouzapw/OmniRoute): repo, found by search, not opened, medium confidence. Search results describe an MIT AI gateway that routes Claude Code to many providers through one endpoint. Provider counts differ by source.
* [find-skills (vercel-labs/skills) (github.com)](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md): tool, in the vault, verified, medium confidence. Another saved post (DePtyBoAOPd) verified this skill, which finds skills by task. I did not check that it is the one the creator showed.
* [Strix (github.com)](https://github.com/usestrix/strix): repo, found by search, not opened, medium confidence. Search results describe an Apache-2.0 autonomous AI pentest agent that proves vulnerabilities with proof-of-concept exploits. It needs Docker and an LLM key.
* [Agent Reach (github.com)](https://github.com/Panniantong/Agent-Reach): repo, in the vault, verified, high confidence. Two other saved posts (DbWAuH_iFvK, DcgRoqMEpZb) verified this MIT repo, which lets agents read many platforms without paid APIs.

### Already in IG saves

* Same: Web: [Open-source GitHub tool for AI agent web access (instagram.com)](https://instagram.com/p/DbWAuH_iFvK/) (`DbWAuH_iFvK`). Same link: Agent Reach.
* Same: Web: [Agent Reach: giving Claude live platform access (instagram.com)](https://instagram.com/p/Dbx-eLST4rh/) (`Dbx-eLST4rh`). Same link: Agent Reach.
* Same: Web: [Open-source repo giving AI agents access to 13 platforms (instagram.com)](https://instagram.com/p/DcgRoqMEpZb/) (`DcgRoqMEpZb`). Agent Reach reaching 13+ platforms.
* Same: Web: [Top five most-installed Claude skills ranking (instagram.com)](https://instagram.com/p/DcgvcNGsEa1/) (`DcgvcNGsEa1`). Same link: find-skills (vercel-labs/skills).
* Same: Web: [Find Skills: searching a million Claude skills (instagram.com)](https://instagram.com/p/DePtyBoAOPd/) (`DePtyBoAOPd`). Same link: find-skills (vercel-labs/skills).

### Key steps

1. claude-code-setup: install it from Anthropic's official plugin marketplace and run it in your project. It recommends hooks, skills and subagents but does not install them.
2. OmniRoute: install from the GitHub repo and start the local gateway. Per search results it listens at http://localhost:20128/v1, and a setup-claude-code command points Claude Code at it.
3. find-skills: add it with `npx skills add vercel-labs/skills --skill find-skills -g`. This command is unverified (see post DePtyBoAOPd), so check `npx skills --help`.
4. Strix: needs Docker and Python 3.12+. Run `pipx install strix-agent`, set STRIX_LLM and LLM_API_KEY, then run `strix --target ./app`. Only test apps you own or have permission to test.
5. Agent Reach: install from the GitHub repo (`pip install https://github.com/Panniantong/agent-reach/archive/main.zip`), then follow docs/install.md. Some platforms need cookies or a login.

### Not found

I did not open the GitHub pages for OmniRoute, Strix or claude-code-setup, so they are not marked verified. I could not confirm that the creator's "FindSkills" is vercel-labs find-skills. The creator's link list is only sent by comment.
