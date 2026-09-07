# LazySpec Skill 分层重构计划（policy 唯一事实源）

## 1. 概述

将 LazySpec Skill 集合从"规则多处复制"重构为四层分层模型，消除审批协议等核心规则的 5-6 处逐字重复：

```
policy   = 唯一事实源（references/）
skill    = 当前阶段算法
prompt   = 生成内容需要的最少指令
template = 输出形状
```

预期收益：Requirements 调用链 ≈49.3KB → ≈27KB（-45%）；approval 语义从 6 处变 1 处，消除"改一处忘五处"的静默分歧。

范围：三步全做（①抽 approval-policy ②瘦身 prompt/template ③router 拆分），测试同步重写为分层守护，并修正 5 个既有失败测试。

## 2. 现状（已核实）

| 文件 | 实际大小 |
|---|---|
| using-lazyspec/SKILL.md | 25,417 B |
| references/risk-policy.md | 6,156 B |
| references/delivery-loop.md | 9,057 B |
| brainstorming/SKILL.md | 8,348 B |
| writing-requirement/SKILL.md | 10,183 B |
| requirement-prompt.md | 5,500 B |
| requirement-templete.md | 2,010 B |
| writing-design/SKILL.md | 10,818 B |
| design-prompt.md | 3,261 B |
| design-templete.md | 1,786 B |
| writing-task/SKILL.md | 7,991 B |
| task-prompt.md | 446 B |
| task-templete.md | 1,595 B |
| fast/SKILL.md | 8,416 B |
| distill-spec-memory/SKILL.md | 11,266 B |

重复分布（已核实）：
- AskUserQuestion JSON 协议完整出现 **5 次**：router L231-239、writing-requirement L42-61、writing-design L37-56、writing-task L25-42、fast L57-59。
- "material change 使 approval 失效"出现 ≥6 处；"一屏摘要/放不下建议拆 Spec"出现 ≥5 处。
- requirement-prompt.md 15 条 instructions 中约 12 条与 SKILL.md/policy 重复；其 Output Format 与 requirement-templete.md 逐字重复。
- router 中 Memory Recall Routing（L81-107，~3.5KB）、Codex Plan Mode 适配（L111-138，~2.5KB）、Executing Instructions（L211-223，~3KB，与 delivery-loop.md 重叠）均为可下沉的大块。

测试现状：`python3 -m unittest discover -s tests` → **53 个测试，5 个失败**（skill 演进快于测试，测试断言是旧语义快照）：
1. `test_brainstorming_plain_language_contracts.test_approach_comparison_is_user_visible_and_decision_relevant`
2. `test_brainstorming_plain_language_contracts.test_questions_keep_three_options_plus_free_form_and_one_decision`
3. `test_codex_plan_mode_contracts.test_requirements_design_tasks_chain_keeps_approval_and_execution_boundaries`
4. `test_human_first_approval_contracts.test_router_defines_adaptive_review_and_revision_behavior`
5. `test_skill_contracts.test_downstream_approval_and_compatibility_boundaries`

## 3. 目标结构与尺寸预算

```
using-lazyspec/
├── SKILL.md                       25,417 → ~10,000（纯路由）
└── references/
    ├── risk-policy.md              6,156 → ~4,500（风险分级+验证深度+自治契约）
    ├── approval-policy.md           新增 ~4,000（审批语义唯一源）
    ├── delivery-loop.md             9,057 → ~10,500（吸收 router 执行指令）
    ├── memory-recall.md             新增 ~3,500（迁自 router）
    ├── codex-plan-mode.md           新增 ~2,500（迁自 router，保持中文）
    └── doc-policy.md               新增 ~1,200（迁自 router Minimum-Sufficient Documentation）
```

| 调用链 | 现值 | 目标 |
|---|---|---|
| Requirements 链 | ≈49.3KB | ≈27KB |
| Design 链 | ≈47.5KB | ≈27KB |

## 4. 变更明细

