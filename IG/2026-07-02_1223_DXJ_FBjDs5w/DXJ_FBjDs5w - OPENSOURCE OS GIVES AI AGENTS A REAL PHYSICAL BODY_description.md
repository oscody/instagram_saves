---
shortcode: "DXJ_FBjDs5w"
url: "https://instagram.com/reel/DXJ_FBjDs5w/"
type: "Reel"
author: "marc.kaz"
shared: "Jul 02, 2026, 12:23 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# DiMOS: open-source OS for AI agent robots

The reel announces DiMOS, an open-source operating system that lets LLM agents such as Claude Code and OpenClaw control drones and humanoid robots through cameras, lidar and actuators. Screen recordings show a terminal agent interface alongside lidar point clouds, detected objects and robot camera feeds.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/dimensionalOS/dimos

## Caption

🚨 OPEN-SOURCE OS GIVES AI AGENTS A REAL PHYSICAL BODY

DiMOS just dropped — the operating system that lets LLMs like Claude Code and OpenClaw control real-world robots.

Ships with:
• Programmable interface for drones & humanoids
• Direct camera, lidar & actuator integration
• Full real-time LLM control of physical hardware
• 100% open source

AI agents now have bodies.

👉 https://github.com/dimensionalOS/dimos

Who’s giving AI agents a physical body today? Drop a 🔥

## Research

* Verdict: Partly valid. DimOS is real and open source, and it works with Claude Code and OpenClaw through MCP and the CLI. The repo calls itself a pre-release beta, and hardware support is uneven (only Unitree Go2 is stable; drones are alpha). So "full real-time LLM control" is overstated.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [DimOS (dimensionalOS/dimos) (github.com)](https://github.com/dimensionalOS/dimos): repo, in the post, verified, high confidence. The repo page describes a Python robot OS for humanoids, quadrupeds and drones with agent and MCP control, matching the post.

### Key steps

1. Run the official installer script from the repo README (sets up Python 3.12 and DimOS). Ubuntu 22.04/24.04 is stable; macOS is alpha.
2. Try it with no hardware: `dimos --replay run unitree-go2`.
3. Simulate a quadruped in MuJoCo: `dimos --simulation run unitree-go2`. For a humanoid, use `dimos --simulation run unitree-g1-sim`.
4. For a real Go2, set ROBOT_IP and run `dimos run unitree-go2`.
5. Point Claude Code or OpenClaw at the repo's AGENTS.md.
6. Drive it from the agent with the CLI: `run --daemon`, `agent-send`, `mcp list-tools` and `mcp call`.

### Not found

The license type was not shown on the repo page. I did not open the LICENSE file.
