# LazySpec

一套面向编码代理的 Spec 驱动开发 Skills，将功能想法转化为可审阅的需求、设计和实施任务。

## 工作流程

```text
正常链路：Brainstorming → Requirements → Design → Tasks → 按需执行任务清单
fast 链路：讨论 → plan.md → 一次审批 → 连续执行全部任务
```

- Brainstorming 确认目标、范围、约束、成功标准和方案，仅保存在当前会话。
- Requirements、Design、Tasks 分别生成 `requirements.md`、`design.md`、`tasks.md`。
- 每个阶段都需要用户明确批准，未获批准不会进入下一阶段。
- fast 模式面向轻量新功能：交互式讨论后生成单个 `specs/<feature-name>/plan.md`，一次明确批准后连续执行全部任务。仅限首次创建（无 `requirements.md`）；已有 Spec 的功能仍走正常链路。

## 安装与接入

### Agent Skills

```bash
npx skills add ccasJay/LazySpec --skill '*' -g
```

按提示选择目标代理。安装完成后，确认七个 Skill 均可发现；日常使用从
`using-lazyspec` 进入。

### Claude Code Plugin

兼容性基线为 Claude Code `2.1.229`。克隆本仓库后，在仓库根目录校验
`.claude-plugin/plugin.json`，再以仓库绝对路径加载本地 Plugin：

```bash
claude --version
claude plugin validate .
claude --plugin-dir /absolute/path/to/LazySpec
```

进入 Claude Code 后可用 `/help` 查看已加载命令；日常推荐使用统一入口：

```text
/lazyspec:using-lazyspec
```

七个可显式调用的 Skill 为：

```text
/lazyspec:using-lazyspec
/lazyspec:brainstorming
/lazyspec:writing-requirement
/lazyspec:writing-design
/lazyspec:writing-task
/lazyspec:distill-spec-memory
/lazyspec:fast
```

Plugin 或 Skill 未出现时，按以下顺序排查：

1. 确认 `claude --version` 不低于兼容性基线，并重新运行
   `claude plugin validate .`。
2. 确认 Manifest 位于仓库根目录的 `.claude-plugin/plugin.json`，其中七个
   `skills` 相对路径均指向包含 `SKILL.md` 的现有目录。
3. 在会话中运行 `/reload-plugins`，然后用 `/help` 再次检查；仍未加载时，
   退出并用正确的绝对路径重新执行 `claude --plugin-dir ...`。
4. 若同一个 Skill 出现两次，运行 `npx skills list -a claude-code --json` 和
   `claude plugin list` 检查是否同时启用了 Agent Skills 与 Plugin。同一会话只
   选择一种入口：使用 Plugin 时不要再向该项目安装同名 Agent Skills；使用
   Agent Skills 时不要传入 `--plugin-dir`，并停用已持久安装的同名 Plugin。

不同代理的问答工具名称可以不同。LazySpec 会优先使用环境提供的审批问答
工具；没有适用工具时，会在会话中直接请求明确批准。

## 快速开始

以下是自然语言调用示例，请替换为所用代理支持的 Skill 调用方式：

```text
# 创建 Spec
使用 using-lazyspec 为“用户认证”创建一个 Spec。

# 修改已有需求
使用 using-lazyspec 修改 specs/user-authentication/requirements.md，新增账户锁定要求。

# 执行全部任务
使用 using-lazyspec 执行 specs/user-authentication/tasks.md 中的全部 TODO。

# 只执行指定 TODO
使用 using-lazyspec 执行 specs/user-authentication/tasks.md 中的 TODO 2.1。

# fast 模式创建轻量新功能
使用 using-lazyspec 以 fast 模式为“导出 CSV”创建 plan 并执行。
```

新功能会先进入 Brainstorming（显式请求 fast 模式时除外）；修改已有
`requirements.md` 时默认直接进入 Requirements。执行任务前会读取该功能的全部
Spec。用户明确要求执行 `tasks.md` 时，默认创建 `codex/<feature-name>` 特性分支，按顺序完成全部未完成 TODO，并在每个 TODO 验证通过后单独提交，中途不等待逐项确认；只有用户明确指定某个 TODO 编号时才限制为单项执行。fast 模式审批后则连续执行 plan 中的全部任务。

