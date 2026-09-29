# Robot Learning Mini Sprint — Stage 3 Handoff

## 0. 用户背景与总体目标

我是软件工程专硕，目标以就业为主，希望走：

**Robot Learning / Embodied AI / Robotics**

整体原则：

> 论文解决毕业，实习解决就业，项目证明能力，基础决定上限。

当前学习路线不是系统学完传统机器人学，而是通过 runnable project 建立足够的机器人直觉，并尽快进入 Robot Learning。

长期路线目前规划为：

**MuJoCo 基础 → Robot Learning Bridge → ManiSkill → Demonstration / Behavior Cloning → LeRobot → PPO → Isaac Lab → 完整项目**

目前：

- Stage 0：DONE
- Stage 1：DONE
- Stage 2：DONE
- Stage 2.5：DONE

现在正式进入：

# Stage 3 — ManiSkill / Robot Learning Environment

不要重新教授 Stage 0 / 1 / 2 / 2.5。

---

# 1. 学习风格要求

之前最有效的教学方式是：

> **一个实验 → 一个现象 → 一个概念**

请继续严格遵循。

不要一次塞很多理论。

优先解释：

> “为什么出现这个现象？”

然后才补必要概念。

我有 C / C++ / 软件工程背景，所以：

- 面向对象
- class
- constructor
- method
- 基础控制流

比较容易理解。

但 Python 基础不算扎实。

遇到新的 Python 写法时可以顺手解释，例如：

- list / dict
- NumPy array
- indexing
- unpacking
- function / return
- class / self
- API 使用方式

但不要把课程变成 Python 基础课。

如果 Python 语法让我看花眼，优先拆成“啰嗦版”解释，再缩写。

---

# 2. 当前开发环境

主力机器：

MacBook Pro M1 Max

Conda environment：

`robot-learning`

Python：

`3.11.16`

MuJoCo：

`3.13.0`

Repo：

`~/Projects/robot-learning`

GitHub：

`weipeiluo1123-ai/robot-learning`

工作流：

Mac：

- 写代码
- VS Code
- Git
- Debug
- 小实验
- ManiSkill 本地开发

未来需要 NVIDIA / CUDA 训练时：

Linux + NVIDIA machine。

Git 工作流：

`edit → run → status → diff → add → commit → push`

不要自动 commit / push。

---

# 3. 当前 Repo 结构

目前核心结构类似：

```text
robot-learning/
├── mujoco/
│   └── 03_two_link_arm/
│
├── bridge/
│   ├── 01_state_action.py
│   ├── 02_goal.py
│   ├── 03_policy.py
│   ├── 04_reward.py
│   ├── 05_episode.py
│   ├── 06_truncated.py
│   ├── 07_env_step.py
│   └── 08_simple_env.py
│
└── maniskill/
    └── ...
```

目录原则：

> 不为了“专业”提前搭复杂 package / utils / controllers 结构。

出现真实复用需求以后再抽象。

---

# 4. Stage 2 已掌握内容

Stage 2 使用 MuJoCo 建立了机器人控制基础。

已经理解：

## Pose / Frame

Pose = Position + Orientation

Pose 一定 relative to 某个 frame。

使用过：

- `site.xpos`
- `site.xmat`

做过：

Local ↔ World coordinate transform

理解：

`p_world = t + R @ p_local`

以及：

`p_local = R.T @ (p_world - t)`

无需重新推导。

---

## FK

理解：

`qpos → EE Pose`

核心直觉：

> FK 就是沿 kinematic tree 不断复合 transforms。

理解：

- parent joint 影响 downstream links
- child joint 不反向影响 upstream link
- body `xpos` 是 body frame origin

---

## Joint Space / Cartesian Space

理解：

Joint Space：

`[q1, q2, ...]`

Cartesian Space：

`[x, y, z, ...]`

关系：

```text
Joint Space ──FK──→ Cartesian Space
Joint Space ←─IK── Cartesian Space
```

---

## IK

实现过 brute-force grid IK。

理解：

- IK solution 不唯一
- 同一 Cartesian target 可以对应多个 q
- trajectory 中独立 IK 会发生 branch jump
- 用 continuity-aware IK，根据上一帧 `prev_q` 选择邻近 solution

---

## Control

做过 position actuator 实验。

理解：

