---
shortcode: "Dd9pxPOiEXF"
url: "https://instagram.com/reel/Dd9pxPOiEXF/"
type: "Reel"
author: "billy.coder"
shared: "Oct 03, 2026, 12:19 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Cheap ESP32 WiFi sensing through walls

The reel promotes a $9 ESP32 project that uses WiFi reflections to detect presence, movement, breathing and multi-person pose through walls, with no camera or microphone. The closing line asks viewers to comment SIGNAL to be sent the repo.

Written by claude-haiku-5-5.

## Source

* How to get it: comment SIGNAL

## Caption

Carnegie Mellon proved WiFi can see through walls. Somebody shipped live WiFi sensing on a $9 chip and open sourced it.

Three antennas in, three out, on ordinary 2.4GHz. The radio bouncing off your body comes back as a Channel State Information matrix, and a neural net maps the phase and amplitude of it onto 24 regions of a human body. No camera. No microphone. Nothing is recorded, because there is nothing to record.

A $9 ESP32 is the whole sensor, 30 subcarriers at 100Hz sampling, movement and breath rate and presence, pose for multiple people at once through a wall, MIT licensed, and the firmware and the dashboard are both in the repo.

Send this to whoever still thinks tape over the webcam is the end of it.

Comment SIGNAL and I'll send you the repo.

.
.
.

live wifi sensing, wifi sensing csi, wifi sensing esp32, wifi sensing technology, wifi sensing github, wifi human detection github, wifi pose estimation, wifi person detection, wifi see through walls, using wifi to see through walls

#engineering #computervision #opensourceproject #privacy #esp32

## Research

* Verdict: Partly valid. The repo is real, MIT licensed, and runs on about $9 ESP32-S3 boards. The reel overstates it: the README lists 17 keypoints, not 24 regions, and the live single-ESP32 pose model is weak. The "comment SIGNAL" gate is unnecessary because the repo is public.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [ruvnet/RuView (WiFi DensePose) (github.com)](https://github.com/ruvnet/RuView): repo, found by search, verified, medium confidence. The README states MIT license, ESP32-S3 nodes at $9, CSI presence, vitals, pose and through-wall sensing. The post doesn't name the repo, so the match rests on those features.
* [Open source WiFi DensePose demonstrates camera-free motion detection through walls (opensourceforu.com)](https://www.opensourceforu.com/2026/03/open-source-wifi-densepose-demonstrates-camera-free-motion-detection-through-walls/): page, found by search, not opened, low confidence. This is a news article on the same project. I didn't open it.

### Key steps

1. Buy an ESP32-S3 board. The original ESP32 and the C3 are not supported. The README recommends 3–6 nodes plus a router for decent resolution.
2. To try it without hardware, pull the Docker image ruvnet/wifi-densepose:latest and set an API token. The container exits without one. Run it on localhost port 3000 with simulated data.
3. For real hardware, flash the firmware with esptool.
4. Run provision.py to set the Wi-Fi credentials and the target IP.
5. Open the dashboard to see presence, breathing and pose.
6. Alternatively, install the ruview or wifi-densepose package from PyPI. Building from source needs Rust 1.85+.
7. Check the beta caveats before relying on the output. Vitals are unvalidated, the README gives through-wall range as about 5 m, and the single-ESP32 pose model scores PCK@20 of 3%.

### Not found

The reel's "24 body regions", "30 subcarriers at 100Hz" and "3x3 antennas" details did not appear in the README (the pose output there is 17 keypoints). I did not open the CMU paper. The post's author never names the repo, so the match rests on its features.
