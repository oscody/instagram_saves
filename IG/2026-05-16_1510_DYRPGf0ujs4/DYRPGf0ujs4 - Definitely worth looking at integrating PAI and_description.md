---
shortcode: "DYRPGf0ujs4"
url: "https://instagram.com/reel/DYRPGf0ujs4/"
type: "Reel"
author: "tysn.dev"
shared: "May 16, 2026, 03:10 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Favorite Claude Code GitHub repos: PAI, OpenSpace, GSD

A reel ranking three favorite Claude Code GitHub repos, shown on screen with a terminal status line and the OpenSpace and Get Shit Done READMEs. The caption says PAI and OpenSpace have an evolving loop architecture worth integrating.

Written by claude-haiku-5-5.

## Source

* Link: PAI, OpenSpace, GSD (repo names written in the post)

## Caption

Definitely worth looking at integrating, PAI and OpenSpace have an evolving loop architecture that will most likely survive new models!

#github #ai #claudecode

## Research

* Verdict: Valid. All three repos exist and match the names in the post. PAI and OpenSpace do have self-improving loop designs. The "will survive new models" line is the creator's opinion. Two repos have changed since the reel: PAI is now LifeOS, and GSD is archived.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [OpenSpace (HKUDS) (github.com)](https://github.com/HKUDS/OpenSpace): repo, found by search, verified, high confidence. MIT skill-management layer that tracks skill outcomes and evolves skills, run as an MCP server.
* [PAI / LifeOS (danielmiessler) (github.com)](https://github.com/danielmiessler/Personal_AI_Infrastructure): repo, found by search, verified, medium confidence. The page now describes itself as LifeOS, an AI harness on Claude Code. The PAI name matches the search results and the PAI 5.0 blog post, but I did not open that post.
* [Get Shit Done (GSD) (github.com)](https://github.com/gsd-build/get-shit-done): repo, found by search, verified, high confidence. Meta-prompting and spec-driven development system for Claude Code. It is now archived and moved to GSD Core.
* [GSD Core (successor) (github.com)](https://github.com/open-gsd/gsd-core): repo, found by search, not opened, medium confidence. The archived GSD page names it as the continuation. I did not open it.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/article - 10 GitHub Repositories To Master Claude Code.md`: Matched a search for one of these names (OpenSpace, PAI or GSD). I did not read it, so I can't say what it says.

### Key steps

1. OpenSpace: git clone https://github.com/HKUDS/OpenSpace.git && cd OpenSpace && pip install -e . (needs Python 3.12+).
2. Check the install with `openspace-mcp --help`.
3. Add an MCP server named `openspace` using the command `openspace-mcp`. Set a 600s tool timeout and set OPENSPACE_WORKSPACE and OPENSPACE_HOST_SKILL_DIRS.
4. Copy the `delegate-task` and `skill-discovery` folders from openspace/host_skills/ into your agent's skills directory, then restart the agent.
5. PAI/LifeOS: install bun, back up ~/.claude, then tell Claude Code: 'Read https://ourlifeos.ai/install and install LifeOS for me.'
6. GSD: the original repo is archived, so use the GSD Core repo (open-gsd/gsd-core) and follow its README.

### Not found

I did not find the exact repo URLs shown in the reel, so I matched the repos by name. I did not open the GSD Core README or the PAI 5.0 blog post. I did not read the vault note. I could not check whether the loops "survive new models". The 46% token-savings figure for OpenSpace appears only in promotional material.