- overshoot
- oscillation
- qvel
- damping
- kp
- steady-state error
- high stiffness numerical instability
- `implicitfast`
- gravity compensation

核心理解：

> reaching target ≠ stably arriving

以及：

> pure P control 在 gravity 下需要 position error 提供抗重力 torque。

使用 gravity compensation 后可以基本精确收敛。

无需继续深入 PID。

---

## Path / Trajectory

做过：

Cartesian Path  
→ IK  
→ Joint Path  
→ Time Parameterization  
→ reference `q(t)`  
→ controller  
→ dynamics  
→ actual `q(t)`

理解：

Path：

> 经过哪里

Trajectory：

> 经过哪里 + 什么时候经过

做过 duration 实验：

duration 短：

> reference 跑得快 → tracking error 大

duration 长：

> robot 更容易跟上

---

# 5. Stage 2 最终 Mental Model

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
actual EE motion
```

实际机器人任务可以理解成：

```text
“拿水杯”
↓
perception
↓
cup pose
↓
grasp target
↓
IK
↓
joint command
↓
controller
↓
robot motion
```

Stage 2：DONE ✅

---

# 6. Stage 2.5 的目的

原本直接进入 ManiSkill 时，我感觉非常吃力。

原因是一次同时遇到了：

- ManiSkill
- Gymnasium
- SAPIEN
- observation
- action
- reward
- terminated
- truncated
- wrapper
- CPU/GPU
- Vulkan

因此重新设计了：

# Stage 2.5 — Robot Learning Bridge

目的：

> 不使用 ManiSkill，先亲手搭一个最小 environment，把 Robot Learning interface 拆开理解。

这个阶段非常有效。

---

# 7. Stage 2.5 已掌握核心概念

## State

理解为：

> 世界实际上是什么样子。

最小实验：

```text
state = position
```

真实机器人可以包含：

- qpos
- qvel
- object pose
- contact
- etc.

---

## Action

理解为：

> 现在我要对 environment 做什么。

toy robot：

```text
+1 → right
-1 → left
```

与 Stage 2 的 controller command / target 有直接联系。

---

## Transition

理解：

```text
state
+
action
↓
next state
```

即：

```text
s_t
a_t
↓
s_(t+1)
```

不需要数学推导。

---

## Observation

理解：

> agent / policy 当前能够获得的信息。

重要区分：

```text
State
= 世界实际上是什么

Observation
= agent 能知道什么
```

toy world 中二者几乎相同。

真实机器人中可能不同，例如：

```text
true simulator state
↓
camera image + qpos
↓
observation
```

使用过：

```python
observation = {
    "position": position,
    "goal": goal
}
```

因此已接触 Python `dict`。

---

## Policy

理解：

> Policy = observation → action

最初手写：

```python
if observation["position"] < observation["goal"]:
    action = 1
elif observation["position"] > observation["goal"]:
    action = -1
else:
    action = 0
```

后整理成：

```python
def policy(observation):
    ...
    return action
```

重要理解：

> policy 不一定是 neural network。

当前 if/else 也是 policy。

以后可能变成：

```text
observation
↓
neural network
↓
action
```

接口思想不变。

---

# 8. Reward

做过：

```python
reward = -abs(goal - next_position)
```

观察：

```text
-3 → -2 → -1 → 0
```

越接近目标 reward 越大。

已经纠正过一个 misunderstanding：

不是：

> reward 越小越好。

而是：

> **RL 一般希望 maximize reward / cumulative reward。**

重要区分：

```text
Reward
→ 越大越好

Loss / Cost
→ 越小越好
```

当前理解：

> reward 是 environment 给出的评价信号。

更严谨：

> RL policy 的目标通常是最大化累计 reward，而不是简单让单步 reward = 0。

暂时不用深入 return / discount。

---

# 9. Episode / Reset / Terminated / Truncated

已经通过实验理解。

## Episode

理解：

> 从 reset 开始，到 episode 结束的一整段 interaction。

例如：

```text
reset
↓
1 → 2 → 3 → 4 → 5
↓
terminated
```

---

## Reset

理解：

> 将 environment 重新初始化，开始新的 episode。

例如：

```text
position 回到起点
step_count 清零
```

---

## Terminated

理解：

> 任务自身逻辑导致 episode 结束。

例如：

```text
goal reached
→ terminated = True
```

或者某些任务：

```text
failure
→ terminated = True
```

---

## Truncated

理解：

> 任务本身没有结束，但由于外部限制停止。

最典型：

```text
max episode steps
time limit
```

因此：

```text
terminated
= 任务自己结束

