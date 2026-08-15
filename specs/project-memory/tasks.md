# 项目记忆体系实施计划

- [x] //TODO 1. 构建并注册完整的 `distill-spec-memory` Skill 与 Memory 格式契约

  - 使用 `skill-creator` 初始化 `distill-spec-memory/`，完成 `SKILL.md`、`agents/openai.yaml` 和 `references/memory-format.md`，实现固定 Capsule frontmatter、正文、`index.md` 表格、项目根相对路径及禁止 Topic、sessions、JSON 和 Spec 复制的边界
  - 更新 `.claude-plugin/plugin.json` 与 `using-lazyspec/SKILL.md` 的注册名称、路由和 sibling fallback，确保普通 Spec 请求不会误触发沉淀
  - 新增自动化合约测试并运行 Skill 校验，验证目录、frontmatter、UI 元数据、格式 reference、manifest 和双平台发现契约
  - _Requirements: [1.1](./requirements.md#req-1-1), [1.2](./requirements.md#req-1-2), [1.3](./requirements.md#req-1-3), [5.1](./requirements.md#req-5-1), [5.2](./requirements.md#req-5-2), [5.3](./requirements.md#req-5-3), [5.4](./requirements.md#req-5-4), [5.5](./requirements.md#req-5-5)_

- [x] //TODO 2. 实现 Feature 完成门槛与 Spec／实现证据核对

  - 在 `distill-spec-memory/SKILL.md` 中实现 `gate → reconcile → deduplicate`：完整读取三份 Spec，验证全部 Tasks、相关自动化检查和用户完成确认，任何门槛失败均不得产生正式或 draft 文件
  - 以会话内 Evidence Matrix 将候选结论关联到 Spec anchors、实现、测试和用户裁决；定向检查已有 index 与相关 Capsule，遇到冲突或证据不足时停止并报告
  - 增加通过、Spec 缺失、未完成 Tasks、验证缺失、未确认、证据冲突和无证据结论场景的自动化契约测试
  - _Requirements: [2.1](./requirements.md#req-2-1), [2.2](./requirements.md#req-2-2), [2.3](./requirements.md#req-2-3), [2.4](./requirements.md#req-2-4), [3.1](./requirements.md#req-3-1), [3.2](./requirements.md#req-3-2), [3.3](./requirements.md#req-3-3), [3.4](./requirements.md#req-3-4)_

- [x] //TODO 3. 实现写入审批、四状态演化与不可变 Capsule

  - 完成 `preview → approve → write → verify`：预览完整候选 Capsule、index 行、状态变化、冲突裁决和来源；未批准或要求修改时保持零正式写入
  - 将批准后的编辑作为一个逻辑写入集，同步 Capsule 与 index；实现 `active`、`needs-review`、`superseded`、`obsolete` 的状态不变量、替代关系和正文冻结边界，并准确报告部分失败
  - 使用 fixture 增加审批循环、禁止 draft、状态同步、双向替代、过期退出默认检索、正文不可变和维护性纠错的自动化回归测试
  - _Requirements: [4.1](./requirements.md#req-4-1), [4.2](./requirements.md#req-4-2), [4.3](./requirements.md#req-4-3), [4.4](./requirements.md#req-4-4), [6.1](./requirements.md#req-6-1), [6.2](./requirements.md#req-6-2), [6.3](./requirements.md#req-6-3), [6.4](./requirements.md#req-6-4), [6.5](./requirements.md#req-6-5)_

- [x] //TODO 4. 接入 LazySpec 按需检索并执行完整回归

  - 修改 `using-lazyspec/SKILL.md`：在阶段路由前读取 `project-memory/index.md`，依据请求从 index 选择最多三份相关 `active` Capsule，形成会话内 `RelevantMemoryContext` 并传入当前阶段
  - 实现无 index、无命中、超过三项、非 `active` 历史追溯、路径或状态损坏的处理，同时保持原 Brainstorming → Requirements → Design → Tasks 审批链和单任务边界
  - 运行新增 Memory 合约测试、现有 `tests/test_skill_contracts.py`、Skill 快速校验和 Plugin manifest 校验，确认所有验收标准与既有 LazySpec 行为通过回归
  - _Requirements: [7.1](./requirements.md#req-7-1), [7.2](./requirements.md#req-7-2), [7.3](./requirements.md#req-7-3), [7.4](./requirements.md#req-7-4), [7.5](./requirements.md#req-7-5)_
