# 项目记忆体系 Brainstorming

> 状态：Brainstorming Context 已于 2026-08-15 获得用户明确批准；尚未创建 Requirements，也不代表 Design 已获批准。

## 1. 初始目标

为 LazySpec 增加一个独立 Skill，在某个 Feature 已完成后，将其 `specs/<feature>/` 中值得长期复用的内容沉淀为项目级 Memory。未来创建或修改其他 Spec 时，Agent 能按需找到相关背景、既有决策、约束和踩坑经验，而不必重读所有历史 Spec。

附件中的 `topics/index → TOPIC → MEMORY → sessions` 四层结构只作为灵感。当前更适合先确定“什么值得记住”和“以什么为主索引”，再决定最终目录名及文件数量。

## 1.1 已确认方向

- **第一服务对象：Agent。** Memory 首先用于帮助未来 Agent 低成本定位和加载相关项目知识，同时保持人类可审阅。
- **组织方案：Feature 来源层 + Topic 提炼层，分阶段实现。** MVP 先建立 Feature Capsule 与 index；只有积累出真实的跨 Feature 重复知识后，才增加 Topic 聚合层。
- **完成判定：组合门槛。** 只有 Tasks 全部完成、相关验证通过，并且用户明确确认 Feature 可以沉淀时，Skill 才能写入长期 Memory。
- **证据策略：Spec + 实现核对。** Spec 用于保留目标与决策意图，代码和测试用于核对最终现实；发现不一致时必须暂停并请求用户裁决，不得由 Agent 静默选择一方。
- **写入审批：先预览、后写入。** Agent 必须先展示拟新增、修改、冲突和来源摘要；只有用户明确批准后，才能修改正式 Feature Memory 与 index。
- **项目目录：`project-memory/`。** Memory 属于目标项目、可版本控制且与具体 Agent/工具解耦；不放入 LazySpec Skill 目录，也不隐藏在工具命名空间中。
- **消费方式：接入现有 LazySpec 流程。** `distill-spec-memory` 负责沉淀；`using-lazyspec` 先读取轻量 index，只选择与当前任务相关的少量 Memory，并传给当前阶段使用。
- **索引格式：仅 `index.md`。** 第一版使用固定表格结构，同时服务 Agent 扫描和人工审阅；不维护或生成第二份 JSON 索引。
- **过期标记：强制。** 已经过期或不再适用的 Memory 必须同时在 Capsule 元数据和 `index.md` 中显式标记，并从 Agent 的默认检索结果中排除；只有追溯历史时才读取。
- **状态模型：四状态。** `active` 表示当前有效，`needs-review` 表示疑似漂移且需要复审，`superseded` 表示已有明确替代项，`obsolete` 表示已经失效但没有替代项。
- **Skill 名称：`distill-spec-memory`。** 只在用户要求把已完成并验证的 Feature Spec 沉淀为项目 Memory 时触发，避免被普通项目文档更新误触发。
- **Capsule 可变性：正文冻结。** Capsule 获批后保留为历史快照；后续 Feature 创建新 Capsule。旧 Capsule 只允许更新状态、替代关系，以及经批准的错字或失效链接。
- 由此带来的倾向：稳定的元数据字段、明确的 `Reuse Triggers`、短而独立的知识单元、可确定性扫描的 index、按需读取而非全库注入。
- 人类阅读体验仍是约束，但不为了叙事完整性保留低价值过程信息。

## 2. Spec 与 Memory 的边界

建议把二者看成不同生命周期的产物：

| 产物 | 回答的问题 | 特性 |
|---|---|---|
| Spec | 这个 Feature 当时要做什么、如何设计和实施？ | 完整、按 Feature 组织、保留历史上下文 |
| Memory | 今后的工作必须知道什么？ | 精炼、当前有效、可检索、可追溯 |

因此，Memory 不应是 Spec 的复制品，也不应默认保存完整会话。它更像从已完成 Spec 中抽取出的“稳定投影”。

### 值得沉淀

- Feature 最终提供的能力和明确边界。
- 仍然有效的架构或流程决策，以及选择理由和被放弃方案。
- 后续 Feature 必须遵守的 contract、invariant、兼容性约束。
- 实施后才能知道的非显然经验、失败路径和验证方式。
- 原始 Spec、关键代码或 ADR 的来源链接。
- Memory 的适用范围、状态，以及何时应被替代或复审。

### 不宜默认沉淀

- `requirements.md`、`design.md`、`tasks.md` 的逐段摘要或全文复制。
- 已完成 checkbox、临时进度、普通命令输出和会话流水账。
- 从当前代码即可低成本重新得出的事实。
- 没有来源、未经验证或仅在讨论中出现的猜测。

## 3. 三种候选组织方案

### 方案 A：Feature Capsule

```text
project-memory/
├── index.md
└── features/
    └── <feature-name>.md
```

每次运行新 Skill，就从一个已完成 Spec 生成一份自包含的 Feature Memory。

