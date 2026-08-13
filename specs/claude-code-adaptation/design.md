# Claude Code 适配设计文档

## Overview

本设计在仓库根目录增加 Claude Code Plugin Manifest，直接注册现有五个 Skill 目录。五份 `SKILL.md` 继续作为 Agent Skills 与 Claude Code Plugin 的共同正文，不创建副本或符号链接。共享指令中的审批和 Skill 路由改为平台感知逻辑，并通过隔离项目分别验证 Claude Code `2.1.229` 与现有 Agent Skills 工作流。

覆盖需求：[双平台安装](requirements.md#req-1-1)、[Claude Code 调用](requirements.md#req-2-1)、[审批门](requirements.md#req-3-1)、[阶段路由](requirements.md#req-4-1)、[单任务边界](requirements.md#req-5-1)、[文档](requirements.md#req-6-1)和[回归验证](requirements.md#req-7-1)。

## Research Findings

- Claude Code Plugin Manifest 的 `skills` 字段接受一个或多个相对目录；目录可以直接包含 `SKILL.md`，不要求迁移到默认 `skills/` 目录。[Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- Plugin Skills 自动使用 `<plugin-name>:<skill-name>` 命名空间；原 `name` frontmatter 可保持不变。[Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- `AskUserQuestion` 输入由 `questions` 数组构成，每个问题包含 `question`、`header`、`options` 和可选 `multiSelect`；官方输入定义不包含 `metadata.source`。[Hooks reference](https://code.claude.com/docs/en/hooks#askuserquestion)
- `npx skills` 支持从同一来源安装多个 Agent Skills，并以 `--list`、`--skill '*'` 和 `--agent` 验证发现与安装结果。[Skills CLI](https://github.com/vercel-labs/skills)

## Architecture

目标结构只新增 Manifest 与本 Spec 的后续产物：

```text
LazySpec/
├── .claude-plugin/
│   └── plugin.json
├── using-lazyspec/SKILL.md
├── brainstorming/SKILL.md
├── writing-requirement/
│   ├── SKILL.md
│   ├── requirement-prompt.md
│   └── requirement-templete.md
├── writing-design/
├── writing-task/
├── README.md
└── specs/
```

Agent Skills 安装器继续发现五个原目录。Claude Code 从 `.claude-plugin/plugin.json` 读取同一组目录，并在运行时为其添加 `lazyspec:` 命名空间。两条入口最终加载完全相同的 Skill 正文和配套资源。

## Key Design Decisions

### 1. Manifest 直接引用现有目录

`.claude-plugin/plugin.json` 使用以下最小结构：

```json
{
  "name": "lazyspec",
  "displayName": "LazySpec",
  "description": "Spec-driven development workflow from brainstorming through implementation tasks.",
  "author": {
    "name": "ccasJay"
  },
  "repository": "https://github.com/ccasJay/LazySpec",
  "skills": [
    "./using-lazyspec",
    "./brainstorming",
    "./writing-requirement",
    "./writing-design",
    "./writing-task"
  ]
}
```

不设置固定 `version`，避免仓库尚无发布版本机制时产生需要人工同步的版本字段。实施时以 `claude plugin validate .` 的实际结果为准；若普通校验要求额外元数据，只补充官方字段，不改变 Skill 布局。

### 2. 保持单一 Skill 正文

不新增 `skills/` 镜像目录，不复制 Prompt 或 Template，也不使用 symlink。这样 Agent Skills 安装、Plugin 加载与仓库维护都指向相同文件，直接满足 [req-1-3](requirements.md#req-1-3)。现有用户的五个 Skill 名称和目录不变。

三个写作 Skill 继续通过同目录相对路径读取 Prompt 和 Template。`using-lazyspec` 继续保留相对 `../<skill>/SKILL.md` 作为跨平台回退，因此 Plugin 被复制到缓存后仍能解析兄弟目录。

### 3. 使用跨平台审批协议

修改 `using-lazyspec` 与三个写作 Skill 中的平台专属审批文字，统一为以下决策顺序：

1. 环境提供 `AskUserQuestion` 时必须使用它，并只传入官方支持的字段。
2. 环境没有该工具但提供等效问答工具时，使用等效工具。
3. 没有适用工具时，直接在会话中提出审批问题并停止当前阶段。

Claude Code 的每次文档审批使用一个单选问题：

```text
question: <当前阶段的原审批问题>
header: Review
options:
  - Approve — 批准并允许路由到下一阶段
  - Request changes — 保留当前阶段并根据反馈修订
multiSelect: false
```

删除所有 `metadata.source` 要求。无论采用哪种问答方式，只有明确的批准回答才更新会话审批状态；超时、解释请求、修改请求或模糊回答都不得触发下一阶段。

`brainstorming` 已有“适用问答工具优先、无工具时会话提问”的平台中立规则，仅需在回归中确认，无需为 Claude Code 建立分支版本。

### 4. 路由使用逻辑 Skill 名称

`using-lazyspec` 中每个路由目标保留逻辑名称与相对路径：

| 逻辑名称 | Claude Code Plugin 调用名 | 相对回退路径 |
|---|---|---|
| `brainstorming` | `lazyspec:brainstorming` | `../brainstorming/SKILL.md` |
| `writing-requirement` | `lazyspec:writing-requirement` | `../writing-requirement/SKILL.md` |
| `writing-design` | `lazyspec:writing-design` | `../writing-design/SKILL.md` |
| `writing-task` | `lazyspec:writing-task` | `../writing-task/SKILL.md` |

路由时优先使用当前环境已注册的 Skill 调用机制；没有该机制时读取相对 `SKILL.md`。共享正文不得假定所有 Claude Code 安装都带 Plugin 命名空间，因为 `npx skills` 也可以把五个 Skills 作为无命名空间的个人 Skills 安装到 Claude Code。

### 5. 文档区分两条使用路径

README 保留现有 `npx skills add ccasJay/LazySpec --skill '*' -g`，新增 Claude Code `2.1.229` 章节：

- 使用 `claude plugin validate .` 校验已克隆仓库。
- 使用 `claude --plugin-dir /path/to/LazySpec` 加载本地 Plugin。
- 列出 `/lazyspec:using-lazyspec` 等五个完整调用名，并以统一入口作为日常推荐。
- 提供 `/help`、`/reload-plugins`、目录位置与 Manifest 校验排障步骤。
- 提醒 Claude Code 用户在同一会话选择 Plugin 或普通 Agent Skills 入口之一，避免重复的自动触发候选。

## Error Handling

- Manifest 校验失败：根据 `claude plugin validate .` 的具体错误修正合法字段或相对路径，不迁移或复制五个 Skill 目录。
- Skill 未发现：依次检查 Claude Code 版本、Manifest 路径、五个目标目录、`SKILL.md` frontmatter，并重新加载 Plugin。
- 审批工具调用失败：先确认调用是否仍包含非官方字段；不得绕过审批门继续执行。
- 原平台回归失败：只修正共享兼容指令；不得以 Claude Code 专用副本掩盖行为差异。
- 测试产生 Spec 文件：所有端到端产物只写入明确创建的隔离临时项目，不写入仓库现有 `specs/`。

## Testing Strategy

### 1. 静态与格式验证

- 解析 `plugin.json`，确认五个 `skills` 路径均存在且各自包含合法 `SKILL.md`。
- 运行 `claude plugin validate .`，要求退出码为 0 且无加载错误。
- 搜索全部共享 Skill，确认不再要求 `metadata.source`，且三个文档阶段都包含跨平台审批回退。
- 运行 `npx skills add . --list`，确认仍发现五个原 Skill 名称。

### 2. Claude Code 发现验证

- 在隔离临时项目中以 `claude --plugin-dir <LazySpec绝对路径>` 启动 Claude Code `2.1.229`。
- 通过 `/help` 或 Plugin 详情确认五个 `lazyspec:` Skills，并逐一显式调用以确认支持资源与兄弟 Skill 可解析。

### 3. Claude Code 工作流回归

- 新功能场景：从 `lazyspec:using-lazyspec` 进入，验证 Brainstorming → Requirements → Design → Tasks 顺序，并分别测试批准与修改分支。
- 已有 Requirements 场景：确认默认跳过 Brainstorming；手动请求 Brainstorming 时只更新会话 Context。
- 任务场景：分别验证任务查询不改代码、执行前读取三份 Spec、只完成一个任务，以及 `//TODO` 文本保持不变。
- 保留交互记录或最终文件状态作为检查证据；任何审批门被跳过都视为失败。

### 4. Agent Skills 无回归验证

- 在另一个隔离项目中从本地仓库安装全部五个 Agent Skills，避免覆盖用户的全局安装。
- 重复最小的新功能路由、文档审批和单任务边界场景。
- 对比两种入口的阶段顺序与停止条件；平台只允许在调用名称和问答 UI 上存在差异。
