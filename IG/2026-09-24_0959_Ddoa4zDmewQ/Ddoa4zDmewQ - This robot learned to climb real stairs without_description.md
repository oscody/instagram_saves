---
shortcode: "Ddoa4zDmewQ"
url: "https://instagram.com/reel/Ddoa4zDmewQ/"
type: "Reel"
author: "githubsignals"
shared: "Sep 24, 2026, 09:59 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# NVIDIA GRAIL: robot stair climbing from synthetic data

The reel walks through the README of NVIDIA's open-source GRAIL project, which generates humanoid loco-manipulation training data from 3D assets and video priors. The on-screen text and captions say the resulting policies transfer to a real Unitree G1 robot for object pick-up and stair-climbing.

Written by claude-haiku-5-5.

## What it teaches

1. Compose 3D assets, simulator-ready scenes, and robot-proportioned characters.
2. Use video foundation model priors to synthesize metric 4D human-object interaction (HOI) trajectories.
3. Retarget those trajectories to a Unitree G1 robot.
4. Train task-general policies for pick-up, whole-body manipulation, sitting, and terrain traversal using only GRAIL-generated data.
5. Transfer the resulting egocentric visual policies to the real robot for object pick-up and stair-climbing.

## Source

* Link: nvlabs/grail

## Caption

This robot learned to climb real stairs without training on real stairs. 

Train a robot to climb stairs without ever touching the real thing. That is exactly what NVIDIA’s GRAIL does. It takes 3D models and video clips to simulate humans moving and grabbing objects in the digital world. Then it teaches a robot brain to copy those moves. The coolest part? The robot can pick up items and climb actual stairs in reality, all from that fake data. It saves researchers from building a thousand test tracks just to learn one trick. If you want to know how robots learn to move without a physical teacher, this is the project to watch.

Open source: nvlabs/grail

Follow for more open source project drops.

#Robotics #EmbodiedAI #NVIDIA #RobotLearning

## Research

* Verdict: Valid. The NVlabs/GRAIL repo exists and its README matches the post: a digital pipeline retargeted to a Unitree G1, with sim-to-real pick-up and stair-climbing demos. The claims rest on demo GIFs and the paper, and the README gives no success rates.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [NVlabs/GRAIL (github.com)](https://github.com/NVlabs/GRAIL): repo, in the post, verified, high confidence. README describes the digital HOI data pipeline, G1 retargeting, and sim-to-real pick-up and stair-climbing, as in the reel.

### Key steps

1. Clone the repo and initialize its submodules.
2. Pull the Docker image docker.io/nvgrail/grail:1.1.1 (or the -minimax-h3 variant) and run it with --gpus all, mounting the repo at /workspace/grail.
3. In the container, run the environment install script and activate the grail conda environment.
4. Download the checkpoints (GEM-SMPL, GEM-SOMA, FoundationPose) and a sample object asset.
5. Create a .env file with OpenAI, Kling and Hugging Face tokens.
6. Run python -m grail.pipelines.gen_terrain to make procedural terrain.
7. Run python -m grail.pipelines.gen_2dhoi, then python -m grail.pipelines.recon_4dhoi, to generate 2D HOI and reconstruct 4D HOI.
8. Use the released tracking policy checkpoints (2026-07-15) for the policy stage.

### Not found

The paper was not opened. No quantitative sim-to-real results were checked. The license is non-commercial.
