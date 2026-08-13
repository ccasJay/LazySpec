# Claude Code 适配需求文档

## 简介

本功能使 LazySpec 的五个 Skills 在保留现有 Agent Skills 安装与使用方式的同时，可作为原生 Claude Code Plugin 安装和运行，并以 Claude Code `2.1.229` 为兼容基线验证完整 Spec 工作流。

## 需求

### 需求 1：提供双平台安装入口

**用户故事：** 作为 LazySpec 使用者，我希望从同一仓库选择适合当前代理的安装方式，以便无需维护不同来源的 LazySpec。

#### 验收标准

1. <a id="req-1-1"></a>当用户采用现有 Agent Skills 安装方式时，安装流程必须继续提供 `using-lazyspec`、`brainstorming`、`writing-requirement`、`writing-design` 和 `writing-task` 五个 Skills。
2. <a id="req-1-2"></a>当用户采用 Claude Code Plugin 方式加载同一仓库时，Claude Code 必须发现并启用上述五个 Skills。
3. <a id="req-1-3"></a>当任一平台安装完成时，用户不得再手工复制或同步 Skill 正文才能使用 LazySpec。

### 需求 2：支持 Claude Code 原生调用

**用户故事：** 作为 Claude Code 用户，我希望通过其原生 Skill 机制调用 LazySpec，以便获得符合平台习惯的使用体验。

#### 验收标准

1. <a id="req-2-1"></a>当 Claude Code `2.1.229` 加载 LazySpec Plugin 时，Plugin 及五个 Skills 必须通过 Claude Code 的格式校验且不得产生加载错误。
2. <a id="req-2-2"></a>当用户查看 Claude Code 的可用 Skills 时，五个 Skills 必须以稳定的 `lazyspec` Plugin 命名空间显示。
3. <a id="req-2-3"></a>当用户调用任一写作 Skill 时，该 Skill 必须能够读取同目录的 Prompt、Template 及所需的上游 Spec 文件。
4. <a id="req-2-4"></a>当 `using-lazyspec` 路由到其他 LazySpec Skill 时，目标 Skill 必须能够在 Plugin 安装位置被正确解析和执行。

### 需求 3：保持跨平台审批门

**用户故事：** 作为 LazySpec 使用者，我希望每份 Spec 文档都经过明确审批，以便代理不会在我确认前进入下一阶段。

#### 验收标准

1. <a id="req-3-1"></a>当 Claude Code 更新 Requirements、Design 或 Tasks 后，对应 Skill 必须使用合法的 `AskUserQuestion` 调用请求用户审批，不得因无效输入字段导致工具调用失败。
2. <a id="req-3-2"></a>当其他受支持代理提供等效问答工具时，对应 Skill 必须使用该工具请求审批；没有适用工具时，必须直接在会话中请求明确审批。
3. <a id="req-3-3"></a>当用户提出修改意见或未明确批准文档时，系统必须修改当前阶段文档并再次请求审批。
4. <a id="req-3-4"></a>当用户未明确批准当前阶段文档时，系统不得从 Requirements 进入 Design、从 Design 进入 Tasks，或从 Tasks 自动开始实现。

### 需求 4：保持 LazySpec 阶段路由行为

**用户故事：** 作为跨平台使用者，我希望 LazySpec 在不同代理中执行相同的阶段流程，以便工作结果保持一致。

#### 验收标准

1. <a id="req-4-1"></a>当用户首次为某项功能创建 Requirements 时，系统必须先完成 Brainstorming，并在方案获得明确批准后才创建 `requirements.md`。
2. <a id="req-4-2"></a>当用户修改已有 `requirements.md` 且未明确要求 Brainstorming 时，系统必须直接进入 Requirements 阶段。
3. <a id="req-4-3"></a>当 Brainstorming 结果尚未获得明确批准或会话 Context 已丢失时，系统不得创建 Requirements。
4. <a id="req-4-4"></a>当系统判断阶段审批状态时，必须以当前会话中的明确回复为准，不得根据 Spec 文件是否存在推断审批完成。

### 需求 5：保持单任务执行边界

**用户故事：** 作为执行 Spec 任务的开发者，我希望代理一次只处理我指定的一项任务，以便每次变更都可独立审阅。

#### 验收标准

1. <a id="req-5-1"></a>当用户请求执行已有 Spec 任务时，系统必须先读取该功能的 `requirements.md`、`design.md` 和 `tasks.md`。
2. <a id="req-5-2"></a>当用户指定一项任务时，系统必须只完成该任务及其子任务，并在完成后停止。
3. <a id="req-5-3"></a>当完成带有 `//TODO` 的任务时，系统必须保留 `//TODO` 及其后的原任务文本，仅更新任务完成状态。
4. <a id="req-5-4"></a>当用户只询问任务信息而未要求实施时，系统必须只回答问题，不得修改代码。

### 需求 6：提供双平台使用文档

**用户故事：** 作为首次使用 LazySpec 的开发者，我希望文档分别说明两种安装和调用方式，以便能够正确完成配置与验证。

#### 验收标准

1. <a id="req-6-1"></a>当用户阅读项目文档时，文档必须分别提供现有 Agent Skills 与 Claude Code Plugin 的安装或加载步骤。
2. <a id="req-6-2"></a>当文档说明 Claude Code 用法时，必须列出兼容基线 `2.1.229`、五个命名空间调用名称及本地验证方式。
3. <a id="req-6-3"></a>当 Claude Code 未发现 Plugin 或 Skill 时，文档必须提供可执行的校验、重新加载和结构排查指引。

### 需求 7：验证完整工作流且不引入回归

**用户故事：** 作为 LazySpec 维护者，我希望通过双平台回归验证确认适配结果，以便发布后现有用户与 Claude Code 用户都能可靠使用。

#### 验收标准

1. <a id="req-7-1"></a>当在 Claude Code `2.1.229` 中执行兼容性验证时，五个 Skills 必须均可被发现并显式调用。
2. <a id="req-7-2"></a>当在隔离测试项目中运行新功能流程时，系统必须完成 Brainstorming、Requirements、Design 和 Tasks 的逐阶段审批，且不得跳过任一审批门。
3. <a id="req-7-3"></a>当验证已有 Spec 的修改、任务查询和任务执行时，系统必须保持既有路由与单任务边界。
4. <a id="req-7-4"></a>当使用现有 Agent Skills 安装与调用方式执行回归验证时，五个 Skills 的发现、路由、审批及任务行为必须继续有效。
