---
shortcode: "DcyTDUmlFao"
url: "https://instagram.com/reel/DcyTDUmlFao/"
type: "Reel"
author: "billy.coder"
shared: "Sep 03, 2026, 10:34 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# NVIDIA LocateAnything: open code, restricted weights

The post describes NVIDIA's LocateAnything 3B grounding model, which predicts whole bounding boxes in one step, and says its code is Apache 2.0 while its weights fall under the NVIDIA License, limited to research or evaluation. It also notes that the released 3B weights don't support visual prompt inference out of the box, according to the repo's README.

Written by claude-haiku-5-5.

## What it teaches

1. Check the licence of the code and the model weights separately, since a repo can carry two different licences.
2. Read the model licence's use terms before building a product, because the NVIDIA License here restricts use to research or evaluation.

## Source

* How to get it: Comment BOXES to receive the repo and the licence by DM

## Caption

Everyone is posting this as open source. The code is. The weights are not.

NVIDIA released LocateAnything, a 3B grounding model that predicts a whole bounding box in one step instead of spelling out the coordinates token by token.

On a single H100 at batch size 1 it does 12.7 boxes per second. Qwen3-VL does 1.1 on the same measure. Against Rex-Omni it is 2.5x rather than 10x, so the figure depends entirely on what you compare it to.

Trained on 12M unique images, 138M language queries and 785M boxes. Accepted to ECCV 2026.

Licence, because nobody else prints it. The code in the repo is Apache 2.0. The weights ship under the NVIDIA License, and section 3.3 limits use to research or evaluation purposes only. You cannot put it in a product you sell.

One thing the posts leave out: the currently released 3B weights do not support visual prompt inference out of the box. That is the repo's own note.

Your model was never slow at looking. It was slow at typing.

Comment BOXES and I will send you the repo and the licence.

#opensourceproject #githubprojects #computervision #objectdetection #nvidia #machinelearning #aitools #devtools #eccv

## Research

* Verdict: Valid. The repo and model card confirm the post: Apache 2.0 code, NVIDIA License weights, 12.7 BPS on H100, and no out-of-the-box visual prompt support. The post's "research or evaluation" wording is looser than the model card, which says non-commercial, academic and non-profit research only. That is stricter, so the conclusion still holds. The ECCV claim was not confirmed.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [NVlabs/Eagle – Embodied (LocateAnything code) (github.com)](https://github.com/NVlabs/Eagle/tree/main/Embodied): repo, found by search, verified, high confidence. README lists Apache 2.0 code, a separate NVIDIA model license, the 12.7 BPS vs Qwen3-VL 1.1 and Rex-Omni 5.0 figures, and the visual prompt note.
* [LocateAnything-3B model card (huggingface.co)](https://huggingface.co/nvidia/LocateAnything-3B): repo, found by search, verified, high confidence. Weights under the NVIDIA License, non-commercial and academic/non-profit research only; install and inference steps given.

### Key steps

1. Clone the repo: git clone https://github.com/NVlabs/Eagle.git eagle && cd eagle/Embodied && pip install -e .
2. Install PyTorch for your CUDA version. MagiAttention is optional and works only on Hopper or Blackwell GPUs.
3. Download the weights: hf download nvidia/LocateAnything-3B
4. Quick start: load LocateAnythingWorker("nvidia/LocateAnything-3B") and call detect, ground_multi, detect_text, ground_gui or point.
5. For batch runs on A100 or L40, use: python batch_infer.py --model . --attn la_flash --scheduler pipeline --batch-size 4 --image <path> --query "<query>"
6. Read the output boxes as <box><x1><y1><x2><y2></box> with coordinates in 0–1000. Divide by 1000 for relative coordinates.
7. Check LICENSE_MODEL before any commercial use. Don't expect visual prompt inference from the released weights.

### Not found

I did not check the ECCV 2026 acceptance, the training data figures (12M images, 138M queries, 785M boxes) or the BPS benchmark details in document/RESULTS.md. The model card doesn't mention ECCV. The post says "section 3.3" of the licence; I did not open the licence text to check it. The 10x figure is against Qwen3-VL and the 2.5x figure is against Rex-Omni, which matches the post's point. The BOXES comment/DM is not needed, since the repo is public.
