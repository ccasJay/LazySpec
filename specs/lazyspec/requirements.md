# LazySpec 职责拆分需求文档

## 简介

本功能将现有 `/Users/sawyerlau/.agents/skills/spec/SKILL.md` 更名并拆分为 `LazySpec` Skill 集合，使 Brainstorming、需求、设计和任务编写职责分别由独立 Skill 承担，并由 `using-lazyspec` 负责核心路由。默认工作流调整为 Brainstorming → Requirements → Design → Tasks，首次创建 `requirements.md` 时必须先通过 Brainstorming 形成已确认的会话上下文，再据此编写需求。

除明确新增的 Brainstorming 阶段和对应路由外，本次变更是纯结构重组，不优化、不纠错、不翻译、不删减、不合并现有指令。为同时满足“改名”和 Skill 文件必须具有独立 YAML frontmatter 的约束，本需求将“原有内容不得修改”定义为：原 `SKILL.md` 的指令正文必须逐字迁移；仅允许新增各子 Skill 必需的 YAML frontmatter、文件加载说明和最小路由引用。若该解释不符合预期，应在进入设计阶段前修订。

## 需求

### 需求 1：建立 LazySpec 目录与 Skill 边界

**用户故事：** 作为 LazySpec 维护者，我希望把单体 `spec` Skill 拆分为职责明确的 Skill 集合，以便各阶段可以独立加载和维护。

#### 验收标准

1. <a id="req-1-1"></a>当执行正式拆分时，系统必须在原 Skill 所在父目录下建立名为 `LazySpec` 的集合目录。
2. <a id="req-1-2"></a>当目录建立完成时，系统必须生成以下结构，且不得增加本次拆分不需要的目录或文件：

   ```text
   LazySpec/
   ├── using-lazyspec/
   │   └── SKILL.md
   ├── brainstorming/
   │   └── SKILL.md
   ├── writing-requirement/
   │   ├── SKILL.md
   │   ├── requirement-prompt.md
   │   └── requirement-templete.md
   ├── writing-design/
   │   ├── SKILL.md
   │   ├── design-prompt.md
   │   └── design-templete.md
   └── writing-task/
       ├── SKILL.md
       ├── task-prompt.md
       └── task-templete.md
   ```
3. <a id="req-1-3"></a>当创建目标文件时，系统必须严格使用带 `.md` 扩展名的 `requirement-prompt.md`、`design-prompt.md`、`task-prompt.md`，并保留 `templete` 拼写，不得自行更正。
4. <a id="req-1-4"></a>`LazySpec` 必须作为集合名称；五个可执行 Skill 的标识必须分别与 `using-lazyspec`、`brainstorming`、`writing-requirement`、`writing-design`、`writing-task` 目录名一致。
5. <a id="req-1-5"></a>在本需求阶段，系统只能创建本需求文档，不得创建、移动、重命名或修改任何 Skill 文件。

### 需求 2：保证原始内容守恒

**用户故事：** 作为原 Skill 的作者，我希望拆分前后的原始指令完全一致，以便职责拆分不会悄然改变既有行为。

#### 验收标准

1. <a id="req-2-1"></a>当准备拆分时，系统必须将 `/Users/sawyerlau/.agents/skills/spec/SKILL.md` 作为唯一原始内容来源。
2. <a id="req-2-2"></a>当把原始指令迁移到目标文件时，系统必须逐字保留其措辞、大小写、标点、代码块、示例和相对顺序，不得改写、纠错、翻译、格式化或语义合并。
3. <a id="req-2-3"></a>当划分内容边界时，每个原始正文区块必须且只能归属一个目标文件，不得遗漏或重复原始正文。
4. <a id="req-2-4"></a>仅当目标 Skill 需要被识别或需要读取其拆分文件时，系统才可以新增 YAML frontmatter、文件加载说明和最小路由引用；新增内容不得改变被迁移原文的含义。
5. <a id="req-2-5"></a>原始 YAML frontmatter 不得作为多个新 Skill 的有效 frontmatter 重复使用；新 Skill 所需的名称与描述必须作为新增元数据处理，原始指令正文仍须保持不变。
6. <a id="req-2-6"></a>如果任何拆分方案必须改动原始正文才能工作，系统必须停止实施并向用户报告冲突，不得自行放宽“仅拆分”约束。
7. <a id="req-2-7"></a>迁移后的skill语言还是英文

### 需求 3：由 using-lazyspec 承担核心路由

**用户故事：** 作为 LazySpec 使用者，我希望从单一入口进入正确阶段，以便无需了解内部文件分布。

#### 验收标准

