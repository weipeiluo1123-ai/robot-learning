# Repository Maintenance and Remote Sync Prompt

你正在协助我维护一个长期发展的 GitHub 学习或项目仓库。

## 项目上下文

本地仓库路径：

```text
<LOCAL_REPOSITORY_PATH>
```

远程仓库：

```text
<REMOTE_NAME>
<REMOTE_URL>
```

项目不是一次性 demo。提交内容应保留真实开发和学习轨迹，不能为了“整洁”而删除有价值的历史记录。

目标：

1. 以磁盘上的真实状态为准检查仓库。
2. 合理区分当前任务、已有本地修改和无关文件。
3. 检查文档、代码、实验结果和项目结构之间的一致性。
4. 只在范围明确、内容安全并得到确认后暂存、提交和推送。
5. 不自动破坏、恢复、覆盖或清理用户已有修改。

---

## 1. 只读检查阶段

开始时不要执行 `git add`、`git commit`、`git push`，也不要使用 `git reset --hard`、`git checkout --` 或删除命令。

先执行：

```bash
pwd
git status --short --branch
git log --oneline -10
git remote -v
find . -maxdepth 3 -type f | sort
```

然后检查：

- 当前工作目录和当前分支。
- 当前分支是否领先或落后远程。
- tracked 文件的修改、删除和重命名。
- untracked 文件。
- docs/、src/、实验目录和配置文件。
- README.md 与 .gitignore。
- 当前项目是否存在已有的 roadmap、current state、troubleshooting 或 checkpoint。
- 是否存在缓存、生成结果、临时文件、环境文件、数据集、大型文件或敏感信息。

必须以磁盘上的真实内容为准，不要根据本 Prompt 猜测仓库状态。

---

## 2. 分类所有变化

建立一份清单，将文件分为三类。

### A. 明确属于本次项目内容

例如：

- README.md
- .gitignore
- 经过检查的 docs/
- 明确属于项目的源代码
- 实验所需的配置或模型文件
- 小型且有明确用途的实验图片
- 学习日志、roadmap、current state 和 checkpoint

### B. 可能提交，但需要检查

例如：

- 新实验目录
- 实验输出图片
- prompt 文件
- 生成结果
- 大型数据文件
- 用途尚不明确的文档或资源
- 与当前项目相关但尚未在文档中说明的文件

对这类文件先检查来源、大小、内容和用途，不要自动加入暂存区。

### C. 不应提交

通常包括：

- .DS_Store
- __pycache__/
- *.pyc
- .env、secrets、tokens
- SSH 私钥
- Conda environment 本体
- logs、runs、wandb、checkpoints
- 临时文件
- 大型数据集
- 编译产物
- 无法确认来源的文件

不要使用以下方式盲目提交：

```bash
git add .
git commit -am "update"
```

---

## 3. 文档与代码一致性检查

如果仓库包含学习文档或项目文档，检查：

- current_state.md 是否反映真实项目进度。
- roadmap.md 是否与当前阶段一致。
- session 文档是否对应实际完成的内容。
- troubleshooting.md 是否记录真实遇到的问题。
- checkpoint 是否能帮助新的 ChatGPT 会话接手。
- README.md 的项目结构是否过时。
- 文件名重命名是否与文档中的引用一致。
- 删除的历史文件是否有意删除。
- 代码、模型文件、实验输出和文档描述是否互相一致。

不要把以下内容写成 Completed：

- 只有代码但没有实际运行或观察过的实验。
- 只听说过但没有理解的概念。
- 尚未验证的推测。
- 计划中的未来主题。

如果发现不一致：

1. 先指出具体差异。
2. 优先修改文档中的错误引用或过时描述。
3. 不要为了让文档看起来一致而篡改实验历史。
4. 不要擅自修改实验代码。
5. 不要删除有价值的历史记录。

---

## 4. 处理删除和重命名

重点检查：

```bash
git diff --name-status
git diff --summary
git ls-files
```

对于疑似重命名：

- 检查旧文件和新文件的内容关系。
- 检查新文件是否保留了旧文件的重要内容。
- 检查 README、文档和脚本中的引用。
- 使用 Git 的重命名检测，但不要为了生成漂亮的 diff 而删除内容。

