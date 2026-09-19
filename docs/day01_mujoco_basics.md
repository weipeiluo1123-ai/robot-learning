---
title: Day 1 — MuJoCo Basics
project: robot-learning
day: 1
status: in_progress
tags: [robot-learning, mujoco, simulation]
---

# Day 1 — MuJoCo Basics

> **Status: In Progress**

Day 1 当前完成了 MuJoCo 初步认识、安装、falling-ball 实验、Viewer 和 Python-controlled simulation。**Joint / DOF / Pendulum 尚未开始。**

## 学习路径

```text
① MuJoCo 是什么
        ↓
② 它和 PyTorch / ROS2 有什么区别
        ↓
③ 安装 MuJoCo
        ↓
④ 跑官方最小例子
        ↓
⑤ 第一次看到仿真画面
        ↓
⑥ 看懂最基本的模型结构
        ↓
⑦ 改一个参数
        ↓
⑧ 让物体/关节真的发生变化
        ↓
⑨ 再解释背后的机器人概念
```

## 1. MuJoCo 是什么

MuJoCo 是 physics simulator，适合 robotics、multi-joint systems 和 contact-rich simulation，可以模拟 gravity、rigid bodies、joints、contact、friction、actuators 和 dynamics。

```text
Robot Learning
├── PyTorch
│   └── neural networks / learning
├── MuJoCo
│   └── physics simulation
└── ROS2
    └── robot software communication / organization

MPS / CUDA
└── compute backend
```

PyTorch 负责神经网络与学习，MuJoCo 负责物理仿真，ROS2 负责机器人软件通信与组织，MPS / CUDA 属于计算 backend。

## 2. 安装 MuJoCo

```bash
python -m pip install mujoco
```

安装成功：mujoco 3.13.0。

```python
import mujoco
print(mujoco.__version__)
```

## 3. MJCF / XML

MuJoCo 原生模型描述格式 MJCF 基于 XML。当前目标是能读简单 MJCF、修改参数、理解 body / geom / joint / actuator 等基本结构，不提前把复杂机器人建模写成已掌握内容。

```xml
<mujoco model="falling_ball">
  <option timestep="0.01" gravity="0 0 -9.81"/>
  <worldbody>
    <geom name="floor" type="plane" size="2 2 0.1"/>
    <body name="ball" pos="0 0 1">
      <freejoint/>
      <geom name="ball_geom" type="sphere"
            size="0.1" mass="1" rgba="0.2 0.6 1 1"/>
    </body>
  </worldbody>
</mujoco>
```

XML 标签可成对出现，也可使用自闭合标签；XML / MJCF 是层级树结构。

## 4. Model / Data / Step

```text
MJCF / XML
    ↓
MjModel
    ↓
MjData
    ↓
mj_step(model, data)
    ↓
new state
```

- MjModel 约等于世界的结构和物理规则。
- MjData 约等于世界当前运行状态。
- mj_step 根据 model 和 data 把物理世界推进一个 timestep。

## 5. Falling Ball experiment

第一个实验是 sphere + ground + gravity。按当时学习记录：

- 初始 z = 1
- 初始 v = 0
- 执行 20 次 step
- time ≈ 0.2
- z ≈ 0.79399
- vz = -1.962

```text
-1.962 = -9.81 × 0.2
```

继续 step 后，z ≈ 0.1、qvel ≈ 0，球最终停在地面。建立了 qpos、qvel、timestep、numerical integration、contact 和 floating-point numerical error 的初步理解。

### 与当前实验文件的差异

当前仓库 ball.xml 是 ball 初始 z=2、gravity 0 0 -0.5；上面的学习记录引用的是 z=1、gravity -9.81。这两组参数不能直接视为同一次运行。我保留学习记录并标注当前文件状态，不修改 ball.xml。

## 6. Viewer

```bash
python -m mujoco.viewer --mjcf=ball.xml
```

第一次直观看到 XML → physics → animation。standalone viewer 内部大致完成：

```text
load model → create data → mj_step loop → render
```

XML 只是 model description，不会自己执行仿真。

## 7. Python-controlled simulation

当前项目结构：

```text
robot-learning/
├── README.md
├── .gitignore
├── docs/
└── mujoco/
    └── 01_falling_ball/
        ├── ball.xml
        └── main.py
```

核心逻辑：

```python
from pathlib import Path
import time
import mujoco
import mujoco.viewer

xml_path = Path(__file__).with_name("ball.xml")
model = mujoco.MjModel.from_xml_path(str(xml_path))
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()
        mujoco.mj_step(model, data)
        viewer.sync()
        time_until_next_step = (
            model.opt.timestep - (time.time() - step_start)
        )
        if time_until_next_step > 0:
            time.sleep(time_until_next_step)
```

macOS 上使用：

```bash
mjpython mujoco/01_falling_ball/main.py
```

| 模式 | 谁控制 simulation loop | Python 是否显式调用 mj_step |
|------|------------------------|-----------------------------|
| standalone viewer | Viewer | 否 |
| passive viewer | Python 主程序 | 是 |

## 8. Day 1 学到的 Python 概念

因为之前主要使用 C++：

```cpp
for (int i = 0; i < 20; i++) {
    ...
}
```

```python
for i in range(20):
    ...
for _ in range(20):
    ...
```

_ 仍是合法变量名，只是约定表示“不关心这个值”。

Python REPL 中，>>> 是主提示符，... 表示 compound statement 尚未结束；输入多行 for、while、if、def 后通常需要空行结束。Python 使用冒号和缩进表示 block，缩进是语法的一部分。

```python
y.device
viewer.is_running()
viewer.sync()
```

y.device 是 attribute；viewer.is_running() 和 viewer.sync() 是 method。with 管理 resource lifecycle，可以和 C++ RAII 建立直觉联系。Path(__file__).with_name("ball.xml") 避免依赖当前 working directory。time.time() 测 wall-clock time，time.sleep() 暂停程序。

## 9. Terminal state 与 Viewer state

在 mj_step 后增加：

```python
print(data.time, data.qpos[:3])
```

可以同时看到 Terminal 的 numerical state 和 Viewer 的 visual state。建立的认知：

```text
MjData = simulation state
Viewer = state visualization
```

## 10. 当前状态

Day 1 仍在进行中，不把 Joint、DOF 或 Pendulum写成已经掌握的内容。

**Next: Joint / DOF / Pendulum**

