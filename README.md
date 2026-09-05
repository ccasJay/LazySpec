# LazySpec

一套面向编码代理的 Spec 驱动开发 Skills，将功能想法转化为可审阅、可执行、可验证的交付，并沉淀有证据的项目经验。

## 工作流程

```text
正常链路：Brainstorming → Requirements → Design → Tasks → 按需执行 → 功能验收
fast 链路：讨论 → plan.md → 一次审批 → 连续执行 → 功能验收
验证失败：诊断 → 范围内修复，或回到 Requirements / Design / Tasks
经验学习：自动提取候选 → 确认完整写入预览 → Project Memory
```

- Brainstorming 确认目标、范围、约束、成功标准和方案，仅保存在当前会话。
- Brainstorming 默认用白话中文、先讲用户能获得的结果，再说明必要的技术取舍；每次只请用户做一个决定。用户主动使用术语或要求深入时，表达会随之提高专业程度，但仍保持简洁且不会省略范围、约束、风险和成功标准。
- Requirements、Design、Tasks 分别生成 `requirements.md`、`design.md`、`tasks.md`。
- low 风险按顺序起草三份 Spec 后合并审批；medium/high 风险逐阶段审批。草稿存在不代表批准。
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
| `tasks.md` | 带成功判据的编码任务、需求链接、Feature Verification 与可选 Learning Candidates |
| `plan.md` | fast 模式产物：目标、约束、方案、任务、Feature Verification 与可选 Learning Candidates |

Brainstorming Context 不会落盘；若进入 Requirements 前会话丢失，需要重新确认。

### 默认精简策略

LazySpec 默认生成“最小充分文档”：Requirements 只记录可验证行为，Design 只记录影响实现的决策，Tasks 的任务清单只记录编码动作、成功判据和验证入口；文末分别保留功能验收与可选学习候选。下游文档通过需求编号引用上游内容，不重复转述。

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
| [`distill-spec-memory`](./distill-spec-memory/SKILL.md) | 提炼已验证功能、推广经确认的学习候选，并维护两类项目 Memory |
| [`fast`](./fast/SKILL.md) | 轻量新功能快速通道：讨论生成 plan.md，一次审批后连续执行 |

## 约束

- 文件存在不代表已经批准；审批以当前会话中的明确回复为准。Requirements 和 Design 的审批对象是顶部摘要及其与正文的一致性，Tasks 审批完整任务计划及预定验收范围；运行证据和学习候选更新不重新触发计划审批。low 风险将三份文档合并审批。
- 手动运行 Brainstorming 不会自动修改已有 Spec。
- Tasks 获批只代表规划完成，实际编码需单独发起任务执行请求。
- fast 模式仅限首次创建（无 `requirements.md`）；`plan.md` 与 requirements/design/tasks 三件套互斥，同一 feature 只保留其中一种产物。
- `templete` 是项目现有文件名约定，请勿自行改名。

## 风险、验收与学习

| 风险 | 典型影响 | 审批与验证 |
|---|---|---|
| low | 局部可撤销，无公共接口、持久化数据、权限变化 | 三份 Spec 合并审批；验收标准覆盖与直接回归 |
| medium | 跨组件、公共接口、兼容数据变化 | 逐阶段审批；增加集成、兼容、异常路径 |
| high | 权限、敏感数据、破坏性迁移或不可逆影响 | 逐阶段审批；确认尚未授权的关键操作与最终验收证据，增加相关安全和恢复验证 |

按最高适用风险判断，不打分；不能证明为 low 时先按 medium，存在未明确的高风险后果时先澄清。fast 各等级均保留单份计划和一次计划审批，同时遵守高风险操作及验收确认。风险升级会暂停受影响工作并补齐审批。

每个 TODO 写清实现目标、具体场景下的可观察成功判据、已发现的命令或测试入口。新测试标记为待实现，不能只用“测试通过”作为判据。完成时只修改复选框，保留 TODO 原文；后续修复追加记录，普通模式单独提交。

全部 TODO 完成后自动进行 Feature-level Verification；请求执行已勾选计划也会补齐缺失或失效的验收。部分任务完成不代表整个功能通过，状态查询不启动执行。结果直接写入 tasks.md / plan.md 的 Feature Verification：预定验收范围与运行结果分开，记录实际证据、时间、被测提交、相关未提交改动及契约版本。结果区分 passed、failed、blocked、pending-human；相关代码或契约变化后标为 stale。必要人工检查未完成，以及高风险证据未经用户确认时，均不能报告功能通过。

实现错误在授权范围内持续修复；同一问题连续两轮没有新证据或改善时暂停。任务遗漏回 Tasks，设计假设失效回 Design，行为或验收标准有误回 Requirements；环境和权限缺失只标 blocked。fast 在同一 plan 内回到目标、方案或任务，实质修订重新审批。不得删减成功判据来掩盖失败。

有价值的成功或失败经验先进入文末 Learning Candidates，确认完整候选与确切写入预览后才进入 project-memory/learnings/。原有 project-memory/features/ 保留；两类共用六列索引和状态生命周期，合计最多召回三条适用的 active 记忆。失败经验不要求功能全部完成，但必须有可归因证据，未经验证的修复建议不能成为长期指导。不会自动修改 AGENTS.md、技能或权限。

现有 Spec 不批量迁移；下次执行时补充风险与验收结构，涉及实质判据变化时按风险规则审批。共享规则见 [risk-policy](./using-lazyspec/references/risk-policy.md) 和 [delivery-loop](./using-lazyspec/references/delivery-loop.md)。安装时保留七个 Skill 及其相对目录，共享参考文档随 using-lazyspec 分发。

历史工作流示例见 [`specs/lazyspec`](./specs/lazyspec/)；该存量 Spec 创建于 Human-First 审批摘要引入前，不代表当前输出格式。
