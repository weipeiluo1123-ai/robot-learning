# Session Handoff

> Historical snapshot from the Stage 1 handoff. Superseded by [the 2026-09-26 Stage 2 completion / Stage 3 handoff](2026-09-26_stage2_complete_stage3_handoff.md); the notes below preserve the project state as it was at that time.

## Project Goal

通过项目驱动的方式学习 Robot Learning / Robotics / Embodied AI，形成可运行代码、实验结果、GitHub 项目和可展示成果。

## Current Environment

- MacBook Pro M1 Max
- Apple Silicon / arm64
- Conda environment: robot-learning
- Python: 3.11.16
- PyTorch: 2.14.0
- MuJoCo: 3.13.0
- MPS: available and previously verified

## Repository

- Local: ~/Projects/robot-learning
- GitHub: weipeiluo1123-ai/robot-learning
- Branch: main
- Existing local changes are not committed.
- Current project includes Stage 0 and Stage 1 documentation, three MuJoCo experiments, an end-effector trajectory image, and prompt/documentation support files.

## Completed This Session

- Inspected the real repository, git status, recent history, README, .gitignore, docs and mujoco experiments.
- Confirmed current repository state is beyond the old Day 1 wording.
- Updated Stage 1 documentation to include the completed 1-DOF pendulum introduction.
- Kept 2-DOF two-link arm as the current unfinished learning target.
- Updated current_state.md from Day-oriented wording to Stage-oriented project context.
- Added roadmap.md with the six long-term stages.
- Preserved troubleshooting.md without adding duplicate problems.
- Created this handoff checkpoint.
- Did not modify experiment code, SSH keys or Conda global configuration.
- Did not commit or push.

## Important Concepts Already Understood

- Conda environment isolation and the difference between system Python, base and project Python.
- PATH, which, type and CONDA_PREFIX as environment inspection tools.
- PyTorch CPU Tensor, MPS backend and Apple GPU computation.
- MuJoCo as a physics simulator; PyTorch as learning framework; ROS2 as robot software communication/organization.
- MJCF/XML describes a model but does not execute a simulation loop.
- MjModel represents model structure/rules; MjData represents current simulation state; mj_step advances physics.
- qpos is not universally XYZ.
- hinge qpos represents a joint angle.
- freejoint has 6 DOF but nq=7 because orientation uses a quaternion.
- joint position and joint axis describe where a joint is and which direction it acts around.
- A joint and an actuator are different concepts.
- Viewer visualizes state; terminal output can expose numerical state.
- Git tracks files, not empty directories.

## Current Code / Experiments

- mujoco/01_falling_ball/: completed basic falling-ball experiment.
- mujoco/02_pendulum/: completed first hinge / 1-DOF pendulum experiment.
- mujoco/03_two_link_arm/: existing 2-DOF arm code with two position actuators and an end-effector trajectory trail; not yet fully understood or marked complete.
- docs/images/End-effector trajectory of a 2-DOF MuJoCo arm under position control.png exists as an experiment artifact.

## Problems Encountered

Detailed entries are in docs/troubleshooting.md. High-value lessons include:

- CLI help is not universal for shell builtins.
- Python attributes are not necessarily callable methods.
- Python REPL ... means continuation, not necessarily a hang.
- A foreground Viewer occupying the terminal is normal process behavior.
- Current ball.xml parameters differ from one earlier numerical falling-ball record; this is documented as a historical discrepancy.

## Decisions Made

- Use Stage 0 / Stage 1 terminology instead of Day 0 / Day 1.
- Keep the existing repository layout rather than forcing a sessions/ directory migration.
- Treat Stage 1 as in progress.
- Treat the two-link arm as the next experiment, not as a completed learning result.
- Do not modify ball.xml, main.py or other experiment code while maintaining documents.
- Do not commit or push automatically.

## Current Position

Stage 1 is at the beginning of the 2-DOF two-link arm experiment. The next work is to run and observe the existing code, then understand parent/child body hierarchy, qpos[0]/qpos[1], actuator/control and end-effector trajectory behavior.

## Next Step

1. Run the existing two-link arm experiment.
2. Observe numerical joint state, control target and end-effector trail.
3. Record only verified concepts in stage1_mujoco_basics.md and current_state.md.

## Things Not To Re-Explain From Scratch

- Basic Conda environment creation and activation.
- Basic PATH / which / type inspection.
- PyTorch CPU versus MPS verification.
- Basic MuJoCo model/data/step mental model.
- Why the standalone Viewer can move without a user-written mj_step.
- The already-recorded troubleshooting entries.

## Learning Preferences

The learner has a C++ / software engineering background and is progressively learning Python, robotics and Robot Learning.

Preferred loop:

experiment -> observe -> find problem -> understand concept -> modify code -> verify -> summarize

Explain why, preserve mistakes and corrections, distinguish understood concepts from first exposure, and avoid dumping large prerequisite courses.

## New Chat Startup Prompt

You are continuing work on the Robot Learning repository at ~/Projects/robot-learning. Read docs/current_state.md, docs/roadmap.md, docs/stages/stage1_mujoco_basics.md and docs/troubleshooting.md before acting.

Current position: Stage 1 — MuJoCo Fundamentals is in progress. Falling ball and 1-DOF pendulum are completed at a basic understanding level. The existing mujoco/03_two_link_arm/ experiment is the next target, but do not call it completed before observing and understanding it.

Use the loop: experiment -> observe -> find problem -> understand concept -> modify code -> verify -> summarize. Preserve the learner's real mistakes and uncertainty. Do not jump to ROS2, VLA, Diffusion Policy, full robotics theory or advanced quaternion math. Do not modify experiment code unless explicitly requested. Do not commit or push without explicit approval.
