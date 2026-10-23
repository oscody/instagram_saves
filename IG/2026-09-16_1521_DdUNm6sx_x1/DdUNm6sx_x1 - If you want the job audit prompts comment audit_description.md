---
shortcode: "DdUNm6sx_x1"
url: "https://instagram.com/reel/DdUNm6sx_x1/"
type: "Reel"
author: "angus.sewell"
shared: "Sep 16, 2026, 03:21 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Auditing job tasks against Anthropic's Economic Index

A prompt for an AI assistant to audit US computer programmer tasks against Anthropic's Economic Index automation and augmentation data, using the O*NET task list. The full prompt is only available by comment, and only the first of two prompt pages is shown on screen.

Written by claude-haiku-5-5.

## What it teaches

1. Download Anthropic's Economic Index dataset and read its data documentation, then download the AEI Claude csv for the release.
2. Filter to GLOBAL, May 2026, category_name=onet, hierarchy_level=0.
3. Pivot the automation and augmentation percentage columns by node_external_id (Task ID), then save the source and filtered files and cite dates and URLs.
4. Download the O*NET task statements and occupation data for 15-1251.00, listing every official task with its wording unchanged.
5. Join the O*NET tasks to the Anthropic data by Task ID, check uniqueness, and show unmatched tasks without forcing matches.
6. For each matched task, calculate automation share as A/(A+U), skipping zero denominators, and sort descending.
7. Read A>U as automation-leaning and U>A as augmentation-leaning, treating the results as usage patterns rather than job-loss probabilities or proof of AI performance.
8. Treat any explanations for missing cells as untested hypotheses.

## Source

* Link: https://huggingface.co/datasets/Anthropic/EconomicIndex
* How to get it: Full prompts are sent by comment: comment "audit"

## Caption

If you want the job audit prompts comment “audit” and I’ll send it your way

There is some real data to show this was an orchestrated PR campaign but that doesn’t mean they don’t genuinely believe the things they say. It’s like a weird SF culture at this point. Idk man I don’t live in SF but every person I know who does seems to be low key preparing for the apocalypse. 

#ai #buildwithai #vibecoding

## Research

* Verdict: Partly valid. The dataset is real and matches the workflow (2026-06-26 release has May 2026 data, GLOBAL geo, onet category, level 0 tasks, automation and augmentation percentages). The exact prompt is only sent by comment, and the post's caption is opinion about an "orchestrated PR campaign".
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Anthropic Economic Index dataset (Hugging Face) (huggingface.co)](https://huggingface.co/datasets/Anthropic/EconomicIndex): other, in the post, verified, high confidence. Link in the post. Page lists the 2026-06-26 release, which has the data documentation and aei_claude_ai CSV the steps use.
* [Release 2026-06-26 data documentation (huggingface.co)](https://huggingface.co/datasets/Anthropic/EconomicIndex/raw/main/release_2026_06_26/data_documentation.md): guide, found by search, verified, high confidence. Documents node_external_id, hierarchy_level 0 = Task, the automation and augmentation pct metrics, GLOBAL geo_id, and April/May 2026 data.

### Key steps

1. Open release_2026_06_26 on the Hugging Face dataset and read data_documentation.md.
2. Download the aei_claude_ai_<date>.csv file from release_2026_06_26/data.
3. Filter to geo_id=GLOBAL, the May 2026 date range, category_name=onet and hierarchy_level=0.
4. Keep metric_id collaboration_bucket_automation_pct and collaboration_bucket_augmentation_pct. Pivot them by node_external_id (O*NET task ID).
5. Download O*NET task statements for 15-1251.00 (Computer Programmers) from onetcenter.org, with the wording unchanged.
6. Join to the Anthropic data on task ID. Check the IDs are unique, and list unmatched tasks without forcing matches.
7. Compute automation share = A/(A+U), skipping zero denominators, and sort descending.
8. Treat the results as usage patterns, not job-loss odds or proof of AI performance.

### Not found

The full prompt text, which is sent only by comment ("audit"). The steps above are rebuilt from the post and the dataset documentation. I did not open the CSV, and I did not check the "orchestrated PR campaign" claim.
