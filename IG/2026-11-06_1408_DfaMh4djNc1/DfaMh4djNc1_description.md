---
shortcode: "DfaMh4djNc1"
url: "https://instagram.com/p/DfaMh4djNc1/"
type: "Carousel"
author: null
shared: "Nov 06, 2026, 02:08 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-06"
---

# AI workflow for making a 3D browser game

A six-slide breakdown of how developer Shikhar built the 3D browser game Sumiro in 24 hours, naming the AI and 3D tools used at each stage. The slides also link to the playable game.

Written by claude-haiku-5-5.

## What it teaches

1. Step 1: Generate a reference video with Flux 3 Max to set the look, world and main character.
2. Step 2: Screenshot the video, rebuild the assets in Blender, and place them in Three.js, using Claude Code dynamic workflows so agents build and check in parallel.
3. Step 3: Screenshot the character, create four side views with GPT Image, turn them into a 3D model with Tripo, and have Claude Opus add cloth physics and animations.
4. Step 4: Play the prototype and confirm it works before building more.
5. Step 5: Use GPT Image and the existing art style to create concept art for each level, up to 8 images per level.
6. Step 6: Build all the scenes, play them, report bugs, let the agents fix them and improve the objects, and repeat until each concept is a playable 3D level.

## Source

* Link: xikhar.github.io/sumiro

## Caption

Swipe ⬅️ Developer Shikhar created a complete 3D browser game called Sumiro in just 24 hours, relying on Claude Opus 5.5 for most of the programming and several other AI tools for the visuals.

The process began with a short reference video generated using Flux 3 Max, establishing the game’s visual style, environment, and main character.

Shikhar then recreated the assets in Blender and assembled the game using Three.js, while multiple Claude Code agents worked simultaneously on development, testing, and debugging.

To build the playable character, he generated four different views using GPT Image, converted them into a 3D model with Tripo, and used Claude to implement cloth physics and character animations.

GPT Image also helped design the individual levels, which Claude’s agents transformed into playable 3D environments. Bugs were addressed through repeated feedback and testing.

The finished game combines puzzles, parkour, and combat against various enemies. It’s available to play for free directly in a browser at xikhar.github.io/sumiro.

Shikhar acknowledged a few limitations, including underwhelming music because Claude cannot evaluate audio directly. He also explained that the awkward movement shown in the demo came from an AI agent controlling the character rather than a human player.

What do you think about AI making this level of game development possible in just 24 hours? 🤔

➡️ Want to stay ahead in the world of AI? Grab your coffee, relax, and let our newsletter deliver the biggest updates straight to your inbox.

## Research

* Verdict: Partly valid. The game page at xikhar.github.io/sumiro exists, but when I opened it I got only a title screen ("grinding ink"). I couldn't confirm the 24-hour claim or the tool chain from any public source. The workflow comes only from Shikhar's X thread, which I couldn't find.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Sumiro (playable game) (xikhar.github.io)](https://xikhar.github.io/sumiro): page, in the post, verified, medium confidence. The URL in the post opens to a page titled Sumiro with the tagline 'grinding ink', but the fetch showed no gameplay or workflow details.
* [Runtimewire: Claude Opus 5.5 builds a browser Spider-Man game, with Shikhar steering (runtimewire.com)](https://runtimewire.com/article/claude-opus-55-spiderbench-browser-game): page, found by search, not opened, low confidence. A search result describes an earlier Shikhar (@xikhar) project using Blender, image generation and Three.js. It is not Sumiro, and I didn't open it.

### Already in IG saves

* Similar: Web: [Five AI tools: Denovo, Yapper, Shipper Max, Tripo, Pickle (instagram.com)](https://instagram.com/p/DYXIrpRSUJu/) (`DYXIrpRSUJu`). A list of AI tools that includes Tripo (text to 3D) and Shipper Max (games built and published).
* Similar: Web: [GPT-6 Astra builds full 3D fantasy game (instagram.com)](https://instagram.com/p/DdJ3WtSORK9/) (`DdJ3WtSORK9`). A browser 3D game built with AI code plus Tripo-generated 3D assets.

### Key steps

1. Make a short reference video with Flux 3 Max to set the look, world and main character.
2. Screenshot the video, rebuild the assets in Blender, and place them in Three.js. Run Claude Code agents in parallel to build and check.
3. Screenshot the character and make four side views with GPT Image. Turn them into a 3D model with Tripo.
4. Have Claude Opus add cloth physics and animations to the character.
5. Play the prototype and confirm it works before building more.
6. Make concept art for each level with GPT Image (up to 8 images per level).
7. Build all the scenes, play them, report bugs, let the agents fix them, and repeat until each concept is a playable 3D level.

### Not found

Shikhar's original X thread (the 'prompt below' mentioned on the slides) was not found. The 24-hour claim, the tool chain and the game's puzzle, parkour and combat features are unconfirmed. The Sumiro page showed only a title screen when fetched, and it may need JavaScript to load.
