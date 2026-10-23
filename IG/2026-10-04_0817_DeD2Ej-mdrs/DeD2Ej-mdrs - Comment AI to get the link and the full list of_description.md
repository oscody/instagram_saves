---
shortcode: "DeD2Ej-mdrs"
url: "https://instagram.com/p/DeD2Ej-mdrs/"
type: "Carousel"
author: "simplifyinai"
shared: "Oct 04, 2026, 08:17 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# OneCanvas: AI answers questions about 3D rooms

The post presents OneCanvas, a NeurIPS 2026 Spotlight paper with public code, which merges video frames of a room into one panorama so an image AI can answer questions about 3D space. It claims new state-of-the-art results on spatial reasoning benchmarks, answers from any viewpoint, and says the method needs depth data and camera positions.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the post says the link and the list of free AI resources are sent after commenting (check DMs).

## Caption

Comment “AI” to get the link and the full list of free AI resources.

This AI answers questions about 3D rooms from a few camera views.

It’s called OneCanvas, a NeurIPS 2026 Spotlight paper with public code and model.

It merges video frames of a room into one panorama, so an ordinary image AI can answer questions about 3D space.

→ New state of the art on spatial reasoning benchmarks

→ Answers from any viewpoint, including the AI’s own position in the room

→ Needs depth data and camera positions, not just plain video

## Research

* Verdict: Valid. OneCanvas is a real paper with public MIT code and a Hugging Face model. The project page lists it as NeurIPS 2026 Spotlight, and the method needs posed RGB-D frames, as the post says.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [OneCanvas GitHub repo (github.com)](https://github.com/baranowskibrt/onecanvas): repo, found by search, verified, high confidence. README describes projecting posed RGB-D frames onto a panoramic canvas read by Qwen3-VL-8B, with SQA3D, VSI-Bench and SPBench evaluation.
* [OneCanvas project page (baranowskibrt.github.io)](https://baranowskibrt.github.io/onecanvas/): page, found by search, verified, high confidence. Lists 'NeurIPS 2026 (Spotlight)' and links the code, paper and video.
* [OneCanvas paper (arXiv 2606.19253) (arxiv.org)](https://arxiv.org/abs/2606.19253): paper, found by search, verified, high confidence. OneCanvas: 3D Scene Understanding via Panoramic Reprojection, by Baranowski, Chen and Nießner.
* [OneCanvas model weights (Hugging Face) (huggingface.co)](https://huggingface.co/BaranowskiBrt/OneCanvas-Qwen3-VL-8B): other, found by search, not opened, medium confidence. The GitHub README gives this ID in its `hf download` command. I did not open the page itself.

### Already in the vault

* Vault: `ZAIHub/search - competition ideas by claude.md`: Lists OneCanvas as 3D scene understanding research that isn't needed for the Quest entry, since WebXR already provides planes and meshes.
* Vault: `ZAIHub/ig repo to review.md`: Mentions the creator simplifyinai. I did not check whether it holds the resource.

### Key steps

1. Clone https://github.com/baranowskibrt/onecanvas and use Python 3.11 with CUDA. Follow the pinned environment in docs/REPRODUCING.md.
2. Run `pip install -e .` for inference. Use `pip install -e '.[train,eval,data]'` for evaluation and training.
3. Download the weights with `hf download BaranowskiBrt/OneCanvas-Qwen3-VL-8B`. Keep "Qwen3-VL" in the directory name. The directory must include lineage.json, resolved_config.json and depth_embedding.pt.
4. Set ONECANVAS_DATA_ROOT and ONECANVAS_CHECKPOINT_DIR.
5. Prepare the input: 32 evenly spaced RGB frames, camera-to-world poses [N,4,4], depth in millimetres [N,H,W], and intrinsics.
6. Call load_onecanvas_model(CKPT), then process_vision_and_generate(...) with the question and the inputs. For questions from the agent's own viewpoint, set center_override and yaw_angle.
7. To reproduce the benchmarks, run training/run_benchmarks.py with --datasets sqa3d, vsi_bench or spbench.

### Not found

The Hugging Face model page was not opened directly. The NeurIPS poster page lists the paper as a poster and does not mention Spotlight. Only the project page says Spotlight. The post's "comment AI" link is a DM giveaway, but the public repo makes it unnecessary.
