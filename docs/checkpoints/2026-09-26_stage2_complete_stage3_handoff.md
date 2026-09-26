# Session Handoff

> 本交接依据 2026-09-26 的仓库核对与用户提供的 Stage 3 handoff。Stage 2 状态以用户实际学习总结为准；代码运行范围会单独注明。

## Project Goal

通过可运行项目学习 Robot Learning / Embodied AI / Robotics，形成能展示的代码与实验成果。就业导向，优先尽快进入 ManiSkill、模仿学习与强化学习的实践。

学习闭环：实验 → 观察 → 发现问题 → 理解概念 → 修改代码 → 验证 → 总结。教学节奏是“一个实验 → 一个现象 → 一个概念”。

## Current Environment

- MacBook Pro M1 Max，Apple Silicon / arm64，macOS 26.6.2。
- Conda 环境：`robot-learning`；Python 3.11.16。
- PyTorch 2.14.0；MuJoCo 3.13.0；NumPy 2.4.6。
- Stage 0 曾成功验证 PyTorch MPS 运算；本次进程检测到 MPS 已构建但不可用，原因未确定。
- 本地环境中尚未安装 `mani_skill`。Stage 3 的安装与 Mac 适配仍待确认。

## Repository

- 本地：`~/Projects/robot-learning`
- GitHub：`weipeiluo1123-ai/robot-learning`
- 当前分支：`main`；remote `origin` 使用 SSH 地址。
- 本次核对开始时 HEAD 为 `3018314`，本地 `origin/main` 引用相同（未联网 fetch）。
- 当前文档改动未提交；`trajectory_test.py` 和 `trajectory_viewer.py` 是用户新增的未跟踪实验文件。

## Completed This Session

- 根据用户提供的 Stage 2 总结，将 Stage 2 标记为基础学习节点完成，近期目标设为 Stage 3。
- 整理 Stage 2 学习记录：Pose / Frame、FK、joint 与 Cartesian 描述、IK 多解与连续性、位置控制观察、重力补偿、路径与时间参数化。
- 更新 `current_state.md`、`roadmap.md`、README 和 Stage 1 的历史状态说明。
- 将真实学习到的控制、IK 连续性、tracking lag 现象补充至 troubleshooting。
- 修正 `docs/checkpoints/` 被通用忽略规则遮蔽的问题，仅放行其中 Markdown handoff。
- 本次助手运行了 6 点无界面 IK 脚本；每点末端位置误差均小于 0.01，最大值约 0.0096501。没有运行 Viewer GUI。
- 未提交或推送。

## Important Concepts Already Understood

- Pose 包含位置与朝向，必须说明参考坐标系；已用 MuJoCo 的 `site.xpos`、`site.xmat` 和 Local ↔ World 变换。
- FK 沿运动学树把关节配置映射为末端位姿；Joint Space 与 Cartesian Space 是同一状态的不同描述。
- 枚举 IK 可能有多个解；沿 Cartesian path 可在容差内参考前一帧关节配置，减少 branch 跳变。
- 阻尼改善振荡不必然消除重力下的位置误差；提高刚度、选择积分器和重力补偿都会影响结果。
- Path 表示经过哪里；trajectory 还表示何时经过。参考关节轨迹与实际关节运动的差异是 tracking error。
- 不需要在进入 Stage 3 前补完插值语法、PID、Jacobian 或高级运动规划。

## Current Code / Experiments

- `mujoco/03_two_link_arm/main.py`：较早的综合实验，含坐标变换、单目标 IK 与控制观察。
- `trajectory_test.py`：Cartesian waypoints、容差候选和相邻 IK 解选择；本次无界面运行成功。
- `trajectory_viewer.py`：51 点关节轨迹插值和 MuJoCo Viewer 执行；用户已报告完成 duration 对照与 tracking lag 观察，本次未独立重跑 GUI。
- 其他已有实验：falling ball 与 pendulum。

## Problems Encountered

- 高刚度与原积分器组合曾出现数值不稳定；用户报告改用 `implicitfast` 后明显改善。
- MPS 的历史成功记录与本次进程的可用性不同，原因待在常规终端复核。
- `docs/checkpoints/` 曾被通用 `checkpoints/` 忽略规则遮蔽，现已为 Markdown handoff 放行。

## Decisions Made

- Stage 0、Stage 1、Stage 2 已完成；Stage 2 表示入门学习节点完成，不表示掌握全部理论。
- 当前进入 Stage 3 — ManiSkill / Robot Learning Environment；尚未安装或开始实验。
- 按最小路线推进：先核对安装与 Mac 适配，再运行一个最小 environment，认识 observation、action、reward、terminated / truncated、reset、step，然后用 random 或 scripted action。
- 后续再进入最小 manipulation task、demonstration / Behavior Cloning、PPO。
- 不为抽象而重构工具目录；有真实复用需求再抽象。
- 不自动 commit 或 push。

## Current Position

Stage 2 收尾完成。Stage 3 Day 1 尚未开始；当前确认 `mani_skill` 未安装，需先查官方安装要求与 Apple Silicon 可运行范围，再选择可行环境。

## Next Step

从“ManiSkill 是什么，它与 MuJoCo Stage 2 有什么关系”开始，简要解释后核对官方要求及当前环境，确定是否适合在 M1 Mac 直接运行。然后准备一个真正可运行的最小环境实验，观察一次 reset / step 与 observation、action、reward、terminated、truncated 的对应关系。不要先讲 PPO 数学。

## Things Not To Re-Explain From Scratch

- Conda / Python 环境隔离与项目环境基础。
- MuJoCo 的 model / data / step、Viewer、hinge / DOF 基础。
- Pose、frame transform、FK、Joint / Cartesian Space、基础 IK、多解连续性。
- 已有位置控制、重力补偿与轨迹 tracking 观察。
- Stage 0–2 的基础认知；仅在新实验遇到具体问题时补必要背景。

## Learning Preferences

用户是软件工程专硕，有 C++ / 软件工程背景，Python 基础仍在巩固，目标以就业为主。解释现象背后的原因，遇到新 Python 写法时用简短对照解释；保持小步实验，不一次展开大段理论。

避免提前深入 SO(3)/SE(3)、Jacobian 推导、解析 IK、高级 PID、完整动力学、复杂 motion planning。除非 Stage 3 实际需要。

## New Chat Startup Prompt

你正在协助我维护 `~/Projects/robot-learning`。请先阅读 `docs/current_state.md`、`docs/roadmap.md`、`docs/stages/stage2_robot_control_kinematics.md` 和 `docs/troubleshooting.md`。

Stage 0–2 已完成。现在从 Stage 3 Day 1 开始：先简要说明 ManiSkill 是什么，以及它如何承接 MuJoCo Stage 2；再核对当前 Conda 环境中 ManiSkill 的安装状态、官方安装要求和 Apple Silicon / M1 Max 适配范围。当前环境是 Python 3.11.16，尚未安装 `mani_skill`。不要直接假设 GUI、GPU 或训练功能在 Mac 上可用。

目标是跑一个最小可运行 environment，用 random 或 scripted action 观察 reset / step，并逐步理解 observation、action、reward、terminated、truncated。保持“一个实验 → 一个现象 → 一个概念”，不要先展开 PPO 数学。用户有 C++ / 软件工程背景但 Python 尚在学习，解释代码中实际遇到的新语法。不要重讲 Stage 0–2；不要因完整掌握插值、PID、Jacobian 而阻塞 Stage 3。不要自动 commit 或 push。
