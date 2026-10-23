---
shortcode: "DcXvWV0z077"
url: "https://instagram.com/reel/DcXvWV0z077/"
type: "Reel"
author: "devilco.nitin"
shared: "Sep 06, 2026, 08:26 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# DramaClaw: open-source novel-to-drama series pipeline

The reel promotes DramaClaw, an open-source, self-hosted pipeline that turns a novel manuscript into a drama series, covering characters, episodes, scripts, storyboards, voice-over and final cut. The on-screen README shows its Docker and local setup, supported model providers and sample series it has produced.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/dramaclaw/dramaclaw

## Caption

# From Novel to Finished Drama Series, 3,800 Stars

Source: https://github.com/dramaclaw/dramaclaw

#OpenSource #AI #AIGC #VideoGeneration Drama Storytelling Filmmaking ContentCreation GenerativeAI fyp foryou

## Research

* Verdict: Partly valid. The repo exists and matches the reel's pipeline and Docker/local setup. It is source-available under Elastic License 2.0, not strictly open source. It now shows about 6.4k stars, not 3,800.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [DramaClaw (github.com)](https://github.com/dramaclaw/dramaclaw): repo, in the post, verified, high confidence. README describes a manuscript-to-series pipeline (episodes, scripts, storyboards, voice-over, final cut) with Docker and local setup.

### Already in the vault

* Vault: `ZAIHub/Ai story tools.md`: Only a bare link to the repo, with no steps or notes. It also lists webnovel-writer and Sudowrite Muse.

### Key steps

1. Clone both dramaclaw and dramaclaw-gateway side by side.
2. Copy .env.example to .env and set PROMPT_EXPORT_PASSWORD.
3. Run `docker compose up -d --build`. Alternatively, run `docker compose -f docker-compose.release.yml up -d` to use published images.
4. For local development, install Python 3.11–3.12, uv and ffmpeg. Then run `uv sync`, configure .env, and run `scripts/start-ce.sh`.
5. Open the web UI on port 8080. The REST API is on port 8780.
6. Go to Settings → Model Config and pick a gateway mode: Official (a DC key from RelayClaw), Custom (your own provider channels via the bundled gateway), or Hybrid.
7. Import a manuscript and run the series pipeline: story structure, episodes, scripts, storyboards, voice-over, final composition.

### Not found

Did not check the reel's visuals or the sample series. The 3,800-star figure is probably out of date.
