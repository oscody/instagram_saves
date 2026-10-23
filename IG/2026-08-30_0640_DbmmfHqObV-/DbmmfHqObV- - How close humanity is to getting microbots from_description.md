---
shortcode: "DbmmfHqObV-"
url: "https://instagram.com/reel/DbmmfHqObV-/"
type: "Reel"
author: "yoiqino"
shared: "Aug 30, 2026, 06:40 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Why microbots from Big Hero 6 are hard

The creator explains why Wi-Fi-style antennas don't suit microbots and proposes infrared optical time-of-flight as a way for tiny robots to communicate. Screen images show a toll-tag reader and an infrared sensor on a breadboard.

Written by claude-haiku-5-5.

## What it teaches

1. Wi-Fi needs an antenna that is a decent fraction of its wavelength (about 12.5 cm for Wi-Fi), so antennas make microbots too big.
2. Using a higher frequency shrinks the antenna but takes more energy than a miniature robot has.
3. Backscatter works like a toll tag: a sender emits waves, a tag reflects them in a pattern, and a receiver reads the pattern.
4. Backscatter handles control-tower communication, but microbots need to talk to each other, so it doesn't fully solve the problem.
5. Optical time-of-flight uses infrared light and a tiny sensor instead of an antenna.
6. The sensor reads information from how long the infrared flashes take to arrive.
7. Communication between microbots is possible without antennas; coordination between them is a separate problem the creator says will be shown in a simulation next week.

## Caption

How close humanity is to getting microbots from Big Hero 6

## Research

* Verdict: Partly valid. The post is an explainer with no single resource. Its main claim holds: antennas limit tiny robots, and infrared optical links are a researched alternative. The specific "time-of-flight" communication idea isn't confirmed, and ToF sensors normally measure distance rather than carry data.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [IR-based Communication and Perception in Microrobotic Swarms (arxiv.org)](https://arxiv.org/pdf/1109.3617): paper, found by search, not opened, medium confidence. Search result describing IR light as the communication and perception link for millimetre-scale swarm robots, which matches the post's general idea. I didn't open it.
* [Free-Space Optical Communication in a Swarm of Microrobots (vde-verlag.de)](https://www.vde-verlag.de/proceedings-en/563042108.html): paper, found by search, not opened, low confidence. Search result on optical communication between swarming microrobots. I didn't open it.

### Not found

The creator's source and the promised simulation video were not found. I didn't check the vault beyond the listed search, which found no notes. I found no source for the time-of-flight and backscatter claims specifically.
