---
shortcode: "DXmWHzIExeq"
url: "https://instagram.com/reel/DXmWHzIExeq/"
type: "Reel"
author: "tpadumke"
shared: "May 02, 2026, 06:36 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Run Claude Code for free with a local proxy

The post shows a free setup for Claude Code that uses the free-claude-code GitHub repo as a local proxy to a free model backend, with NVIDIA NIM as the recommended option. It also mentions OpenRouter and local options (Ollama, LM Studio) and promotes a setup guide available by comment.

Written by claude-haiku-5-5.

## What it teaches

1. Get the free-claude-code repo by Alishahryar1 from GitHub and install its prerequisites (uv and the proxy).
2. Sign up at build.nvidia.com and copy your NVIDIA NIM API key.
3. Paste the API key into the one config file in the repo.
4. Start the proxy, which runs on your machine on port 8082.
5. Open two terminals: run the proxy in one and Claude Code in the other.
6. Claude Code talks to the proxy as if it were Anthropic, and the proxy forwards requests to the free model you chose.
7. Optionally, point the proxy at OpenRouter for free DeepSeek R1, or run it fully local through Ollama or LM Studio if you have a capable GPU.

## Source

* Link: https://github.com/Alishahryar1/free-claude-code
* How to get it: The setup guide with the exact two terminal commands and NVIDIA signup link is offered by commenting NVIDIA.

## Caption

Claude Code without the $20–$200 a month subscription. The trick is a 12,332-star GitHub repo by Alishahryar1 called free-claude-code. It’s a tiny Python proxy that sits on your machine on port 8082. Claude Code talks to it like it’s Anthropic, and the proxy forwards your requests to whichever free model you picked.

The recommended free backend is NVIDIA NIM. NVIDIA gives you 40 LLM requests every minute at zero cost, which covers a full day of coding. You sign up at build.nvidia.com, grab the API key, paste it into one config file, and start the proxy.

You open two terminals — proxy on the left, Claude Code on the right. The interface is the same — same commands, same agents, same tool calls. The only thing that changes is the bill at the end of the month.

You can also point it at OpenRouter for free DeepSeek R1. Or run it fully local through Ollama or LM Studio if you’ve got a halfway decent GPU. Zero internet dependency, zero rate limits, and total privacy. The repo also ships a Discord bot so you can send Claude Code tasks from your phone.

The repo has 12,332 stars on GitHub and was last updated today. Anthropic isn’t going to advertise this because it cannibalizes their plans. The workaround lives on GitHub for anyone who looks for it.

I put together a free setup guide with the exact two terminal commands and the NVIDIA signup link. Comment NVIDIA and I’ll send it over.

#ClaudeCode #AI #FreeAI #DevTools #Coding
