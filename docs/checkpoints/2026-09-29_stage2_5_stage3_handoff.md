# Session Handoff

## Project Goal

长期、项目驱动地学习 Robot Learning / Robotics / Embodied AI，最终形成可运行实验和求职可展示成果；保留真实学习轨迹。

## Current Environment

2026-09-29 本机核对：macOS 15.8 arm64（已有记录为 MacBook Pro M1 Max）；Conda `robot-learning`；Python 3.11.16、PyTorch 2.14.0、MuJoCo 3.13.0、ManiSkill 3.0.1、Gymnasium 1.3.0、SAPIEN 3.0.3。当前进程 MPS built=True、available=False，原因未确定。使用 `conda run -n robot-learning` 可运行项目环境 Python。

## Repository

`~/Projects/robot-learning`，GitHub `weipeiluo1123-ai/robot-learning`。2026-09-29 检查时 `main` HEAD `74fed7d`，本地 `origin/main` 同指该提交，未联网刷新。`mujoco/` 保留 Stage 1/2 实验；`bridge/01`–`08` 为 Stage 2.5；`docs/` 有阶段记录与交接。维护开始前该详细学习记录尚未跟踪；现已按用户要求改名并纳入版本控制，正文未覆盖。

## Completed This Session

检查 Git、目录、README、文档、MuJoCo 与 bridge 文件；核对环境版本。重新运行 `bridge/06_truncated.py` 和 `08_simple_env.py`，确认时间截断及到达目标的输出。整理 Stage 2.5 学习记录、当前状态、路线及 renderer 故障记录。本次未运行 ManiSkill 环境，也未修改实验代码。

## Important Concepts Already Understood

Stage 1/2：qpos 与 joint 类型、joint/actuator、Pose/Frame、FK、IK 多解、控制与 tracking。Stage 2.5：state/observation/action/transition、规则 policy、负距离 reward、reset/episode、terminated/truncated、`env.step()`；初步理解 Python `dict`、返回值解包、`class`/`self`/`__init__`。理解范围以 toy 实验为准。

## Current Code / Experiments

`bridge/08_simple_env.py`：reset 返回 `{'position': 1, 'goal': 5}`；四次 `+1` 达到目标，reward -3→0，terminated=True。`bridge/06_truncated.py`：max_steps=3 时未到目标而 truncated=True。MuJoCo 实验已在 Stage 1/2 记录，本次未重跑 Viewer。仓库尚无 ManiSkill 实验文件。

## Problems Encountered

首次直接进入 ManiSkill 信息量过大，故插入 Stage 2.5。原始 handoff 记录：ManiSkill 可导入，但 `python -m mani_skill.examples.demo_random_action -e PickCube-v1` 报 Vulkan `ErrorIncompatibleDriver`；本次未复跑，headless CPU 可行性未知。MPS 的历史成功记录与本次不可用状态仍需分开看待。

## Decisions Made

保留 Stage 0–6 总路线；Stage 2.5 是过渡，不表示 Stage 3 已完成。下一实验只做最小 ManiSkill 环境创建和 `reset()` 的结构观察；先辨别失败层级，再决定环境处理。保留原始 handoff 与历史文档，不自动 commit/push。

## Current Position

`SimpleEnv` 已运行并理解接口；ManiSkill 安装存在，但没有成功创建环境的证据。当前正处于 Stage 3 第一个最小实验之前。

## Next Step

在已安装环境中尝试最小 headless CPU ManiSkill 任务，调用 `reset()`，仅查看返回结构及少量 state/state_dict 字段，与 `SimpleEnv.reset()` 对照。若失败，保存准确异常并定位 Python、SAPIEN、renderer 等层级；不要把未验证的参数组合当成解决方案。

## Things Not To Re-Explain From Scratch

不重新从头讲 MuJoCo 基础、Pose/FK/IK、规则 policy、reward 方向、reset/step、terminated/truncated。直接从 `SimpleEnv → ManiSkill` 的接口对照开始，遇到差异再解释。

## Learning Preferences

用户有 C++/软件工程背景，Python 与机器人知识逐步建立。采用“一个实验 → 一个现象 → 一个概念”，解释为什么；新 Python 语法随代码解释，不一次展开大型理论树。

## New Chat Startup Prompt

我在维护 `~/Projects/robot-learning`（GitHub `weipeiluo1123-ai/robot-learning`）。请先读取 `docs/current_state.md`、`docs/stages/stage2_5_robot_learning_bridge.md` 和本 handoff，并检查真实 Git 状态。Stage 0–2 的基础节点与 Stage 2.5 的 `SimpleEnv` 已完成；ManiSkill 3.0.1 可导入，但此前 PickCube 示例遇到 Vulkan `ErrorIncompatibleDriver`，还没有成功运行的 ManiSkill 环境。请按“一个实验 → 一个现象 → 一个概念”，从最小 headless CPU 环境创建和 `reset()` 开始，对照 `bridge/08_simple_env.py`，只观察返回结构与少量字段；失败时先定位报错层级。不要提前进入 BC/PPO、camera、GUI 或大型理论树，也不要自动 commit/push。
