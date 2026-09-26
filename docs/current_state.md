# Current State

更新：2026-09-26。交接入口；详细过程见 [Stage 2](stages/stage2_robot_control_kinematics.md)，错误经验见 [Troubleshooting](troubleshooting.md)。

## Long-term Goal

通过项目驱动学习 Robot Learning / Robotics / Embodied AI，形成可运行代码、实验结果、GitHub 项目和可展示的求职成果。

## Current Stage

**Stage 2 — Robot Control & Kinematics：Completed（基础学习节点）**。用户于 2026-09-26 补充学习总结，确认从 Pose/Frame、FK、IK 走到控制调参、轨迹时间参数化和 tracking lag。**Stage 3 — Robot Learning Environment / ManiSkill：下一阶段，尚未开始。**

## Environment

2026-09-26 直接调用项目环境 Python 核对：

- macOS 26.6.2 / arm64；设备为此前记录的 MacBook Pro M1 Max。
- Conda：`robot-learning`，位于 `/Users/weipeiluo/miniforge3/envs/robot-learning`。
- Python 3.11.16；PyTorch 2.14.0；MuJoCo 3.13.0；NumPy 2.4.6。
- ManiSkill 当前未安装；Stage 3 尚未开始，需先核对官方安装要求与 Apple Silicon 适配情况。
- MPS：Stage 0 曾成功验证 GPU Tensor 与矩阵运算；本次执行进程中 `is_built=True`、`is_available=False`。原因未确定，日常终端待复核；保留历史成功记录。

## Repository State

本地：`~/Projects/robot-learning`；GitHub：`weipeiluo1123-ai/robot-learning`。

```text
robot-learning/
├── README.md
├── .gitignore
├── docs/
│   ├── current_state.md
│   ├── roadmap.md
│   ├── troubleshooting.md
│   ├── stages/          # Stage 0、1、2 学习记录
│   ├── checkpoints/     # 历史与当前 handoff
│   ├── images/
│   └── prompts/
└── mujoco/
    ├── 01_falling_ball/
    ├── 02_pendulum/
    └── 03_two_link_arm/
        ├── arm.xml
        ├── main.py
        ├── trajectory_test.py
        └── trajectory_viewer.py
```

维护开始时：`main` 的 HEAD 为 `3018314`，与本地 `origin/main` 引用一致（未联网刷新）。`3679bf0` 添加单点 IK，`3018314` 调整重力补偿；两个 trajectory 脚本为用户新增、未跟踪文件。本次文档修改尚未提交。

## Completed

- Stage 0：Conda/Python 隔离、pip、PyTorch CPU/MPS、Git 基础。
- Stage 1：falling ball、pendulum、MJCF、Model/Data/Step、Viewer、hinge/DOF。
- Stage 2：two-link arm 的位姿/坐标变换、FK、Joint/Cartesian Space、枚举 IK、多解连续性、位置控制调参与路径/轨迹实验。
- 用户已观察振荡、稳态误差、数值不稳定、重力补偿后的改善，以及 duration 变化造成的 tracking lag；定性过程已写入 Stage 2，未补造历史数值。

## Concepts Understood

- qpos 不一定是 XYZ；hinge qpos 是关节角；joint 与 actuator 的作用不同。
- Pose 包含 Position + Orientation，必须明确参考 frame。
- FK 按运动学树把关节配置映射为 body/site 位姿；父关节影响下游位姿。
- Joint Space 与 Cartesian Space 是不同描述；IK 可能有多解，路径中应考虑相邻解连续性。
- 稳定与准确到达不同；kp、阻尼、积分器和重力补偿各自影响实验结果。
- Path 描述经过哪里；加入时间形成 reference q(t)，控制与动力学产生 actual q(t)，两者差异是 tracking error。
- XML 描述模型、mj_step 推进物理、Viewer 显示状态。以上是用户确认的基础理解，尚不扩展为完整控制或运动学理论。

## Experiments Completed

- `01_falling_ball/`、`02_pendulum/`：已有历史运行与观察记录。
- `03_two_link_arm/main.py`：用户完成位姿变换、单点 IK、控制调参与重力补偿观察；本次没有重跑 GUI。
- `trajectory_test.py`：用户轨迹学习的一部分；本次助手运行 6 点检查成功，最大 FK 位置误差约 0.0096501，全部小于 0.01。
- `trajectory_viewer.py`：用户确认已完成时长/跟踪滞后观察；代码当前为 51 点预计算、6 秒仿真时间关节插值。本次仅检查代码，未独立重跑 GUI。

## Problems / Lessons

- IK 位置误差、控制器关节跟踪误差和实际末端路径误差需要分开记录。
- 加阻尼能改善振荡，但重力下仍可能有静止位置偏差；高 kp 还要关注数值积分。
- 选择接近上一解的候选有助于连续性，不能等同于完整轨迹约束或最优规划。
- `docs/checkpoints/` 曾被训练输出忽略规则遮蔽，现仅放行其中 Markdown；历史记录保留。
- MPS 历史成功与当前进程不可用的差异待复核，详见 troubleshooting。

## Current Position

Stage 2 已收尾，已连通“Cartesian path → IK → Joint path → 时间参数化 → reference q(t) → controller/dynamics → actual q(t) → FK → actual EE trajectory”。历史调参的完整量化记录尚可补充，但不会把用户已完成的基础学习降回进行中。

## Next Step

1. 先核对 ManiSkill 运行要求与当前 Mac 的适配情况，确定实际运行环境。
2. 在下一次获得对应实施授权后准备环境，运行一个最小任务。
3. 结合该任务认识 observation、action、reset、step；从已学会的仿真/控制衔接到学习环境接口。

## Do Not Jump Ahead

Stage 3 尚未安装或验证；暂不展开 BC/PPO 训练、ROS2、VLA、Diffusion Policy、完整机器人理论或高级四元数推导。解析/Jacobian IK 与复杂规划也不作为进入下一阶段的强制前置课程。

## Learning Style

用户有 C++ / 软件工程背景，正逐步学习 Python 与机器人。按“实验 → 观察 → 发现问题 → 理解概念 → 修改代码 → 验证 → 总结”推进；解释为什么，在代码出现时讲解新语法。保留错误、修正和未理解点，不一次展开庞大的前置知识树。
