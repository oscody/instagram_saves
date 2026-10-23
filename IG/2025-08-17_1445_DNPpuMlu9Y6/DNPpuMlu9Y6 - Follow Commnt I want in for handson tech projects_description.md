---
shortcode: "DNPpuMlu9Y6"
url: "https://instagram.com/reel/DNPpuMlu9Y6/"
type: "Reel"
author: "itsnextwork"
shared: "Aug 17, 2025, 02:45 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Skit on exposed app data and access control

A skit in which an intern's dating app exposes government IDs and private messages because a storage bucket has no security rules and the message database has no ownership check. The clip uses a diagram and a boss character to walk through what went wrong.

Written by claude-haiku-5-5.

## What it teaches

1. Logging in (authentication) does not mean a user may read other people's data (authorization); check permissions on every request.
2. Set security rules and permissions on databases and storage buckets; don't leave a bucket publicly accessible with no rules.
3. Users should never query the database directly.
4. Route every data request through an API layer that verifies ownership first and returns only the requesting user's data.

## Source

* Link: learn.nextwork.org
* How to get it: comment 'I want in' for the hands-on tech projects

## Caption

Follow & Commnt "I want in" for hands-on tech projects to add to your resume! 

In this video we cover how the intern made a rookie mistake when creating the Tea dating app...

Got to set those permissions right...

#security #cybersecurity #systemsdesign

## Research

* Verdict: Partly valid. The security lesson is sound and standard (authentication isn't authorization; lock down buckets; check ownership server-side). The post is mainly a funnel for NextWork's project platform, with the "I want in" comment as the hook.
* Checked: 2026-10-23 by claude-sonnet-5-5

### Resources

* [NextWork (learn.nextwork.org redirects to nextwork.ai) (nextwork.ai)](https://nextwork.ai/): product, in the post, verified, medium confidence. The link in the post redirects here; it is a hands-on project platform with a Security learnlist, but no project specific to this skit and no prices are shown.

### Key steps

1. Authenticate the user, then authorize every request separately.
2. Set security rules on databases and storage buckets; keep buckets private by default.
3. Don't let clients query the database directly.
4. Send all data requests through an API layer that checks ownership and returns only the requesting user's data.

### Not found

The "I want in" material is only sent after a comment, and no public copy was found. The site doesn't say which projects are free. I did not check the Tea app breach claim.
