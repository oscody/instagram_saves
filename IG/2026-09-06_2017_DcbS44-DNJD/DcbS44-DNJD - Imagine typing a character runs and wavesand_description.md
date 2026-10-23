---
shortcode: "DcbS44-DNJD"
url: "https://instagram.com/p/DcbS44-DNJD/"
type: "Carousel"
author: "activeprogrammer"
shared: "Sep 06, 2026, 08:17 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# kimodo.cpp: text-to-3D motion on local hardware

The post introduces kimodo.cpp, a community C++ port of NVIDIA's Kimodo model that turns a text description into skeletal 3D character motion locally on CPU or Vulkan, without a full PyTorch and CUDA setup. Screenshots show a "Text to motion" app where prompts like "A person does a star jump" generate animations that can be replayed and edited.

Written by claude-haiku-5-5.

## Source

* Link: kimodo.cpp

## Caption

Imagine typing “a character runs and waves”—and getting a 3D animation directly on your computer. 🤯

A developer created kimodo.cpp, a community C++ port of NVIDIA’s Kimodo animation model.

It transforms plain-language descriptions into skeletal motion locally using CPU or Vulkan—without requiring a full PyTorch and CUDA setup.

The motion can then be applied to compatible 3D characters for games, apps and animation projects.

It’s still an early, research-only project—but the possibilities are wild.

Would you use a text prompt to animate your next 3D character? 👀

Follow @activeprogrammer for more AI and programming stories.

Credit: jichiep / NVIDIA Research

#ai #nvidia #3danimation #programming  #gamedev

## Research

* Verdict: Valid. The repo exists and matches the post: a C++/GGML port of NVIDIA Kimodo that runs on CPU or Vulkan. The "research-only" caveat holds for one model, SMPL-X RP; the SOMA and G1 models use the NVIDIA Open Model License.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [kimodo.cpp (localai-org) (github.com)](https://github.com/localai-org/kimodo.cpp): repo, in the vault, verified, high confidence. The README describes a GGML/C++ port of NVIDIA Kimodo text-to-motion with CPU and Vulkan backends and a web demo. It says the code is Apache-2.0, and the SMPL-X RP weights are restricted to non-production R&D.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Already lists the GitHub link, marked done on 2026-09-19, with the note 'creates animation - only' and a ChatGPT share link for installation.

### Key steps

1. Install a C++23 compiler, CMake 3.25+, Ninja, Python 3 with huggingface_hub, and the Vulkan loader and headers if you want Vulkan.
2. Clone the repo, then run: git submodule update --init --recursive
3. Download weights: scripts/download_gguf_weights.sh --output "$PWD" --model soma-rp-v1.1
4. Build with: cmake --preset debug, then cmake --build --preset debug. Use the release preset for speed.
5. Optionally run the tests: ctest --preset debug
6. Start the web demo with: go run ./demo -addr 0.0.0.0:8094, then open http://localhost:8094.
7. Type a prompt such as 'A person does a star jump'. Each result also exports a skeleton-only animation.glb.
8. To use it from code, call kimodo_generate (text) or kimodo_generate_embedding (4096 F32 values) in include/kimodo/kimodo_capi.h.

### Not found

The post's wording about applying the motion to compatible 3D characters is not backed by the repo. The README lists skinned-mesh GLB export as not yet implemented, so you get skeleton-only output. The README's install steps are for Linux, and I did not check macOS.
