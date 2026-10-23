---
shortcode: "DdlAM5CDUFS"
url: "https://instagram.com/reel/DdlAM5CDUFS/"
type: "Reel"
author: "githubsignals"
shared: "Sep 22, 2026, 07:40 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Open-source DLSS 5 reimplementation in Vulkan

The reel presents OpenDLSS-NR, a Vulkan reimplementation of NVIDIA's DLSS 5 Neural Rendering network that is claimed to match the original bit for bit. Screen recordings of the GitHub README show an NR off/on comparison on a cowboy scene plus the network's architecture and inputs and outputs.

Written by claude-haiku-5-5.

## Source

* Link: maanhimself/opendlss-nr

## Caption

This Open-Source DLSS 5 Reimplementation Recreates NVIDIA Neural Rendering 

NVIDIA just showed that AI can invent new details in your game, and someone built the exact math to run it on your own computer. This project is a Vulkan reimplementation of the DLSS 5 Neural Rendering network, meaning it takes a blurry frame and generates sharp new pixels from scratch. The crazy part is that it matches the original output perfectly, down to the single byte. It is not just a filter that makes things look nicer. It is a heavy math puzzle solved on your graphics card to make a 4K image from a 1080p input.

Open source: maanhimself/opendlss-nr

Follow for more open source project drops.

#NVIDIA #DLSS #GraphicsProgramming #Vulkan #NeuralRendering

## Research

* Verdict: Partly valid. The repo exists and matches the post. The bit-exact claim can't be checked from the repo, because the reference captures aren't included and you must supply the model weights yourself. The reel also frames it as a 1080p→4K upscaler, but the README says input and output have the same resolution.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [maanhimself/opendlss-nr (github.com)](https://github.com/maanhimself/opendlss-nr): repo, in the post, verified, high confidence. README describes a Vulkan reimplementation of the DLSS 5 neural rendering network, MIT-licensed, with a claim of bit-exact output against the original.

### Key steps

1. You need Windows and an NVIDIA Ada or newer GPU. The driver must expose VK_KHR_cooperative_matrix, VK_NV_cooperative_matrix2, VK_EXT_shader_float8 and VK_NV_cuda_kernel_launch.
2. Install Visual Studio 2022 or later with the C++ x64 toolset, plus git and Python 3.
3. Run scripts\fetch_tools.ps1 to download glslang, Vulkan-Headers, volk, CMake and Ninja.
4. Run scripts\build.ps1 to build build\dlss5vk.exe.
5. Supply your own model weights. They are not in the repo. Pass them with --model <dir>, set DLSS5VK_MODEL, or place them in models\nr.
6. Run dlss5vk.exe with bench, profile, parity or verify. parity needs a --fixture directory of captures, which the repo doesn't include.
7. For the demo, run fetch_filament.ps1, build_filament.ps1 and build_demo.ps1. This needs Node.js and Pillow, about 15 minutes, and about 6 GB of disk.

### Not found

I couldn't verify the bit-exact claim myself. I also didn't find where to get the NVIDIA weights or the parity captures.
