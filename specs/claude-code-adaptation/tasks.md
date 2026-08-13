# Claude Code 适配实施计划

- [x] //TODO 1. 添加 Claude Code Plugin Manifest

  - 创建 `.claude-plugin/plugin.json`，以 `lazyspec` 命名空间直接注册现有五个 Skill 目录，不复制正文或引入符号链接
  - 运行 JSON 解析与 `claude plugin validate .`，确认 Plugin、路径和五个 Skill frontmatter 均可加载
  - _Requirements: [1.2](./requirements.md#req-1-2), [1.3](./requirements.md#req-1-3), [2.1](./requirements.md#req-2-1), [2.2](./requirements.md#req-2-2)_

- [x] //TODO 2. 实现跨平台 Skill 路由与资源解析

  - 修改 `using-lazyspec/SKILL.md`，优先调用当前环境已注册的逻辑 Skill，并保留兄弟 `SKILL.md` 相对路径回退及既有阶段顺序
  - 校验三个写作 Skill 在 Plugin 缓存与普通 Agent Skills 安装位置都能读取同目录 Prompt、Template 和上游 Spec
  - _Requirements: [2.3](./requirements.md#req-2-3), [2.4](./requirements.md#req-2-4), [4.1](./requirements.md#req-4-1), [4.2](./requirements.md#req-4-2), [4.3](./requirements.md#req-4-3)_

- [x] //TODO 3. 实现跨平台文档审批协议

  - 修改 `using-lazyspec` 与三个写作 Skill：Claude Code 使用合法 `AskUserQuestion` 输入，其他环境使用等效工具或会话回退，并删除全部 `metadata.source` 要求
  - 保留修改后重新审批、只接受明确批准和不得从文件存在推断审批状态的规则
  - _Requirements: [3.1](./requirements.md#req-3-1), [3.2](./requirements.md#req-3-2), [3.3](./requirements.md#req-3-3), [3.4](./requirements.md#req-3-4), [4.4](./requirements.md#req-4-4)_

- [x] //TODO 4. 补齐单任务执行边界的回归保护

  - 核对并按需调整 `using-lazyspec/SKILL.md` 与 `writing-task/SKILL.md`，确保执行前读取三份 Spec、一次只处理一项任务且查询不触发实施
  - 增加自动化断言，确认任务完成只更新 checkbox，始终保留 `//TODO` 及其后的原任务文本
  - _Requirements: [5.1](./requirements.md#req-5-1), [5.2](./requirements.md#req-5-2), [5.3](./requirements.md#req-5-3), [5.4](./requirements.md#req-5-4)_

- [x] //TODO 5. 更新双平台安装与排障文档

  - 更新 `README.md`，保留现有 Agent Skills 安装入口，并补充 Claude Code `2.1.229` 的 Plugin 校验、加载和五个命名空间调用示例
  - 增加 `/help`、`/reload-plugins`、Manifest 路径和重复入口的排障说明，并验证文档命令与实际 CLI 一致
  - _Requirements: [1.1](./requirements.md#req-1-1), [6.1](./requirements.md#req-6-1), [6.2](./requirements.md#req-6-2), [6.3](./requirements.md#req-6-3)_

- [x] //TODO 6. 执行 Claude Code 隔离工作流回归

  - 在临时项目中通过 `claude --plugin-dir` 加载本仓库，自动验证五个 `lazyspec:` Skills 的发现、显式调用及支持资源解析
  - 使用隔离会话和结构化审批回答覆盖新建 Spec、修改分支、审批门、任务查询与单任务执行，并断言阶段产物及停止位置
  - _Requirements: [7.1](./requirements.md#req-7-1), [7.2](./requirements.md#req-7-2), [7.3](./requirements.md#req-7-3)_

- [x] //TODO 7. 执行现有 Agent Skills 无回归验证

  - 在另一个临时项目中从本地仓库安装五个 Skills，验证发现结果且不覆盖用户的全局安装
  - 运行最小的新建 Spec、逐阶段审批和单任务场景，对比 Claude Code Plugin 的阶段顺序与停止条件
  - _Requirements: [7.4](./requirements.md#req-7-4)_
