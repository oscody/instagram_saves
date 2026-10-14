---
shortcode: "DdhgEIeAqzY"
url: "https://instagram.com/reel/DdhgEIeAqzY/"
type: "Reel"
author: "githubsignals"
shared: "Sep 21, 2026, 09:20 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Procedura: open-source text-to-editable-3D model tool

A showcase of Procedura, an open-source tool that turns a text prompt into a parametric 3D program with named parts, materials and moving joints. The video walks through the project's README install section and configuration variables on screen.

Written by claude-haiku-5-5.

## What it teaches

1. Clone the repo with git clone git@github.com:SpatiaOS/Procedura.git, then cd into Procedura.
2. Run bash scripts/install-deps.sh to install Bun, the packages, a Manifold-capable OpenSCAD, Blender and a starter .env.
3. Re-run the script safely; it leaves working parts alone, and bash scripts/install-deps.sh --check reports what is missing without installing.
4. Use --no-blender to skip the roughly 350 MB Blender download, or set PREFIX=/opt to install binaries somewhere else.
5. Make sure OpenSCAD has the Manifold backend, since a pre-Manifold build falls back to CGAL and runs far slower; the installer checks for --backend.
6. Copy .env.example to .env in the repo root and add your endpoint and key.
7. Set OPENAI_BASE_URL (for example https://api.openai.com/v1) and the key variable to choose the endpoint, or use GEMINI_API_KEY and GEMINI_BASE_URL with a gemini: model id for Gemini's native path.
8. Pick any model id your endpoint serves with PROCEDURA_MODEL, for example gpt-5.2 or gemini:gemini-3-pro-preview.

## Source

* Link: spatiaos/procedura

## Caption

Most AI 3D tools give you a frozen mesh. This one gives you the actual code behind the model. 

Generate 3D models from a simple text prompt that you can actually edit like code. Procedura solves the frustrating problem where AI usually spits out a frozen block of geometry that you cannot change without starting over. This tool uses an AI agent to write a parametric program, meaning every part is a named variable you can adjust, scale, or move later. It also adds realistic materials and moving joints, so your model isn’t just a static statue. The coolest part is that it’s not a black box; you get the actual source file to tweak.

Open source: spatiaos/procedura

Follow for more open source project drops.

#3DDesign #CreativeCoding #GenerativeAI #AICoding #Procedural3D

## On screen text

ghub.omspatiosprocedura
C
e
README
MITlicense
LUIILIUI
ric PageaperFO
rther objects coloured by the
edmoe.apar ecopoon h
omes reewth the representation.
a
Install
THEFRUSTRATING...
One commano
OpenADBlender and aarer
what amImissing" check:
# install binaries some
what
where it goes
why
Bun21.3
.bun
OpenSCAD
copiles the generated
t onen
hub.ospataoprocedur
MIT icense
OpenAD.nder andarer
env
what a Imissing" check:
report only, install
the whole pipeline is one
Bun1.3
7.bun
TypeScript program
compiles the generated
opt/openscad
(newes
program to a mesh
Snapshot)
the AOpartscolourPBR
Blender(newest
release)
tic looks at
YOU CANADJUST
Packages
dependencies
node_modules
copied rom.env.exampte ;
repo root
add your endpoint and key
which turns aworking run into
hat ooshung forhours.The instale
checks for
backer
2021.01and predates it.
run ithout it
dref
@GithubSignals
CGALOPENSCAD
Configuration
ubparc
giub.ospatioprocedur
the AO/parts-colour/PBR
Blender (newest
optblenderr
renders the critic looks at
node_modules/.web
pipeline+ Studio
node_modules/
copied fromenv.oxampte;
hich turns aworking run i
checks fo
2021.01 and predates it.
versionmost disribution pe
Procedura makes the sa
atsarup and reustorunwhou
you configure, through
ariabl
V
ETHEACTUAL SOURCE
T
nstean use a emoe key.
not this repo has heard of it:
PROCEDURA_MODELgp-5.2
