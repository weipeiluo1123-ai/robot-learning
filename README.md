# robot-learning

一个通过项目驱动学习 Robot Learning、Robotics 和 Embodied AI 的长期项目。

我的学习方式不是先完成一整套大型前置课程，而是通过真实实验逐步建立理解：

```text
实验 → 观察 → 发现问题 → 理解概念 → 修改代码 → 验证 → 总结
```

## Current Progress

当前阶段：**Stage 1 — MuJoCo Fundamentals（进行中）**

已完成基础实验：

- Falling ball：gravity、contact、qpos、qvel、mj_step
- Pendulum：hinge joint、1-DOF、joint angle

当前正在学习：

- 2-DOF two-link arm
- parent/child body hierarchy
- actuator / control
- end-effector trajectory

下一步：**2-DOF Two-Link Arm / Actuator / Control**

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
│   │   └── stage1_mujoco_basics.md
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
        └── main.py
```

## Experiments

| Experiment | Main concepts | Status |
|------------|---------------|--------|
| [01 Falling Ball](mujoco/01_falling_ball/) | gravity、contact、qpos、qvel、mj_step | Completed |
| [02 Pendulum](mujoco/02_pendulum/) | hinge joint、1-DOF、joint angle | Completed |
| [03 Two-Link Arm](mujoco/03_two_link_arm/) | 2-DOF、actuator、control、end-effector | In Progress |

## Documentation

- [Current State](docs/current_state.md)：当前环境、进度、已理解概念和下一步
- [Roadmap](docs/roadmap.md)：Stage 0–6 的长期学习路线
- [Stage 0 — Development Environment](docs/stages/stage0_environment_setup.md)
- [Stage 1 — MuJoCo Fundamentals](docs/stages/stage1_mujoco_basics.md)
- [Troubleshooting](docs/troubleshooting.md)：实际遇到的问题和长期经验
- [Checkpoints](docs/checkpoints/)：用于新会话接手项目的上下文记录
- [Prompts](docs/prompts/)：项目维护和会话整理 Prompt

## Environment

- Device: MacBook Pro M1 Max
- Architecture: Apple Silicon / arm64
- Conda environment: robot-learning
- Python: 3.11.16
- PyTorch: 2.14.0
- MuJoCo: 3.13.0
- MPS backend: available and verified

## Quick Start

激活项目环境：

```bash
conda activate robot-learning
```

验证 Python、PyTorch 和 MuJoCo：

```bash
which python
python --version
python -c "import torch; print(torch.__version__)"
python -c "import mujoco; print(mujoco.__version__)"
```

运行 MuJoCo 实验：

```bash
mjpython mujoco/01_falling_ball/main.py
mjpython mujoco/02_pendulum/main.py
mjpython mujoco/03_two_link_arm/main.py
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
- MuJoCo：物理世界和机器人仿真
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
