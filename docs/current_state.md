# Current State

这是 Robot Learning 项目的上下文交接文件。优先以磁盘上的代码和本文件判断当前进度；详细问题记录见 troubleshooting.md。

## Long-term Goal

通过项目驱动的方式学习 Robot Learning / Robotics / Embodied AI，逐步形成可运行代码、实验结果、GitHub 项目和可展示的求职成果，而不是只完成一次性 demo 或大量前置课程。

## Current Stage

Stage 1 — MuJoCo Fundamentals（进行中）。

---

## Environment

MacBook Pro M1 Max
Apple Silicon arm64

Conda environment:
robot-learning

Python:
3.11.16

PyTorch:
2.14.0

MuJoCo:
3.13.0

MPS:
available and verified

---

## Repository

~/Projects/robot-learning

GitHub:
weipeiluo1123-ai/robot-learning

Current structure:

```text
robot-learning/
├── README.md
├── .gitignore
├── docs/
│   ├── current_state.md
│   ├── roadmap.md
│   ├── troubleshooting.md
│   ├── stages/
│   │   ├── stage0_environment_setup.md
│   │   └── stage1_mujoco_basics.md
│   └── checkpoints/
└── mujoco/
    ├── 01_falling_ball/
    ├── 02_pendulum/
    └── 03_two_link_arm/
```

---

## Completed

Stage 0:
- Conda
- Python environment isolation
- pip
- PyTorch
- Apple MPS
- Git / GitHub SSH

Stage 1:
- MuJoCo concept
- MJCF/XML basics
- MjModel / MjData
- mj_step
- qpos / qvel
- timestep
- contact
- standalone viewer
- passive viewer
- falling ball
- hinge joint
- joint pos / axis
- DOF
- pendulum
- basic Python syntax encountered during experiments

The two-link arm has code and an end-effector trajectory image in the repository, but it is not yet marked as fully understood or completed.

---

## Important Concepts Already Understood

- qpos is NOT always XYZ.
- hinge qpos = joint angle.
- freejoint has 6 DOF but nq=7 because orientation uses quaternion.
- no joint = fixed body = 0 DOF.
- joint pos = where the joint is.
- joint axis = which direction it rotates/translates around.
- XML describes the model; it does not execute simulation.
- mj_step advances physics.
- Viewer visualizes state.

## Experiments Completed

- `mujoco/01_falling_ball/`: falling sphere, gravity, contact, Viewer and Python-controlled stepping.
- `mujoco/02_pendulum/`: first hinge joint / 1-DOF pendulum experiment.

Present but not yet completed as a learning checkpoint:

- `mujoco/03_two_link_arm/`: 2-DOF two-link arm with position actuators and end-effector trail.

## Problems / Lessons

Keep only high-value lessons here; detailed entries live in `troubleshooting.md`.

- System Python, Conda base and project Python must be distinguished with PATH and executable checks.
- XML/MJCF describes a model; a Viewer or Python loop advances and renders the simulation.
- `qpos` is not universally XYZ; its meaning depends on the joint configuration.
- Git tracks files, not empty directories.
- The current `ball.xml` parameters differ from one earlier falling-ball numerical record; this discrepancy is documented rather than silently rewritten.

## Current Position

Stage 1 is in progress. Falling ball and 1-DOF pendulum experiments have been run and documented at a basic level. The next active experiment is the existing 2-DOF two-link arm; its hierarchy, qpos mapping, actuators and control behavior still need to be understood through observation.

## Next Step

1. Inspect and run the existing two-link arm experiment.
2. Observe the relationship between joint state, actuator target and end-effector trajectory.
3. Update Stage 1 documentation only with concepts actually verified.

Do NOT jump ahead to:
- ROS2
- VLA
- Diffusion Policy
- full robotics theory
- advanced quaternion math.

---

## Learning Style

User has C++ / software engineering background,
but is learning Python and robotics concepts progressively.

Preferred method:

experiment
→ observe
→ ask why
→ explain concept
→ modify code
→ verify

Explain new syntax when it actually appears.
Do not dump prerequisite courses or jump to ROS2, VLA, Diffusion Policy, full robotics theory or advanced quaternion mathematics.
