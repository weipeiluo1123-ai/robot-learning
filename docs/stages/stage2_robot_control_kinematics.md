---
title: Stage 2 — Robot Control & Kinematics
project: robot-learning
stage: 2
status: completed
updated: 2026-09-26
tags: [robot-learning, mujoco, control, kinematics, ik, trajectory]
---

# Stage 2 — Robot Control & Kinematics

> **Status: Completed。** 用户于 2026-09-26 确认本阶段学习节点完成；下一阶段是 Robot Learning Environment / ManiSkill。

## 记录依据与范围

这份笔记合并了用户的 Stage 2 学习总结、当前实验代码和本次助手核验。Completed 表示本阶段的实验与基本认知已经建立，并不表示掌握通用 IK、完整控制理论或轨迹规划算法。

- **用户回顾**：Pose / Frame、FK、IK 多解、控制调参、重力补偿、trajectory duration 与 tracking lag 的实际学习经历。
- **已提交实现**：`3679bf0` 添加 IK 和位姿/坐标变换；`3018314` 调整 body 重力补偿。
- **当前新实现**：`trajectory_test.py` 和 `trajectory_viewer.py` 已有代码，维护开始时尚未被 Git 跟踪。
- **本次助手核验**：2026-09-26 运行现有 6 点无界面测试成功；没有重跑 Viewer 或重建历史调参实验。
- 用户尚未给出每次调参的完整数值日志；下文保留定性观察，不补造 kp、duration、误差或运行截图。旧末端轨迹图片属于早期位置控制，不能作为新轨迹实验的证据。

[当前状态](../current_state.md) · [总体路线](../roadmap.md) · [问题库](../troubleshooting.md)

## What did I build?

从 Stage 1 的 falling ball、pendulum 继续到 two-link arm，最终形成：

```text
Cartesian target/path
        ↓
       IK
        ↓
Joint path
        ↓
time parameterization
        ↓
reference q(t)
        ↓
controller
        ↓
dynamics
        ↓
actual q(t)
        ↓
       FK
        ↓
actual end-effector trajectory
```

| 文件 | 当前用途 |
|---|---|
| [arm.xml](../../mujoco/03_two_link_arm/arm.xml) | 两根 link、两个 hinge、两个 position actuator、末端 site |
| [main.py](../../mujoco/03_two_link_arm/main.py) | 位姿/坐标变换、单点枚举 IK、位置控制与末端轨迹显示 |
| [trajectory_test.py](../../mujoco/03_two_link_arm/trajectory_test.py) | 6 点 Cartesian path、候选 IK 选择、delta q 与位置误差 |
| [trajectory_viewer.py](../../mujoco/03_two_link_arm/trajectory_viewer.py) | 51 点 IK、关节插值、6 秒仿真时间的目标轨迹播放、关节误差打印 |

当前 XML 中：两根 link 长度均为 0.6；两个 hinge 的局部 axis 为 `[0, 1, 0]`，joint damping 为 1；全局 gravity 为 `[0, 0, -9.81]`，两个 body 的 gravcomp 均为 1；timestep 为 0.01，integrator 为 implicitfast；position actuator 的 kp 为 160、dampratio 为 1。这些是当前配置，不能替代历史对照参数。

## What did I learn?

### 1. Pose / Coordinate Frame

建立的理解是：

```text
Pose = Position + Orientation
     = 原点的位置 + 自身坐标轴的朝向
```

描述一个位姿时先问：**relative to which frame？**

实际用过末端 site 的世界位置与姿态：

```python
p = site.xpos.copy()
R = site.xmat.reshape(3, 3).copy()

world_point = p + R @ local_point
recovered_local_point = R.T @ (world_point - p)
```

已经理解 Local → World 和 World → Local 的含义；不要求现在背出所有公式，也不提前扩展到完整变换群理论。

### 2. Forward Kinematics

```text
qpos
  ↓
沿 kinematic tree 复合 parent → child transforms
  ↓
body / site Pose
```

