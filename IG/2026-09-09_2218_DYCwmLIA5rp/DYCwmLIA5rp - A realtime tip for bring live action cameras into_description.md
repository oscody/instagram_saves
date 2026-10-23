---
shortcode: "DYCwmLIA5rp"
url: "https://instagram.com/reel/DYCwmLIA5rp/"
type: "Reel"
author: "sirwadefx"
shared: "Sep 09, 2026, 10:18 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Using a phone as a virtual camera in Unreal

The creator shows using a phone as a live action style camera to record camera moves in a 3D scene built in Unreal Engine, with the phone's view streaming into the Unreal session. The footage can be exported to Maya or Blender.

Written by claude-haiku-5-5.

## What it teaches

1. Install the Virtual Camera app from Epic Games on your phone.
2. Connect the app to your session in Unreal Engine.
3. Move the phone like a real camera and record a take in the scene.
4. To use the move in Maya or Blender, right-click the camera in Unreal and choose Export.
5. Import the exported FBX file into the other 3D software.

## Caption

A realtime tip for bring live action cameras into 3d animated scenes! 🎥✨ Check out the latest YT vid for an overview of what other features we can play with in Unreal, especially the GPU accelerated tools 😄

This VCam setup is super lightweight and works on pretty much any hardware, while other features get… a bit heavier. Shoutout to my NVIDIA GeForce RTX 5090, and @nvidiastudio for sponsoring the video 🫶🏼

#animation #unrealengine5 #b3d #vfx #animator

## Research

* Verdict: Valid. Epic's Unreal VCam app and VirtualCamera plugin are real and work as the post describes. The post's steps skip the plugin setup, and Epic's page doesn't cover export; right-click Export of the camera to FBX is the standard Unreal route, but I didn't check it against a source.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Controlling a Virtual Camera Actor using Live Link in Unreal Engine (Epic docs) (dev.epicgames.com)](https://dev.epicgames.com/documentation/unreal-engine/controlling-a-virtual-camera-actor-using-live-link-in-unreal-engine): guide, found by search, verified, high confidence. Official Epic guide for the Unreal VCam iOS/Android app, the VirtualCamera plugin and connecting a phone to the editor.

### Key steps

1. In Unreal, enable the VirtualCamera, Live Link and Take Recorder plugins (Edit > Plugins), then restart the editor.
2. Install the Unreal VCam app (iOS/iPadOS 15+ with ARKit, or Android with ARCore) and accept the license.
3. Drag a VCam Actor from the Place Actors panel into the scene.
4. Put the phone and the computer on the same network.
5. In the editor's Pixel Streaming dropdown, copy the Signalling Server URL on your network. Enter it in the app and tap Connect. If you have several cameras, pick one.
6. Record the camera move with Take Recorder.
7. To use the move elsewhere, right-click the camera and choose Export, then import the FBX into Maya or Blender. This step comes from the post, not Epic's page.

### Not found

The creator's YouTube video (sponsored by NVIDIA) wasn't searched for or opened. I found no Epic documentation for the FBX export step.
