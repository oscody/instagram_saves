---
shortcode: "Dcw2I9jkohy"
url: "https://instagram.com/reel/Dcw2I9jkohy/"
type: "Reel"
author: "globalaiforce"
shared: "Sep 04, 2026, 01:24 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Unity MCP: AI builds Unity scenes from prompts

The post promotes Unity MCP, an open-source integration that connects AI agents such as Claude and Cursor to the Unity Editor so they can build and modify game scenes from text prompts. The frames show a README header and a yellow hover vehicle on a platform above water.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post to receive the link

## Caption

You can now command AI to build fully functional 3D game worlds inside Unity in real time.

An open-source integration called "Unity MCP" connects AI agents like Claude and Cursor directly to the Unity Editor, bridging natural language prompts with live game development.

Instead of copying code snippets or manually placing assets, you simply type what you want—like stacking geometric objects or generating custom metallic shaders—and the AI creates, textures, and organizes the scene live in your viewport. Packed with over 70 built-in developer tools, it works inside active running builds and can even turn your custom C# scripts into autonomous AI actions automatically.

This removes the tedious manual friction of scene assembly, letting game designers and solo developers prototype complex levels at 10x speed.

Game development is evolving from manual 3D manipulation to natural-language world building powered by autonomous coding agents.

Credit: Unity MCP / Open-Source Community

Comment “AI” to get to get the link 🚀

Follow @globalaiforce for daily AI updates

#GameDev #Unity3D #IndieDev #ClaudeAI #AITools

## Research

* Verdict: Valid. The post matches IvanMurzak's open-source Unity-MCP: 70+ tools, runtime support, custom C# tools, and Claude and Cursor support. The link is public, so you don't need to comment. "10x speed" is unsupported marketing.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Unity-MCP (IvanMurzak), AI Game Developer (github.com)](https://github.com/IvanMurzak/Unity-MCP): repo, found by search, verified, medium confidence. The README lists 70+ built-in tools, runtime use in compiled games, custom C# tools via attributes, and Claude and Cursor support, which matches the caption. I did not match it to the reel's visuals.
* [MCP for Unity (CoplayDev) (github.com)](https://github.com/CoplayDev/unity-mcp): repo, found by search, not opened, low confidence. A popular alternative with a similar name, but its README lists 47 tools, so it fits the post less well.

### Key steps

1. Install the plugin: `openupm add com.ivanmurzak.unity.mcp`, or import the .unitypackage installer, or run `npm i -g unity-mcp-cli` then `unity-mcp-cli install-plugin`.
2. Keep the Unity project path free of spaces.
3. Pick an MCP-capable agent (Claude Code is recommended; Cursor and others work).
4. In Unity open Window/AI Game Developer and click Auto-generate skills, or configure MCP manually.
5. Prompt the agent to create or modify scenes, such as objects, shaders or hierarchy.
6. For custom actions: mark a class with [AiToolType] and a method with [AiTool], and add Description attributes.
7. For runtime in a built game: call UnityMcpPluginRuntime.Initialize, register tools with WithToolsFromAssembly, then call Connect. Runtime registers no tools by default.

### Not found

I did not confirm which repo the reel shows. IvanMurzak/Unity-MCP is the best fit by features, and the README header in the frames wasn't checked.
