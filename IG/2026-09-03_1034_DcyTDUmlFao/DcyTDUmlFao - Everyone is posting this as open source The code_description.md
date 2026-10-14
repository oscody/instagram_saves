---
shortcode: "DcyTDUmlFao"
url: "https://instagram.com/reel/DcyTDUmlFao/"
type: "Reel"
author: "billy.coder"
shared: "Sep 03, 2026, 10:34 AM"
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

## On screen text

Open Source.
Until You Sell
OM
boxes in training data
ITDRAWS
ina
DAY
Until You Sell.
5.3
DOVS
boxes per second
EVER
Parall
GEORGE
MODEL
SPELLS
VER
T-U
straight off their READE
Model LicenseNVIDIA License
Apache 2.0
Code License
wo badges,
two different licences
APACHE
WEIGHTS
