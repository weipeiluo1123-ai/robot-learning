---
title: Troubleshooting
project: robot-learning
status: living_document
tags: [robot-learning, troubleshooting, debugging]
---

# Troubleshooting

这不是错误清单，而是把实际遇到的问题整理成可长期复用的工程认知。

统一结构：

- Symptom：实际看到什么。
- Cause：为什么发生。
- Fix：如何解决。
- What I learned：建立了什么长期认知。

## 1. Conda initially not found

### Symptom

```text
zsh: command not found: conda
```

### Cause

尚未安装 Miniforge / Conda，shell 也没有完成 Conda integration。

### Fix

安装 Miniforge 并完成 zsh integration。

### What I learned

命令找不到时，先区分软件未安装、executable 不在 PATH、shell integration 未加载，不能只重复安装。

## 2. Base environment automatically activating

### Symptom

打开新 shell 时提示符自动出现 (base)。

### Cause

Conda auto activation 默认会在 shell 启动时激活 base。

### Fix

```bash
conda config --set auto_activate_base false
conda config --show auto_activate
```

确认 auto_activate: False。

### What I learned

conda init zsh 提供 shell integration，不等于必须自动进入 base。

## 3. System Python vs Conda Python

### Symptom

曾看到：

```text
/usr/bin/python3
/Users/weipeiluo/miniforge3/bin/python
/Users/weipeiluo/miniforge3/envs/robot-learning/bin/python
```

### Cause

它们分别对应系统 Python、Miniforge base 和 robot-learning 项目环境。

### Fix

```bash
which python
which python3
echo $CONDA_PREFIX
python --version
conda env list
```

### What I learned

不同 Python 路径不一定是安装冲突；先确认当前 shell 和实际 executable。

## 4. CLI help is not universal

### Symptom

```bash
type --help
type -h
```

不能按预期工作。

### Cause

type 是 zsh builtin，不是普通 external executable。

### Fix

```bash
man zshbuiltins
type conda
type python
```

### What I learned

不要假设所有命令都支持 -h 或 --help。先判断 builtin、function、alias 还是 external executable。

## 5. y.device() error

### Symptom

```python
y.device()
```

得到 TypeError: torch.device object is not callable。

### Cause

device 是 attribute，不是 callable method。

### Fix

```python
y.device
```

### What I learned

object is not callable 时，检查是否把 attribute 当成 method。

## 6. Misspelled MuJoCo import

### Symptom

```python
import mujico
```

得到 ModuleNotFoundError。

### Cause

模块名称拼写错误，正确名称是 mujoco。

### Fix

```python
import mujoco
```

### What I learned

ModuleNotFoundError 也可能来自拼写错误或当前 Python 环境错误。

## 7. Python REPL ... misunderstood as hanging

### Symptom

```python
for _ in range(20):
```

看到 ...，误以为卡住并按 Ctrl+C，产生 KeyboardInterrupt。

### Cause

REPL 正在等待 compound statement 的剩余内容；... 是 continuation prompt。

### Fix

```python
for _ in range(20):
    print(_)

```

### What I learned

>>> 表示等待顶层语句；... 表示当前语句还没有结束。

## 8. Standalone Viewer moves without my mj_step

### Symptom

```bash
python -m mujoco.viewer --mjcf=ball.xml
```

没有在自己的 Python 文件中写 mj_step，Viewer 中的球仍会运动。

### Cause

standalone viewer 自己实现了 simulation loop：

```text
load model → create data → mj_step loop → render
```

XML 只是 model description，不会自己执行。

### Fix

需要自己控制 loop 时，使用 Python 程序和 passive viewer，显式调用 mujoco.mj_step(model, data)。

### What I learned

区分 model description、simulation loop 和 renderer / viewer。

## 9. Viewer occupies terminal

### Symptom

运行 Viewer 时 shell prompt 不再出现。

### Cause

Viewer 是 foreground process，shell 正在等待它结束。

### Fix

关闭 Viewer、按 Ctrl+C、新开 Terminal tab；后台运行 & 目前只作为知识了解。

### What I learned

程序占用终端不等于程序挂死；输入会交给 foreground process。

## 10. GitHub HTTPS authentication issue

### Symptom

GitHub repository 使用 HTTPS 时遇到认证问题。

项目：weipeiluo1123-ai/robot-learning。

### Cause / Fix

后来在新 Mac 上配置 SSH：

```text
id_ed25519
id_ed25519.pub
wpcloud
wpcloud.pub
```

id_ed25519 用于 GitHub，wpcloud 用于已有云服务器 / rsync。remote 改为：

```text
git@github.com:weipeiluo1123-ai/robot-learning.git
```

### What I learned

一台机器拥有多组 SSH keys 很正常；private key 不可分享、不可 commit；.pub 是 public key；known_hosts 保存远程服务器 host keys。

## 11. Empty directories not shown by Git

### Symptom

创建 mujoco/01_falling_ball/ 后，git status 没有变化。

### Cause

Git tracks files, not empty directories。

### Fix

加入 ball.xml 和 main.py 后目录会被 Git 识别。

### What I learned

Git 的版本跟踪对象是文件内容，不是空目录。

## 12. 学习记录与当前实验文件的参数差异

### Symptom

学习记录出现 z = 1、gravity = -9.81，而当前 ball.xml 是：

```xml
<body name="ball" pos="0 0 2">
<option timestep="0.01" gravity="0 0 -0.5"/>
```

### Cause

记录与当前文件可能来自不同次实验或后续修改。

### Fix

不自动修改历史记录，也不自动修改实验代码。复现实验时以实际 XML 参数为准，并标注参数版本。

### What I learned

学习日志应分开记录当时结果、当前文件内容和复现实验参数，不能为了“一致”抹平差异。

## 13. Git project organization

### Symptom

项目文件、环境文件和生成结果容易混在一起，或误把 ~/Projects 当成 Git repository。

### Fix

```text
~/Projects/
└── robot-learning/
```

当前约定：

- ~/Projects/ 不是 Git repository。
- ~/Projects/robot-learning/ 是独立 Git repository。
- repository names：kebab-case。
- Python folders / files：snake_case。
- Python variables / functions：snake_case。
- classes：PascalCase。

不要 ignore .py、.xml、README、docs；不要提交 Conda environment、secrets、大型 checkpoints 或 datasets。gitignore 对已经 tracked 的文件不会自动停止 tracking。

推荐开发循环：

```text
edit → run / verify → git status → git diff → git add → git commit → git push
```

