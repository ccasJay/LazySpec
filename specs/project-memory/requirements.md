# 项目记忆体系需求

## 引言

本功能为 LazySpec 增加 Agent 优先的项目级 Memory 体系：通过独立的 `distill-spec-memory` Skill，将已经完成并验证的 Feature Spec 提炼为可追溯、可审阅、可按需检索的长期知识，并让现有 LazySpec 流程只加载当前任务真正相关的有效 Memory。

## 需求

### 需求 1：提供独立的 Spec 沉淀入口

**用户故事：** 作为 LazySpec 使用者，我希望通过职责明确的独立 Skill 沉淀已完成 Feature，以便普通 Spec 工作流和长期知识维护不会混淆。

#### 验收标准

1. <a id="req-1-1"></a> 当 LazySpec 安装或加载完成时，系统必须提供可独立发现和调用的 `distill-spec-memory` Skill。
2. <a id="req-1-2"></a> 当用户要求把已经完成的 Feature Spec 沉淀为项目 Memory 时，系统必须将该请求交给 `distill-spec-memory` 处理。
3. <a id="req-1-3"></a> 当用户仅创建、修改或执行普通 Spec 工作时，系统不得自动触发 Memory 沉淀。

### 需求 2：执行 Feature 完成门槛

**用户故事：** 作为项目维护者，我希望只有真正完成并验证的 Feature 才能进入长期 Memory，以便未来 Agent 不会依赖未完成的计划。

#### 验收标准

1. <a id="req-2-1"></a> 当用户请求沉淀某个 Feature 时，系统必须确认目标 `specs/<feature-name>/` 中存在完整的 `requirements.md`、`design.md` 和 `tasks.md`。
2. <a id="req-2-2"></a> 当目标 Feature 存在未完成 Tasks 时，系统必须停止沉淀并指出未满足的完成条件，不得创建或更新正式 Memory。
3. <a id="req-2-3"></a> 当相关验证尚未通过或缺少可确认的验证结果时，系统必须停止沉淀并报告缺失证据。
4. <a id="req-2-4"></a> 即使 Tasks 与验证均已完成，系统也必须取得用户对“该 Feature 可以沉淀”的明确确认后才能继续。

### 需求 3：核对 Spec 与最终实现

**用户故事：** 作为未来使用 Memory 的 Agent，我希望沉淀结论同时反映已批准意图和最终实现，以便长期知识不会只记录计划或只记录偶然代码状态。

#### 验收标准

1. <a id="req-3-1"></a> 当 Feature 通过完成门槛后，系统必须读取其完整 Requirements、Design 和 Tasks，并核对与结论直接相关的代码及测试证据。
2. <a id="req-3-2"></a> 当 Spec 与代码或测试的可观察事实一致时，系统必须以二者共同支持的结论生成候选 Memory。
3. <a id="req-3-3"></a> 当 Spec 与代码或测试不一致时，系统必须明确展示差异并请求用户裁决，在裁决前不得写入正式 Memory。
4. <a id="req-3-4"></a> 当证据不足以确认某项候选结论时，系统不得把该结论作为已确认事实写入 Memory。

### 需求 4：写入前提供预览与审批

**用户故事：** 作为项目维护者，我希望在长期 Memory 落盘前审阅具体变化，以便避免低质量、重复或冲突知识进入项目事实源。

#### 验收标准

1. <a id="req-4-1"></a> 当候选 Memory 准备完成时，系统必须在会话中展示拟新增内容、拟修改状态、已发现冲突及其来源摘要。
2. <a id="req-4-2"></a> 当用户尚未明确批准预览时，系统不得创建或更新正式 Feature Capsule 与 `index.md`，也不得以 `draft` 文件代替审批。
3. <a id="req-4-3"></a> 当用户要求修改候选内容时，系统必须保持在预览阶段，更新候选结果后再次请求批准。
4. <a id="req-4-4"></a> 只有用户明确批准当前预览后，系统才能执行本次 Memory 写入并报告实际变更。

### 需求 5：生成精炼且可追溯的 Memory 产物

**用户故事：** 作为后续任务中的 Agent，我希望通过轻量索引定位精炼的 Feature Memory，以便用较少上下文恢复重要能力、决策和约束。

#### 验收标准

1. <a id="req-5-1"></a> 当首次批准 Memory 写入时，系统必须在目标项目根目录建立 `project-memory/index.md` 和 `project-memory/features/`，并将 Feature Capsule 写入 `project-memory/features/<feature-name>.md`。
2. <a id="req-5-2"></a> 每份 Feature Capsule 必须记录最终能力与边界、长期有效决策、Contracts 与 Invariants、非显然 Lessons、Reuse Triggers、当前状态以及来源。
3. <a id="req-5-3"></a> 每条长期结论必须能够追溯到对应 Spec、代码、测试或用户裁决；来源链接失效或缺失时，系统必须把该问题暴露给用户。
4. <a id="req-5-4"></a> `index.md` 必须以固定结构记录每份 Memory 的路径、简短说明、tags、状态和 source Spec，并且不得复制 Capsule 正文。
5. <a id="req-5-5"></a> MVP 不得复制完整 Spec、保存会话流水、创建 Topic 聚合层或生成 JSON 索引。

### 需求 6：管理 Memory 状态与不可变历史

**用户故事：** 作为项目维护者，我希望当前知识与过期历史被清楚区分，以便 Agent 不会误用旧结论，同时仍能追溯项目演化。

#### 验收标准

1. <a id="req-6-1"></a> 每份 Feature Capsule 和对应 index 项必须使用 `active`、`needs-review`、`superseded` 或 `obsolete` 之一表示当前状态，且两处状态必须保持一致。
2. <a id="req-6-2"></a> 当 Memory 疑似因实现漂移而过期但尚未确认时，系统必须将其标记为 `needs-review`，不得继续作为普通任务的有效事实。
3. <a id="req-6-3"></a> 当新 Capsule 明确替代旧 Capsule 时，系统必须把旧项标记为 `superseded`、记录替代项，并让新项记录 `supersedes` 关系。
4. <a id="req-6-4"></a> 当 Memory 已失效且没有替代项时，系统必须将其标记为 `obsolete`；所有非 `active` 项默认不得参与普通任务检索。
5. <a id="req-6-5"></a> Feature Capsule 获批后，系统不得原地改写其结论正文；只允许同步状态与替代关系，或在用户批准后修正错字和失效链接。

### 需求 7：在 LazySpec 中按需消费 Memory

**用户故事：** 作为 LazySpec 使用者，我希望后续阶段自动获得少量相关的当前 Memory，以便跨会话保持项目知识，同时避免全库内容占用上下文。

#### 验收标准

1. <a id="req-7-1"></a> 当 LazySpec 处理新请求且目标项目存在 `project-memory/index.md` 时，系统必须先读取 index，并依据当前请求筛选相关 `active` Memory。
2. <a id="req-7-2"></a> 在普通情况下，系统必须只向当前阶段提供一至三份最相关的 Feature Memory，不得默认加载全部 Memory 正文。
3. <a id="req-7-3"></a> 当用户明确要求追溯历史或复审状态时，系统可以读取相关的 `needs-review`、`superseded` 或 `obsolete` Memory，但必须同时说明其非当前有效状态。
4. <a id="req-7-4"></a> 当 index 不存在或没有相关 `active` Memory 时，系统必须继续执行原有 LazySpec 流程，不得把 Memory 缺失视为错误。
5. <a id="req-7-5"></a> Memory 的读取和沉淀不得绕过或改变 Brainstorming → Requirements → Design → Tasks 的阶段顺序、审批门及单任务执行约束。
