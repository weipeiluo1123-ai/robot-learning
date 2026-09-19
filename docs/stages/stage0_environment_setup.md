---
title: Stage 0 — Development Environment Setup
project: robot-learning
stage: 0
status: completed
tags: [robot-learning, environment, conda, pytorch, mps]
---

# Stage 0 — Development Environment Setup

## Status

**Completed**

这个阶段的重点不是记住安装命令，而是形成“先观察、再理解、再修改”的环境管理方法。

## 1. Mac 基础环境

设备：MacBook Pro M1 Max，Apple Silicon / arm64。

最开始检查：

```bash
python3 --version
git -v
uname -m
conda --version
```

观察到：

- macOS 系统 Python：3.9.6
- architecture：arm64
- Git 已安装
- Conda 尚未安装
- Homebrew 位于 /opt/homebrew/bin/brew

后来通过 Miniforge 安装 Conda：

- 路径：/Users/weipeiluo/miniforge3
- 版本：conda 26.7.2

## 2. Conda 与 shell

- (base) 表示 Conda base environment 已激活。
- Conda 没有替换 macOS 自带 Python。
- 不同 environment 可以拥有不同 Python。
- conda activate 会修改当前 shell，尤其是 PATH。
- conda deactivate 会撤销对应修改。
- CONDA_PREFIX 可以显示当前环境路径。

```bash
which python
which python3
which brew
type conda
echo $CONDA_PREFIX
echo $PATH | tr ':' '\n'
```

观察到：

- 未激活 Conda 时，python3 来自 /usr/bin/python3。
- brew 来自 /opt/homebrew/bin/brew。
- conda 是由 .zshrc 加载的 shell function。
- 未激活时 miniforge3/condabin 在 PATH 中，但 miniforge3/bin 不在最前面。
- 激活后，当前 environment 的 bin 会加入 PATH 前部。

```bash
conda init zsh
conda config --set auto_activate_base false
conda config --show auto_activate
```

conda init zsh 是 shell integration；是否自动进入 base 由 auto activation 配置决定。最终确认 auto_activate: False。

## 3. CLI 自我发现方法

不要只背命令，而应该通过帮助、错误信息和官方文档自己发现用法。

```bash
command --help
command subcommand --help
man command
man zshbuiltins
```

不是所有命令都支持 -h 或 --help。例如 zsh builtin type 应通过 man zshbuiltins 查看。

建立的习惯：

```text
先查询当前状态
    ↓
阅读 help / docs
    ↓
理解参数
    ↓
再修改系统
```

## 4. Conda package / environment

```bash
conda env list
conda list
conda search xxx
conda create -n robot-learning python=3.11
conda activate robot-learning
```

理解：

- -n / --name 是 CLI option。
- python=3.11 是 package specification。
- Python 在 Conda 中本身也是一个 package。
- environment 可以先创建，再逐步安装 packages。
- 不需要一开始知道全部依赖。

最终环境：

```text
/Users/weipeiluo/miniforge3/envs/robot-learning
Python 3.11.16
```

当前主要使用 conda-forge 和 osx-arm64。Solving environment 是寻找满足约束且互相兼容的软件包版本。Python 的依赖包括 openssl、libffi、readline、sqlite、pip、setuptools、wheel 等。

## 5. pip 与 Conda

```bash
which python
which pip
which pip3
python -m pip install <package>
```

Conda 主要负责 environment isolation 和整体环境管理；pip 主要负责在当前 Python environment 中安装 Python packages。使用 python -m pip 可以明确绑定当前 Python。

## 6. PyTorch 与 MPS

安装：

```bash
python -m pip install torch torchvision
```

当时成功安装 torch 2.14.0、torchvision 0.29.0。默认 Tensor device 是 cpu。

```python
import torch

x = torch.rand(5, 3)
print(torch.__version__)
print(x.device)

print(torch.backends.mps.is_built())
print(torch.backends.mps.is_available())

y = x.to("mps")
print(y.device)

a = torch.rand(1000, 1000, device="mps")
b = torch.rand(1000, 1000, device="mps")
c = a @ b
print(c.shape)
print(c.device)
```

结果包括 True、True、mps:0、torch.Size([1000, 1000]) 和 mps:0。

计算链路：

```text
Python → PyTorch → MPS backend → Metal → Apple Silicon GPU
```

## 7. 工程组织习惯

当前项目是独立 Git repository：

```text
~/Projects/robot-learning
```

命名约定：

| 对象 | 约定 |
|------|------|
| repository | kebab-case |
| Python folder / file | snake_case |
| variable / function | snake_case |
| class | PascalCase |

.gitignore 至少考虑：

```gitignore
.DS_Store
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
env/
.vscode/
.idea/
.env
.env.*
!.env.example
.ipynb_checkpoints/
outputs/
runs/
logs/
checkpoints/
wandb/
*.log
```

不要 ignore .py、.xml、README、docs；不要提交 Conda environment、secrets、大型 checkpoints 或 datasets。

## 8. Stage 0 回看

### What is it?

Conda environment 是隔离的项目运行环境；PATH 决定 shell 查找 executable 的顺序；Tensor 有明确 device；MPS 是 PyTorch 使用 Apple GPU 的 backend。

### What did I actually observe?

激活环境后 PATH 和 which python 发生变化；CPU Tensor 默认是 cpu；移动到 MPS 后变为 mps:0；M1 Max 矩阵乘法成功返回 MPS Tensor。
