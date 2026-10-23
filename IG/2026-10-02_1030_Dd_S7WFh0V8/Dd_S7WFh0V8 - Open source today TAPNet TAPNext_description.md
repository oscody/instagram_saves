---
shortcode: "Dd_S7WFh0V8"
url: "https://instagram.com/reel/Dd_S7WFh0V8/"
type: "Reel"
author: "index.opensource"
shared: "Oct 02, 2026, 10:30 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Open source today: TAPNet / TAPNext++

Shows the TAPNext++ point tracker from Google DeepMind on cheetah and octopus clips, with rainbow point overlays that vanish when a pole hides the cheetah and return when it reappears. It ends by asking which element (particles, strokes or stickers) viewers would attach to a moving subject.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/google-deepmind/tapnet/tree/730cda1c730877cfedbe01bf87fb1cadb78a565d

## Caption

Open source today: TAPNet / TAPNext++
Pick points in one frame and follow their positions through a video.

The model updates a memory of the points and predicts where they are and whether they are visible. Xity ran Google DeepMind's checkpoint on Apple MPS.

The cheetah and octopus footage comes from CC0 files on Wikimedia Commons. Query points, rainbow drawing and trail filtering are ours; the points themselves are the model's output. This edit is not a tracking benchmark.

What would you attach to a moving subject: particles, strokes or stickers?

The cover is an AI-generated illustration based on the original source material.

오늘 소개할 오픈소스는 TAPNet / TAPNext++입니다.
한 프레임에서 고른 점의 위치를 영상 속에서 따라가요.

모델이 점의 기억을 갱신하고 위치와 보이는지 여부를 예측합니다. Xity가 Google DeepMind의 체크포인트를 Apple MPS에서 실행했어요.

치타와 문어 입력 영상은 Wikimedia Commons의 CC0 파일입니다. 질의 점 선택, 무지개 그림, 궤적 필터는 저희 구성이고 점의 위치는 모델 출력이에요. 이번 편집은 추적 성능 측정이 아닙니다.

움직이는 대상에 입자, 선, 스티커 중 무엇을 붙여 보고 싶으신가요?

📎 Source / 원본:
https://github.com/google-deepmind/tapnet/tree/730cda1c730877cfedbe01bf87fb1cadb78a565d
Original creators / 원작: Google DeepMind
✳︎ License / 라이선스: Apache-2.0 (code and linked pretrained checkpoints)
https://github.com/google-deepmind/tapnet/blob/730cda1c730877cfedbe01bf87fb1cadb78a565d/README.md#license-and-disclaimer
Footage / 입력 영상: CC0
Cheetah / 치타: HAV0Xunderscore
https://commons.wikimedia.org/wiki/File:Rozi_the_cheetah_running_at_the_Cincinnati_Zoo.webm
Octopus / 문어: Martin Thoma
https://commons.wikimedia.org/wiki/File:Sealife-Munich-Octopus.ogv
Footage trimmed/cropped; tracking graphics by Xity / 영상 구간·크롭 편집, 추적 그림: Xity
Curated by @hyun2xyz

## Research

* Verdict: Valid. The linked Google DeepMind tapnet repo lists TAPNext++ checkpoints with occlusion tracking and re-detection, as the reel shows. The reel states it is not a benchmark.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [google-deepmind/tapnet (TAPNext++) (github.com)](https://github.com/google-deepmind/tapnet/tree/730cda1c730877cfedbe01bf87fb1cadb78a565d): repo, in the post, verified, high confidence. README lists TAPNext++ 256 and 512 PyTorch checkpoints, occlusion tracking and re-detection, a Colab demo, and Apache-2.0 licensing.

### Key steps

1. Open the repo README and find the TAPNext++ section.
2. Pick a checkpoint: 256×256 (DAVIS First AJ 65.6%) or 512×512 (DAVIS First AJ 67.0%). Both are PyTorch with a TrecViT-B backbone.
3. Open the Colab notebook torch_tapnextpp_demo.ipynb to try it. The README gives no local TAPNext++ usage steps.
4. Give the model query points from one frame. It returns each point's position and a visibility flag for every frame.
5. For a local run, use the 512 checkpoint's VOTSp2026 README for setup. The post's author ran it on Apple MPS.

### Not found

The author's own scripts for query points, rainbow drawing and trail filtering were not found. The Apple MPS setup is not documented in the repo page I read.