1. <a id="req-3-1"></a>当用户首次创建某个功能的 `requirements.md` 时，`using-lazyspec/SKILL.md` 必须先把工作路由到 `brainstorming`，待 Brainstorming 结果获得用户确认后再路由到 `writing-requirement`。
2. <a id="req-3-2"></a>当用户修改已存在的 `requirements.md` 时，核心路由默认必须直接路由到 `writing-requirement`；只有用户显式调用或要求 Brainstorming 时，才先路由到 `brainstorming`。
3. <a id="req-3-3"></a>当用户已批准需求并请求创建设计文档时，核心路由必须把工作路由到 `writing-design`。
4. <a id="req-3-4"></a>当用户已批准设计并请求创建任务清单时，核心路由必须把工作路由到 `writing-task`。
5. <a id="req-3-5"></a>当用户询问或执行既有 Spec 任务时，核心路由必须保留原 Skill 中对应的任务查询与单任务执行职责，因为目标结构未定义额外的执行 Skill。
6. <a id="req-3-6"></a>核心路由必须执行 Brainstorming → Requirements → Design → Tasks 的默认阶段顺序，并保留 Requirements、Design 与 Tasks 的既有审批门。
7. <a id="req-3-7"></a>核心路由不得复制四个阶段 Skill 已承接的阶段正文，只能保留原有全局规则、流程路由、任务执行规则及必要的新引用。

### 需求 4：拆分 writing-requirement 职责

**用户故事：** 作为需求编写者，我希望需求阶段拥有独立 Skill、Prompt 和模板，以便只加载生成 `requirements.md` 所需的上下文。

#### 验收标准

1. <a id="req-4-1"></a>当进入需求阶段时，`writing-requirement/SKILL.md` 必须承接原 Skill 中 Requirement Gathering 的阶段规则、约束、审批循环及相关故障处理内容。
2. <a id="req-4-2"></a>`writing-requirement/requirement-prompt.md` 必须承接原 Skill 中用于驱动需求生成的原始提示内容。
3. <a id="req-4-3"></a>`writing-requirement/requirement-templete.md` 必须承接原 Skill 中 Requirements Document 的原始示例模板。
4. <a id="req-4-4"></a>`writing-requirement` 必须继续生成 `specs/{feature_name}/requirements.md`，并保留原有 EARS、用户故事、验收标准和显式审批行为。
5. <a id="req-4-5"></a>当需求文档尚未获得用户明确批准时，`writing-requirement` 不得开始 Design 或 Tasks 阶段。
6. <a id="req-4-6"></a>`writing-requirement` 不得包含 Design、Tasks 或既有任务执行的阶段正文。
7. <a id="req-4-7"></a>当 `writing-requirement` 在 Brainstorming 后被调用时，必须以当前会话中已经获得用户确认的 Brainstorming 结果作为需求输入，不得脱离该上下文另行假设目标、约束或成功标准。

### 需求 5：拆分 writing-design 职责

**用户故事：** 作为设计编写者，我希望设计阶段拥有独立 Skill、Prompt 和模板，以便只加载生成 `design.md` 所需的上下文。

#### 验收标准

1. <a id="req-5-1"></a>当进入设计阶段时，`writing-design/SKILL.md` 必须承接原 Skill 中 Create Feature Design Document 的阶段规则、约束、审批循环及相关故障处理内容。
2. <a id="req-5-2"></a>`writing-design/design-prompt.md` 必须承接原 Skill 中用于驱动设计生成的原始提示内容。
3. <a id="req-5-3"></a>`writing-design/design-templete.md` 必须承接原 Skill 中设计文档必需章节的原始模板内容。
4. <a id="req-5-4"></a>`writing-design` 必须继续读取已批准的 `requirements.md` 并生成 `specs/{feature_name}/design.md`，保留原有研究、架构、组件、数据模型、错误处理和测试策略要求。
5. <a id="req-5-5"></a>当需求文档尚未获得明确批准时，`writing-design` 不得开始设计；当设计文档尚未获得明确批准时，不得开始 Tasks 阶段。
6. <a id="req-5-6"></a>`writing-design` 不得包含 Requirement Gathering、Create Task List 或既有任务执行的阶段正文。

### 需求 6：拆分 writing-task 职责

**用户故事：** 作为任务规划者，我希望任务阶段拥有独立 Skill、Prompt 和模板，以便只加载生成 `tasks.md` 所需的上下文。

#### 验收标准

1. <a id="req-6-1"></a>当进入任务阶段时，`writing-task/SKILL.md` 必须承接原 Skill 中 Create Task List 的阶段规则、约束、审批循环及任务规划相关内容。
2. <a id="req-6-2"></a>`writing-task/task-prompt.md` 必须承接原 Skill 中用于代码生成 LLM 制定实施计划的原始 Prompt。
3. <a id="req-6-3"></a>`writing-task/task-templete.md` 必须承接原 Skill 中 Implementation Plan 的原始示例模板。
4. <a id="req-6-4"></a>`writing-task` 必须继续读取已批准的 `requirements.md` 与 `design.md`，并生成 `specs/{feature_name}/tasks.md`。
5. <a id="req-6-5"></a>生成的任务清单必须继续保留原 Skill 定义的层级、复选框、需求引用、增量实施和测试驱动约束，不得借拆分机会修正原模板格式。
6. <a id="req-6-6"></a>当设计文档尚未获得明确批准时，`writing-task` 不得创建任务清单；任务清单完成后必须保留原有审批循环并停止继续实施。
7. <a id="req-6-7"></a>`writing-task` 不得包含 Requirement Gathering、Create Feature Design Document 或既有任务执行的阶段正文。

