# LazySpec Codex Plan Mode 适配需求

## 引言

本功能让 LazySpec 在 Codex 原生 Plan Mode 中复用用户已批准的计划，直接替代新功能创建前的标准 Brainstorming，并在计划确认后继续进入 Requirements → Design → Tasks 三阶段；非 Codex 环境、Codex 普通模式以及既有 Spec 的默认行为保持不变。

## 需求

### 需求 1：在 Codex Plan Mode 中复用原生计划

**用户故事：** 作为 Codex 用户，我希望 LazySpec 能直接使用原生 Plan Mode 的计划，以便减少重复的 Brainstorming 交互并快速进入标准 Spec 流程。

#### 验收标准

1. <a id="req-1-1"></a>当目标功能尚不存在 `requirements.md` 且 Codex 运行时明确报告当前处于 Plan Mode 时，系统必须使用 Codex 原生计划作为 Brainstorming 输入，不得再启动标准 `brainstorming` 阶段。
2. <a id="req-1-2"></a>当用户明确批准 Codex 原生计划后，系统必须将工作路由到 Requirements 阶段。
3. <a id="req-1-3"></a>当 Codex 运行时明确报告当前未处于 Plan Mode 时，新功能创建必须继续遵循标准 Brainstorming 路由。

### 需求 2：保留完整的计划会话产物

**用户故事：** 作为 Requirements 编写者，我希望获得完整的原生计划内容，以便在不丢失上下文的情况下提炼可观察需求。

#### 验收标准

1. <a id="req-2-1"></a>当用户批准一个非空的 Codex 原生计划时，系统必须把计划的完整原文作为当前会话中的 Brainstorming 产物传递给 Requirements 阶段。
2. <a id="req-2-2"></a>当系统接收 Codex 原生计划时，不得要求固定字段结构、额外头部或五字段 `BrainstormingContext` 才能传递该计划。
3. <a id="req-2-3"></a>当 Requirements 阶段读取 Codex 原生计划时，计划原文必须保持与批准时一致，不得在适配过程中被摘要、改写或截断。
4. <a id="req-2-4"></a>当计划内容为空或不存在时，系统不得将其视为有效的 Brainstorming 产物。

### 需求 3：阻止未完成计划越过前置门

**用户故事：** 作为 LazySpec 使用者，我希望未完成或未批准的计划不会触发需求编写，以便保持 Spec 流程的可控性。

#### 验收标准

1. <a id="req-3-1"></a>当 Codex 已生成计划但用户尚未明确批准时，系统不得创建或更新 `requirements.md`。
2. <a id="req-3-2"></a>当系统无法确认当前运行时是否处于 Codex Plan Mode 时，系统必须停留在当前阶段并提示用户完成确认，不得自动把不确定的计划交给 Requirements。
3. <a id="req-3-3"></a>当计划为空、计划未获批准或模式状态未知时，系统必须向用户说明阻塞原因及可选的下一步，包括补全并批准计划或明确切换到标准 Brainstorming。
4. <a id="req-3-4"></a>当 Codex 计划被作为 Brainstorming 产物使用时，系统不得创建 `plan.md`、Brainstorming 文档或其他持久化中间产物。

### 需求 4：保持标准三阶段审批链

**用户故事：** 作为 Spec 审阅者，我希望 Codex 计划只替代 Brainstorming，而不改变后续阶段的审批，以便每份 Spec 文档仍然可以独立审阅。

#### 验收标准

1. <a id="req-4-1"></a>当已批准的 Codex 计划进入 Requirements 阶段后，系统必须继续生成并请求用户独立审批 `requirements.md`。
2. <a id="req-4-2"></a>当 `requirements.md` 尚未获得用户明确批准时，系统不得进入 Design 阶段。
3. <a id="req-4-3"></a>当 `design.md` 尚未获得用户明确批准时，系统不得进入 Tasks 阶段。
4. <a id="req-4-4"></a>当 Tasks 阶段完成审批时，系统必须结束规划流程，不得仅凭该审批自动开始实现任务。

### 需求 5：保持既有 Spec 与跨环境兼容性

**用户故事：** 作为 LazySpec 维护者，我希望 Codex 适配只影响明确适用的会话，以便现有用户和既有 Spec 不发生行为回归。

#### 验收标准

1. <a id="req-5-1"></a>当请求来自非 Codex 环境或 Codex 普通模式时，系统必须保留新功能创建前的标准 Brainstorming 行为。
2. <a id="req-5-2"></a>当目标功能已经存在 `requirements.md` 且用户未明确要求重新规划时，系统必须继续直接进入 Requirements 阶段。
3. <a id="req-5-3"></a>当用户在既有 Spec 中明确请求使用 Codex Plan Mode 重新规划时，系统可以更新当前会话中的 Brainstorming 产物，但不得因此自动修改既有 Spec 文件。
4. <a id="req-5-4"></a>当用户明确要求执行既有 Spec 的 `tasks.md` 时，系统必须先读取完整的三份 Spec，在新的特性分支上按依赖顺序完成全部未完成 TODO，并在每项完成后单独提交；执行过程中不得因单项完成而等待新的用户指令，且必须保留 `//TODO` 及其后的原任务文本。

### 需求 6：提供可验证的适配反馈

**用户故事：** 作为 LazySpec 维护者，我希望能够验证 Codex 适配的路由和失败分支，以便确认新增能力没有削弱原有流程。

#### 验收标准

1. <a id="req-6-1"></a>当运行 Codex Plan Mode 新建 Spec 的回归场景时，验证结果必须证明标准 Brainstorming 未被调用且 Requirements 已被正确接收。
2. <a id="req-6-2"></a>当运行未批准、空计划和未知模式的回归场景时，验证结果必须证明系统没有创建 Requirements。
3. <a id="req-6-3"></a>当运行非 Codex、Codex 普通模式和既有 Spec 的回归场景时，验证结果必须证明原有路由和审批行为保持不变。
4. <a id="req-6-4"></a>当运行完整的 Requirements → Design → Tasks 回归场景时，验证结果必须证明三个阶段的审批门和任务执行边界均未被跳过。
