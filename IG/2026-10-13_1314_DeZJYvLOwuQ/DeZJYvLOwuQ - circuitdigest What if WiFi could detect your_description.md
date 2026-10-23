---
shortcode: "DeZJYvLOwuQ"
url: "https://instagram.com/p/DeZJYvLOwuQ/"
type: "Post"
author: "circuit_digest"
shared: "Oct 13, 2026, 01:14 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# DIY Wi-Fi sensing with three ESP32-S3 boards

The post presents a DIY project that uses three ESP32-S3 boards to detect people and track movement from Wi-Fi signals alone, reporting nearly 80% accuracy. It shows a 3D room illustration of Wi-Fi signals bouncing around a living room with a person standing in it, plus photos of the boards, and mentions uses such as smart home security and fall detection.

Written by claude-haiku-5-5.

## Caption

circuit_digest What if Wi-Fi could detect your movements without a camera? This DIY project uses 3
ESP32-S3 boards to detect people and track movements with nearly 80% accuracy using Wi-Fi
signals alone! From smart home security to fall detection, this technology has some exciting
possibilities.

Learn more from the link in the bio.

CC: @betterstackhq 

#ESP32 #WiFiSensing #DIYProjects #IoT #AI

## Research

* Verdict: Partly valid. The project is real: Better Stack tested RuView on three ESP32-S3 boards and got 79.5% across eight movements. The figure comes from one person in one room, and waving was only 13%, so "detects movements" is overstated.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Circuit Digest article: DIY ESP32-S3 Wi-Fi Sensing System (80% accuracy) (circuitdigest.com)](https://circuitdigest.com/news/this-diy-esp32-s3-wi-fi-sensing-system-detects-people-and-tracks-movements-without-a-camera-at-80-accuracy): page, found by search, verified, high confidence. Describes three ESP32-S3 boards, 79.5% accuracy, and use of RuView, matching the caption.
* [RuView (ruvnet/RuView) (github.com)](https://github.com/ruvnet/RuView): repo, found by search, verified, high confidence. The open-source Wi-Fi CSI sensing project named in the article; its README supports 3–6 ESP32-S3 mesh nodes and ships flashing instructions.

### Key steps

1. Buy 3 ESP32-S3 boards (DevKitC-1 or WROOM). The original ESP32 and the C3 are not supported.
2. Get the firmware binaries from the RuView releases page, or build them from firmware/esp32-csi-node.
3. Flash each board: python -m esptool --chip esp32s3 --port <PORT> --baud 460800 write_flash 0x0 bootloader.bin 0x8000 partition-table.bin 0xf000 ota_data_initial.bin 0x20000 esp32-csi-node.bin
4. Provision each board: python firmware/esp32-csi-node/provision.py --port <PORT> --ssid <WiFi> --password <pw> --target-ip <host IP>
5. Place the boards at different spots in the room so the signals cross several paths.
6. Record about 9 minutes of varied movements for training. The article used a webcam with MediaPipe pose detection for labels.
7. Train the model on the Wi-Fi data, then remove the camera and test live.
8. To try it with no hardware, run the Docker image ruvnet/wifi-densepose with RUVIEW_API_TOKEN set (it uses simulated data).

### Not found

I did not find the Better Stack YouTube video itself. The article does not link to it. Training details are from the article only, since the RuView README does not describe the webcam-labelled training run.
