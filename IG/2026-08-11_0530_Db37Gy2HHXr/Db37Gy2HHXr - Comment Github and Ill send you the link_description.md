---
shortcode: "Db37Gy2HHXr"
url: "https://instagram.com/p/Db37Gy2HHXr/"
type: "Carousel"
author: "godofprompt"
shared: "Aug 11, 2026, 05:30 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Vision Agents: open-source toolkit for video AI agents

A four-slide carousel presenting Vision Agents, an open-source toolkit by Stream for building AI agents that watch, listen to, and react to live video. It lists supported models and providers, sample use cases such as live pose-tracking coaching and robotics, and shows a short code snippet.

Written by claude-haiku-5-5.

## Source

* Link: visionagents.ai
* How to get it: Comment "Github" on the post; the setup guide link is sent to you by comment/DM.

## Caption

Comment “Github” and I’ll send you the link.

Someone open-sourced a toolkit for building AI agents that watch, listen, and understand video in real time.

It’s called Vision Agents, built by Stream. Low latency by design, open source, production ready. It works with your own models and your own edge layer, not locked to one vendor. Supports YOLO, Moondream, Cartesia, Deepgram, ElevenLabs, Gemini, OpenAI, and more, with quick model switching and a simple API.

It’s built for coaching tools with live pose tracking, collaboration apps, real-time avatars, and robotics, anywhere an agent needs to actually see and react to what’s happening, not just process text.

## Research

* Verdict: Valid. Vision Agents is a real open-source (MIT) Stream framework for real-time voice and video agents, and the listed providers match. The link is public, so you don't need to comment to get it.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Vision Agents (GetStream/Vision-Agents) (github.com)](https://github.com/GetStream/Vision-Agents): repo, found by search, not opened, high confidence. Search results and the visionagents.ai page both point to this repo as Stream's open-source video/voice agent framework. I did not open the repo itself.
* [Vision Agents site (visionagents.ai)](https://visionagents.ai): page, in the post, verified, high confidence. Opened it. It describes a low-latency voice and video agent framework with 35+ integrations, including YOLO, Deepgram, ElevenLabs, OpenAI and Gemini.

### Key steps

1. Install with `uv add vision-agents`, adding extras for the plugins you need (Stream, OpenAI, ElevenLabs, Deepgram).
2. Follow the Quickstart on visionagents.ai, which says you can scaffold and run a first agent in under 5 minutes.
3. Pick your LLM, speech and vision providers (e.g. Gemini or OpenAI plus YOLO), then switch models as needed.
4. Use Stream's edge network for low latency, or bring your own edge layer.

### Not found

I didn't open the GitHub README or the Quickstart page, so the exact install and setup commands come from a search summary. The latency figure of about 500ms is Stream's own claim.
