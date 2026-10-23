---
shortcode: "Da05QgdBcTh"
url: "https://instagram.com/reel/Da05QgdBcTh/"
type: "Reel"
author: "itsbetterwithai"
shared: "Jul 19, 2026, 08:51 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Film Space: iPhone camera moves as AI video reference

The creator presents Film Space, a free open-source iPhone app that builds a rough 3D scene and records physical phone movement as a camera reference for AI video generators such as Seedance. Screens show the lens selector, Edit/Camera toggle and record button.

Written by claude-haiku-5-5.

## What it teaches

1. Build a rough 3D version of the scene in Film Space.
2. Place characters and objects inside the scene.
3. Choose a virtual lens.
4. Use the iPhone as the camera: walk through the shot, tilt, push toward the subject, or orbit around it.
5. The app records that movement as a reference video.
6. Feed the reference video into an AI video generator such as Seedance to guide the shot.

## Caption

AI video is getting much easier to direct.
Because the biggest limitation with most AI video generators is not imagination. It is control.

You might know exactly how you want a shot to look, but translating the camera angle, lens, framing, subject placement, and movement into a prompt can be incredibly difficult.

Film Space offers a completely different approach.

It is a free, open-source app that lets you build a rough 3D version of your scene, place characters and objects inside it, choose a virtual lens, and then use your iPhone like an actual camera.

You can physically walk through the shot, tilt the phone, push toward the subject, orbit around them, or create more complicated camera movements.

The app records that movement and turns it into a reference video that can be used to guide an AI video generator like Seedance.
Filmmakers have already been using tools like Blender to do something similar, but that normally requires a lot more technical knowledge and time.

Film Space makes the same basic workflow much more accessible.

And I think this is a preview of where AI filmmaking is going.

Not a world where you type a few words and let the AI make every creative decision for you.
A world where filmmakers can direct AI with the same kind of intention they would bring to a real camera.

## Research

* Verdict: Valid. The repo maxprokopp/film-space is an iPhone ARKit app that matches the post's Edit/Camera modes, lens presets and recording. The "free, open-source" claim is only partly confirmed: the page shows no license, and it is built from source in Xcode, not installed from the App Store.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Film Space (maxprokopp/film-space) (github.com)](https://github.com/maxprokopp/film-space): repo, found by search, verified, high confidence. SwiftUI/ARKit iPhone app with Edit and Camera modes, lens presets and recording to the photo library, for use as an AI video camera reference.

### Key steps

1. Clone the repo and open the Xcode project; build and run it on a physical iPhone (ARKit needs a real device).
2. Edit mode: orbit and zoom around the grid floor and place human stand-ins to block the scene.
3. Pick a lens preset: 35, 50, 75 or 200mm.
4. Switch to Camera mode and move the phone to move the virtual camera. Use the shoulder placement and lock/return viewpoint tools if needed.
5. Press Record. The clip, with mic audio, saves to the photo library.
6. Upload the clip to Seedance 2.0 or a similar tool as a motion and camera-path reference.

### Not found

No license found on the repo page. No App Store listing or install steps found. I didn't check the creator's profile for a link.
