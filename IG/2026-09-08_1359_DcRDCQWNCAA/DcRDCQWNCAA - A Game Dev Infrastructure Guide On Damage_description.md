---
shortcode: "DcRDCQWNCAA"
url: "https://instagram.com/reel/DcRDCQWNCAA/"
type: "Reel"
author: "taori_dev"
shared: "Sep 08, 2026, 01:59 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Centralizing Damage Logic With a Damage Manager

A Unity game dev reel on structuring damage code, showing a 1,000,000-hit damage calculation benchmark that drops from 1000 ms of CPU time without Burst to 240 ms with Burst compile.

Written by claude-haiku-5-5.

## What it teaches

1. Don't program damage inline where each hit is applied; it may work for a while but is slow and inefficient.
2. Create a separate damage manager script (the reel shows a New Script.cs file).
3. When inflicting damage, call a function on the damage manager instead of handling it in place.
4. Centralizing damage logic in one place makes it easier to update and optimize.
5. Use Unity's Burst compiler on the damage manager to speed up the calculations.
6. For reference, the reel's benchmark of 1,000,000 damage calculations took about 1000 ms of CPU time without Burst and 240 ms with Burst (about 4x faster).

## Caption

A Game Dev Infrastructure Guide On Damage

## On screen text

CENTRALIZE DAMAGE
New Script.cs
do is createa
NoOptimization
With.Optimization
Here'sasideby
1,000,000 DAMAGE
CALCULATIONS
CPUTIME
1000ms
NO BURST
X SPEDUP
Cpu time. That is
240 ms
BURST