- 优点：与 `specs/<feature>/` 一一对应，落地简单，来源清楚，适合作为 MVP。
- 缺点：跨 Feature 的同一主题可能重复；Feature 多了以后，检索依赖 index 和关键词。
- 适合：先验证“沉淀动作”是否真正有价值。

### 方案 B：Topic Knowledge Base

```text
project-memory/
├── index.md
└── topics/
    └── <topic-name>/
        ├── TOPIC.md
        ├── MEMORY.md
        └── sources.md
```

以认证、审批、兼容性等稳定主题组织知识，多个 Spec 可以更新同一 Topic。

- 优点：贴近附件中的检索模型，跨 Feature 复用强，长期阅读体验好。
- 缺点：一次 Feature 可能命中多个 Topic；合并、冲突和过期判断明显更难。
- 适合：主题边界已经稳定、Memory 数量较多的成熟项目。

### 方案 C：Feature 来源层 + Topic 提炼层

```text
project-memory/
├── index.md
├── features/
│   └── <feature-name>.md
└── topics/
    └── <topic-name>.md
```

Feature Memory 是可追溯的沉淀单元；Topic 是跨 Feature 的当前共识视图。Topic 只引用 Feature Memory，不复制原 Spec。

- 优点：兼顾写入简单、来源追踪和长期主题检索；可以逐步演进。
- 缺点：需要定义何时更新 Topic、发生冲突时谁是 source of truth。
- 适合：把体系作为 LazySpec 的长期组成部分。

**已选择：方案 C，分阶段实现。** 第一版只实现 Feature Capsule 和 index，目录为未来的 Topic 层留出演进空间；等真实积累出重复知识后，再增加 Topic 聚合。这样不会在缺乏样本时过早设计 taxonomy。

## 4. 单份 Feature Memory 的候选结构

```markdown
---
feature: <feature-name>
status: active | needs-review | superseded | obsolete
source: specs/<feature-name>/
distilled_at: YYYY-MM-DD
tags: []
supersedes: []
---

# <Feature 名称>

## Capability
最终提供了什么，以及明确不包含什么。

## Durable Decisions
仅保留会影响未来工作的决策：选择、理由、替代方案、后果。

## Contracts and Invariants
未来修改不得意外破坏的行为、接口、数据或流程约束。

## Lessons
非显然的失败路径、兼容性发现、验证经验。

## Reuse Triggers
以后遇到哪些任务或关键词时应读取本 Memory。

## Sources
原 Spec、代码、测试或 ADR 的相对链接。
```

状态字段最终采用 `active | needs-review | superseded | obsolete`。`superseded` 必须提供替代项引用；`needs-review`、`superseded`、`obsolete` 默认不参与普通任务检索。

这里刻意不设置 `sessions/`：Spec 已经保留完整过程，Memory 只保存长期有效知识。如果以后确实需要审计会话，可以作为独立的 History/Archive 能力，而不是核心 Memory 的必需层。

## 5. 独立 Skill 的候选职责

名称讨论：

- `distill-spec-memory`：已选择；强调从 Spec 提炼 Memory，且输入、动作、输出都清楚。
- `archive-feature-spec`：强调 Feature 完成后的归档，但容易让人误以为只是搬文件。
- `update-project-memory`：覆盖面更广，但触发边界可能与普通文档维护混淆。

`distill-spec-memory` 的初步工作流可以是：

1. 绑定用户项目根目录，定位用户指定的 `specs/<feature>/`。
2. 验证 Feature 确实完成：Tasks 全部完成、相关验证通过，并取得用户明确确认；不能仅凭文件存在推断完成状态。
3. 读取完整 Requirements、Design、Tasks，并针对性核对代码和测试；发现偏差时请求用户裁决。
4. 抽取候选 Memory，过滤临时信息和可轻易重建的信息。
5. 检查已有 Memory 中的重复、冲突、替代关系。
6. 向用户展示拟新增、修改、冲突和来源摘要；明确批准前不得创建或更新正式 Memory。
7. 更新 Feature Memory 与 index，保留到来源的相对链接。
8. 验证链接、元数据、唯一性和“没有把 Spec 整份复制进来”。

初步安全边界：

- 独立显式触发，不自动挂在 Tasks 完成之后。
- 不删除或移动原 Spec。
- 不先写 `draft` 文件代替审批；预览保留在会话中，批准后才落盘。
- 不静默覆盖冲突结论；使用 `supersedes` 或请求用户裁决。
- 不允许过期 Memory 继续以普通有效项参与检索；状态变化必须与 index 同步更新。
- 不原地改写已批准 Capsule 的结论来伪装历史；新结论通过新 Capsule 和 `supersedes` 关系表达。
- 不把 Spec 或实现单独视为绝对权威；Memory 只能记录二者核对后确认的事实与决策。
- Memory 是项目拥有、可版本控制的内容，不与 Skill 自身的模板和脚本混放。
- 默认只按需读取相关 Memory，不在每次任务开始时加载全库。
- `using-lazyspec` 不直接加载全部 Memory 正文；先以 index 粗筛，再读取命中的少量文件。