### 4.1 新增 `using-lazyspec/references/approval-policy.md`（唯一事实源）

从 6 处合并以下语义，保留最完整版本（如 material 定义保留 router L27 的完整 8 类枚举）：

1. **Explicit approval 语义**：只有明确肯定算批准；沉默、文件存在、超时、解释、模糊回答、请求修改都不算。
2. **Material vs non-material**：material = 可观察行为、范围与排除、公共接口或数据变更、兼容性、外部副作用、安全或隐私、失败与恢复行为、关键技术选择及其风险；non-material = 文件名、内部 helper、代码组织、测试布局等不改变 material 项的等价实现细化；不确定时按 material。
3. **失效语义**：material change 使相关 approval 及下游证据失效；non-material body-only refinement 不失效。
4. **审批时机**：从 risk-policy.md 的 "Approval timing" 节整体迁入（combined vs phase-by-phase、draft ≠ 批准、fast 例外：一个 plan approval + 持续执行、escalation 不制造阶段审批）。
5. **审批协议骨架**：AskUserQuestion payload 结构约束（唯一一份 JSON：`{"questions":[...]}`、header `Review`、两单选项 `Approve`/`Request changes`、`multiSelect: false`、字段集 question/header/options/multiSelect、option 字段 label/description）+ fallback 链（等效用户问题工具 → 直接对话提问并停下）。**question 文案与 option description 由各阶段 skill 自定义**，policy 只约束结构。
6. **审批摘要通用契约**：summary 是 user-facing approval contract、body 必须与之一致且有界、按认知复杂度自适应、完整一屏、覆盖全部 material 项、放不下先建议拆分 Spec、material revision 后替换完整摘要并在会话呈现 delta（增/改/删/风险变化）。
7. **旧版迁移**：不批量迁移已有 Spec；下次创建/修订时加 `审批摘要`。
8. 开头声明适用范围：所有审批门（Requirements/Design/Tasks、fast plan、Brainstorming context、Memory preview）。

### 4.2 新增其余三个 references

- **memory-recall.md**：router L81-107 原文迁移（英文），含 RelevantMemoryContext 接口、index 校验、排序选取、advisory 边界。
- **codex-plan-mode.md**：router L111-138 原文迁移（保持中文），含 RuntimeMode/CodexPlanArtifact 接口、fail-closed 规则、会话边界。
- **doc-policy.md**：router "Minimum-Sufficient Documentation" 节（L15-20）原文迁移。

### 4.3 修改 `references/risk-policy.md`

- 删除 "Approval timing" 节（整体迁入 approval-policy.md，内容合并不丢规则）。
- Classification 表保留（第 3 列"Normal planning approval"简化为指向 approval-policy 的 combined review 语义，等级本身留在此处）。
- 保留：Autonomy contract、Classification、Existing artifacts。
- 开头 "governs approval timing across all seven skills" 改为分工声明（风险与验证深度在此，审批语义见 approval-policy.md）。

### 4.4 修改 `references/delivery-loop.md`

吸收 router "Executing Instructions"（L211-223）中与执行算法相关的内容：
- 分支创建规则（`codex/<feature-name>` 默认分支名、不提交无关变更）。
- checkbox 语义（`[ ]` → `[x]`、保留 `//TODO` 后原文）——与现有内容合并去重。
- 批量执行语义（执行全部未勾选 TODO、不逐任务等待批准、指定编号时限定范围）——与现有 Execution strategy 合并。
- Memory 影响候选检查（handoff 时只查 index、不改状态）。

### 4.5 七个 SKILL.md 去重

通用改法：每个 skill 的 "Shared policies" 段按 Resource Loading 加载矩阵（见 4.6 节）声明本路由所需 references（相对路径解析规则不变）；删除各自复制的通用审批语义，保留阶段特有内容 + 指向 policy 的引用。

各文件保留的阶段算法（删除项为与 policy 重复的通用语义）：

