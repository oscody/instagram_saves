---
shortcode: "DdqpiDaGdUF"
url: "https://instagram.com/p/DdqpiDaGdUF/"
type: "Carousel"
author: "simplifyinai"
shared: "Sep 25, 2026, 05:40 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Free open-source tool tracks object relationships in browser

The post introduces RelateAnything, a free, open-source model that predicts how objects in an image or video relate to each other. It says the model runs entirely in the browser with no install.

Written by claude-haiku-5-5.

## What it teaches

1. Open http://maelic.github.io/RelateAnythingProject/demo in a browser.
2. Upload a photo or video, or use your webcam.
3. The model runs entirely in your browser, so nothing needs to be installed.

## Source

* Link: http://maelic.github.io/RelateAnythingProject/demo

## Caption

Comment “AI” to get the link and the full list of free AI resources.

this ai can track how every object relates to each other. 100% free.

relateanything is a free, open-source model that takes an image/video + a set of regions (boxes or masks, from any detector)

try it with zero install:

> go to http://maelic.github.io/RelateAnythingProject/demo
> upload a photo or video, or use your webcam
> it runs entirely in your browser

100% free & open-source.

## Research

* Verdict: Valid. The demo exists and runs in the browser, and the code and weights are public. One nuance: it first shows a precomputed sample, and you must click "Run it live" to download about 157 MB of models before it works on your own input.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [RelateAnything browser demo (maelic.github.io)](http://maelic.github.io/RelateAnythingProject/demo): tool, in the post, verified, high confidence. Opened it. It is an open-vocabulary scene-graph demo that takes an image, video or webcam and runs locally in the browser.
* [RelateAnything project page (maelic.github.io)](https://maelic.github.io/RelateAnythingProject/): page, found by search, verified, high confidence. Opened it. It links to the repo, the Hugging Face weights and dataset, and cites the paper by Maëlic Neau.
* [RelateAnything GitHub repo (github.com)](https://github.com/Maelic/RelateAnything): repo, found by search, not opened, medium confidence. Linked from the project page, but I did not open the repo itself.
* [RelateAnything weights on Hugging Face (huggingface.co)](https://huggingface.co/collections/maelic/relateanything): other, found by search, not opened, medium confidence. Linked from the project page; not opened.

### Key steps

1. Open the demo page. It first shows a precomputed graph for a sample photo.
2. Click "Run it live" to download the models: about 105 MB for relation, 24 MB for the detector and 28 MB for the WASM runtime.
3. Choose an image, a video or the webcam as input.
4. Edit the relation word list (for example "person riding horse") and adjust the sliders.
5. For your own pipeline, use the GitHub repo. The model exports to one ONNX graph, and the predicate list is an input tensor.

### Not found

I did not open the GitHub README, so I have no install commands. I also did not find the arXiv preprint link. The vault has no note on RelateAnything.