我在 FK 中观察到：父关节会影响下游 body；只改变 child joint 不会反向改变 parent 的运动学位姿。这里说的是给定配置下的 FK 关系，不是在宣称动力学上不存在相互作用。

代码通过设置 qpos 后调用 `mj_forward` 更新位姿等派生量。它执行正向动力学计算但不做时间积分；IK 搜索逻辑仍由 Python 代码实现。参见 [MuJoCo API reference](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-forward)。

### 3. Joint Space vs Cartesian Space

```text
Joint Space                         Cartesian Space
用关节配置描述机器人                 用末端位置/姿态描述机器人
[q1, q2, ...] ───── FK ─────→        [x, y, z, ...]
              ←──── IK ─────
```

已经能用这两种描述方式思考同一机器人配置，但不应把它们理解为一一对应：一个末端目标可能对应多组关节配置。

### 4. Brute-force IK 与多解连续性

单点目标是 `[-0.8, 0, 0.7]`。每个关节在 `[-1.5, 1.5]` 范围取 121 个角度，逐对赋给独立的 ik_data，经过 FK 后比较末端与目标的距离：

```text
猜 q → FK → 查看 EE 位置 → 比较 target → 保留更好的 q
```

用户实际发现同一个 target 可以得到不同的 joint configurations。因此轨迹求解时，不能只看每个点的位置误差，还需要考虑与上一组 q 的距离。

当前 solve_ik 的做法是先保留位置误差小于 0.01 的候选，再选择最接近 prev_q 的一组；没有合格候选时则退回网格中的最小误差解。它目前不会显式报告不可达或未满足阈值。

这是有限搜索范围内的近似 IK。该范围来自 Python 搜索代码，并不是 XML 中已设置的 joint limit；尚未实现解析 IK、Jacobian 方法或碰撞筛选。

### 5. Control / Dynamics

用户经历的顺序如下；定性结果来自本次补充总结：

| 实验/修改 | 当时观察到的现象 | 建立的认知 |
|---|---|---|
| 只有 position control | 剧烈振荡 | 设定目标不等于立即稳定到达 |
| 加入 dampratio | 运动稳定，但停在错误位置 | 阻尼处理振荡，静止误差仍需另找原因 |
| 提高 kp | 稳态误差减小 | 位置刚度影响误差与响应 |
| kp 太大，仍用原积分器 | numerical instability | 控制参数与数值积分共同影响仿真 |
| 改用 implicitfast | 高 stiffness 下稳定很多 | 积分方法也是实验条件的一部分 |
| 加入 gravity compensation | 稳态误差基本消失 | 控制器不必再主要依靠位置偏差产生支撑力 |

由此区分了 kp、阻尼、重力和重力补偿的作用。当前 `gravcomp="1"` 在 body 上提供抵消其重量的补偿力；全局 gravity 依然存在。参见 [MuJoCo XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-gravcomp)。

用户最终观察到：

```text
IK target q ≈ actual qpos
Cartesian error ≈ IK 网格搜索本身的误差
```

这是一条定性实验结论。未提供当时的完整收敛曲线或精确残差，本次也没有把后面的六点 FK 测试误差当作动态收敛误差。

### 6. Path / Trajectory / Tracking

```text
Cartesian Path：末端经过哪里
        ↓ IK
Joint Path：关节经过哪些配置
        ↓ 加入时间
reference q(t)：随时间变化的目标
        ↓ controller + dynamics
actual q(t)：实际运动
```

reference q(t) 与 actual q(t) 的差异就是本次观察的 joint tracking error。用户通过改变 duration 观察到了真实的 tracking lag。

当前 Viewer 先计算 51 个 IK 点，再根据仿真时间在相邻关节目标之间线性插值，并写入 ctrl。duration 当前为 6.0，到达末尾后保持最后目标，直到关闭 Viewer。循环的 sleep 加上计算、打印、绘制开销意味着墙钟时间不严格等于仿真时间。

## What did I observe?