truncated
= 外部把 episode 截断
```

---

# 10. env.step() 的理解

Stage 2.5 Experiment 7 手写过：

```python
env_step(
    position,
    goal,
    action,
    step,
    max_steps
)
```

函数内部负责：

```text
execute action
↓
next state
↓
next observation
↓
reward
↓
terminated
↓
truncated
↓
return
```

理解了 multiple return values 和 unpacking：

```python
position, observation, reward, terminated, truncated = env_step(...)
```

也理解：

```python
return a, b, c
```

可以被：

```python
x, y, z = function()
```

解包。

---

# 11. SimpleEnv：亲手写过最小 Environment Class

Stage 2.5 最后写了：

```python
class SimpleEnv:
```

Environment 内部保存：

```python
self.start_position
self.position
self.goal
self.step_count
self.max_steps
```

实现：

```python
env.reset()
env.step(action)
```

核心主循环：

```python
env = SimpleEnv()

observation = env.reset()

while True:

    action = policy(observation)

    observation, reward, terminated, truncated = env.step(action)

    if terminated or truncated:
        break
```

已经完全理解这个结构。

---

# 12. Python OOP 当前理解

因为我有 C++ 背景，所以 class 很容易理解。

已经理解：

```python
class SimpleEnv:
```

类似 C++ class。

---

## `__init__`

理解：

```python
def __init__(self):
```

是 Python 规定的初始化 special method。

类似 C++：

```cpp
SimpleEnv()
```

但严格来说：

Python：

```text
__new__
→ 创建 object

__init__
→ 初始化 object
```

无需继续深入 `__new__`。

---

## `self`

理解：

Python：

```python
self.position
```

大致对应 C++：

```cpp
this->position
```

定义：

```python
def reset(self):
```

调用：

```python
env.reset()
```

Python 自动把：

```text
env → self
```

传入。

---

# 13. Stage 2.5 最终 Mental Model

目前已建立：

```text
Environment internal state
        ↓
generate observation
        ↓
      Policy
        ↓
      Action
        ↓
    env.step()
        ↓
update world state
        ↓
next observation
+
reward
+
terminated / truncated
```

完整 interaction loop：

```text
reset
↓
observation
↓
policy
↓
action
↓
environment
↓
next observation + reward
↓
terminated / truncated?
├── No → continue
└── Yes → reset / episode end
```

Stage 2.5：DONE ✅

---

# 14. ManiSkill 当前环境状态

已经安装：

```text
mani_skill 3.0.1
```

路径：

`robot-learning` conda env。

Import 测试：

```bash
python -c "import mani_skill; import gymnasium; import sapien; import torch; print('ManiSkill imports OK')"
```

成功：

```text
ManiSkill imports OK
```

但会出现：

```text
Failed to find system libvulkan.
Fallback to SAPIEN builtin libvulkan.
```

以及：

```text
pinnochio package is not installed
```

Pinocchio warning 当前忽略即可。

---

# 15. 当前 ManiSkill 阻塞点

运行：

```bash
python -m mani_skill.examples.demo_random_action -e PickCube-v1
```

失败。

核心错误：

```text
Detected MacOS system, forcing render backend to be sapien_cpu
```

然后：

```text
Your GPU driver does not support Vulkan.
```

最终：

```text
RuntimeError:
vk::createInstanceUnique:
ErrorIncompatibleDriver
```

因此：

> ManiSkill Python / dependency 本身安装正常。

当前问题是：

> macOS Vulkan / MoltenVK renderer 初始化失败。

Stage 3 重新开始时，不要一上来把重点放在修 Vulkan。

---

# 16. Stage 3 新的教学原则

Stage 3 不要再像第一次尝试那样同时讲：

```text
obs
action
reward
terminated
truncated
Gymnasium
SAPIEN
renderer
Vulkan
```

这些基础概念 Stage 2.5 已经学完。

现在应该采用：

> **SimpleEnv → ManiSkill 一一映射。**

例如：

```text
SimpleEnv
env.reset()

↕

ManiSkill
env.reset()
```

以及：

```text
SimpleEnv
env.step(action)

↕

