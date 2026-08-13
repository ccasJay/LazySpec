# Claude Code Plugin 隔离回归记录

验证日期：2026-08-13
兼容环境：Claude Code `2.1.229`

## 静态与发现验证

1. `python3 -m json.tool .claude-plugin/plugin.json` 通过。
2. 五个 `skills` 目录、`SKILL.md` frontmatter 及三个写作 Skill 的 Prompt/Template
   均存在，注册树不含符号链接或正文副本。
3. `claude plugin validate .` 退出码为 0；仅提示设计中故意未设置的可选
   `version` 字段。
4. `claude --plugin-dir /Users/sawyerlau/Project/LazySpec plugin details lazyspec`
   显示 `Source=lazyspec@inline` 及全部五个 Skills。
5. 在禁用工具写入的隔离会话中，逐一显式调用
   `/lazyspec:brainstorming`、`/lazyspec:using-lazyspec`、
   `/lazyspec:writing-requirement`、`/lazyspec:writing-design` 和
   `/lazyspec:writing-task`，五者均返回对应的 `SKILL_OK:<name>` 标记。

## 隔离交互回归

- 临时项目：`/private/tmp/lazyspec-claude-e2e.ftZUGU`
- 入口：`claude --plugin-dir /Users/sawyerlau/Project/LazySpec`
- 调用：`/lazyspec:using-lazyspec`

1. 新建 `e2e-demo-3` 时，会话先选择技术方案，再独立请求完整
   Brainstorming Context 审批；方案选择未被当成上下文批准。
2. Requirements、Design 和 Tasks 分别使用合法的 `AskUserQuestion`
   单选请求审批，未出现 `metadata.source` 或工具输入错误。
3. 三份 Spec 均写入会话启动的临时项目，未写入 Plugin 仓库或缓存目录。
4. Tasks 批准后流程停止，未自动实施。任务查询未修改文件或 checkbox。
5. 修改已有 Requirements 时没有重新运行 Brainstorming；选择 `Request changes`
   后留在 Requirements，应用反馈后再次请求审批。
6. 执行任务 1 前读取全部 `requirements.md`、`design.md` 和 `tasks.md`，
   仅创建并验证 `greet.sh`（输出 `hello`、退出码 0），然后只将
   checkbox 改为 `[x]`，完整保留 `//TODO` 及其后原文。

## 回归中发现并修正的问题

1. 方案选择曾被误认为完整 Brainstorming Context 批准；现已强制两次独立
   问答并增加契约测试。
2. Spec 产物曾被解析到 Plugin 仓库；现已引入 `ACTIVE_PROJECT_ROOT`，明确以
   会话启动的用户项目目录为根，并通过上述隔离写入验证。

## 结果

Claude Code Plugin 的五 Skill 发现、资源解析、阶段顺序、审批与修改分支、
任务查询和单任务执行边界均通过隔离回归。