| 文件 | 保留 | 删除 |
|---|---|---|
| using-lazyspec/SKILL.md | 路由协议、ACTIVE_PROJECT_ROOT、三个 Routing 小节（Distillation/Fast/触发指针）、Workflow Diagram、Task Questions、Resource Loading 加载矩阵（见 4.6） | Human-First Approval Contract 节（→approval-policy）、Brainstorming Conversation Contract 节（→brainstorming/SKILL.md 已有等价内容，迁移前逐条核对 8 条无信息丢失）、Memory Recall 全文（→memory-recall.md，留 3 行触发+指针）、Codex 适配全文（→codex-plan-mode.md，留路由决策行：何时直连 writing-requirement、何时 brainstorming、未知时停下）、Executing Instructions（→delivery-loop.md，留 1 行指针）、Minimum-Sufficient Documentation（→doc-policy.md）、Approval Protocol 节（→approval-policy，留 1 行指针） |
| writing-requirement/SKILL.md | 输入契约（BrainstormingContext/CodexPlanArtifact）、语言与 anchor 规则、摘要子节名（目标/范围/核心行为/风险与待确认）与位置、Content Boundaries/Size、Troubleshooting、approval question 文案一行 | Approval 节的 JSON payload 与三步 fallback、material/失效/delta/一屏等通用语义、Constraints 中重复行 |
| writing-design/SKILL.md | 同上模式（子节名：方案/关键决策表/风险与待确认）、Diagram Policy、Research Limitations、Design Complexity | 同上 |
| writing-task/SKILL.md | approval 对象定义（双摘要+一致性+完整计划）、链接格式与校验规则、Plan Shape and Size | JSON payload、通用失效语义 |
| fast/SKILL.md | Pre-conditions、Discussion、plan.md 结构、Execution、Handoff、fast 特有审批（一个 plan approval+持续执行、material plan change 重批） | 通用协议三步 fallback 与通用失效语义 |
| brainstorming/SKILL.md | Human-First Interaction、完整 Workflow、Session-Only Boundary、自身问题形态 | 通用"明确肯定才算批准"语义改为引用 policy（自身问题选项结构保留） |
| distill-spec-memory/SKILL.md | preview artifact 审批特有逻辑、全部 Memory 规则 | 通用 explicit-approval 语义改为引用 policy |

三个 writing skill 的 "Before starting, read..." 行增加 doc-policy.md。

### 4.6 router 新增 Resource Loading 加载矩阵（长期维护契约）

在 router 的 Shared policies 位置新增以下矩阵，替代现有散文式读取指令（"Before routing planning... also read delivery-loop.md" 一段），成为按路由加载资源的唯一契约：

```markdown
## Resource Loading

Load only resources required by the selected route.

| Route | Required resources |
|---|---|
| brainstorming | risk-policy, approval-policy |
| requirements | risk-policy, approval-policy, doc-policy |
| design | risk-policy, approval-policy, doc-policy |
| tasks | risk-policy, approval-policy, doc-policy, delivery-loop |
| execute | risk-policy, approval-policy, delivery-loop |
| fast | risk-policy, approval-policy, delivery-loop |
| memory-recall | memory-recall |
| memory-distill | approval-policy |
| codex-plan-adapter | codex-plan-mode |

Rules:
- Load the routed Skill after selecting the route.
- Load conditional resources only when their route or condition applies.
- Do not preload every reference at session start.
- A routed Skill may load its own prompt/template/resources.
```

说明：
- 矩阵落地在 **Step 3**（doc-policy/memory-recall/codex-plan-mode 均创建后才能写全表）；Step 1 期间 router 的 Shared policies 散文先临时加上 approval-policy。
- 矩阵行的含义：该路由激活时，router 或被路由 skill 必须已读对应 references；各 skill 自身的 "Shared policies" 段与矩阵保持一致（如 memory-distill 只读 approval-policy，不再读 risk-policy）。
- 矩阵是长期维护入口：后续新增 reference 时在此表加列/加行，配合 5.4 的守护测试防止漂移。