### 需求 7：保持行为一致并验证拆分结果

**用户故事：** 作为 LazySpec 维护者，我希望通过自动化与人工可读检查确认拆分结果，以便证明此次变更只有结构差异。

#### 验收标准

1. <a id="req-7-1"></a>当目标文件生成后，系统必须验证五个 `SKILL.md` 均具有合法且与目录一致的 Skill 名称和有效 YAML frontmatter。
2. <a id="req-7-2"></a>当完成内容分配后，系统必须生成或执行可重复的内容映射检查，以证明所有原始正文区块均被覆盖一次且未被修改。
3. <a id="req-7-3"></a>除本需求明确新增的 Brainstorming 阶段与路由行为外，当对比拆分前后行为时，Requirements、Design、Tasks、审批循环、任务查询与单任务执行的可观察规则必须保持一致。
4. <a id="req-7-4"></a>如果运行环境无法发现 `LazySpec` 下的嵌套 Skill，系统必须在设计阶段报告该兼容性问题，不得擅自改变用户指定的目录结构。
5. <a id="req-7-5"></a>在全部目标 Skill 验证通过前，系统不得删除、覆盖或移动原始 `spec` Skill。
6. <a id="req-7-6"></a>当本需求文档创建完成后，系统必须停止，不得自动创建设计文档或执行 Skill 拆分。


### 需求 8：新增会话内 Brainstorming 阶段

**用户故事：** 作为 LazySpec 使用者，我希望在首次编写需求前通过结构化 Brainstorming 明确目标、约束与方案，以便 `requirements.md` 建立在经过确认的上下文上。

#### 验收标准

1. <a id="req-8-1"></a>当设计 `brainstorming/SKILL.md` 时，系统必须参考 `/Users/sawyerlau/.codex/plugins/cache/openai-curated-remote/superpowers/6.2.0/skills/brainstorming/SKILL.md` 中的项目探索、逐问澄清、方案比较和用户确认流程。
2. <a id="req-8-2"></a>当首次创建某个功能的 `requirements.md` 且文件尚不存在时，`using-lazyspec` 必须自动调用 `brainstorming`；在 Brainstorming 完成前不得调用 `writing-requirement`。
3. <a id="req-8-3"></a>当 `requirements.md` 已存在时，修改需求默认不得自动重新运行 Brainstorming；只有用户手动调用 `brainstorming` 或明确要求重新 Brainstorming 时才执行该阶段。
4. <a id="req-8-4"></a>当 Brainstorming 开始时，`brainstorming` 必须先读取与当前功能直接相关的项目文件、文档和现有 Spec 上下文，再判断范围是否需要拆分。
5. <a id="req-8-5"></a>当需要澄清目标、约束或成功标准时，`brainstorming` 必须一次只向用户提出一个问题；如果当前环境提供适用的问答 Tool，则优先调用该 Tool，否则必须直接在会话中提问。
6. <a id="req-8-6"></a>当收集到足够上下文后，`brainstorming` 必须提出 2–3 个可行方案，说明各自权衡，并给出带理由的推荐方案。
7. <a id="req-8-7"></a>当方案提出后，`brainstorming` 必须等待用户明确选择或批准；用户未确认时不得进入 `writing-requirement`。
8. <a id="req-8-8"></a>Brainstorming 的结果必须仅保留在当前会话 Context 中，不得创建 Brainstorming 文档、设计文档、临时文件或其他持久化产物。
9. <a id="req-8-9"></a>传递给 `writing-requirement` 的会话 Context 必须至少包含已确认的目标、范围、约束、成功标准和选定方案；存在未决问题时不得开始编写需求。
10. <a id="req-8-10"></a>`brainstorming` 不得执行参考 Skill 中的设计文档落盘、Git Commit、调用 `writing-plans` 或进入实现阶段等终段行为。
11. <a id="req-8-11"></a>当用户在既有 Requirements、Design、Tasks 或任务执行阶段手动调用 `brainstorming` 时，其输出仍只能作为当前会话 Context；后续是否修改对应 Spec 文件必须由用户另行明确请求。
12. <a id="req-8-12"></a>如果 Brainstorming 结果在调用 `writing-requirement` 前因会话中断或 Context 丢失而不可用，则系统必须重新执行 Brainstorming，不得从磁盘伪造或恢复未保存的结果。
