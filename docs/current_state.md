# Current State

更新：2026-09-29。详细学习过程见 [Stage 2.5](stages/stage2_5_robot_learning_bridge.md)；本次交接见 [Session Handoff](checkpoints/2026-09-29_stage2_5_stage3_handoff.md)。

## Long-term Goal

通过项目驱动学习 Robot Learning / Robotics / Embodied AI，形成可运行代码、实验结果、GitHub 项目和求职可展示成果。遵循“实验 → 观察 → 发现问题 → 理解概念 → 修改代码 → 验证 → 总结”。

## Current Stage

Stage 0、Stage 1、Stage 2 的基础学习节点及 **Stage 2.5 — Robot Learning Bridge** 已完成。Stage 3 — Robot Learning Environment / ManiSkill 正在准备：已安装 ManiSkill，尝试运行示例时遇到 Vulkan 初始化错误；仓库中尚无 ManiSkill 实验文件或成功运行记录。

## Environment

2026-09-29 在本机核对：

- macOS 15.8 / arm64；硬件型号 MacBook Pro M1 Max 来自已有学习记录，本次未重新读取硬件信息。
- Conda 环境 `robot-learning`：`/Users/weipeiluo/miniforge3/envs/robot-learning`；当前 shell 未激活它，使用 `conda run -n robot-learning` 运行。
- Python 3.11.16；PyTorch 2.14.0；MuJoCo 3.13.0；NumPy 2.4.6；ManiSkill 3.0.1；Gymnasium 1.3.0；SAPIEN 3.0.3。
- PyTorch MPS `is_built=True`、本次进程 `is_available=False`；Stage 0 有成功使用 MPS 的历史记录，差异原因尚未确认。
- Stage 2.5 handoff 记录 ManiSkill 导入成功，`demo_random_action -e PickCube-v1` 在 macOS 上因 Vulkan `ErrorIncompatibleDriver` 失败。本次未复跑该示例，也未验证 headless CPU 路径。

## Repository State

本地 `~/Projects/robot-learning`；GitHub `weipeiluo1123-ai/robot-learning`。2026-09-29 检查时在 `main`，HEAD `74fed7d`，与本地 `origin/main` 引用一致；未联网刷新。维护开始前只有未跟踪的 `docs/checkpoints/stage2.5.md`。

```text
robot-learning/
├── README.md, .gitignore
├── bridge/               # 01–08：state/action 到 SimpleEnv
├── docs/                 # current_state、roadmap、troubleshooting、stages、checkpoints、images、prompts
└── mujoco/               # falling ball、pendulum、two-link arm 与 trajectory 脚本
```

## Completed

- Stage 0：项目环境、Python/Conda、PyTorch CPU/MPS 的基础实验和 Git 工作流。
- Stage 1：MuJoCo falling ball、pendulum、MJCF、Model/Data/Step、Viewer、hinge/DOF。
- Stage 2：two-link arm 的 Pose/Frame、FK、枚举 IK、多解连续性、位置控制、重力补偿和时间参数化轨迹。
- Stage 2.5：手写 toy state/action/goal/policy/reward/episode、时间截断、`env_step()` 和 `SimpleEnv.reset()/step()`；未使用 ManiSkill 实现这些概念。

## Concepts Understood

- `qpos` 不一定是 XYZ；hinge 的 `qpos` 是关节角；joint 与 actuator 不同。Pose 必须相对于某个 frame；FK 从关节配置求末端位姿，IK 可能有多解。
- Path 说明经过哪里，trajectory 加入时间；reference `q(t)` 与实际 `q(t)` 会有 tracking error。稳定运动与准确到达是不同问题。
- toy environment 中 state 是内部状态，observation 是 policy 可见信息；policy 把 observation 映射到 action，且可以是手写规则。
- reward 是环境的评价信号；当前实验用负距离，越接近目标越大。episode 从 reset 开始；任务达成触发 terminated，时间限制触发 truncated。
- `env.step()` 包装状态转移、observation、reward 和结束标志；已初步理解 Python `dict`、多返回值解包及 `class`/`self`/`__init__`。这些是 toy 实验的理解，尚未映射到真实 ManiSkill 任务。

## Experiments Completed

- `mujoco/01_falling_ball/`、`02_pendulum/`、`03_two_link_arm/main.py`、`trajectory_test.py`、`trajectory_viewer.py`：历史实验与观察见 Stage 1/2；本次未重跑 GUI。
- `bridge/01_state_action.py` 至 `08_simple_env.py`：八个递进实验已有提交和 Stage 2.5 用户学习记录。本次重新运行 `06_truncated.py`，确认第 3 步 `truncated=True`；运行 `08_simple_env.py`，确认从位置 1 到目标 5、reward -3→0，最终 `terminated=True`。
- ManiSkill：安装和导入曾成功；示例启动失败，不列为完成的环境实验。

## Problems / Lessons

- 直接进入 ManiSkill 时同时遇到环境接口、物理引擎和渲染术语，故增加 Stage 2.5 的 toy environment 过渡。先解释观察，再引入一个概念。
- reward 与 loss/cost 的优化方向曾混淆；负距离 reward 随接近目标由 -3 增至 0，当前只理解单步信号，累计 return 尚未学习。
- ManiSkill 安装/导入成功不等于环境能创建；已有示例在 renderer/Vulkan 层失败。详细记录见 [Troubleshooting](troubleshooting.md)。

## Current Position

`SimpleEnv` 已跑通；准备把其中的 `reset()` 和 observation 对应到 ManiSkill。尚无成功创建的 ManiSkill environment，也没有 PickCube 的 observation/action 实测数据。

## Next Step

1. 基于已安装版本，做一个最小 ManiSkill 环境创建与 `reset()` 实验，优先 headless、CPU、结构化状态观察；先验证该组合在本机是否可行。
2. 只检查返回结构和少量字段，并与 `SimpleEnv.reset()` 对照；若仍失败，记录准确异常和发生层级，再决定运行环境。

## Do Not Jump Ahead

暂不展开 BC/PPO 训练、LeRobot/Isaac Lab、ROS2、VLA、Diffusion Policy、camera/RGB、GUI 渲染或大型理论树。Stage 3 先解决最小可运行 `reset()`，不把 headless 方案写成已成功。

## Learning Style

用户有 C++ / 软件工程背景，正在逐步学习 Python 与机器人。偏好“一个实验 → 一个现象 → 一个概念”、解释“为什么”，在出现新 Python 写法时顺手解释，不只复制命令，也不一次展开庞大前置知识树。保留真实误解、修正和未完成项。
