---
shortcode: "DdrPLe8AGxt"
url: "https://instagram.com/reel/DdrPLe8AGxt/"
type: "Reel"
author: "githubsignals"
shared: "Sep 25, 2026, 05:41 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# AI Texture Painting on 3D Models in ComfyUI

Presents the open-source ComfyUI Yedp UV Painter node, which generates AI textures for separate parts of a 3D mesh and lets you sketch hard-surface details onto the UV map with a live 3D preview. Screenshots show its README, a generation stack of face, belt and pauldron layers, and a ComfyUI node graph.

Written by claude-haiku-5-5.

## Source

* Link: yedp123/comfyui-yedp-uv-painter

## Caption

Paint AI Textures Directly Onto 3D Models in ComfyUI 

Paint textures directly onto your 3D models using AI, right inside ComfyUI, without ever leaving your browser. ComfyUI Yedp UV Painter lets you isolate specific parts of a complex mesh, like a belt or a shoulder pad, and generate unique textures for each one independently, just like working with layers in Photoshop. The coolest part is the live sketch tool: draw hard-surface details directly on the two-dimensional map and watch them project onto the three-dimensional geometry in real-time. This is perfect for artists who want precise control without needing a massive graphics card, as it runs smoothly on modest hardware.

Open source: yedp123/comfyui-yedp-uv-painter

Follow for more open source project drops.

#ComfyUI #3DArt #AIArt #UVMapping

## Research

* Verdict: Valid. The repo exists and matches the post: a ComfyUI node for layered AI texturing of 3D model parts, with a live canny sketch preview, designed for 8GB VRAM. It's labeled experimental.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [yedp123/comfyui-yedp-uv-painter (github.com)](https://github.com/yedp123/comfyui-yedp-uv-painter): repo, in the post, verified, high confidence. README describes a non-destructive 3D-to-2D AI texturing node with layers, a live canny sketch preview and 8GB VRAM SDXL support. It is MIT licensed.

### Key steps

1. Clone the repo into ComfyUI/custom_nodes and restart ComfyUI. The nodes appear under Yedp/Texture.
2. Get the recommended models: a GGUF SDXL UNet (Juggernaut XL Q5_K_M), ControlNet++ Union SDXL, SDXL VAE FP16 fix (needed to avoid black images), and the clip_g and clip_l text encoders.
3. Add the Yedp UV Painter node and load an FBX, OBJ or GLTF model.
4. Use the Select (Mask) tool to click the UV islands or faces that make up one material zone.
5. Name the layer and enter its generation prompt.
6. Optionally use the Draw (Canny) tool to sketch hard-surface lines.
7. Queue the prompt. The result shows in the Gen Stack tab.
8. Repeat for other layers, lock or hide layers as needed, then export the texture.

### Not found

Nothing outside the README was checked. I didn't test the node or view the video.
