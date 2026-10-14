---
shortcode: "DddNPtGGayH"
url: "https://instagram.com/p/DddNPtGGayH/"
type: "Carousel"
author: "simplifyinai"
shared: "Sep 19, 2026, 08:25 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# EgoExoMoCap: free motion capture from smart glasses

The post presents EgoExoMoCap, a free, open-source tool that captures full-body motion from two or more people wearing smart glasses, with no cameras or markers. It explains the tool's core idea and shows its installation commands and method diagram.

Written by claude-haiku-5-5.

## What it teaches

1. Create a Python 3.10 environment: conda create -n egoexomocap python=3.10 -y
2. Activate it: conda activate egoexomocap
3. Install PyTorch matching your CUDA version first
4. Install the dependencies: pip install -r requirements.txt
5. How the method works: each person's glasses record their own point of view, and head and wrist tracking gives a rough starting pose
6. The model finds the same person in the other glasses' views and fuses the clearest views together, so accuracy holds when someone briefly leaves view

## Source

* How to get it: Comment "AI" on the post; the link is sent by DM

## Caption

Comment “AI” to get the link and the full list of free AI resources.

This tool can capture any motions without any cameras and markers.

It’s called EgoExoMoCap, and it can capture full-body motion from nothing but two or more people wearing smart glasses.

So this is how it works:
> each person’s glasses see their own pov
> head and wrist tracking gives a rough starting pose
> the model finds that same person inside the other glasses’ views and fuses the clearest ones together
> accuracy holds even when someone drops out of view for a while, since the other glasses cover the gap.

100% free & open-source.
