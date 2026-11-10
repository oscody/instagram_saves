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

## Research

* Verdict: Valid. OneCanvas is a real paper with public code and weights from TUM and Huawei affiliates. The depth and pose requirement is correct. The Spotlight label appears only on the project page, not on the NeurIPS poster page.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [OneCanvas project page (baranowskibrt.github.io)](https://baranowskibrt.github.io/onecanvas/): page, found by search, verified, high confidence. Lists the title, TUM and Huawei affiliations, the results and the NeurIPS 2026 Spotlight label (checked earlier in the saved post DeD2Ej-mdrs).
* [OneCanvas paper (arXiv 2606.19253) (arxiv.org)](https://arxiv.org/abs/2606.19253): paper, found by search, verified, high confidence. OneCanvas: 3D Scene Understanding via Panoramic Reprojection, by Baranowski, Chen and Nießner.
* [OneCanvas GitHub repo (github.com)](https://github.com/baranowskibrt/onecanvas): repo, in the vault, verified, high confidence. An earlier saved-post note for the same resource (DeD2Ej-mdrs) opened it and found a README for the panorama canvas read by Qwen3-VL-8B. I did not reopen it this time.
* [OneCanvas NeurIPS poster page (neurips.cc)](https://neurips.cc/virtual/2026/poster/148266): page, found by search, not opened, medium confidence. The search result shows the same title. The earlier note says it lists a poster and does not mention Spotlight.

### Already in the vault

* Vault: `ZAIHub/search - competition ideas by claude.md`: Lists OneCanvas (simplifyinai) as 3D scene understanding research that isn't needed for the Quest entry. The link goes to the earlier post DeD2Ej-mdrs.
* Vault: `ZAIHub/ig repo to review.md`: Mentions the creator simplifyinai only. It doesn't appear to hold the OneCanvas link.

### Already in IG saves

* Same: Web: [OneCanvas: AI answers questions about 3D rooms (instagram.com)](https://instagram.com/p/DeD2Ej-mdrs/) (`DeD2Ej-mdrs`). Same link: OneCanvas GitHub repo.

### Key steps

1. Clone https://github.com/baranowskibrt/onecanvas. Use Python 3.11 with CUDA and follow docs/REPRODUCING.md.
2. Run `pip install -e .` for inference.
3. Run `hf download BaranowskiBrt/OneCanvas-Qwen3-VL-8B`. Keep "Qwen3-VL" in the directory name.
4. Prepare 32 evenly spaced RGB frames, camera-to-world poses, depth in millimetres and intrinsics.
5. Call load_onecanvas_model, then process_vision_and_generate with your question. For questions from the agent's own viewpoint, set center_override and yaw_angle.

### Not found

I did not reopen the GitHub repo or the Hugging Face model page in this session. The repo details come from the earlier note DeD2Ej-mdrs. The post's \"comment AI\" link is a DM giveaway, but the public repo makes it unnecessary.
