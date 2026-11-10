---
shortcode: "DcgRoqMEpZb"
url: "https://instagram.com/reel/DcgRoqMEpZb/"
type: "Reel"
author: "nateherkai"
shared: "Nov 06, 2026, 06:09 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-06"
---

# Open-source repo giving AI agents access to 13 platforms

The reel claims a free open-source GitHub repo lets an AI agent reach 13 platforms such as Twitter, Reddit, YouTube, GitHub, and LinkedIn. Its frames show a grid of platform logos, a Reddit comment thread, and a README for a voice tool called Voicebox with REST and MCP examples.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment 'SEARCH' on the post; the creator says they will send the repo.
* Identified source (2026-11-10): Agent Reach, https://github.com/Panniantong/Agent-Reach (MIT). Matches the 13+ platform claim, free use, YouTube transcripts, Reddit and Twitter reading. The README shown in frame 3 is a different project (Voicebox).

## Caption

Comment 'SEARCH' and I'll send it over.

## Research

* Verdict: Partly valid. Agent Reach is a real, free, MIT repo that matches the reel. The claims are loose: it covers 14 channels, not 13. Several need logins. It does not bypass captchas. The README shown in the reel is Voicebox, a different project.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Agent Reach (Panniantong/Agent-Reach) (github.com)](https://github.com/Panniantong/Agent-Reach): repo, in the vault, verified, high confidence. I opened the repo. It is a read-only MIT CLI for agents covering YouTube, Reddit, X, GitHub, LinkedIn and others, as the reel describes. The vault review also confirms it.
* [Agent Reach install guide (github.com)](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md): guide, in the vault, not opened, medium confidence. The vault review and the repo README both point to it as the install guide. I did not open it.

### Already in the vault

* Vault: `ZAIHub/claude - Agent Reach review 2026-11-10.md`: Full static review of v1.6.1: what it is, a safety check, concerns, what the reel got wrong, and a Pi-safe install recipe.

### Already in IG saves

* Same: Web: [Open-source GitHub tool for AI agent web access (instagram.com)](https://instagram.com/p/DbWAuH_iFvK/) (`DbWAuH_iFvK`). Same link: Agent Reach install guide.
* Same: Web: [Agent Reach: giving Claude live platform access (instagram.com)](https://instagram.com/p/Dbx-eLST4rh/) (`Dbx-eLST4rh`). Same link: Agent Reach install guide.
* Same: Web: [Five Claude plugins to upgrade your workflow (instagram.com)](https://instagram.com/p/DeNy_grv_AM/) (`DeNy_grv_AM`). Same link: Agent Reach install guide.

### Key steps

1. Install from the GitHub release, not PyPI. The PyPI 'agent-reach' is an unrelated package: uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip
2. Run: agent-reach setup. This links the skill into the agents it finds on the machine.
3. If you don't want Hermes touched, run: agent-reach skill unlink ~/.hermes/skills
4. Run: agent-reach doctor --text to see which channels work.
5. Out of the box you get web, GitHub, YouTube transcripts, V2EX and Bilibili. No login is needed for these.
6. Reddit, LinkedIn, X, Instagram and Facebook need a login, which you do with: agent-reach login <channel>. Use Reach's own browser window, not your daily Chrome.
7. YouTube speech-to-text needs a Groq or OpenAI key.
8. To remove it, run: agent-reach uninstall --dry-run to see the paths, then uninstall.

### Not found

The Voicebox README shown in frame 3 was not looked up, because it is unrelated to the main claim. I did not open install.md directly.
