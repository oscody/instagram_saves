---
shortcode: "DcOYjLqtQAv"
url: "https://instagram.com/reel/DcOYjLqtQAv/"
type: "Reel"
author: "githubsignals"
shared: "Sep 12, 2026, 10:55 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# AnyCreature: text-to-3D creature generator from a JSON spec

A reel promoting the open-source AnyCreature project, which compiles an animated, game-ready 3D creature from one JSON spec or a text prompt. The video shows a flying creature model and the project's README, with its quick start, knob table and folder layout.

Written by claude-haiku-5-5.

## What it teaches

1. Run `bash setup.sh` to install dependencies and the red/green ruler checks.
2. Confirm setup.sh prints `calibrate OK` before trusting any other output.
3. Generate a model with `node engine/cli.js example/wolf.json out/wolf.glb`.
4. For a full text-to-creature session, point an agent at MANUAL.md and have it read cards/ in order: 00_START, 01_LOW, 02_MID, 03_HIGH, 04_SHIP.
5. Tune smooth_angle (default 50) in the spec root or per volume/part: higher gives a smoother body, lower gives more facets.
6. Set shading in the spec root to control the vertical colour gradient and grain.
7. Use build: "rigid" in the spec root only for robots and crystals, since it is the only way to get a fully faceted body past the checker.
8. Set ao to false in the spec root to skip the ambient occlusion bake.
9. Pick a QC role preset (minion.json, npc.json, boss.json) in harness/presets/ for different budgets and thresholds.

## Source

* Link: ariescar/anycreature

## Caption

Turn a Text Prompt Into an Animated, Game-Ready 3D Creature

AnyCreature is the text-to-3D pipeline that turns a simple written order into a fully animated, game-ready model. This is the creature generator that actually works, solving the nightmare of hand-sculpting every asset from scratch. Instead of downloading generic packs or wrestling with complex software, you just type a prompt like "menacing mountain giant." The system handles the heavy lifting, asking only a couple of clarifying questions before it builds the shape, colors, and animations itself. The coolest part is its strict quality control, where a separate AI agent acts as a blind judge to ensure the final model actually looks good, not just technically correct.

Open source: ariescar/anycreature
Spotted on Hacker News.

Follow for more open source project drops.

#3DGeneration #GameDev #GenerativeAI #AiAgents #aitools

## On screen text

ubAreaanyrea
githubomariescarranyere
e
Security
MIT license
README
plain text.
Quick start
deps reargren rute
one spec that has to pa
d from bad on your machine.
bearanyr
github.omanescaranyreatur
deps + redrgreen rule
pash setup.sh
Driving it harder
What it changes
Knob
Where
reasethreshol ngree.auit
spec root or
hoiebody vercal colourap and
rainrane op.bto
Shading
Specroot
noise:[size,aount
The onywytoget auly faceted
build:
Spec root
body past
rigid"
crystals, not for animals.
Penverexmbinocusona
to skip the bake.
Rolepresets-anonson
harness
peon bo.onaeren
QC
presets
budges andthreshold perole.
What is actually in here
What it holds
Folder
ub-Arearanyre
github.omarescaranyereatur
C
E.igherooher boy lower
mooth_ang le
per volume/
more facets.
part
wholebody verica coourapand
radientop.bottm
noise:(size,amounty
The onlywy togetaly facete
body past hecheckerfrobosand
rigian
rystals, not for animals.
Perverexamblen ocusionatse
ao
Role presets-anon-son
pe-Json boss.ondirent
presets/
budgets and thresholdsperole.
Zero runtime dependencies
engine
The five stage
gsenres
cards/
BLINDJUDGETO
. claims judge.
harness/
thedeivery paker and the puiser
exampler
calibration/
How it works
The two gates
