---
shortcode: "DcUy9rhR0Uo"
url: "https://instagram.com/reel/DcUy9rhR0Uo/"
type: "Reel"
author: "ayoships"
shared: "Oct 10, 2026, 08:38 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Two app habits: session replays and review prompts

A creator talking to the camera about two things he would prioritize for an app from day one: PostHog session replays and a pre-review feedback prompt. On-screen text repeats the key phrases.

Written by claude-haiku-5-5.

## What it teaches

1. Use PostHog session replays from day one to watch what users do step by step.
2. Use replays to find why users churn, bugs you would not otherwise catch, and broken UX flows or onboarding.
3. Ask for reviews at a key moment in the app.
4. Show your own feedback prompt before the native App Store review pop-up.
5. If the user says they love the app, show the native review prompt.
6. If the user does not, route them to a feedback form instead so negative reviews stay private.

## Caption

If you find this useful please like, save, and share to your business partner

## Research

* Verdict: Valid. PostHog session replay exists and does what the post says. The review-prompt routing is a common practice (a pre-prompt before the native review request), not a specific resource.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [PostHog Session Replay docs (posthog.com)](https://posthog.com/docs/session-replay): page, found by search, verified, high confidence. Page describes recording user sessions with linked events, console logs and errors, with SDKs for iOS and React Native.

### Key steps

1. Add the PostHog SDK for your platform (iOS, React Native, web) using the installation guide: https://posthog.com/docs/session-replay/installation
2. Enable session replay in project settings.
3. Review recording rules and privacy masking (text, inputs) before shipping.
4. Link replays to funnel drop-offs or errors to find the session behind them.

### Not found

The review pre-prompt has no single named resource. I did not look for a specific implementation.
