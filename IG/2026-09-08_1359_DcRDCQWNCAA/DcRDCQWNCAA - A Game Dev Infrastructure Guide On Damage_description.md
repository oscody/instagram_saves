---
shortcode: "DcRDCQWNCAA"
url: "https://instagram.com/reel/DcRDCQWNCAA/"
type: "Reel"
author: "taori_dev"
shared: "Sep 08, 2026, 01:59 PM"
transcribed_by: "faster-whisper base"
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

## Research

* Verdict: Partly valid. This is a general Unity design tip with no single resource. Centralizing damage logic and using Burst is sound advice. The 1000 ms to 240 ms benchmark is the reel's own number and I couldn't check it. Burst also only works on a restricted C# subset (static methods or jobs with unmanaged data), not on any MonoBehaviour.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Unity Burst compiler manual (docs.unity3d.com)](https://docs.unity3d.com/Packages/com.unity.burst@1.8/manual/index.html): guide, found by search, verified, medium confidence. Official docs confirm Burst compiles a C# subset (HPC#) via [BurstCompile] on jobs or static methods, and give no speedup figures.

### Key steps

1. Create a DamageManager script instead of applying damage inline at each hit.
2. Have attackers call a DamageManager method when they deal damage.
3. Put the bulk math in a static method or an IJob struct that uses unmanaged data such as NativeArray.
4. Add [BurstCompile] to that job or method and its parent type.
5. Profile before and after (the reel shows 1,000,000 calculations at about 1000 ms without Burst and 240 ms with it).

### Not found

No downloadable code or named repo was shown in the reel, and I couldn't check the benchmark numbers. The vault has no related notes.
