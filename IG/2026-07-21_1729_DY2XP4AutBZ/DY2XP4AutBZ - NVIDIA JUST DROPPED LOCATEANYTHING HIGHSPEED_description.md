---
shortcode: "DY2XP4AutBZ"
url: "https://instagram.com/reel/DY2XP4AutBZ/"
type: "Reel"
author: "marc.kaz"
shared: "Jul 21, 2026, 05:29 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# NVIDIA LocateAnything visual search model announcement

The reel announces NVIDIA's LocateAnything, a visual grounding model that finds the location of an object in an image from a text prompt. It lists features (10x dense-detection speedup, Qwen2.5-3B + Moon-ViT backbone, Fast/Slow/Hybrid modes, 138M training samples) over demo clips with bounding boxes on conveyor parcels, sea animals and F1 cars.

Written by claude-haiku-5-5.

## Source

* Link: https://research.nvidia.com/labs/lpr/locate-anything/

## Caption

🚨 NVIDIA JUST DROPPED LOCATEANYTHING HIGH-SPEED VISUAL SEARCH ENGINE

You give it a text prompt and it instantly pinpoints the exact location of any object in an image.

Ships with:
• 10x speedup for dense object detection
• Qwen2.5-3B + Moon-ViT backbone
• Fast / Slow / Hybrid modes
• Trained on 138M samples (UI, docs & generic grounding)

Insanely fast and accurate visual grounding from NVIDIA.

👉 https://research.nvidia.com/labs/lpr/locate-anything/

## Research

* Verdict: Partly valid. LocateAnything is real, open and from NVIDIA, and the features match the project page. The "10x" speedup holds only against Qwen3-VL; the overall gain is about 2.5x. "Just dropped" is stale, since the release was around June 2026.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [LocateAnything project page (research.nvidia.com)](https://research.nvidia.com/labs/lpr/locate-anything/): page, in the post, verified, high confidence. Opened it. It describes Fast/Slow/Hybrid modes, Moon-ViT + Qwen2.5, 138M queries and the 12.7 vs 1.1 BPS comparison with Qwen3-VL.
* [nvidia/LocateAnything-3B (Hugging Face) (huggingface.co)](https://huggingface.co/nvidia/LocateAnything-3B): tool, found by search, not opened, high confidence. The project page and search results name it as the official 3B weights, built on Qwen2.5-3B-Instruct. I did not open it.
* [NVlabs/Eagle Embodied (code) (github.com)](https://github.com/NVlabs/Eagle/tree/main/Embodied): repo, found by search, not opened, medium confidence. The project page and the model card point to this as the code location. I did not open it.
* [LocateAnything demo Space (huggingface.co)](https://huggingface.co/spaces/nvidia/LocateAnything): tool, found by search, not opened, medium confidence. The project page lists it as the demo. I did not open it.

### Key steps

1. Try the demo Space at huggingface.co/spaces/nvidia/LocateAnything.
2. Download the weights from nvidia/LocateAnything-3B on Hugging Face.
3. Get the inference code from NVlabs/Eagle, in the Embodied folder, and follow its README.
4. Pick a decoding mode: Hybrid is the default, Fast is the quickest, and Slow is the most precise.
5. Give it an image and a text query, such as an object name, to get bounding boxes or points.

### Not found

The project page has no install or usage instructions, and I did not open the GitHub repo or the Hugging Face model card. The vault has no note on LocateAnything itself. The notes that matched only mention the creator marc.kaz.
