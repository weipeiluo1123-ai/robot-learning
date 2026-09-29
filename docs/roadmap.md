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

**Status: Completed（基础学习节点）**

- MuJoCo 与 PyTorch / ROS2 的职责区别
- MJCF / XML model description
- MjModel / MjData / mj_step
- falling ball、gravity、contact
- standalone Viewer 与 passive Viewer
- Python simulation loop
- hinge joint、1-DOF pendulum
- 完成基础实验后，将 two-link arm 的控制与运动学实践衔接到 Stage 2。

## Stage 2 — Robot Control & Kinematics

**Status: Completed（基础学习节点，用户于 2026-09-26 确认）**

- Pose / Coordinate Frame、局部/世界坐标变换、FK 与 Joint / Cartesian Space。
- 枚举搜索 IK、多解现象，以及结合上一组关节角选择候选解。
- 位置控制、振荡与阻尼、kp 与稳态误差、积分器数值稳定性、重力补偿。
- Cartesian path → IK → joint path → time parameterization → controller → actual trajectory。
- 用户已完成 duration / tracking lag 观察；本次另行核验了 6 点无界面 IK 测试。
- 完成的是入门实验与认知节点，不表示已掌握通用 IK、完整轨迹规划或控制理论；历史调参的完整数值日志仍可后续补充。

详见 [Stage 2 学习记录](stages/stage2_robot_control_kinematics.md)。

## Stage 2.5 — Robot Learning Bridge（Stage 3 前的过渡）

**Status: Completed（2026-09-29，toy environment 入门节点）**

- 首次直接接触 ManiSkill 时，环境接口与渲染/依赖术语同时出现；因此插入一个小型过渡实验，不改变 Stage 0–6 总路线。
- `bridge/01`–`08` 从 state/action 递进到 policy、reward、episode、terminated/truncated、`env_step()` 和 `SimpleEnv.reset()/step()`。
- 已理解 toy 接口；ManiSkill 的实际 observation/action、环境创建仍待 Stage 3 实测。详见 [Stage 2.5 学习记录](stages/stage2_5_robot_learning_bridge.md)。

## Stage 3 — Robot Learning Environment / ManiSkill

**Status: Preparing — 已安装和尝试示例，尚无成功运行的环境实验**

- 本机 `robot-learning` 环境已有 ManiSkill 3.0.1；此前 PickCube 随机动作示例在 Vulkan 初始化失败，不能据此推断 headless CPU 路径的结果。
- 第一个实验只尝试创建最小 headless 环境并调用 `reset()`，对照 Stage 2.5 的 `SimpleEnv`，观察返回结构。
- 成功后逐步检查少量 observation 字段、action 与 `step()`；再看任务 reward 和 episode 结束条件。

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

2026-09-29 调整依据：`bridge/01`–`08` 已提交，用户原始 handoff 确认 Stage 2.5 的学习过程；本次复跑时间截断和 `SimpleEnv`。因此把 Stage 2.5 标为完成，并把 Stage 3 状态改为“准备中”。Stage 4–6 目标不变；LeRobot / Isaac Lab 等只作为后续候选工具，不新增为当前必经阶段。

2026-09-26 更新依据：用户补充完整 Stage 2 学习总结，确认已完成坐标变换、IK、多解连续性、控制调参和轨迹时长实验；现有代码与本次无界面核验提供对应实现依据。将 Stage 2 收尾并把近期目标移到 Stage 3，Stage 0–6 总体方向不变。

- 当前阶段优先于远期主题。
- 只根据实际运行、观察和理解更新状态。
- 若路线调整，说明调整原因，不因偶然接触概念而跳过基础。
- 下一阶段之前，不展开 ROS2、VLA、Diffusion Policy 或完整机器人理论树。
