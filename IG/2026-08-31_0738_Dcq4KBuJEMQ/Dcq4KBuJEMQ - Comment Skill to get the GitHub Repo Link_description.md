---
shortcode: "Dcq4KBuJEMQ"
url: "https://instagram.com/reel/Dcq4KBuJEMQ/"
type: "Reel"
author: "100xengineers"
shared: "Aug 31, 2026, 07:38 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Scanning Claude skills for malicious code with SkillSpector

The post warns that Claude skills can hide malicious code and credits Nvidia's research on skills across AI agent marketplaces. It presents SkillSpector, an open-source Nvidia scanner that checks an agent skill before installation.

Written by claude-haiku-5-5.

## What it teaches

1. Point SkillSpector at a skill directory, a zip file, or the GitHub URL of a skill.
2. It runs a 71-pattern vulnerability test covering things like prompt injection, data exfiltration, and dangerous code calls.
3. It returns a risk score from 0 to 100; the video names 50 as the cutoff, with anything above 50 flagged.
4. Optionally run SkillSpector as an MCP server so an AI agent scans each new skill before installing it.

## Source

* How to get it: Comment "Skill" to receive the GitHub repo link (per the post)

## Caption

Comment "Skill" to get the GitHub Repo Link 🔗

Your Claude skills might have malicious code hidden inside them which can even hack your PC, and everyone should thank Nvidia for solving this.

So Nvidia did research over 42,000 skills across AI agent marketplaces and found 1 in every 4 agent skills you install could compromise your entire system.

And to tackle this, Nvidia built SkillSpector, which is an open-source scanner that checks any agent skill before you install it.

## Research

* Verdict: Valid. NVIDIA's SkillSpector is a real open-source scanner, and the repo matches the post's claims: 71 patterns, a 0–100 score with a cutoff at 50, and an MCP mode. The "1 in 4 skills" line matches NVIDIA's reported figure of 26.1% of 42,447 skills having at least one vulnerability. Only 5.2% show likely malicious intent.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [NVIDIA/SkillSpector (github.com)](https://github.com/NVIDIA/SkillSpector): repo, found by search, verified, high confidence. README lists 71 patterns across 17 categories, a 0–100 risk score with exit code 1 above 50, input as a directory, zip or Git URL, and an MCP server mode.
* [NVIDIA docs: scanning agent skills (docs.nvidia.com)](https://docs.nvidia.com/skills/scanning-agent-skills): guide, found by search, not opened, medium confidence. Official NVIDIA documentation page for scanning agent skills, which appeared in search results. I did not open it.
* [Help Net Security coverage (helpnetsecurity.com)](https://www.helpnetsecurity.com/2026/08/03/skillspector-open-source-agent-skill-security-scanner/): page, found by search, not opened, medium confidence. News article on the SkillSpector release. I did not open it.

### Already in the vault

* Vault: `ZAIHub/repo - SkillSpector.md`: Your install of SkillSpector (2026-10-11) and repo notes.
* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Repo link, the saved reel, similar saves, and a to-do to scan candidate repos.
* Vault: `ZAIHub/claude - Claude and Codex Skills Index.md`: Links to your SkillSpector scans of several skills.

### Key steps

1. Install: uv tool install git+https://github.com/NVIDIA/skillspector.git (add the [mcp] extra for MCP mode).
2. Scan a skill with skillspector scan <dir | SKILL.md | repo URL | .zip>.
3. Add --no-llm for static analysis only. The optional LLM pass needs an OpenAI-compatible endpoint and key.
4. Add --format json --output report.json to save a report.
5. Read the score: 0–20 safe, 21–50 caution, 51–80 and 81–100 do not install. The command exits 1 above 50.
6. Register the MCP server with Claude Code: claude mcp add skillspector -- skillspector mcp.
7. The MCP tool scan_skill returns risk_score, severity, safe_to_install and findings, so an agent can check a skill before installing it.

### Not found

The post says the repo link is only sent after a comment. A public copy exists on GitHub, so that isn't needed. I didn't open the NVIDIA research paper or the NVIDIA docs page.
