---
shortcode: "DcNOMyTCXmO"
url: "https://instagram.com/reel/DcNOMyTCXmO/"
type: "Reel"
author: "githubsignals"
shared: "Aug 20, 2026, 09:48 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Mixamo LLM Mocap: Turning Video Into 3D Animation

The post shows the GitHub README for an open-source tool that converts a locked-camera video into a Mixamo character animation in Blender, including a two-person fight example. It also lists the tool's ten-stage processing pipeline.

Written by claude-haiku-5-5.

## What it teaches

1. Start with a video shot on a locked camera (or AI-generated), with a T-pose at the beginning and end.
2. Set up your Mixamo character with setup_rig.py, which builds a Blender scene from your own Mixamo download and writes a rig_profile.json.
3. Estimate the pose from the video with estimate_pose_gvhmr.py (GVHMR mesh recovery).
4. Detect beats numerically with analyze_landmarks.py.
5. Describe the motion in a small JSON spec in action_specs/<name>.json, covering the support foot for each phase, when fists close, and where the clip locks back to rest.
6. Retarget the motion onto the Mixamo character with lift_to_mixamo.py, rebuilding positions from the character's bone lengths.
7. Apply FK aim and foot planting with apply_mixamo_fk.py, solving hip height instead of using IK.
8. Run the automated QA gate with qa_clip.py.
9. Compare the result frame by frame against the source video with compare_reference.py.
10. For two performers, run the stages once per fighter with --person left|right, build one scene with setup_duo.py, and check interactions with compare_pair.py.
11. Check real mesh-vs-mesh contact in Blender with run_in_blender.py.
12. Render a preview and side-by-side showcase with render_preview.py.

## Source

* Link: squall01337/mixamo-llm-mocap

## Caption

Turn Any Video Into a 3D Character Animation With AI 

You can turn any static video into a clean, playable animation for any character, without a single motion capture suit or manual keyframe. Mixamo LLM Mocap uses computer vision to read human movement from the footage, then automatically maps that motion onto your chosen digital rig inside Blender. It even handles two people fighting in the same scene, keeping their movements realistic and grounded. The most surprising part is that an AI agent can run this entire process end-to-end, meaning no human needs to touch the software at all.

Open source: squall01337/mixamo-llm-mocap

Follow for more open source project drops.

#MotionCapture #Blender3D #AIAnimation #AITools #GameDev
