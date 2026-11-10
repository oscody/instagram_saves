---
shortcode: "DfFUd0vMSEi"
url: "https://instagram.com/reel/DfFUd0vMSEi/"
type: "Reel"
author: "marc.kaz"
shared: "Oct 29, 2026, 04:15 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-30"
---

# BLA: shield against AI reverse engineering

The post presents BLA, a tool that hardens a shipped build (JS, Electron, WASM and more) so AI reverse-engineering agents chase decoys and burn their budgets, while the app's runtime behavior stays the same. The on-screen project page shows the npm package, MIT license, and a harden command.

Written by claude-haiku-5-5.

## What it teaches

1. Point BLA at the build you ship, for your own builds only (MIT licensed).
2. Run `npx bla-agents harden .` in the project to harden the release.

## Source

* Link: https://github.com/qybaihe/bla

## Caption

🚨 A SHIELD THAT MAKES AI REVERSE ENGINEERING WASTE TOKENS

BLA hardens your release so AI reverse-engineering tools chase decoys, hit limits, and stop. Your app still runs the same.

Ships with:
• Fake keys, decoy interfaces, and interference logic
• Triggers budget and capacity errors in REA-style tools
• 14 benchmarks matched the originals after hardening
• Works on JS, Electron, WASM, and more
• `npx bla-agents harden .` MIT. For your own builds

👉 https://github.com/qybaihe/bla

## Research

* Verdict: Partly valid. The repo exists, is MIT licensed, and the harden command matches the post. The effectiveness figures (14/14 benchmarks, token amplification) are the author's own numbers and cover only his test fixtures. They don't cover tools like Ghidra or Frida.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [BLA (qybaihe/bla) (github.com)](https://github.com/qybaihe/bla): repo, in the post, verified, high confidence. README describes a Counter-REA defense CLI/MCP, npm bla-agents, MIT, `npx bla-agents harden .`, and 14 benchmark targets, all as in the post.

### Key steps

1. Use Node.js ^22.23.4 or >=24.0.0.
2. In your project or release directory, run `npx bla-agents harden .`. It runs audit, protect and verify.
3. Optional: run `npx bla-agents setup` to register BLA with Claude Code, Cursor or Codex, then ask the agent to harden your software against REA.
4. Optional: add `blaVitePlugin` from `bla-agents/bundler` to your Vite config.
5. Run `npx bla-agents benchmark` to reproduce the 14-target showcase locally.
6. Use it on your own builds only.

### Not found

I did not run the tool or check the benchmark figures independently. The README says the amplification numbers (about 639x tokens) are internal estimates. The vault notes that matched only share the creator and don't cover BLA.
