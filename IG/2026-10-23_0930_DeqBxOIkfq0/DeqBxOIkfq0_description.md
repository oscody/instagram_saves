---
shortcode: "DeqBxOIkfq0"
url: "https://instagram.com/reel/DeqBxOIkfq0/"
type: "Reel"
author: "nocodealex"
shared: "Oct 23, 2026, 09:30 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-04"
---

# Claude builds 3D game worlds inside Blender

The post promotes a free, open-source Blender add-on that connects Claude to Blender so it can build 3D scenes from a text description, including pulling models and textures from free libraries. The repo link is not written in the post; it is sent by DM after commenting SCULPT.

Written by claude-haiku-5-5.

## What it teaches

1. Save your Blender project before letting Claude build anything, because the add-on can run any Python code inside Blender.
2. Turn on safe mode in the add-on.
3. Describe the scene in plain language, for example "a low poly dungeon with a dragon guarding gold", and Claude creates the objects, colours, lights and camera.

## Source

* How to get it: Comment "SCULPT" to receive the repo link by DM

## Caption

Comment "SCULPT" and I'll DM you the repo link that lets Claude build 3D game worlds inside Blender for you. Follow so the DM lands 📩

👇 READ BELOW: what it does, from the repo's own README.

1. It's a free, open-source Blender add-on with about 31,500 stars on GitHub, and it plugs Claude straight into Blender.

2. You describe the scene, like "a low poly dungeon with a dragon guarding a pot of gold", and Claude makes the objects, colours, lights and camera.

3. It can pull real models and textures from Poly Haven, Sketchfab and Poly Pizza, or generate new models.

4. It looks at its own scene from several angles and renders, then fixes what looks wrong.

5. Setup is one line in Claude Code plus the Blender add-on, and the guide has four prompts to try, from a game level to studio lighting.

The catch: it can run any Python code inside Blender, so save your project first, and turn on safe mode.

For the link, comment "SCULPT"

#claudeai #claudecode #claude #claudetips

## Research

* Verdict: Valid. The repo is public and matches the post: free, MIT, about 33.9k stars (post says 31.5k), Poly Haven, Sketchfab and Poly Pizza support, the dungeon/dragon example prompt, and the arbitrary-code warning with a safe mode. The link is only sent by DM, but the repo is public.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [MCP for Blender (ahujasid/blender-mcp) (github.com)](https://github.com/ahujasid/blender-mcp): repo, found by search, verified, high confidence. README has the 'low poly scene in a dungeon, with a dragon guarding a pot of gold' prompt, Poly Haven, Sketchfab and Poly Pizza sources, and the save-first and safe-mode warning.

### Already in IG saves

* Same: Web: [Blender robot model built with Opus 5.5 (instagram.com)](https://instagram.com/p/Ddp8_uQGW5-/) (`Ddp8_uQGW5-`). Same link: MCP for Blender (ahujasid/blender-mcp).
* Similar: Web: [Blender 3D product videos with Claude (instagram.com)](https://instagram.com/p/DfaV3s0DuSq/) (`DfaV3s0DuSq`). Claude working in Blender through the official Blender connector and MCP add-on.

### Key steps

1. Install uv with the official installer (not pip).
2. Add the server to Claude Code: claude mcp add blender uvx mcp-for-blender
3. Install the Blender add-on: uvx mcp-for-blender install-addon
4. In Blender, go to Edit > Preferences > Add-ons and enable 'Interface: MCP for Blender'.
5. In the 3D viewport press N, open the MCP for Blender tab, and click Start MCP Server.
6. Save your Blender project, because execute_blender_code can run any Python.
7. Set BLENDER_MCP_SAFE_MODE=1 to block risky scripts.
8. Prompt Claude, for example: 'Create a low poly scene in a dungeon, with a dragon guarding a pot of gold'. Poly Pizza needs a free API key.

### Not found

The post's DM link was not seen. The repo was identified by matching content, not from the DM. Blender 3.0+ and Python 3.10+ are required, per the README.