上面的多解、振荡、稳态误差与 tracking lag 是用户历史实验观察。以下是 **2026-09-26 助手独立运行当前脚本** 的数值核验，不能混为同一次实验。

```bash
# 仓库根目录，使用 robot-learning Conda 环境
python -B mujoco/03_two_link_arm/trajectory_test.py
```

| alpha | 目标位置 | 选中 q | delta q | FK 位置误差 |
|---|---|---|---|---|
| 0.0 | [0, 0, 0.3] | [0, 0] | [0, 0] | 约 5.55e-17 |
| 0.2 | [-0.16, 0, 0.38] | [-0.2, 0.675] | [-0.2, 0.675] | 0.0050632 |
| 0.4 | [-0.32, 0, 0.46] | [-0.125, 0.85] | [0.075, 0.175] | 0.0053838 |
| 0.6 | [-0.48, 0, 0.54] | [0, 0.925] | [0.125, 0.075] | 0.0013771 |
| 0.8 | [-0.64, 0, 0.62] | [0.175, 0.9] | [0.175, -0.025] | 0.0086266 |
| 1.0 | [-0.8, 0, 0.7] | [0.425, 0.725] | [0.25, -0.175] | 0.0096501 |

六点位置误差都小于 0.01。这个带相邻解偏好的结果不一定等于 main.py 单点“纯最小误差”的 IK 解。第一段第二关节仍变化 0.675 rad，也说明“更接近上一解”不等于已经满足某种严格平滑性标准。

脚本中的误差有不同含义：

- trajectory_test：FK 末端位置与离散目标位置的距离。
- trajectory_viewer：实际 qpos 与当前 target_q 的距离。
- 实际末端与连续目标路径的偏差：当前 Viewer 没有持续记录这一指标。

## What confused me? / What mistakes did I make?

回顾时需要保留的认知变化：

- 最初着眼于末端位置，后来开始主动问位姿属于哪个 frame。
- 从单点最小位置误差，推进到同一目标存在不同关节配置，以及轨迹中还要考虑解的连续性。
- 从“加阻尼后稳定”进一步认识到稳定与准确到达是不同的观察结果。
- 从“增加 kp”进一步发现数值稳定性也受积分器影响，并理解重力造成静止时的支撑需求。
- 从“有一串关节目标”推进到给路径安排时间，再观察目标与实际运动之间的 lag。

这些是用户总结中已有的学习轨迹。没有为它们补写未提供的异常堆栈、参数值或失败次数。

## How were they resolved?

对应处理已体现在当前代码中：坐标变换实验；独立 IK data 与误差比较；候选解结合 prev_q；position actuator 的 dampratio/kp；implicitfast；body gravcomp；基于仿真时间的目标插值。主要控制与 IK 经验已追加到 [Troubleshooting](../troubleshooting.md)。

## What concepts are now understood?

用户确认已建立 Pose/Frame、FK、Joint/Cartesian Space、IK 多解与连续性、位置控制与重力补偿、Path/Trajectory/Tracking 的基本认知。Stage 2 在这个层次完成。

Jacobian/解析 IK、完整动力学推导、控制理论证明和全局轨迹优化尚未学习，不因本阶段完成而列为已掌握。

## What remains incomplete?

以下属于后续可补充的工程记录或进阶范围，不阻止本次入门学习节点收尾：

- 历史调参和 duration 对照的具体值、误差曲线和最新 Viewer 截图尚未系统归档。
- 当前 IK 缺少不可达/容差失败的显式报告，轨迹未加入碰撞、速度和加速度约束。
- 还没有实际末端路径的定量跟踪误差记录。
- 两个 trajectory 脚本仍待用户 review 后纳入 Git。
- 本次维护只运行无界面脚本；Viewer 观察依据用户回顾。

## Next Step

进入 Stage 3 的最小准备：先确认 ManiSkill 的运行条件与现有 Mac 的适配情况，再选择环境、运行一个最小任务并认识 observation/action/reset/step。Stage 3 尚未开始，当前不安装新依赖或预写其学习成果。