如果无法确定以下事项，必须暂停并向我报告：

- 某个历史文件是否应该删除。
- 某个中文或旧版学习日志是否应该保留。
- 某个实验代码是否属于本次提交。
- 某个图片或生成结果是否应该纳入版本控制。
- 某个 untracked 文件是否来自当前项目。

---

## 5. 安全检查

提交前执行：

```bash
git diff --check
find . -type f -size +50M -print
```

检查敏感信息时，只输出疑似文件路径，不要打印匹配内容：

```bash
rg -l --hidden -g '!*.pyc' -g '!.git/**' \
  'AKIA|BEGIN .*PRIVATE KEY|ghp_|github_pat_|password=|token=|api_key=' .
```

如果发现疑似 secret、token、私钥或大型文件：

- 不要暂存。
- 不要提交。
- 不要把内容打印出来。
- 只报告文件路径、类型和风险。
- 等待我的确认。

不要读取或展示私钥内容。

---

## 6. 生成提交计划

在执行 `git add` 之前，必须向我展示：

```markdown
准备提交：
- ...

不提交：
- ...

需要确认：
- ...

建议提交分组：
1. docs: ...
2. feat(...): ...
3. chore: ...
```

根据内容决定一个提交还是多个逻辑提交：

- 同一个连续文档维护任务，可以使用一个 docs 提交。
- 文档、源代码、实验资产彼此独立时，建议拆分。
- 不要为了拆分而制造大量无意义的小提交。

提交信息应具体，例如：

```text
docs: update project learning state
feat(simulation): add pendulum experiment
chore: organize repository documentation
```

不要使用：

```text
update
changes
fix
misc
```

---

## 7. 暂存和验证

只有在我确认提交计划后，才可以暂存。

只暂存明确的文件列表：

```bash
git add <明确的文件列表>
```

然后执行：

```bash
git status
git diff --cached --stat
git diff --cached --check
git diff --cached
```

逐项确认：

- 没有 secrets 或私钥。
- 没有缓存、临时文件或不必要的生成结果。
- 没有误删学习记录。
- 删除和重命名符合预期。
- 文档与代码状态一致。
- staged 内容只属于已确认范围。

如果发现问题，先停止，不要继续 commit。

---

## 8. 提交

确认暂存内容正确后：

```bash
git commit -m "<清晰、具体的提交信息>"
```

提交后检查：

```bash
git status --short --branch
git log --oneline -5
```

如果仍有无关未提交修改：

- 不要清理。
- 不要恢复。
- 不要删除。
- 只在最终报告中列出。

---

## 9. 推送

推送前再次确认：

- 当前分支。
- 当前分支与远程的关系。
- upstream 分支。
- 远程地址。
- 即将推送的 commit。
- 是否会直接修改远程 main。
- 是否存在远程新提交。

如果当前在 main，且没有明确授权直接推送 main，优先创建工作分支：

```bash
git switch -c codex/repository-sync
git push -u <REMOTE_NAME> codex/repository-sync
```

如果我明确允许直接推送当前分支：

```bash
git push <REMOTE_NAME> <CURRENT_BRANCH>
```

不要：

- force push。
- 自动合并远程分支。
- 覆盖远程提交。
- 在未确认时直接推送 main。

如果 push 被拒绝：

1. 不要 force push。
2. 执行 `git fetch`。
3. 检查本地与远程差异。
4. 报告可选方案。
5. 等待我决定是否 rebase、merge 或创建新分支。

---

## 10. 最终报告

完成后报告：

1. 创建、修改、删除和重命名了哪些文件。
2. 实际提交了哪些文件。
3. 哪些文件被排除以及原因。
4. commit 数量和 commit hash。
5. 推送到哪个远程分支。
6. 远程推送是否成功。
7. 最终 `git status`。
8. 是否还存在未处理的本地修改。
9. 是否发现需要人工确认的问题。
10. 如果没有执行 commit 或 push，明确说明停在哪一步以及原因。

除非我明确要求，不要：

- 删除文件。
- 恢复文件。
- 修改实验代码。
- 修改 SSH 配置。
- 修改 Conda 全局配置。
- 提交无关文件。
- force push。
- 自动合并远程分支。
