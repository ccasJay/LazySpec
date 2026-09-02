# LazySpec Codex Plan Mode 适配实施计划

每项任务完成后必须保持代码与 Skill 文档处于可用状态；用户明确执行本任务清单时，默认在特性分支上按顺序完成全部未完成 TODO，并在每个 TODO 验证通过后单独提交；只有用户明确指定 TODO 编号时才限制为单项执行。始终保留 `//TODO` 及其后的任务文本。

- [x] //TODO 1. 实现 Codex Plan Mode 路由与会话契约

  - 修改 `using-lazyspec/SKILL.md`，仅在新功能、Codex 运行时明确处于 Plan Mode 且尚无 `requirements.md` 时跳过标准 `brainstorming`，并将下一阶段保持为 `requirements`。
  - 增加 `RuntimeMode`、`CodexPlanArtifact` 和 `BrainstormingInput` 的逻辑契约；只在非空计划获得用户明确批准后建立会话产物，并保留完整原文。
  - 增加针对 active、inactive 和未批准状态的聚焦契约验证。
  - _Requirements: [1.1](./requirements.md#req-1-1), [1.2](./requirements.md#req-1-2), [1.3](./requirements.md#req-1-3), [3.1](./requirements.md#req-3-1), [3.2](./requirements.md#req-3-2)_

- [x] //TODO 2. 接通 CodexPlanArtifact 到 Requirements 阶段

  - 修改 `writing-requirement/SKILL.md` 与 `requirement-prompt.md`，让 Requirements 同时接收标准 `BrainstormingContext` 和完整 Codex 计划。
  - 保证 Codex 计划不需要固定字段或额外头部，且原始 Markdown、换行和长文本在传递时不被摘要、改写或截断。
  - 保留 Requirements 自己的文档生成与独立审批行为，并增加原文保真度验证。
  - _Requirements: [2.1](./requirements.md#req-2-1), [2.2](./requirements.md#req-2-2), [2.3](./requirements.md#req-2-3), [2.4](./requirements.md#req-2-4), [4.1](./requirements.md#req-4-1)_

- [ ] //TODO 3. 实现阻塞、重规划与会话不落盘边界

  - 在 `using-lazyspec` 中补齐空计划、未批准计划和未知模式的阻塞反馈，说明原因及补全批准或明确切换标准 Brainstorming 的下一步。
  - 处理计划修改导致的批准失效，并确保适配过程不创建 `plan.md`、Brainstorming 文档或其他持久化中间产物。
  - 验证既有 Spec 显式重新规划只更新会话 Context，不自动修改已有 Spec 文件；默认既有 Requirements 路由保持不变。
  - _Requirements: [3.3](./requirements.md#req-3-3), [3.4](./requirements.md#req-3-4), [5.2](./requirements.md#req-5-2), [5.3](./requirements.md#req-5-3)_

- [ ] //TODO 4. 锁定标准三阶段与既有任务兼容性

  - 核对并按需调整 `using-lazyspec/SKILL.md`、`writing-requirement/SKILL.md` 和 `writing-task/SKILL.md`，确保 Requirements、Design、Tasks 的审批门继续独立生效。
  - 增加验证，确认 Tasks 审批只结束规划，不自动实施，并保留任务查询、完整 Spec 读取、逐 TODO 提交和 `//TODO` 文本规则。
  - 对 Codex 普通模式、非 Codex 环境和既有任务路径执行兼容性回归，确认标准 Brainstorming 与原有行为不变。
  - _Requirements: [4.2](./requirements.md#req-4-2), [4.3](./requirements.md#req-4-3), [4.4](./requirements.md#req-4-4), [5.1](./requirements.md#req-5-1), [5.4](./requirements.md#req-5-4)_

- [ ] //TODO 5. 增加 Codex Plan Mode 隔离工作流回归验证

  - 新增或扩展 Skill 契约测试，覆盖新建 Spec 的成功路由、原文传递、未批准/空计划/未知模式阻塞及无持久化产物。
  - 在隔离项目或会话场景中覆盖非 Codex、Codex 普通模式、既有 Spec 重新规划，以及 Requirements → Design → Tasks 的完整审批链。
  - 运行聚焦测试和完整测试套件，区分当前工作区 `distill-spec-memory/SKILL.md` 未提交修改造成的既有基线失败，不修改该无关文件。
  - _Requirements: [6.1](./requirements.md#req-6-1), [6.2](./requirements.md#req-6-2), [6.3](./requirements.md#req-6-3), [6.4](./requirements.md#req-6-4)_
