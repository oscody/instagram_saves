---
shortcode: "DdJUHolm52S"
url: "https://instagram.com/p/DdJUHolm52S/"
type: "Carousel"
author: "simplifyinai"
shared: "Sep 11, 2026, 05:58 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Alibaba's ABot-Recon: open-source video-to-3D model

The post introduces ABot-Recon, an open-source 3D scene reconstruction model from Amap CV Lab (Alibaba) that works from a normal RGB video. It highlights a fixed 12-frame local window, lower peak memory, and a Hugging Face demo, with the full resource list gated behind a comment.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the link and resource list are sent by DM

## Caption

Comment “AI” to get the link and the full list of free AI resources.

Alibaba just open-sourced an AI that turns any video into a 3D scene, no depth sensor needed.

It’s called ABot-Recon, from Amap CV Lab (Alibaba).

Most streaming reconstruction systems keep growing their memory buffer as a video gets longer, so they slow down the longer they run. This one doesn’t.

→ Reconstructs scenes spanning 10,000+ frames using only a fixed 12-frame local window, so speed and memory stay flat no matter how long the video runs

→ Cuts peak memory use to roughly a third of comparable methods, making real-time reconstruction possible on regular consumer hardware

→ Only needs a normal RGB video, no depth sensor, no camera calibration

One thing to know: running it locally needs conda, PyTorch, and CUDA, but there’s a live Hugging Face demo if you just want to try it first.

100% Free. Open Source.
