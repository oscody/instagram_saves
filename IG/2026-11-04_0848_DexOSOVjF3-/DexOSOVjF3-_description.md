---
shortcode: "DexOSOVjF3-"
url: "https://instagram.com/reel/DexOSOVjF3-/"
type: "Reel"
author: "vibe_withkevin"
shared: "Nov 04, 2026, 08:48 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-05"
---

# Add your devices to Claude Code mobile app

A creator explains how to connect a home computer to the Claude Code mobile app so the phone can reach the whole machine, not just one locked remote-control session. The on-screen device and session lists show a Mac Studio connected and an Air offline.

Written by claude-haiku-5-5.

## What it teaches

1. Don't rely on running remote control from inside an existing Claude Code session, because that session stays locked to one repo or folder and stops working if it times out.
2. On your main computer, open a regular terminal (not a Claude Code session) and run the remote-control command. The speaker says it as 'Cloud RC' or 'Cloud Remote Control'.
3. That command opens a secure SSH tunnel and keeps the terminal alive on your machine, giving access to the whole computer for running other sessions.
4. Optionally, set a startup script so the remote-control terminal launches automatically when the computer restarts or turns on.
5. In the Claude Code mobile app, pick your computer under the remote-control environments when creating a new session, or choose a cloud environment, repo or GitHub instead.
6. Keep the always-on remote-control terminal running so you can reach your machine from anywhere, including from another country.

## Caption

adding your devices to the Claude Code mobile app is probably the greatest unlock I've had all year. sure other things have been more intelligent or impactful, but I can always access my computer after this change

#greenscreen #claude #ai #aiagent #anthropic

## Research

* Verdict: Partly valid. The official docs confirm `claude remote-control` server mode, which stays running in a plain terminal and serves multiple sessions. The creator's details are off in two ways. The command is `claude remote-control`, not "Cloud RC". The "SSH tunnel" description is wrong: the docs say it makes outbound HTTPS requests only and opens no inbound ports. I did not check whether a short alias exists.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Claude Code Remote Control docs (server mode) (code.claude.com)](https://code.claude.com/docs/en/remote-control): guide, found by search, verified, high confidence. I opened the page. It describes `claude remote-control` server mode that keeps running in the terminal and works with the Claude mobile app. It also lists requirements, flags and limits.

### Key steps

1. Requires a claude.ai Pro, Max, Team or Enterprise plan. API keys are not supported. On Team and Enterprise, an Owner must first turn on the Remote Control toggle in admin settings.
2. Run `claude` once and use `/login` to sign in with your claude.ai account.
3. In a normal terminal (not inside a Claude session), cd to your project and run `claude remote-control`. Optional: `--name "My Project"`.
4. Leave the process running. It prints a session URL. Press spacebar to show a QR code.
5. Optional flags: `--spawn same-dir|worktree` sets how sessions are created. `--capacity N` sets the maximum concurrent sessions (default 32).
6. Open the Claude mobile app or claude.ai/code and pick your machine to start or continue sessions.
7. To keep it always on, run it inside tmux or screen, or start it from a login or boot script (the docs don't cover boot scripts). If the process stops, the machine goes offline until you restart it.

### Not found

The creator's startup script is not public. I did not check for a short `claude rc` alias. The docs give no per-machine device list beyond what the post shows.