### 4.7 prompt / template 瘦身

| 文件 | 处理 |
|---|---|
| requirement-prompt.md（5.5KB→~1.3KB） | 删 instructions 1-7、12、15（与 policy/SKILL 重复）及 Output Format 模板正文（与 template 重复）；保留：EARS 中文表达（禁止字面 WHEN/THEN/SHALL）、需求结构（用户故事+编号验收标准）、anchor 格式 `req-<r>-<c>`、一句话输入说明 |
| requirement-templete.md（2.0KB→~1.5KB） | 删 Usage Guidelines 中审批语义/一屏/拆分/material 覆盖等重复行；保留形状：骨架、placeholder 说明、anchor 用法、中文输出 |
| design-prompt.md（3.3KB→~1.0KB） | 删与 SKILL.md 重复的摘要契约/失效/re-escalation；保留：最小可实施设计指令、条件章节选择、研究边界、Testing Strategy 定位 |
| design-templete.md（1.8KB→~1.4KB） | 删重复契约语义段；保留形状：摘要骨架、核心/条件章节清单 |
| task-prompt.md（446B→~400B） | 微调去重（本已很小，保留文件维持资源契约一致性） |
| task-templete.md | 不变（纯示例形状，无重复） |

### 4.8 不动的文件

- 各 SKILL.md 的 frontmatter `description`（常驻系统提示词，本就精简）。
- `specs/`（项目自身历史 Spec）、`docs/`、`brain.md`、`tests/fixtures/`。

## 5. 测试改写（tests/，六个文件）

### 5.1 分层守护原则

- 规则本体断言 → 指向唯一事实源文件（approval-policy.md / memory-recall.md / codex-plan-mode.md / delivery-loop.md）。
- skill 断言 → 只断言含指向对应 policy 的相对链接，且链接目标存在。
- payload 唯一性：`{"questions"` JSON payload 在整个仓库的 SKILL.md 层只出现在 approval-policy.md；各 skill 保留自己的 question 文案断言（如 writing-requirement 的"审批摘要是否准确覆盖…"）。

### 5.2 断言迁移映射

| 现断言位置 | 新位置 |
|---|---|
| ROUTER 上的 Human-First Approval Contract 断言（test_human_first_approval_contracts） | approval-policy.md |
| ROUTER/writing-* 上的 payload 结构断言（test_skill_contracts.test_approval_payloads_use_only_supported_fields） | approval-policy.md（恰好 1 个 payload；各 skill 断言为 0 个） |
| ROUTER 上的 Codex 断言（test_codex_plan_mode_contracts，30 条） | references/codex-plan-mode.md；router 保留路由行断言 |
| ROUTER 上的 Memory Recall 断言（test_memory_contracts 中钉 ROUTER 的部分） | references/memory-recall.md |
| ROUTER 上的执行断言（codex/<feature-name>、checkbox token 等，test_task_execution_contract_batches_todos_on_feature_branch） | delivery-loop.md |
| REQUIREMENT_PROMPT 上的重复语义断言 | approval-policy.md / writing-requirement SKILL.md |

### 5.3 既有 5 个失败的修正

原则：**语义冲突以现行 skill 文件为准**（skill 已演进为 combined-review、不强制三选项；测试是旧需求快照）：
- 失败 1、2（brainstorming 三选项格式）：按现行"只在 trade-off 重要时比较、选项数不强制"语义重写断言。
- 失败 3、5（旧 phase-gate 断言如 "MUST NOT proceed to the design document"）：按现行 combined-review 语义 + 新分层位置重写。
- 失败 4（旧失效文案）：断言目标改为 approval-policy.md 的现行文案。

### 5.4 新增守护断言

