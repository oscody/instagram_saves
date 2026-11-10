---
shortcode: "DfQFQX3sPjY"
url: "https://instagram.com/reel/DfQFQX3sPjY/"
type: "Reel"
author: "marc.kaz"
shared: "Nov 02, 2026, 07:57 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Craft Anything: AI tool to clone and rebuild apps

A creator promotes Craft Anything, an open-source Rust tool that inspects an existing website, app, or game with 314 inspection tools, then has a coding agent build a new version in a chosen stack. The post lists features such as clean-room mode, layout, style, and behavior comparison, and MIT/Apache-2.0 licensing, with a GitHub link.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/storytold/craft-anything

## Caption

🚨 STUDY ANY SITE, APP, OR GAME. THEN BUILD YOUR OWN

Craft Anything inspects the original with real tools, then a coding agent builds a new version in whatever stack you ask for and keeps refining until it is close.

Ships with:
• 314 inspection tools, CLI or any agent
• Clean-room mode by default
• Recreate in Next.js, Rust, or whatever you name
• Compares layout, style, and behavior
• Pure Rust. MIT or Apache-2.0. 2.7k stars

👉 https://github.com/storytold/craft-anything

## Research

* Verdict: Valid. The repo exists and matches the post: pure Rust, MIT or Apache-2.0, clean-room by default, and it builds with a coding agent. The numbers have changed: the README now says 320 tools and about 26k stars, not 314 and 2.7k. It is also labelled early alpha.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [storytold/craft-anything (github.com)](https://github.com/storytold/craft-anything): repo, in the post, verified, high confidence. README describes a Rust tool that inspects a site, app or game and has a coding agent rebuild it; MIT/Apache-2.0; clean-room default.

### Key steps

1. Install Rust 1.97 or newer. On Debian or Ubuntu, the desktop app also needs system packages listed in the README.
2. Clone the repo.
3. Run the desktop app with `cargo run --release -p craft-anything`, or install the CLI with `cargo install --path apps/craft-anything-cli`. Prebuilt installers are on the Releases page.
4. Run `craft-anything-cli doctor` to see what is missing.
5. Install and sign in to a coding agent such as Claude Code. It does the building.
6. Run `craft-anything-cli rebuild https://example.com "Recreate this website"`.
7. Refine an existing project with `--continue-in`, or pick a folder with `--project-folder`.
8. Clean-room mode is the default: it uses only what a visitor can see. Deep mode, which looks inside the target, has to be switched on.

### Not found

The vault has no note on this tool. Other saved posts don't cover it either. I didn't check the 314 vs 320 tool count beyond the README.
