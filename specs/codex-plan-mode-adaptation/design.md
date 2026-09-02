# LazySpec Codex Plan Mode 适配设计

## Overview

本设计为 LazySpec 增加 Codex 原生 Plan Mode 输入适配。适配只替代新功能创建前的 Brainstorming，不新增 LazySpec 阶段；已批准计划仍须依次经过 Requirements、Design 和 Tasks 的独立审批。设计覆盖 [需求 1](./requirements.md#req-1-1)、[需求 2](./requirements.md#req-2-1)、[需求 3](./requirements.md#req-3-1)、[需求 4](./requirements.md#req-4-1)、[需求 5](./requirements.md#req-5-1) 和 [需求 6](./requirements.md#req-6-1)。

## Research Findings

- OpenAI 官方文档将 Plan Mode 描述为先收集上下文、提出澄清问题并形成计划，并说明可通过 `/plan` 或 `Shift`+`Tab` 切换。[Codex 最佳实践](https://learn.chatgpt.com/zh-Hans/guides/best-practices)
- 官方文档说明了用户可见的模式行为，但没有为 LazySpec Skill 承诺稳定的文件、环境变量或可调用 API 来读取模式。因此本设计只依赖 Codex 运行时向当前会话提供的模式标记；不自行发明或解析其他信号。若标记不可用，按未知模式处理。

## Architecture

Plan Mode 是路由输入来源，不作为独立的 `RouteDecision.stage`。`using-lazyspec` 仍把下一阶段报告为 `requirements`，并在 `reason` 中标明来源为 `codex-plan-mode`。

```text
Codex runtime mode marker
          |
          v
using-lazyspec
     |                         |
     | new feature +           | existing requirements.md
     | Codex Plan Mode         |
     v                         v
Codex Plan Mode session   writing-requirement
          |
 explicit user approval
          v
  CodexPlanArtifact
          |
          v
  writing-requirement
          |
          v
    writing-design
          |
          v
     writing-task
```

已知的非 Codex 环境或 Codex 普通模式从 `using-lazyspec` 进入现有 `brainstorming`，再连接到 `writing-requirement`；该兼容分支不改变原有阶段顺序。

## Key Design Decisions

### 1. 将适配放在统一路由层

`using-lazyspec` 负责读取 Spec 文件状态与运行时模式，并决定使用原生计划还是标准 `brainstorming`。不新增 `codex-plan-bridge` Skill，避免安装、发现、命名空间和跨 Skill 回退协议出现额外分支。该决策落实 [req-1-1](./requirements.md#req-1-1)、[req-1-3](./requirements.md#req-1-3) 和 [req-5-1](./requirements.md#req-5-1)。

路由顺序固定为：

1. `requirements.md` 已存在时，沿用现有默认路由，直接进入 `writing-requirement`。
2. `requirements.md` 不存在且运行时明确为 Codex + Plan Mode 时，等待已批准的原生计划并进入 `writing-requirement`。
3. `requirements.md` 不存在且运行时明确不是 Plan Mode 时，进入标准 `brainstorming`。
4. 运行时平台或模式为未知时，不自动选择任何一条分支；只有用户明确切换到标准 Brainstorming 后才进入该分支。

### 2. 以联合输入保持既有契约兼容

保留标准流程的五字段 `BrainstormingContext`，另增原生计划输入类型。两者都是会话内输入，不写入项目文件。适配层不要求计划具备固定章节、额外头部或五字段内容，落实 [req-2-1](./requirements.md#req-2-1) 和 [req-2-2](./requirements.md#req-2-2)。

### 3. 复用原生批准，不重复发起 Brainstorming 批准

只有用户在原生 Plan Mode 计划生成后明确批准，适配层才建立 `CodexPlanArtifact`。计划生成、模式切换、用户提出修改或沉默都不算批准。计划一旦被修改，先前批准立即失效，必须重新批准；这落实 [req-3-1](./requirements.md#req-3-1) 和 [req-3-3](./requirements.md#req-3-3)。

Requirements、Design、Tasks 仍分别请求自己的明确审批；原生计划批准不能代替任一后续审批，落实 [req-4-1](./requirements.md#req-4-1) 至 [req-4-4](./requirements.md#req-4-4)。

### 4. 只做最小结构校验并保持原文

适配层只校验计划来源为 `codex-plan-mode`、原文去除首尾空白后非空，以及会话中存在明确批准。它不解释正文语义，也不检查标题或字段。传给 Requirements 的 `content` 是批准时的完整计划原文，包括其原有 Markdown 包装；不得摘要、改写、截断或另存副本，落实 [req-2-3](./requirements.md#req-2-3) 和 [req-2-4](./requirements.md#req-2-4)。

### 5. 保持既有 Spec 的不落盘边界

在既有 Spec 中显式使用 Plan Mode 只更新当前会话输入，不自动修改已有 Requirements、Design 或 Tasks。适配过程不创建 `plan.md`、Brainstorming 文档或临时项目产物；任务查询、批量 TODO 实施和 `//TODO` 保留规则继续由现有路由负责，落实 [req-3-4](./requirements.md#req-3-4) 和 [req-5-2](./requirements.md#req-5-4)。

## Components and Interfaces

### `using-lazyspec`

- 读取当前会话的运行时模式标记和目标 Spec 文件状态。
- 在新功能的 Codex Plan Mode 分支中等待或承接 `CodexPlanArtifact`，然后以 `requirements` 为下一阶段路由结果。
- 在缺少批准计划、计划为空或模式未知时只报告阻塞原因和下一步，不调用 `writing-requirement`。
- 不复制 `brainstorming`、Requirements、Design 或 Tasks 的阶段正文。

### `writing-requirement`

- 接收标准 `BrainstormingContext` 或 `CodexPlanArtifact`。
- 对 `CodexPlanArtifact` 使用完整 `content` 作为上下文，仍只把可观察行为写入 `requirements.md`。
- 如果原始计划存在会实质影响需求的空缺，留在 Requirements 阶段进行针对性澄清，不回到适配层猜测，也不提前进入 Design。

### `brainstorming`

继续作为非 Codex、Codex 普通模式和用户明确切换后的标准入口。其逐问、方案比较、独立 Context 审批和不落盘规则不变。

## Data Models

运行时模式标记是当前会话提供的逻辑上下文，不序列化、不落盘：

```ts
interface RuntimeMode {
  readonly platform: "codex" | "non-codex" | "unknown";
  readonly planMode: "active" | "inactive" | "unknown";
}
```

输入契约如下；`BrainstormingContext` 保持现有定义不变：

```ts
interface CodexPlanArtifact {
  readonly source: "codex-plan-mode";
  readonly content: string;
  readonly approved: true;
}

type BrainstormingInput =
  | BrainstormingContext
  | CodexPlanArtifact;
```

`CodexPlanArtifact` 只在 `RuntimeMode.platform === "codex"` 且 `RuntimeMode.planMode === "active"` 时建立。`content.trim()` 为空、`approved` 不为 `true` 或来源不匹配时，输入无效。`RouteDecision.stage` 不增加 `codex-plan` 值。

## Data Flow

1. `using-lazyspec` 先检查 `requirements.md` 是否存在，再读取 `RuntimeMode`。
2. 新功能处于 Codex Plan Mode 时，当前会话继续完成原生计划；计划生成但尚未批准时不创建任何 Spec 文件。
3. 用户明确批准后，保存完整计划原文到会话内的 `CodexPlanArtifact`，不做语义转换。
4. `using-lazyspec` 将该输入传给 `writing-requirement`；Requirements 只生成可观察需求并请求自己的审批。
5. 需求批准后沿用 `writing-design`，设计批准后沿用 `writing-task`；Tasks 审批完成只结束规划，不自动执行任务。
6. 任何计划修改都会清除旧的 `CodexPlanArtifact` 和批准状态，回到当前 Plan Mode 继续确认。

## Error Handling

- **计划缺失或为空：** 提示需要先完成非空的原生计划，保持当前阶段，不创建 Requirements。
- **计划未批准：** 明确说明原生计划尚未获得用户批准，不把生成结果当作已批准输入。
- **模式未知：** 明确说明无法确认 Codex Plan Mode，提供“补充模式确认”或“明确切换到标准 Brainstorming”的下一步；不自动回退或兜底。
- **用户要求修改计划：** 使旧批准失效，修改完成后重新等待用户批准。
- **Requirements 信息不足：** 由 `writing-requirement` 在当前阶段提出针对性问题；在信息充分并完成 Requirements 审批前，不进入 Design。
- **既有 Spec 的显式重新规划：** 只更新会话 Context；除非用户另行请求修订，否则不写入已有 Spec。

## Testing Strategy

### 静态契约验证

- 在现有 Skill 契约测试中验证 `CodexPlanArtifact`、`BrainstormingInput`、运行时模式分支、原文传递、未知模式阻断和无 `plan.md` 边界。
- 验证 `writing-requirement/SKILL.md` 与 Prompt 同时支持标准 `BrainstormingContext` 和完整 Codex 计划，并保留现有 EARS、审批及任务约束。
- 验证没有新增 Skill 目录、Plugin 注册项或持久化计划文件，覆盖 [req-3-4](./requirements.md#req-3-4) 和 [req-5-4](./requirements.md#req-5-4)。

### 隔离工作流场景

| 场景 | 预期结果 | 需求覆盖 |
|---|---|---|
| 新功能、Codex + Plan Mode、非空计划且已批准 | 跳过标准 `brainstorming`，进入 Requirements | [req-1-1](./requirements.md#req-1-1)、[req-1-2](./requirements.md#req-1-2) |
| 计划为空、未批准或模式未知 | 不创建 Requirements，并报告原因 | [req-2-4](./requirements.md#req-2-4)、[req-3-1](./requirements.md#req-3-3) |
| 非 Codex 或 Codex 普通模式 | 继续标准 Brainstorming | [req-1-3](./requirements.md#req-1-3)、[req-5-1](./requirements.md#req-5-1) |
| 已有 `requirements.md`，未请求重新规划 | 直接进入 Requirements | [req-5-2](./requirements.md#req-5-2) |
| 已有 Spec，显式使用 Plan Mode 重新规划 | 只更新会话 Context，不自动改文件 | [req-5-3](./requirements.md#req-5-3) |
| 计划包含特殊 Markdown、长文本或换行 | Requirements 收到逐字一致的原文 | [req-2-1](./requirements.md#req-2-1)、[req-2-3](./requirements.md#req-2-3) |
| Requirements、Design、Tasks 分别批准或拒绝 | 各阶段独立停留或顺序推进，Tasks 批准不启动实现 | [req-4-1](./requirements.md#req-4-4) |
| 既有任务查询与批量 TODO 执行 | 保留三份 Spec 读取、逐 TODO 提交和 `//TODO` 文本规则 | [req-5-4](./requirements.md#req-5-4) |

### 验证边界

先运行新增的聚焦契约与隔离场景验证，再运行完整测试套件。当前工作区已有 `distill-spec-memory/SKILL.md` 未提交修改造成一项无关基线失败；实现和验证不得修改该文件，并应在结果中区分基线失败与本功能回归。
