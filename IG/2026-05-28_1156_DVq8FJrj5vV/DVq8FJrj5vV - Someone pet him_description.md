---
shortcode: "DVq8FJrj5vV"
url: "https://instagram.com/reel/DVq8FJrj5vV/"
type: "Reel"
author: "prettywiredbuilds"
shared: "May 28, 2026, 11:56 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Robot dog gets emotionally dependent on pets

A woman tells the story of Pixel, her robot dog, whose head touch sensor drives a pet timer that makes him needy and stops her from working. The caption is "Someone pet him 😭", and the on-screen text reads "anyhow units", "but that backfired on me" and "so now my robot".

Written by claude-haiku-5-5.

## What it teaches

1. Use a touch sensor on the robot's head to reset a countdown timer each time it is touched.
2. Track time since the last pet with a satisfaction meter; the longer the gap, the needier the robot gets.
3. At about 1 second without a pet, the robot starts with a head tilt.
4. At about 4 seconds, it starts to whine.
5. At about 7 seconds, it escalates fully and growls.
6. Simple taps also count as pets, which keeps resetting the timer, so stricter logic is needed.
7. Use the sensor's direction of contact: a pet from back to front delays the countdown by 30 seconds.

## Caption

Someone pet him 😭

## Research

* Verdict: Partly valid. The creator's own code wasn't found, and the dog is likely a SunFounder PiDog, which is my guess and not confirmed. The directional head touch sensor it uses supports the idea in the post, but the post is mostly a story. The timer values are the creator's own.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [SunFounder PiDog – Dual Touch (head sensor) docs (docs.sunfounder.com)](https://docs.sunfounder.com/projects/pidog/en/latest/python/py_b12_dual_touch.html): guide, found by search, not opened, low confidence. The page describes a head touch sensor that returns L, R, LS, RS or N, with swipes for direction. That fits the 'back to front petting' step, but I only saw it in search results, and nothing ties it to this creator's robot.

### Key steps

1. Read the head sensor in a loop with dog.dual_touch.read(). It returns N, L, R, LS or RS.
2. Treat any touch as a pet and store the time of the last pet.
3. Each loop, compute the time since the last pet. About 1s: head tilt. About 4s: whine. About 7s: growl.
4. Ignore plain L or R taps for resetting the timer. Only count a swipe (LS or RS) as a real pet.
5. Make a back-to-front swipe add a 30-second delay before the neediness starts.

### Not found

The creator's code or project page. Nothing was found for prettywiredbuilds or a robot named Pixel. The robot model is unconfirmed.
