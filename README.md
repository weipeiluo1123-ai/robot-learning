# robot-learning

一个通过项目驱动学习 Robot Learning、Robotics 和 Embodied AI 的长期项目。

我的学习方式不是先完成一整套大型前置课程，而是通过真实实验逐步建立理解：

```text
实验 → 观察 → 发现问题 → 理解概念 → 修改代码 → 验证 → 总结
```

## Current Progress

当前学习节点：**Stage 2 — Robot Control & Kinematics 已完成**。下一阶段是 Stage 3 — Robot Learning Environment / ManiSkill，尚未开始。

已完成基础实验：

- Falling ball：gravity、contact、qpos、qvel、mj_step
- Pendulum：hinge joint、1-DOF、joint angle
- Two-link arm：Pose / Frame、FK、Joint / Cartesian Space、枚举搜索 IK 与多解连续性
- Position control：振荡、阻尼、稳态误差、积分器与重力补偿的实验观察
- Path / trajectory：目标路径采样、逐点 IK、时间参数化、关节插值与 tracking lag

本阶段建立的实验流程：

```text
Cartesian target/path → IK → Joint path → time parameterization
    → reference q(t) → controller → dynamics → actual q(t) → FK
    → actual end-effector trajectory
```

完成状态依据用户的 Stage 2 学习总结；本次额外核验了 6 点无界面 IK 测试。详细观察与验证边界见 [Stage 2](docs/stages/stage2_robot_control_kinematics.md)。

下一步：**确认 Stage 3 学习环境的运行条件，再开始一个最小任务，认识 observation / action / reset / step。**

## Project Structure

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
│   │   ├── stage1_mujoco_basics.md
│   │   └── stage2_robot_control_kinematics.md
│   ├── checkpoints/
│   ├── images/
│   └── prompts/
└── mujoco/
    ├── 01_falling_ball/
    │   ├── ball.xml
    │   └── main.py
    ├── 02_pendulum/
    │   ├── pendulum.xml
    │   └── main.py
    └── 03_two_link_arm/
        ├── arm.xml
        ├── main.py
        ├── trajectory_test.py
        └── trajectory_viewer.py
```

## Experiments

| Experiment | Main concepts | Status |
|------------|---------------|--------|
| [01 Falling Ball](mujoco/01_falling_ball/) | gravity、contact、qpos、qvel、mj_step | Completed |
| [02 Pendulum](mujoco/02_pendulum/) | hinge joint、1-DOF、joint angle | Completed |
| [03 Two-Link Arm](mujoco/03_two_link_arm/) | Pose / FK、枚举 IK、position control、重力补偿 | 基础学习节点完成 |
| [Trajectory Test](mujoco/03_two_link_arm/trajectory_test.py) | 6 点目标路径、位置容差、相邻 IK 解选择 | 本次无界面运行通过 |
| [Trajectory Viewer](mujoco/03_two_link_arm/trajectory_viewer.py) | 51 点 IK、关节插值、tracking lag | 用户已完成观察；本次未重跑 GUI |

## Documentation

- [Current State](docs/current_state.md)：当前环境、进度、已理解概念和下一步
- [Roadmap](docs/roadmap.md)：Stage 0–6 的长期学习路线
- [Stage 0 — Development Environment](docs/stages/stage0_environment_setup.md)
- [Stage 1 — MuJoCo Fundamentals](docs/stages/stage1_mujoco_basics.md)
- [Stage 2 — Robot Control & Kinematics](docs/stages/stage2_robot_control_kinematics.md)
- [Troubleshooting](docs/troubleshooting.md)：实际遇到的问题和长期经验
- [Latest Checkpoint](docs/checkpoints/2026-09-26_stage2_complete_stage3_handoff.md)：Stage 2 完成后的新会话交接与 Stage 3 起点
- [Prompts](docs/prompts/)：项目维护和会话整理 Prompt

## Environment

- Device: MacBook Pro M1 Max
- OS: macOS 26.6.2
- Architecture: Apple Silicon / arm64
- Conda environment: robot-learning
- Python: 3.11.16
- PyTorch: 2.14.0
- MuJoCo: 3.13.0
- NumPy: 2.4.6
- MPS backend: Stage 0 曾验证 GPU 计算；本次执行进程的可用性差异见 [Current State](docs/current_state.md#environment)

软件版本于 2026-09-26 从本机项目环境读取。

## Quick Start

以下命令使用已有项目环境，从仓库根目录运行：

```bash
cd ~/Projects/robot-learning
conda activate robot-learning
```

验证 Python、PyTorch 和 MuJoCo：

```bash
which python
python --version
python -c "import torch; print(torch.__version__)"
python -c "import mujoco; print(mujoco.__version__)"
```

按需运行一个 MuJoCo 实验；关闭 Viewer 后可继续执行下一条：

```bash
mjpython mujoco/01_falling_ball/main.py
mjpython mujoco/02_pendulum/main.py
mjpython mujoco/03_two_link_arm/main.py
```

two-link arm 的 main.py 会先搜索单点 IK 并打印位姿/坐标变换，再启动控制与可视化。新增轨迹入口：

```bash
# 无界面：打印 6 点路径的 IK 解、delta q 与位置误差
python mujoco/03_two_link_arm/trajectory_test.py

# 有界面：预计算 51 点 IK，再按仿真时间播放关节目标
mjpython mujoco/03_two_link_arm/trajectory_viewer.py
```

查看 falling-ball 的 standalone Viewer：

```bash
python -m mujoco.viewer --mjcf=mujoco/01_falling_ball/ball.xml
```

## Robot Learning 中的工具关系

```text
                    Robot Learning
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     PyTorch          MuJoCo            ROS2
        │                │                │
   神经网络/训练        物理仿真         机器人软件通信
        │
        ▼
  MPS / CUDA
        │
   计算加速后端
```

- PyTorch：神经网络、Tensor 和学习算法
- MuJoCo：物理世界和机器人仿真, FK, IK
- ROS2：机器人软件通信与系统组织
- MPS / CUDA：计算加速 backend

## Learning Questions

这些问题会随着实验逐步回答，而不是一次性假设已经掌握：

- observation 和 state 有什么区别？
- action 是什么？
- policy 是什么？
- demonstration 是什么？
- Behavior Cloning 在优化什么？
- 为什么 BC 会出现 distribution shift？
- reward 是什么？
- PPO 和 BC 最大的区别是什么？
- simulation 为什么重要？
- Sim2Real 是什么？
- 如果把程序放到真实机械臂上，还缺什么？

## Project Principle

这个仓库保留真实的学习过程，包括实际观察、错误、误解、修正和仍未完成的内容。文档中的 `Completed` 只表示已经实际运行并建立了基本理解，不代表掌握了完整理论。
