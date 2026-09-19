你正在协助我维护 Robot Learning 学习仓库。

Repository:
~/Projects/robot-learning

GitHub repository:
weipeiluo1123-ai/robot-learning

这是一个长期学习项目，不是一次性 demo。

我的学习目标是：
通过项目驱动的方式学习 Robot Learning / Robotics / Embodied AI，
最终形成可运行代码、实验结果、GitHub 项目和求职可展示成果。

我的学习原则：

实验
→ 观察
→ 发现问题
→ 理解概念
→ 修改代码
→ 验证
→ 总结

不要把项目整理成“我已经掌握所有知识”的教程。
需要保留真实学习轨迹，包括：
- 当天做了什么
- 实际观察到了什么
- 遇到了什么问题
- 哪些误解被纠正
- 哪些知识已经理解
- 哪些只是初步接触
- 下一步准备做什么

==================================================
任务 1：检查真实 repository
==================================================

首先检查：

- 当前工作目录
- git status
- git log --oneline 最近若干条
- 当前目录结构
- docs/ 已有文件
- mujoco/ 下现有实验
- README.md
- .gitignore
- current_state.md（如存在）
- troubleshooting.md（如存在）

不要根据 Prompt 猜仓库状态。
以磁盘上的真实内容为准。

不要修改实验代码，除非为了修复明显的文档引用错误。
不要删除历史学习记录。

==================================================
任务 2：维护学习文档
==================================================

文档建议结构：

docs/
├── current_state.md
├── roadmap.md
├── troubleshooting.md
├── stages/
│   ├── stage0_environment_setup.md
│   ├── stage1_mujoco_basics.md
│   └── ...
├── checkpoints/
│   └── ...
├── images/
│   └── ...
├── prompts/
│   └── ...

如果仓库已有不同但合理的结构，
优先沿用现有结构，不要为了模板强行大规模重构。

本次 session 对应的 Day / Stage 请根据 current_state.md
和真实文件判断。

更新对应 session 文档。

文档重点记录：

What did I build?
What did I observe?
What did I learn?
What confused me?
What mistakes did I make?
How were they resolved?
What concepts are now understood?
What remains incomplete?

不要把尚未学习的内容写成 Completed。

==================================================
任务 3：更新 current_state.md
==================================================

这是整个项目最重要的上下文交接文件。

它必须保持简洁，目标是：

“把这个文件交给一个全新的 ChatGPT 会话，
它可以在几分钟内准确接手项目。”

current_state.md 应至少包含：

# Current State

## Long-term Goal

## Current Stage

## Environment

记录实际版本，例如：
- OS / architecture
- Conda environment
- Python
- PyTorch
- MuJoCo
- relevant hardware/backend

但必须以当前机器实际状态或已有可靠文档为准。

## Repository State

简要目录结构。

## Completed

已经真正完成并理解的内容。

## Concepts Understood

例如：
- qpos 不一定是 XYZ
- hinge qpos 表示 joint angle
- joint 与 actuator 不同
等等。

只记录真正已经学习过的。

## Experiments Completed

列出实际存在且运行过的实验。

## Problems / Lessons

只保留下一阶段仍然有价值的关键经验，
详细错误记录放 troubleshooting.md。

## Current Position

精确描述当前停在哪里。

## Next Step

只列最近一阶段应该继续的内容。

## Do Not Jump Ahead

列出暂时不应该展开的大型主题，
防止下一 Chat 重新把路线膨胀。

## Learning Style

说明用户有 C++ / 软件工程背景，
正在逐步学习 Python 与机器人，
希望解释“为什么”，
不希望只复制命令，
也不希望一次展开巨大的前置知识树。

==================================================
任务 4：维护 troubleshooting.md
==================================================

如果今天出现新的真实问题，
按以下格式追加：

## <Problem>

### Symptom

### Cause

### Fix

### What I learned

不要重复已经存在的问题。

不要记录毫无长期价值的小拼写错误，
除非它带来了重要认知。

==================================================
任务 5：维护 roadmap.md
==================================================

当前总体路线应该围绕：

Stage 0 — Development Environment
Stage 1 — MuJoCo Fundamentals
Stage 2 — Robot Control & Kinematics
Stage 3 — Robot Learning Environment / ManiSkill
Stage 4 — Imitation Learning / Behavior Cloning
Stage 5 — Reinforcement Learning / PPO
Stage 6 — Evaluation / Demo / Portfolio Artifact

不要因为今天讨论了某个细节就改变总体目标。

路线可以根据实际进度调整，
但必须说明为什么调整。

==================================================
任务 6：生成 Chat Handoff
==================================================

在：

docs/checkpoints/

生成或更新一个适合本次 session 的 checkpoint。

内容必须能直接粘贴到一个新的 ChatGPT 会话。

格式：

# Session Handoff

## Project Goal

## Current Environment

## Repository

## Completed This Session

## Important Concepts Already Understood

## Current Code / Experiments

## Problems Encountered

## Decisions Made

## Current Position

## Next Step

## Things Not To Re-Explain From Scratch

## Learning Preferences

最后额外输出一段：

“New Chat Startup Prompt”

让我能够直接复制进新的 ChatGPT 对话。

==================================================
安全和 Git 要求
==================================================

不要：
- 删除实验
- 修改 SSH keys
- 输出 secrets
- 读取或展示私钥
- 修改 Conda 全局配置
- 自动重构大量代码
- 自动 git commit
- 自动 git push

完成后只展示：

1. 创建了哪些文件
2. 修改了哪些文件
3. 每个文件做了什么
4. git status
5. git diff --stat
6. 是否发现需要我人工确认的问题

等待我 review 后再决定是否 commit / push。