## 6. Index 的角色

在已确定的 `project-memory/` 下，第一版只使用人和 Agent 都能读的 `index.md`：

- 记录 Memory 路径、简短说明、tags、状态和 source Spec。
- 作为粗筛路由，不承载正文。
- 使用固定表格列和稳定路径，保证 Agent 可以确定性粗筛。
- 规模变大、确实需要机器索引时再重新讨论；第一版不维护第二份 source of truth。

## 7. 衡量成功的候选标准

- 新 Agent 只读取 index 和 1–3 个相关 Memory，就能说出相关既有决策与约束。
- 每条重要结论都能追溯到 Spec、代码、测试或明确的用户确认。
- 同一事实只有一个当前有效的权威表述；旧结论可追溯但不会被误当成现状。
- 沉淀结果明显短于原 Spec，且不依赖完整会话流水。
- 新增 Memory 不会修改或破坏 LazySpec 现有 Brainstorming → Requirements → Design → Tasks 审批链。

## 8. 外部灵感与取舍

- [ADR 组织](https://adr.github.io/)把 ADR 定义为记录单个决策及其理由、权衡和后果。这支持把“Durable Decisions”作为 Memory 的核心原子，而不是写泛化总结。
- [GitHub Spec Kit](https://github.com/github/spec-kit)将项目原则保存在 `.specify/memory/constitution.md`，由各阶段按需读取；其[升级文档](https://github.github.com/spec-kit/upgrade.html)进一步强调实时读取单一事实源、使用指针而非复制。这支持“按需加载 + 引用来源”的方向。
- Spec Kit 的一个[项目 Memory 所有权讨论](https://github.com/github/spec-kit/issues/2681)提出将工具管理资产与项目拥有的长期知识分开。这支持把 Memory 建在目标项目中，而不是放进 LazySpec Skill 目录。
- Cline 的旧版 Memory Bank 采用 Project、Active Context、Progress、Decisions 等多文件层次；它启发了分层，但“每次读取全部文件”和持续记录进度不适合这里以完成 Spec 为输入的低噪声沉淀目标。

## 9. 决策状态

第一服务对象、组织方案、完成门槛、证据策略、写入审批、目录、消费方式、索引格式、状态模型、Skill 名称和 Capsule 可变性均已确认。完整 Brainstorming Context 已获得用户明确批准；等待用户另行请求进入 Requirements。

## 10. 当前讨论焦点

关键问题均已确认，等待用户审批完整 Brainstorming Context。

## 11. Brainstorming Context（已批准）

### objective

为 LazySpec 增加项目级 Memory 体系：通过独立的 `distill-spec-memory` Skill，将已经完成并验证的 Feature Spec 提炼为可供未来 Agent 按需检索的长期知识。

### scope

- 在目标项目根目录维护 `project-memory/index.md` 与 `project-memory/features/<feature-name>.md`。
- `distill-spec-memory` 负责完成检查、Spec 与实现核对、候选提炼、预览审批、写入和索引同步。
- `using-lazyspec` 先读取 index，再为当前阶段按需加载少量相关 Memory。
- MVP 只实现 Feature Capsule 层；Topic 聚合层待真实出现跨 Feature 重复知识后再设计。

### constraints

- Agent 优先，同时保持 Markdown 可审阅；不保存会话流水，不复制完整 Spec，不生成 JSON 索引。
- 仅当 Tasks 全部完成、相关验证通过且用户明确确认时，Feature 才可沉淀。
- Spec 表达意图，代码与测试核对现实；不一致时暂停并请求用户裁决。
- 正式写入前必须展示新增、修改、冲突和来源摘要，并取得用户明确批准。
- Memory 使用 `active | needs-review | superseded | obsolete`；非 `active` 项退出默认检索。
- Capsule 获批后正文冻结；新 Feature 通过新 Capsule 与 `supersedes` 表达演化，旧 Capsule 仅允许状态、关系和经批准的维护性纠错。
- 不删除、移动或覆盖原 Spec，不破坏 LazySpec 现有阶段顺序与审批门。

### successCriteria

- 新 Agent 读取 index 与 1–3 个相关 `active` Memory，即可识别既有能力、决策、约束和复用条件。
- 每条长期结论均可追溯至 Spec、代码、测试或用户裁决。
- 过期、疑似漂移或已被替代的 Memory 有明确状态，且不会进入默认检索。
- 沉淀产物明显短于原 Spec，并且没有把低价值过程信息带入长期上下文。
- 未满足完成门槛或未获得写入批准时，项目 Memory 不发生正式变更。

### selectedApproach

采用“Feature 来源层 + Topic 提炼层”的分阶段方案：MVP 先建立不可变 Feature Capsule 与 Markdown index，未来再根据真实重复知识增加 Topic 层。

### approval

`approved: true`（用户于 2026-08-15 明确选择 Approve）。
