---
shortcode: "DXxcwjWDDgo"
url: "https://instagram.com/reel/DXxcwjWDDgo/"
type: "Reel"
author: "michellescomputer"
shared: "May 01, 2026, 01:15 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Codex heartbeats and proactive actions for app maintenance

A talking-head reel where the creator, after building 10 apps in 10 weeks, says maintenance was the hardest part and credits Codex heartbeats (scheduled wake-ups that keep memory of past context) with handling updates on its own. An on-screen screenshot of a post by pash describes heartbeats as automations that keep context in one thread.

Written by claude-haiku-5-5.

## Research

* Verdict: Valid. Codex thread automations (called heartbeats in the community) are real. They wake a thread on a schedule and keep its context. The claim that they can handle maintenance holds, though they need the app running and unattended runs are limited by sandbox settings.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Codex Automations docs (OpenAI) (developers.openai.com)](https://developers.openai.com/codex/app/automations): guide, found by search, verified, high confidence. The docs (redirected to learn.chatgpt.com) describe in-chat scheduled tasks that return to the same chat and keep its context, matching the heartbeat idea. The page never uses the word "heartbeat".
* [Codex as a Proactive Teammate: Thread Automations (Daniel Vaughan) (codex.danielvaughan.com)](https://codex.danielvaughan.com/2026/05/15/codex-proactive-teammate-thread-automations-scheduled-monitoring-durable-views/): guide, found by search, not opened, medium confidence. Third-party write-up on thread automations and heartbeats that turned up in search. I did not open it.

### Key steps

1. Test the maintenance prompt manually in a normal Codex chat first.
2. In the thread, ask Codex to schedule a recurring task that returns to the current thread.
3. Pick a schedule: minute-based for active loops, or daily or weekly for check-ins.
4. Write a durable prompt: what to do each run, when something is worth reporting, and when to stop or ask you.
5. Keep the desktop app open, since local-project tasks need the computer on and the app running.
6. Review the first few runs and adjust the prompt or cadence.
7. Archive old worktrees if frequent schedules on Git repos build up many.

### Not found

I did not find the pash post shown in the reel. The vault has no notes on Codex heartbeats; the "heartbeat" hits are about OpenClaw.
