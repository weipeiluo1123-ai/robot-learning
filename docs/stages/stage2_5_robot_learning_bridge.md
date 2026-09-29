# Stage 2.5 — Robot Learning Bridge

**Status: Completed（toy environment 的入门学习节点）**。依据：2026-09-28/29 的 `bridge/01`–`08` 提交、用户的 [Stage 2.5 原始 handoff](../checkpoints/stage2.5.md)，以及 2026-09-29 对 `06` 和 `08` 的重新运行。原始 handoff 是未跟踪文件，保留原样，待用户 review。

## Why this stage was added

第一次直接接触 ManiSkill 时，observation、action、reward、episode、Gymnasium、SAPIEN、renderer/Vulkan 等一起出现，难以分辨概念和故障层级。因此先不用 ManiSkill，亲手实现最小环境接口。这是 Stage 2 与 Stage 3 之间的教学过渡，不改变 Stage 0–6 的长期目标。

## What did I build?

`bridge/01_state_action.py` 到 `08_simple_env.py` 依次实现：一维状态转移、带 goal 的 observation、规则 policy、负距离 reward、任务完成标志、步数截断、`env_step()` 函数，以及有 `reset()`/`step()` 的 `SimpleEnv` 类。最后的循环是 `reset → observation → policy → action → step → next observation/reward/terminated/truncated`。

## What did I observe?

- 原始 handoff 记录：从 position=1 朝 goal=5 前进时，reward 按 -3、-2、-1、0 变化；目标达成后 episode 结束。
- 本次运行 `bridge/08_simple_env.py` 再次看到 reset observation 为 `{'position': 1, 'goal': 5}`；四次 `+1` 后 position=5、`terminated=True`、`truncated=False`。
- 本次运行 `bridge/06_truncated.py`：`max_steps=3` 时 position 走到 4，任务未完成，第三步 `truncated=True`。
- 这些是确定性 toy 程序的输出；没有物理仿真，也没有证明 ManiSkill 环境已可运行。

## What did I learn?

State 表示内部世界状态；observation 是 policy 获得的信息；action 触发转移；规则 `if/else` 也可以构成 policy。Reward 是环境给的评价，RL 通常关心累计 reward；本阶段只用了负距离单步 reward。Episode 从 reset 开始，达到任务目标是 terminated，达到外部时间限制且未完成是 truncated。`env.step()` 把这些步骤合在一个接口里。

Python 方面接触了 `dict`、函数返回多个值后的解包，以及 `class`、`self`、`__init__`。这些理解来自小程序和用户回顾，尚不能推断对 Gymnasium/ManiSkill API 的细节已掌握。

## What confused me? What mistakes did I make? How were they resolved?

- 直接进入 ManiSkill 时概念与环境报错混在一起；通过 toy environment 逐个实验拆开。
- 曾把 reward 与 loss/cost 的方向混淆。负距离实验显示越接近目标 reward 越大；当前只确认了这个例子和一般最大化目标，尚未深入 return/discount。
- ManiSkill 包可导入，但原始 handoff 记录的 `demo_random_action -e PickCube-v1` 在 Vulkan 初始化失败。安装成功不代表任务运行成功；故障细节见 [Troubleshooting](../troubleshooting.md)。

## What remains incomplete?

- 尚未在本仓库创建并成功运行 ManiSkill 环境；`SimpleEnv.reset()` 到 ManiSkill `reset()` 的映射仍待实测。
- 尚未查看 PickCube observation 字段、action 维度、reward/termination 的实际定义。
- headless CPU 方案只是下一步尝试，未验证可行；不以 GUI 或 Vulkan 修复作为理解接口的前置条件。

## Next Step

Stage 3 的第一个实验只做最小环境创建和 `reset()`，先检查返回结构，再选少量 observation 字段与 `SimpleEnv` 对照。保持“一个实验 → 一个现象 → 一个概念”。
