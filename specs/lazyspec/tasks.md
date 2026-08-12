# LazySpec 职责拆分实施计划

原 `spec/SKILL.md` 是不可修改的迁移基线。每个任务完成后保留对应 `//TODO` 文本；在结构、格式、原文守恒、发现和工作流验证全部通过前，不得删除、覆盖或移动原 Skill。

- [x] //TODO 1. 新增会话内 Brainstorming Skill

  - 创建 `LazySpec/brainstorming/SKILL.md`，使用合法且与目录一致的英文 frontmatter。
  - 参考 `superpowers:brainstorming` 迁入项目探索、逐问澄清、2–3 个方案比较与用户确认流程，但排除文档落盘、Git Commit、`writing-plans` 和实现阶段。
  - 实现问答 Tool 优先、会话提问回退和 Context 不落盘边界。
  - 验证 Brainstorming 只生成包含目标、范围、约束、成功标准和选定方案的已批准会话 Context。
  - _需求：[1.1](requirements.md#req-1-1)、[1.2](requirements.md#req-1-2)、[1.4](requirements.md#req-1-4)、[8.1](requirements.md#req-8-1)、[8.4](requirements.md#req-8-4)、[8.5](requirements.md#req-8-5)、[8.6](requirements.md#req-8-6)、[8.7](requirements.md#req-8-7)、[8.8](requirements.md#req-8-8)、[8.9](requirements.md#req-8-9)、[8.10](requirements.md#req-8-10)、[8.11](requirements.md#req-8-11)、[8.12](requirements.md#req-8-12)_

- [x] //TODO 2. 拆分 writing-requirement 的 Skill、Prompt 与 Template

  - 在迁移前记录 `/Users/sawyerlau/.agents/skills/spec/SKILL.md` 的 SHA-256，并始终从该文件提取原始英文内容。
  - 创建 `LazySpec/writing-requirement/SKILL.md`、`requirement-prompt.md` 和 `requirement-templete.md`，按 Design 的 Source Content Allocation 逐字迁移对应区块。
  - 仅新增合法 frontmatter、读取 Prompt／Template 的最小指令，以及消费已批准 `BrainstormingContext` 的必要接口文字。
  - 验证 Requirements 的 EARS、用户故事、验收标准、审批循环和 Requirements Clarification Stalls 未被改写、遗漏或重复。
  - 对 `writing-requirement/SKILL.md` 运行 Skill 格式校验，并逐字节核对所有迁移区块。
  - _需求：[1.2](requirements.md#req-1-2)、[1.3](requirements.md#req-1-3)、[1.4](requirements.md#req-1-4)、[2.1](requirements.md#req-2-1)、[2.2](requirements.md#req-2-2)、[2.3](requirements.md#req-2-3)、[2.4](requirements.md#req-2-4)、[2.5](requirements.md#req-2-5)、[2.6](requirements.md#req-2-6)、[2.7](requirements.md#req-2-7)、[4.1](requirements.md#req-4-1)、[4.2](requirements.md#req-4-2)、[4.3](requirements.md#req-4-3)、[4.4](requirements.md#req-4-4)、[4.5](requirements.md#req-4-5)、[4.6](requirements.md#req-4-6)、[4.7](requirements.md#req-4-7)、[8.9](requirements.md#req-8-9)_

- [x] //TODO 3. 拆分 writing-design 的 Skill、Prompt 与 Template

  - 创建 `LazySpec/writing-design/SKILL.md`、`design-prompt.md` 和 `design-templete.md`，按 Source Content Allocation 从原 Skill 逐字迁移唯一归属区块。
  - 仅新增合法 frontmatter 和读取 Prompt／Template 的最小指令，不调整原研究、架构、组件、数据模型、错误处理、测试策略或审批要求。
  - 将 Research Limitations 与 Design Complexity 原文只放入 `writing-design/SKILL.md`，不得复制到其他 Skill。
  - 对 `writing-design/SKILL.md` 运行 Skill 格式校验，并逐字节核对所有迁移区块。
  - _需求：[1.2](requirements.md#req-1-2)、[1.3](requirements.md#req-1-3)、[1.4](requirements.md#req-1-4)、[2.1](requirements.md#req-2-1)、[2.2](requirements.md#req-2-2)、[2.3](requirements.md#req-2-3)、[2.4](requirements.md#req-2-4)、[2.5](requirements.md#req-2-5)、[2.6](requirements.md#req-2-6)、[2.7](requirements.md#req-2-7)、[5.1](requirements.md#req-5-1)、[5.2](requirements.md#req-5-2)、[5.3](requirements.md#req-5-3)、[5.4](requirements.md#req-5-4)、[5.5](requirements.md#req-5-5)、[5.6](requirements.md#req-5-6)_

- [x] //TODO 4. 拆分 writing-task 的 Skill、Prompt 与 Template

  - 创建 `LazySpec/writing-task/SKILL.md`、`task-prompt.md` 和 `task-templete.md`，按 Source Content Allocation 从原 Skill 逐字迁移唯一归属区块。
  - 将面向代码生成 LLM 的原始实施计划 Prompt 放入 `task-prompt.md`，将原 Implementation Plan 示例完整放入 `task-templete.md`。
  - 仅新增合法 frontmatter 和读取 Prompt／Template 的最小指令，不修正原模板的 `//TODO`、复选框、层级或缩进格式。
  - 对 `writing-task/SKILL.md` 运行 Skill 格式校验，并逐字节核对所有迁移区块。
  - _需求：[1.2](requirements.md#req-1-2)、[1.3](requirements.md#req-1-3)、[1.4](requirements.md#req-1-4)、[2.1](requirements.md#req-2-1)、[2.2](requirements.md#req-2-2)、[2.3](requirements.md#req-2-3)、[2.4](requirements.md#req-2-4)、[2.5](requirements.md#req-2-5)、[2.6](requirements.md#req-2-6)、[2.7](requirements.md#req-2-7)、[6.1](requirements.md#req-6-1)、[6.2](requirements.md#req-6-2)、[6.3](requirements.md#req-6-3)、[6.4](requirements.md#req-6-4)、[6.5](requirements.md#req-6-5)、[6.6](requirements.md#req-6-6)、[6.7](requirements.md#req-6-7)_

- [x] //TODO 5. 实现 using-lazyspec 核心路由并接通四个阶段 Skill

  - 创建 `LazySpec/using-lazyspec/SKILL.md`，迁入原 Skill 的 Goal、Rule、Workflow 总览、Workflow Diagram、Task Instructions、Task Questions 和 IMPORTANT EXECUTION INSTRUCTIONS。
  - 新增最小英文路由：首次创建 `requirements.md` 时执行 Brainstorming → Requirements；修改既有 Requirements 时默认跳过 Brainstorming；用户手动调用时允许重新 Brainstorming。
  - 接通 Requirements → Design → Tasks 的原审批门，并保留既有任务查询及一次只执行一个任务的行为。
  - 确保核心路由只引用阶段 Skill，不复制四个阶段 Skill 已承接的正文。
  - 对 `using-lazyspec/SKILL.md` 运行 Skill 格式校验，并验证五个 Skill 的 `name` 均与子目录一致。
  - _需求：[1.1](requirements.md#req-1-1)、[1.2](requirements.md#req-1-2)、[1.4](requirements.md#req-1-4)、[2.2](requirements.md#req-2-2)、[2.3](requirements.md#req-2-3)、[2.4](requirements.md#req-2-4)、[2.5](requirements.md#req-2-5)、[2.6](requirements.md#req-2-6)、[2.7](requirements.md#req-2-7)、[3.1](requirements.md#req-3-1)、[3.2](requirements.md#req-3-2)、[3.3](requirements.md#req-3-3)、[3.4](requirements.md#req-3-4)、[3.5](requirements.md#req-3-5)、[3.6](requirements.md#req-3-6)、[3.7](requirements.md#req-3-7)、[7.1](requirements.md#req-7-1)、[8.2](requirements.md#req-8-2)、[8.3](requirements.md#req-8-3)_

- [x] //TODO 6. 执行结构、格式与原文守恒自动化验证

  - 校验 `LazySpec` 的目录和文件集合与 Requirements 完全一致：五个 `SKILL.md`、三个 `*-prompt.md`、三个 `*-templete.md`，且无额外产物。
  - 对五个 Skill 分别运行 `quick_validate.py`，验证 frontmatter、名称、描述和英文正文。
  - 重新计算原 `spec/SKILL.md` 的 SHA-256，确认源文件自迁移前起未发生变化。
  - 按 Source Content Allocation 对每个原始连续区块与唯一目标执行逐字节比较，验证无遗漏、无重复、无改写。
  - 如果任一校验失败，只修正拆分文件并重新验证；不得通过修改原文、改变目录结构或增加非需求文件绕过失败。
  - _需求：[1.2](requirements.md#req-1-2)、[1.3](requirements.md#req-1-3)、[1.4](requirements.md#req-1-4)、[2.1](requirements.md#req-2-1)、[2.2](requirements.md#req-2-2)、[2.3](requirements.md#req-2-3)、[2.4](requirements.md#req-2-4)、[2.5](requirements.md#req-2-5)、[2.6](requirements.md#req-2-6)、[2.7](requirements.md#req-2-7)、[7.1](requirements.md#req-7-1)、[7.2](requirements.md#req-7-2)_

- [x] //TODO 7. 执行 Skill 发现与 LazySpec 工作流回归验证

  - 在可重新加载 Skill 的环境中验证五个 `LazySpec/*/SKILL.md` 均能被发现并显式调用；若嵌套发现失败，停止并报告，不移动目录或替换原 Skill。
  - 覆盖首次创建 Requirements、修改既有 Requirements、手动 Brainstorming、问答 Tool 回退、方案未批准和 Context 丢失场景。
  - 覆盖 Requirements、Design、Tasks 三个审批门，以及既有任务查询和一次只执行一个任务的场景。
  - 验证除新增 Brainstorming 路由外，原 Requirements、Design、Tasks 和任务执行行为保持一致。
  - 全部验证通过后仍保留原 `spec` Skill；删除、覆盖或移动旧目录必须等待用户另行明确授权。
  - _需求：[3.1](requirements.md#req-3-1)、[3.2](requirements.md#req-3-2)、[3.3](requirements.md#req-3-3)、[3.4](requirements.md#req-3-4)、[3.5](requirements.md#req-3-5)、[3.6](requirements.md#req-3-6)、[3.7](requirements.md#req-3-7)、[4.4](requirements.md#req-4-4)、[4.5](requirements.md#req-4-5)、[4.6](requirements.md#req-4-6)、[4.7](requirements.md#req-4-7)、[5.4](requirements.md#req-5-4)、[5.5](requirements.md#req-5-5)、[5.6](requirements.md#req-5-6)、[6.4](requirements.md#req-6-4)、[6.5](requirements.md#req-6-5)、[6.6](requirements.md#req-6-6)、[6.7](requirements.md#req-6-7)、[7.3](requirements.md#req-7-3)、[7.4](requirements.md#req-7-4)、[7.5](requirements.md#req-7-5)、[8.2](requirements.md#req-8-2)、[8.3](requirements.md#req-8-3)、[8.4](requirements.md#req-8-4)、[8.5](requirements.md#req-8-5)、[8.6](requirements.md#req-8-6)、[8.7](requirements.md#req-8-7)、[8.8](requirements.md#req-8-8)、[8.9](requirements.md#req-8-9)、[8.10](requirements.md#req-8-10)、[8.11](requirements.md#req-8-11)、[8.12](requirements.md#req-8-12)_
