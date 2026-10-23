---
shortcode: "Db_BKM3xYLT"
url: "https://instagram.com/reel/Db_BKM3xYLT/"
type: "Reel"
author: "malvika.jain"
shared: "Oct 12, 2026, 02:10 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Getting started in robotics without a robot

A creator walks through the setup she used to start learning robotics without physical hardware, showing a simulator demo of a robot arm picking up an object and a blog post with the write-up. The on-screen text covers choosing a simulator and a robot arm.

Written by claude-haiku-5-5.

## What it teaches

1. Start with a robot simulator instead of physical hardware.
2. Pick a simulator that fits your computer: MuJoCo was chosen because it runs without a graphics card and is less complex than Gazebo, while NVIDIA Isaac Sim needs a graphics card.
3. Know that simulators are controlled through simple Python interfaces, so the robot's movement and the scene are set by code.
4. Match the robot to the task when you can; if you just want to learn, pick a common robot arm, such as the LeRobot SO101, to get familiar with it in the simulator.

## Source

* Link: https://www.aamir.me/getting-started-robotics/

## Caption

link: https://www.aamir.me/getting-started-robotics/ 
author: @aamir1rasheed 

#robotics #engineer #creative

## Research

* Verdict: Valid. The blog post exists and matches the reel. It picks MuJoCo over Isaac Sim and Gazebo for the reasons given, uses the SO101 arm, and drives everything from Python.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Getting Started in Robotics Without a Robot (aamir.me) (aamir.me)](https://www.aamir.me/getting-started-robotics/): guide, in the post, verified, high confidence. Opened it. It covers MuJoCo vs Isaac Sim and Gazebo, and the LeRobot SO101 arm.
* [mujoco_menagerie (github.com)](https://github.com/google-deepmind/mujoco_menagerie): repo, in the post, not opened, medium confidence. Linked from the blog post as the source of the SO101 model files. I did not open it.
* [MuJoCo (mujoco.org)](https://mujoco.org/): tool, in the post, not opened, medium confidence. Linked from the blog post as the simulator. I did not open it.
* [LeRobot ACT docs (huggingface.co)](https://huggingface.co/docs/lerobot/en/act): page, in the post, not opened, medium confidence. Linked from the blog post as the docs for the ACT model it trains. I did not open it.

### Key steps

1. Install MuJoCo and use its Python interface. It runs on a modest laptop with no GPU.
2. Get the SO101 arm model from mujoco_menagerie.
3. Build a pick-and-place scene: a red cube placed at random, a green target pad, a scene camera and a wrist camera.
4. Generate about 1,000 expert demonstrations with inverse kinematics, using the simulator's exact object positions.
5. Train an ACT policy of about 60M parameters on camera images and joint angles.
6. Evaluate on 100 new setups and count the cubes placed fully on the pad.
7. Iterate: fix label misalignment first, then add training, a larger pad and smoother trajectories. The author reached 99/100.

### Not found

I did not open the three linked pages (MuJoCo, mujoco_menagerie, the LeRobot ACT docs). The success rates and the 60M-parameter figure come from the blog post only.
