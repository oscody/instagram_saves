---
shortcode: "DaJuh6euSLq"
url: "https://instagram.com/reel/DaJuh6euSLq/"
type: "Reel"
author: "ai.honeycove"
shared: "Jul 21, 2026, 05:28 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# NVIDIA open-source vision model with parallel box decoding

The reel announces an NVIDIA computer vision model said to be up to 10 times faster than leading models, because it predicts an entire bounding box at once through parallel box decoding. It says the model was trained on over 100 million queries and is open-sourced on Hugging Face and GitHub, and shows a Roboflow object detection arena comparing models on a person-detection task.

Written by claude-haiku-5-5.

## Caption

NVIDIA released a new computer vision model that is up to 10 times faster than leading models by using parallel box decoding to predict entire bounding boxes at once. The model was trained on massive datasets and is fully open-sourced on HuggingFace and GitHub. 
#NVIDIA #computervision #parallelboxdecoding #openai #huggingface

## Research

* Verdict: Partly valid. NVIDIA's LocateAnything-3B is real, uses parallel box decoding, and has open weights on Hugging Face. The "10x faster" claim is relative to Qwen3-VL (about 2.5x vs the next-best model), and the weights are non-commercial, so "open source" is loose.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [nvidia/LocateAnything-3B (Hugging Face) (huggingface.co)](https://huggingface.co/nvidia/LocateAnything-3B): tool, found by search, verified, high confidence. Model card opened; it matches the parallel box decoding grounding model, with usage code and an NVIDIA non-commercial license.
* [LocateAnything paper (arXiv 2605.27365) (arxiv.org)](https://arxiv.org/abs/2605.27365): paper, found by search, verified, high confidence. Title and abstract describe Parallel Box Decoding and LocateAnything-Data with over 138M samples (the post says 100M+ queries).
* [NVlabs/Eagle (Embodied) GitHub (github.com)](https://github.com/NVlabs/Eagle/tree/main/Embodied): repo, found by search, not opened, medium confidence. The Hugging Face model card links to it as the code repo. I did not open the repo itself.
* [LocateAnything demo Space (huggingface.co)](https://huggingface.co/spaces/nvidia/LocateAnything): tool, found by search, not opened, medium confidence. A blog post lists it as the official demo. I did not open it.

### Key steps

1. Check you have a GPU with about 8 GB of VRAM, since the model runs in BF16.
2. Run pip install transformers accelerate pillow.
3. Load nvidia/LocateAnything-3B with trust_remote_code=True, bfloat16 and device_map=auto.
4. Open an image and prompt it, for example 'Detect all people in this image'.
5. Call model.generate with generation_mode='hybrid' (or 'fast' or 'slow') and max_new_tokens=8192.
6. Parse the <box> output into pixel coordinates. The card's LocateAnythingWorker class has detect and point methods and parsers for this.
7. For batch runs, use the batch_infer.py CLI from the card.
8. Check the license before any commercial use: the weights are non-commercial.

### Not found

The Roboflow arena comparison shown in the reel was not checked. The 10x throughput figures come from secondary blogs, not the paper's abstract. I did not open the GitHub repo.
