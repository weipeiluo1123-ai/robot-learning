# Robot Learning Roadmap

这是一条长期、项目驱动的学习路线。阶段不会因为接触到某个术语就自动完成；只有实际实验、观察和理解达到当前目标后，才更新状态。

## Stage 0 — Development Environment

**Status: Completed**

- macOS / Apple Silicon
- Miniforge / Conda environment isolation
- Python and pip relationship
- PyTorch CPU Tensor
- MPS backend and Apple GPU computation
- Git / GitHub project organization

## Stage 1 — MuJoCo Fundamentals

**Status: In Progress**

- MuJoCo 与 PyTorch / ROS2 的职责区别
- MJCF / XML model description
- MjModel / MjData / mj_step
- falling ball、gravity、contact
- standalone Viewer 与 passive Viewer
- Python simulation loop
- hinge joint、1-DOF pendulum
- 当前下一步：2-DOF two-link arm、actuator、control 和 end-effector trajectory

## Stage 2 — Robot Control & Kinematics

**Status: Planned**

- joint state 与 control 的关系
- forward kinematics
- end-effector position
- basic trajectory and control experiments

## Stage 3 — Robot Learning Environment / ManiSkill

**Status: Planned**

- 选择并运行适合项目的机器人学习环境
- observation、action、state 的实际接口
- 任务环境与 evaluation loop

## Stage 4 — Imitation Learning / Behavior Cloning

**Status: Planned**

- demonstration 数据
- policy 输入输出
- supervised behavior cloning
- distribution shift

## Stage 5 — Reinforcement Learning / PPO

**Status: Planned**

- reward 与 return
- policy optimization
- PPO 基础实验
- 与 Behavior Cloning 的区别

## Stage 6 — Evaluation / Demo / Portfolio Artifact

**Status: Planned**

- 可复现实验
- 清晰的 README 和结果记录
- demo、视频或可视化结果
- 面向 GitHub 和求职展示的项目整理

## 路线维护原则

- 当前阶段优先于远期主题。
- 只根据实际运行、观察和理解更新状态。
- 若路线调整，说明调整原因，不因偶然接触概念而跳过基础。
- 下一阶段之前，不展开 ROS2、VLA、Diffusion Policy 或完整机器人理论树。

