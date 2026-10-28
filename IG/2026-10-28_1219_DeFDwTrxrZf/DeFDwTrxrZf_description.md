---
shortcode: "DeFDwTrxrZf"
url: "https://instagram.com/reel/DeFDwTrxrZf/"
type: "Reel"
author: "simplifyinai"
shared: "Oct 28, 2026, 12:19 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-28"
---

# OneCanvas: Teaching image AI to understand 3D rooms

The post presents OneCanvas, a research method that lets a regular vision-language model answer spatial questions about a whole 3D room by reading one merged panorama built from video frames, depth data and camera positions. It is described as a NeurIPS 2026 Spotlight paper from TUM and Huawei, with code and model said to be public.

Written by claude-haiku-5-5.

## What it teaches

1. Collect video frames of a room together with depth data and camera positions; plain video alone is not enough.
2. Merge the frames, depth and camera positions into one single panorama of the whole space.
3. Pass that panorama to a normal vision-language model like any other image.
4. Ask the model questions about distance, direction and where things are, from any viewpoint in the room, including its own position.

## Source

* How to get it: Comment "AI" to get the link and the full list of free AI resources (per the caption)

## Caption

Comment “AI” to get the link and the full list of free AI resources.

OneCanvas teaches a regular image AI to understand an entire 3D room.

It takes video frames of a room, along with depth data and camera positions, and merges them into one single panorama of the whole space.

A normal vision-language model then reads that panorama like any other image, and answers questions about distance, direction, and where things are.

It can answer from any viewpoint in the room, including the AI’s own position, which is useful for robots figuring out where they are.

It sets a new state of the art on major spatial reasoning benchmarks, using far less compute than models with custom 3D encoders.

One thing to know: it needs depth data and camera positions, not just plain video.

A NeurIPS 2026 Spotlight paper from TUM and Huawei. Code and model are public.
