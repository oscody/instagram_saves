---
shortcode: "DeeKcrZI7eG"
url: "https://instagram.com/reel/DeeKcrZI7eG/"
type: "Reel"
author: "robot_o_0"
shared: "Oct 14, 2026, 05:30 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Quadruped robot with AI depth estimation on Hailo

A small quadruped robot built on a Raspberry Pi 5 with a Hailo 8L AI HAT runs depth estimation alongside object detection and pose detection. The clip shows the depth view with a detected refrigerator and a blue point cloud on a monitor, and the creator says the depth data will later be used for AI navigation.

Written by claude-haiku-5-5.

## Caption

Today I am planning to work with AI vision features in this robot, wait for it.
Based on @raspberrypi 5 and AI hat hailo 8L
#ai #robotics #computervision #opencv #python

## Research

* Verdict: Partly valid. The creator's own code isn't public. Hailo's official hailo-apps repo has a depth app that runs on Hailo-8L, so the setup is plausible. Forum users report Hailo-8L problems with the depth model.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [hailo-ai/hailo-apps (github.com)](https://github.com/hailo-ai/hailo-apps): repo, in the vault, verified, medium confidence. The repo lists hailo-depth, detection and pose apps and Hailo-8L support, which matches the features shown, though the post doesn't name it.
* [hailo-rpi5-examples (older, marked outdated) (github.com)](https://github.com/hailo-ai/hailo-rpi5-examples): repo, found by search, not opened, low confidence. Search results say it has basic_pipelines/depth.py using scdepthv3, and that the repo now points to hailo-apps.
* [Problem using hailo-depth on RPI5 (Hailo community) (community.hailo.ai)](https://community.hailo.ai/t/problem-using-hailo-depth-on-rpi5/17938): page, found by search, not opened, low confidence. Search results describe users hitting crashes with hailo-depth on a CM5 with Hailo-8L.

### Already in the vault

* Vault: `2. Areas/Botstack/Pi/pi todo/repo - hailo-apps.md`: hailo-apps overview. It lists pipeline apps (depth, pose, detection) and gives commands such as `source setup_env.sh` and `hailo-detect --input usb`. Your Hailo is a 10H, not an 8L.
* Vault: `2. Areas/Botstack/Pi/Raspberry Pi AI HAT.md`: Your notes on the Raspberry Pi AI HAT and Hailo.

### Key steps

1. Clone hailo-ai/hailo-apps and follow its Installation Guide for your platform. Install HailoRT first.
2. Run `source setup_env.sh`.
3. Run `hailo-depth --input usb` for depth. Use `hailo-detect` and `hailo-pose` for objects and pose. The depth command name comes from the repo page. The `--input usb` flag is copied from your vault note's detect example and wasn't checked for depth.
4. On a Hailo-8L, use the 8L build of the model file (.hef). A Hailo-8 build gives an architecture mismatch error.
5. Only one process can use the Hailo at a time, so close one app before starting another.

### Not found

The creator's own code or a build write-up. I didn't check their profile. I didn't open the forum threads or the older examples repo, so those results are unverified.
