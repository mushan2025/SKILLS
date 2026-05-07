# Codex Skills 仓库

这是一个用于存放可复用 Codex Skills 的仓库，主要面向以下场景：

- 把常用技能整理成可长期维护的版本；
- 上传到 GitHub，方便备份、展示和分享；
- 安装到本地 Codex，作为稳定可复用的技能库；
- 后续继续扩展更多垂直领域的 skill。

---

## 当前收录的 Skills

### 1. `general-bioinformatics-teaching-script`

适用于把生物信息学分析脚本改写成“小白教学型脚本”。

这个 skill 更偏向通用教学版，强调：

- 脚本结构清晰，适合分节运行；
- 注释不仅说明做什么，还说明为什么做；
- 解释输入、输出、统计方法和生物学意义；
- 兼顾可运行性、可学习性和可交接性。

适合场景：

- 想把已有生信代码改写得更适合新手学习；
- 想为 bulk RNA-seq、单细胞、富集分析、差异分析等任务写教学型脚本；
- 想让后续接手项目的人更容易理解分析逻辑。

位置：

`general-bioinformatics-teaching-script/SKILL.md`

---

### 2. `general-bioinformatics-teaching-script-enhanced`

这是上面那个 skill 的强化版，适合“代码基础和生信基础都比较弱”的用户。

这个增强版会比标准版解释得更细，重点包括：

- 常见 R 语法和符号怎么读；
- 函数、参数、对象结构分别是什么意思；
- 每一步运行后应该检查什么；
- 出错时优先检查哪些地方；
- 结果怎么看才算正常；
- 如何把前一步结果自然衔接到后一步分析。

适合场景：

- 希望脚本像“边运行边讲解的课程讲义”；
- 需要面向完全新手写单细胞或 bulk 分析脚本；
- 想减少“会运行但看不懂代码”的问题。

位置：

`general-bioinformatics-teaching-script-enhanced/SKILL.md`

---

### 3. `general-project-handoff`

适用于编写高质量项目交接文档，让新的 AI 对话、未来工作会话，或者其他协作者能够无缝接手项目。

这个 skill 强调：

- 不只做摘要，而是做“连续性文档”；
- 明确记录项目目标、当前状态、已完成工作和下一步；
- 保留关键决策、被否决路径、风险点和注意事项；
- 给下一个 AI 或协作者一份可以直接接手工作的上下文。

适合场景：

- 聊天太长，准备换一个新窗口继续；
- 想让另一个 AI/代理继续当前项目；
- 想为未来自己或同事留一份清晰的项目交接说明。

位置：

`general-project-handoff/SKILL.md`

---

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── general-bioinformatics-teaching-script/
│   └── SKILL.md
├── general-bioinformatics-teaching-script-enhanced/
│   └── SKILL.md
└── general-project-handoff/
    └── SKILL.md
```

---

## 如何使用

你可以按下面几种方式使用这个仓库：

### 1. 直接在 GitHub 上查看

适合先浏览 skill 内容，确认是否符合你的工作流。

### 2. 复制 skill 到本地 Codex skills 目录

适合把其中某个 skill 安装到本地长期使用。

常见本地目录示例：

```text
C:\Users\你的用户名\.codex\skills\
```

每个 skill 以独立目录存在，目录中至少包含一个 `SKILL.md`。

### 3. 作为你自己的 skills 仓库继续维护

你可以继续在这个仓库里新增更多 skill，并通过 GitHub 持续版本化管理。

---

## 安装到本地 Codex

如果你已经有一个规范的 skill 目录，例如：

```text
general-bioinformatics-teaching-script/
└── SKILL.md
```

那么把整个目录复制到本地 Codex skills 目录即可。

安装完成后：

- 重启 Codex；
- 新 skill 就可以被识别和调用。

---

## 更新 GitHub 的常用流程

如果你修改了 skill 内容，最常用的同步命令是：

```powershell
git status
git add .
git commit -m "update skill"
git push
```

含义可以简单理解为：

- `git status`：查看当前改了什么；
- `git add .`：把本次改动加入待提交列表；
- `git commit -m "..."`：保存一个版本，并写一句说明；
- `git push`：把本地最新版本上传到 GitHub。

---

## 适合继续扩展的方向

这个仓库后面还可以继续加入例如：

- 单细胞专项分析 skill；
- bulk RNA-seq 专项 skill；
- 生信项目结果解读 skill；
- 论文图表写作 skill；
- AI 项目交接 / 项目审阅 / 项目归档 skill。

---

## License

本仓库采用 MIT License。

详见：

`LICENSE`
