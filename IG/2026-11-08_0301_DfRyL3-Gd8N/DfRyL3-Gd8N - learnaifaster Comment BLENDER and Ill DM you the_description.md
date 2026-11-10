---
shortcode: "DfRyL3-Gd8N"
url: "https://instagram.com/p/DfRyL3-Gd8N/"
type: "Carousel"
author: "learnaifaster"
shared: "Nov 08, 2026, 03:01 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-09"
---

# StableGen: free AI Blender add-on for characters

Introduces StableGen, a free, open-source Blender add-on that creates textured, ready-to-animate 3D characters from a text prompt, with ComfyUI running locally. The post's GitHub link is not written in the caption; it is sent by DM after commenting BLENDER.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "BLENDER" on the post and the GitHub link is sent by DM

## Caption

learnaifaster Comment "BLENDER" and I'll DM you the GitHub link.

Creating 3D characters in Blender just got a lot easier.

There's a free, open-source tool called StableGen that can turn a simple text prompt into a fully textured 3D character that's ready to animate.

You describe the character you want, choose a preview image, and the AI handles the 3D modeling, textures, and rigging.

It can even add textures to existing 3D models, apply Mixamo animations, and export characters for game engines like Unreal Engine, Unity, and Godot.

What's really interesting is that it works with ComfyUI, meaning you can run it locally without paying for an AI subscription.

Of course, you'll need a capable GPU and some setup, but for indie game developers and 3D artists, this could be a huge time-saver.

## Research

* Verdict: Valid. StableGen is a real, free GPL-3.0 Blender add-on that uses ComfyUI. Version 0.4.0 does the prompt-to-mesh, auto-rig, Mixamo retarget and export steps the post describes. The link is public, so you don't need the DM.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [StableGen (sakalond) (github.com)](https://github.com/sakalond/StableGen): repo, found by search, verified, high confidence. The README covers TRELLIS.2 prompt-to-mesh, SkinTokens rigging, Mixamo/FBX retargeting, glTF/FBX export and ComfyUI. I opened it. The sakalond owner name came from search results, and the opened page also credits Ondřej Sakala.
* [StableGen 0.4.0 release news (ComfyUI Wiki) (comfyui-wiki.com)](https://comfyui-wiki.com/en/news/2026-10-28-stablegen-0-4-0): page, found by search, verified, medium confidence. I opened it. It confirms the 0.4.0 character generation, auto-rig, Mixamo retargeting and FBX export features. It is a secondary source.

### Key steps

1. Download the ZIP for your OS from the GitHub Releases page.
2. In Blender (4.2–4.5 or 5.1+; not 5.0): Edit > Preferences > Get Extensions > Install from Disk, then pick the ZIP.
3. Under System > Network, enable Allow Online Access.
4. Press N in the 3D Viewport and open the StableGen panel. In the ComfyUI setup page, install StableGen's own ComfyUI, point to an existing ComfyUI folder, or connect to a remote server.
5. Under Models, install what you need, such as TRELLIS.2 for meshes or SDXL/Qwen Image for texturing.
6. Set the Output Directory in the add-on preferences.
7. In the Mesh tab, enter a text prompt, pick a preview image, and enable Auto-rig to get a rigged character.
8. Retarget Mixamo FBX/BVH animations onto the rig. Export to FBX (Unreal/Unity) or glTF (Godot).

### Not found

The post's own DM link wasn't visible. I matched the public repo by name and features. Hardware limits: about 8 GB VRAM for SDXL, 16 GB or more for Qwen Image, and 10–50+ GB of disk. Some models, such as Qwen Image 2.1, are non-commercial only. A Zaws77/StableGen mirror also turned up in search, which I did not open.