ManiSkill
env.step(action)
```

---

# 17. Stage 3 推荐推进顺序

正式进入：

# Stage 3A — ManiSkill as a Robot Environment

先不要 PPO。

先不要 Behavior Cloning。

先不要复杂 reward。

先不要 camera / vision。

先不要 Vulkan GUI。

---

## Experiment 1

目标：

> 创建最小 headless ManiSkill environment，并只观察 `reset()` 返回什么。

优先：

```text
CPU physics
state/state_dict observation
render_backend=None
```

不要把 GUI 作为前置条件。

建议使用：

```text
PickCube-v1
```

或其他最小 manipulation task。

---

## Experiment 2

重点：

> ManiSkill observation 到底包含什么？

优先使用：

```python
obs_mode="state_dict"
```

而不是一上来：

```python
obs_mode="state"
```

因为 `state_dict` 教学上更直观。

希望逐步查看类似：

```text
agent
├── qpos
├── qvel
└── ...

extra
├── tcp_pose
├── cube_pose
├── goal
└── ...
```

不要一次打印几百个数字然后解释全部。

仍然：

> 一个实验 → 一个现象 → 一个概念。

---

## Experiment 3

目标：

> action 到底控制什么？

不要 random action 全维乱动。

优先实验：

```text
action = zeros
```

观察 robot state。

然后：

```text
只修改一个 action dimension
```

例如：

```text
action[0] = +0.2
```

观察：

```text
哪个 joint / robot state 发生变化？
```

从而建立：

> ManiSkill action 与 Stage 2 joint/controller command 的联系。

---

## Experiment 4

再开始：

```text
observation
→ action
→ next observation
```

此时再映射：

```text
SimpleEnv
position update

↕

ManiSkill
controller + SAPIEN physics
```

---

## Experiment 5

之后才重新看：

```text
reward
terminated
truncated
```

因为概念已经理解，现在只需要看：

> PickCube-v1 如何定义这些东西。

---

# 18. Stage 3 与 Stage 2 的关键连接

Stage 2：

```text
target_q(t)
↓
controller
↓
MuJoCo
↓
actual q
```

Stage 3：

```text
observation
↓
policy
↓
action
↓
ManiSkill controller
↓
SAPIEN dynamics
↓
next observation
```

中间：

```text
action
↓
controller
↓
dynamics
↓
robot motion
```

Stage 2 已经学过。

Stage 3 真正新增的是：

```text
observation
↓
policy
```

以及：

```text
task/reward/episode
```

---

# 19. 后续路线确认

Stage 3 后续自然进入：

```text
ManiSkill
↓
demonstration
↓
trajectory dataset
↓
Behavior Cloning
↓
LeRobot
↓
PPO
↓
Isaac Lab
```

---

## LeRobot

计划在：

> Demonstration / Behavior Cloning 阶段较早进入。

重点理解：

```text
obs_t
action_t
episode
trajectory
dataset
policy
```

---

## Isaac / Isaac Lab

后面再学。

粗略阶段：

```text
Stage 6
Isaac Sim / Isaac Lab
```

重点：

- GPU parallel simulation
- RL / IL at scale
- NVIDIA workflow

不要现在就切 Isaac Lab。

---

# 20. 当前学习目标

现在请直接从：

# Stage 3A — Experiment 1  
## “把我们自己写的 SimpleEnv，映射到 ManiSkill 的 env.reset()”

开始。

第一目标：

> 在 Mac M1 Max 上用 headless CPU simulation 成功创建一个 ManiSkill environment。

然后只检查：

```text
env.reset()
↓
observation
```

不要一开始就同时进入：

- PPO
- reward design
- BC
- camera
- RGB
- Vulkan
- GUI
- parallel envs

---

# 21. 教学节奏

请继续严格保持：

> **一个实验 → 一个现象 → 一个概念**

如果出现报错：

> 先解释“哪一层出了问题”。

例如区分：

```text
Python
ManiSkill
SAPIEN
physics
renderer
Vulkan
```

不要为了修一个渲染问题同时修改多个环境变量。

---

# 22. Stage 3 开场建议

新窗口第一句话可以直接从：

> **Stage 3A — Experiment 1：我们已经亲手写过 SimpleEnv 了，现在来看看 ManiSkill 的 env.reset() 和我们自己的 reset() 到底有什么区别。**

开始。

然后直接带我完成第一个真正 runnable 的 headless ManiSkill experiment。