## Spec 产物

产物保存在 `specs/<feature-name>/`：

| 文件 | 内容 |
|---|---|
| `requirements.md` | Human-First 审批摘要、用户故事和带稳定锚点的 EARS 验收标准 |
| `design.md` | Human-First 审批摘要、关键实现决策、测试策略及必要的技术章节 |
| `tasks.md` | 可增量执行的编码任务及需求链接 |
| `plan.md` | fast 模式产物：目标、约束、方案和带勾选框的任务清单 |

Brainstorming Context 不会落盘；若进入 Requirements 前会话丢失，需要重新确认。

### 默认精简策略

LazySpec 默认生成“最小充分文档”：Requirements 只记录可验证行为，Design 只记录影响实现的决策，Tasks 只记录编码动作和自动化验证。下游文档通过需求编号引用上游内容，不重复转述。

- Requirements 默认不超过 8 组、每组 2–5 条验收标准，总数尽量不超过 30 条。
- Design 的详细正文默认约 100–180 行（不含审批摘要）；架构、接口、数据模型、错误处理、调研结论和图表按需生成。
- Tasks 每项通常不超过 3 个说明点，只链接直接落实的验收标准。

以上均为软限制，不会截断必要信息。需要更多上下文时，可以明确要求展开某个相关章节。

### Human-First 审批摘要

新创建或修订的 Requirements 与 Design 会在文档顶部生成中文 `审批摘要`。摘要面向用户审批，详细正文继续面向 Agent 执行：

- Requirements 摘要集中展示目标、范围、核心行为、风险与待确认事项。
- Design 摘要集中展示方案、关键决策及其影响、风险与待确认事项。
- 用户批准的是摘要表达的实质意图、决策与风险，以及正文与摘要的一致性；不是逐行批准内部实现细节。
- 范围、行为、关键决策或风险发生实质变化时必须重新审批；不改变摘要的内部实现细化不使批准失效。
- 摘要不设置固定条数，由模型按认知复杂度压缩到一屏内；无法完整压缩时会先建议拆分 Spec。
- 修订时文档保留完整的当前摘要，会话中另外突出新增、修改、删除和风险变化。

现有 Spec 不会批量迁移；某份 Requirements 或 Design 下次被修订时才补充摘要。已经批准的旧 Requirements 仍可直接用于创建新的 Design。

## Skill 职责

| Skill | 职责 |
|---|---|
| [`using-lazyspec`](./using-lazyspec/SKILL.md) | 统一入口、阶段路由、审批门和任务执行 |
| [`brainstorming`](./brainstorming/SKILL.md) | 澄清目标、比较方案并生成会话 Context |
| [`writing-requirement`](./writing-requirement/SKILL.md) | 创建或修改 Requirements |
| [`writing-design`](./writing-design/SKILL.md) | 基于已批准需求创建设计 |
| [`writing-task`](./writing-task/SKILL.md) | 将已批准设计转为编码任务 |
| [`distill-spec-memory`](./distill-spec-memory/SKILL.md) | 将已完成并验证的 Feature Spec 提炼为项目 Memory |
| [`fast`](./fast/SKILL.md) | 轻量新功能快速通道：讨论生成 plan.md，一次审批后连续执行 |

## 约束

- 文件存在不代表已经批准；审批以当前会话中的明确回复为准。Requirements 和 Design 的审批对象是顶部摘要及其与正文的一致性，Tasks 仍审批完整任务文档。
- 手动运行 Brainstorming 不会自动修改已有 Spec。
- Tasks 获批只代表规划完成，实际编码需单独发起任务执行请求。
- fast 模式仅限首次创建（无 `requirements.md`）；`plan.md` 与 requirements/design/tasks 三件套互斥，同一 feature 只保留其中一种产物。
- `templete` 是项目现有文件名约定，请勿自行改名。

历史工作流示例见 [`specs/lazyspec`](./specs/lazyspec/)；该存量 Spec 创建于 Human-First 审批摘要引入前，不代表当前输出格式。