1. **单一源守护**：全仓库 SKILL.md 层 grep，`AskUserQuestion` JSON payload 只在 approval-policy.md 出现一次；"invalidates prior approval" 完整定义只在 approval-policy.md。
2. **引用完整性**：所有 SKILL.md 中 `](../...)` 相对链接的目标文件存在（`Path.resolve().exists()`），覆盖 approval-policy/memory-recall/codex-plan-mode/doc-policy/delivery-loop/risk-policy。
3. **保留既有断言**：路由表 fallback、ACTIVE_PROJECT_ROOT、language 等未受影响的断言原样保留。

## 6. 执行顺序与验证

按三步推进，每步结束跑 `python3 -m unittest discover -s tests`：

1. **Step 1**：新建 approval-policy.md → risk-policy.md 迁节 → 七个 SKILL.md 去重 → 同步改 test_human_first_approval_contracts.py、test_skill_contracts.py 相关断言 + 修正失败 1、2、4、5 中属本步的部分 → 跑测试。
2. **Step 2**：瘦身 6 个 prompt/template → 同步改 REQUIREMENT_PROMPT/DESIGN 相关断言 → 跑测试。
3. **Step 3**：router 拆出 memory-recall/codex-plan-mode/doc-policy + delivery-loop 吸收执行指令 → router 重组为纯路由并落地 Resource Loading 加载矩阵（4.6 节，替代散文式 Shared policies）→ 同步改 test_memory_contracts.py、test_codex_plan_mode_contracts.py、test_skill_contracts.py（ROUTER 断言迁移 + 新增矩阵守护断言）+ 修正失败 3 → 跑测试全绿。
4. **终检**：
   - `python3 -m unittest discover -s tests` 全绿（53 个测试，含改写与新增）。
   - `rg -c "AskUserQuestion" --glob '!tests/'` 确认 skill 层只剩 approval-policy.md 一处协议定义。
   - `wc -c` 复测尺寸预算表；Requirements 链合计 ≤ 30KB。
   - 抽查一条引用链：确认 writing-requirement 的 approval question 文案、子节名断言与 template 断言仍然成立。

不主动 commit（用户未要求）；如用户后续要求提交，按项目规则 `feat(模块): 功能描述` 格式。

## 7. 假设与决定

1. **policy 文件语言**：approval-policy/memory-recall/doc-policy 用英文（与 risk-policy/delivery-loop 一致）；codex-plan-mode.md 保持中文原文迁移（测试钉了中文字符串）。
2. **question 文案归属**：各阶段 approval question 文本与 option description 属于阶段算法，留在各 SKILL.md；policy 只约束 payload 结构。
3. **prompt/template 不合并**：维持用户四层模型，保留独立文件；只删除跨层重复内容。
4. **测试语义裁决**：5 个失败以现行 skill 语义为准修正，不回滚 skill。
5. **不迁移 specs/**：项目自身历史 Spec 与本次重构无关，不动。
6. **brainstorming 语义合并**：router 的 Brainstorming Conversation Contract 删除前逐条与 brainstorming/SKILL.md 的 Human-First Interaction 核对，如有独有规则则迁入后者，不允许丢失。

## 8. 风险与对策

| 风险 | 对策 |
|---|---|
| 迁移合并时丢规则 | 每次搬移为"剪切-粘贴+去重"，保留最完整版本；测试断言作为规则清单逐条迁移核对 |
| 测试字符串与新文件内容不一致 | 先改内容、后改断言、跑测试对齐；断言迁移逐条映射（5.2 表） |
| 直接调用（不经 router）时 skill 漏读 policy | 每个 skill 的 Shared policies 段保留硬性读取要求（含 approval-policy.md）；新增引用完整性测试守护 |
| router 拆分后路由行为变化 | 路由决策行（何时进 brainstorming/writing-requirement/停留）留在 router 本体；Codex/memory-recall 只迁"怎么做"，不迁"何时走" |
| material 定义在合并中被弱化 | approval-policy.md 采用 router L27 的完整 8 类枚举版本；单一源测试守护 |
