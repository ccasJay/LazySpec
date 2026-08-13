# Agent Skills 无回归验证记录

验证日期：2026-08-13
兼容环境：Claude Code `2.1.229`、本机 `npx skills`

## 隔离方式

- 临时项目：`/private/tmp/lazyspec-agent-regression.hMVAei`
- 在临时项目中初始化独立 Git 仓库，仅执行项目作用域安装。
- 未使用 `-g`，未修改或覆盖用户的全局 Agent Skills。

## 已验证

1. `npx skills add /Users/sawyerlau/Project/LazySpec --list` 发现五个 Skill。
2. 以下命令成功安装五个 Skill：

   ```bash
   npx skills add /Users/sawyerlau/Project/LazySpec \
     --skill '*' --agent claude-code -y
   ```

3. `npx skills list -a claude-code --json` 返回五个 `scope: "project"` 项：
   `brainstorming`、`using-lazyspec`、`writing-requirement`、
   `writing-design`、`writing-task`。
4. 安装目录为临时项目的 `.claude/skills/`；三个写作 Skill 的 Prompt 和
   Template 均存在。逐目录 `diff -qr` 与本地仓库源目录一致。
5. 普通 `claude` 会话识别 `/using-lazyspec`。作为对照，`claude --bare`
   会话返回 `Unknown command`，因此 `--bare` 不用于该安装入口的回归验证。
6. 重新安装当前工作树后，从 `/using-lazyspec` 创建 `agent-e2e` Spec，完整经过
   Brainstorming Context、Requirements、Design 和 Tasks 四个独立审批门。
7. Tasks 批准后会话停止在规划结束处，未自动实施。单独查询任务 1 时未创建
   `bin/ping.sh` 且 checkbox 保持 `[ ]`。
8. 单独执行任务 1 时，Claude 先读取全部三份 Spec，仅创建并验证
   `bin/ping.sh`（输出 `pong`、退出码 0），随后只将 checkbox 改为 `[x]`，
   `//TODO` 及后续原文完整保留。

## 结果

现有 Agent Skills 入口的发现、资源解析、阶段顺序、逐阶段审批、任务查询与
单任务边界均通过隔离回归。回归只修改临时项目，未覆盖用户全局 Skills。
