---
shortcode: "Dc4kGD7D56E"
url: "https://instagram.com/reel/Dc4kGD7D56E/"
type: "Reel"
author: "githubsignals"
shared: "Sep 22, 2026, 08:04 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Open-source project controls robot with AR glasses

The reel presents Spectacles Dimensional OS, an open-source project that turns Snap Spectacles AR glasses into a controller for Unitree robots, showing the robot's path and sensor data in the glasses view. Screen captures of the GitHub README list the supported hardware and the setup requirements.

Written by claude-haiku-5-5.

## What it teaches

1. Supported hardware: Snap Spectacles 2024 developer kit as the AR glasses, with a Unitree Go2 pro/air quadruped (fully supported and tested) or a Unitree G1 humanoid (supported, not tested).
2. Setup requirement: the Mac running DimOS, the Spectacles glasses and the robot must all be on the same WiFi network with a stable internet connection.
3. Recommended setup path: use the launcher ("Via launcher" is marked recommended in the README).

## Source

* Link: v4c38/spectacles-dimensional-os

## Caption

This Open-Source Project Lets You Control a Robot With AR Glasses 

Steer a real robot with your eyes. Spectacles Dimensional OS turns Snap Spectacles into a controller for Unitree robots. You see the robot’s path and sensors right in front of you. No joystick needed. Just look where you want it to go. It even lets you talk to it. This is a cool look at the future of human robot interaction.

Open source: v4c38/spectacles-dimensional-os

Follow for more open source project drops.

#SnapSpectacles #HumanRobotInteraction #AR #RobotControl

## Research

* Verdict: Valid. The GitHub repo exists and its README matches the post's hardware list, same-WiFi requirement and recommended launcher setup. The "just look where to go" framing is the reel's gloss. The README also describes voice commands and an AprilTag registration step.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [v4c38/spectacles-dimensional-os (github.com)](https://github.com/v4c38/spectacles-dimensional-os): repo, in the post, verified, high confidence. README lists Snap Spectacles 2024, Unitree Go2 (tested) and G1 (untested), same WiFi, and a recommended launcher setup; MIT license.

### Key steps

1. Get a Mac, Snap Spectacles 2024 dev kit and a Unitree Go2 (or G1). Put all three on the same WiFi.
2. Start the launcher: double-click launcher/Start Launcher.command, or run ./launcher/scripts/start-launcher.sh. Keep the terminal open.
3. Open http://127.0.0.1:8790. In Dependencies, choose Go2 or G1 and press Install.
4. Select the robot, press Start, wait for Bridge Ready and note the Bridge IP.
5. In Config, generate the AprilTag PDF. Print it at 100% scale (70 mm tag, ID 0, for the Go2) and mount it on the robot.
6. Open lens-studio/spectacles-dimensional-os.esproj in Lens Studio and send the Lens to the Spectacles.
7. In the Lens Registration Wizard, enter the Bridge IP. Keep the robot still and walk around it, looking at the tag from 0.5 to 1.5 m.
8. For voice Agent Mode, set OPENAI_API_KEY in the launcher. The Mac needs internet access.
