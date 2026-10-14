---
shortcode: "Dc9JM6POZSJ"
url: "https://instagram.com/reel/Dc9JM6POZSJ/"
type: "Reel"
author: "taori_dev"
shared: "Sep 06, 2026, 11:59 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Shrinking attack network traffic with a shared lookup table

A high attack speed can lag multiplayer games because each attack resends mostly unchanged data. The reel shows a "Bolt" projectile whose ID, lifetime, and spec hash are stored once in a client lookup table, so each attack only needs to send ID 37 plus position and velocity.

Written by claude-haiku-5-5.

## What it teaches

1. Look at the data sent for each attack and find the values that don't change between attacks.
2. Group those unchanging values (for example projectile ID, lifetime, spec hash) into one shared data set.
3. Assign that combination an ID and store it in a lookup table that every client already has.
4. Send only the ID plus the changing values (position and velocity) over the network instead of the full data.
5. Clients look up the ID in their local table to recover the full data, which greatly reduces network traffic.

## Caption

Your Attack Speed Is Lagging Everyone!
