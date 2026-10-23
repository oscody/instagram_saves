---
shortcode: "Ddt_E-QJbzD"
url: "https://instagram.com/reel/Ddt_E-QJbzD/"
type: "Reel"
author: "tech.explain1"
shared: "Sep 25, 2026, 05:53 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Radar heartbeat sensor built with Grok

A demo of a homemade radar sensor that tracks a person's position behind walls and doors, shown on a radar-style screen modeled on the Call of Duty heartbeat sensor. The creator explains the radar principle and how the build was split into three jobs.

Written by claude-haiku-5-5.

## What it teaches

1. The sensor sends out millimeter radio waves, which pass through walls.
2. Because the body is mostly water, the waves bounce back off a person.
3. Breathing moves the chest a few millimeters, which shifts the frequency of the returning echo.
4. The sensor times the echoes to work out a person's location, speed, and direction.
5. A Raspberry Pi connected to the radar draws the on-screen display.
6. Build step 1: turn the sensor's raw data into tracked people.
7. Build step 2: recreate the radar screen, using stills from the game to match the look.
8. Build step 3: test the display to confirm the data is shown accurately.

## Caption

Can you build a real heartbeat sensor? @grok #grokbot #spacexaipartner

## Research

* Verdict: Partly valid. The reel's own source (Grok-built code) wasn't found. Similar public builds exist and show that mmWave radar plus a Raspberry Pi can track people through walls. Real radar tracks presence and motion, not heartbeats, so "heartbeat sensor" is a game-style name.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Heartbeat sensor from Modern Warfare 2 (Hackaday.io) (hackaday.io)](https://hackaday.io/project/205879-heartbeat-sensor-from-modern-warfare-2): page, found by search, not opened, medium confidence. Similar build: a 24GHz radar module drives a Call of Duty-style heartbeat sensor display, but I didn't open it and it isn't confirmed as the reel's source.
* [Using mmWave Radar to Detect and Track Humans – Raspberry Pi Guide (Core Electronics) (core-electronics.com.au)](https://core-electronics.com.au/guides/using-mmwave-radar-to-detect-and-track-humans-raspberry-pi-guide/): guide, found by search, verified, medium confidence. Opened it: RD-03D radar on a Raspberry Pi with a 2D radar visualisation that tracks people, matching the post's pipeline, though it isn't the reel's own project.

### Key steps

1. Wire the RD-03D radar to the Pi: 5V to 5V, GND to GND, radar TX to Pi pin 15 (RX), radar RX to Pi pin 14 (TX).
2. Install 64-bit Pi OS and enable the Serial Port under Interfaces, then reboot.
3. Download the guide's library and demo zip. On a Pi 5, change the UART port in rd03d.py to /dev/ttyS0. On a Pi 4, leave it.
4. Run rd03d_demo_usage.py to read each target's distance, angle, speed and X/Y position.
5. Use single-target mode for reliability. Multi-target tracks up to 3 people but can give false readings.
6. Run radar_visualisation.py to draw tracked people on a 2D radar screen. Restyle it to look like the game by giving an AI like Grok screenshots of the game's display.
7. Mount the sensor still, at chest to head height. Expect phantom targets from wall reflections.

### Not found

The reel's actual Grok prompts or code weren't found, and nothing from tech.explain1 is public. I didn't verify the Hackaday project. The post's claim that breathing is detected through walls wasn't tested.
