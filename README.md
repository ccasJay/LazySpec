# LazySpec

一套面向编码代理的 Spec 驱动开发 Skills，将功能想法转化为可审阅的需求、设计和实施任务。

## 工作流程

```text
Brainstorming → Requirements → Design → Tasks → 按需执行单个任务
```

- Brainstorming 确认目标、范围、约束、成功标准和方案，仅保存在当前会话。
- Requirements、Design、Tasks 分别生成 `requirements.md`、`design.md`、`tasks.md`。
- 每个阶段都需要用户明确批准，未获批准不会进入下一阶段。

## 接入

```bash
npx skills add ccasJay/LazySpec --skill '*' -g
```

按提示选择目标代理。安装完成后，确认五个 Skill 均可发现；日常使用从
`using-lazyspec` 进入。

> [!NOTE]
> 不同代理的 Skill 扫描规则和问答工具不同。现有审批指令使用
> `AskUserQuestion`；若目标代理使用其他工具名称，需要先适配。

## 快速开始

以下是自然语言调用示例，请替换为所用代理支持的 Skill 调用方式：

```text
# 创建 Spec
使用 using-lazyspec 为“用户认证”创建一个 Spec。

# 修改已有需求
使用 using-lazyspec 修改 specs/user-authentication/requirements.md，新增账户锁定要求。

# 执行单个任务
使用 using-lazyspec 执行 specs/user-authentication/tasks.md 中的任务 2.1。
```

新功能会先进入 Brainstorming；修改已有 `requirements.md` 时默认直接进入
Requirements。执行任务前会读取该功能的全部 Spec，并且一次只执行一个任务。

## Spec 产物

产物保存在 `specs/<feature-name>/`：

| 文件 | 内容 |
|---|---|
| `requirements.md` | 用户故事和带稳定锚点的 EARS 验收标准 |
| `design.md` | 关键实现决策、测试策略及必要的技术章节 |
| `tasks.md` | 可增量执行的编码任务及需求链接 |

Brainstorming Context 不会落盘；若进入 Requirements 前会话丢失，需要重新确认。

### 默认精简策略

LazySpec 默认生成“最小充分文档”：Requirements 只记录可验证行为，Design 只记录影响实现的决策，Tasks 只记录编码动作和自动化验证。下游文档通过需求编号引用上游内容，不重复转述。

- Requirements 默认不超过 8 组、每组 2–5 条验收标准，总数尽量不超过 30 条。
- Design 默认约 100–180 行；架构、接口、数据模型、错误处理、调研结论和图表按需生成。
- Tasks 每项通常不超过 3 个说明点，只链接直接落实的验收标准。

以上均为软限制，不会截断必要信息。需要更多上下文时，可以明确要求展开某个相关章节。

## Skill 职责

| Skill | 职责 |
|---|---|
| [`using-lazyspec`](./using-lazyspec/SKILL.md) | 统一入口、阶段路由、审批门和任务执行 |
| [`brainstorming`](./brainstorming/SKILL.md) | 澄清目标、比较方案并生成会话 Context |
| [`writing-requirement`](./writing-requirement/SKILL.md) | 创建或修改 Requirements |
| [`writing-design`](./writing-design/SKILL.md) | 基于已批准需求创建设计 |
| [`writing-task`](./writing-task/SKILL.md) | 将已批准设计转为编码任务 |

## 约束

- 文件存在不代表已经批准；审批以当前会话中的明确回复为准。
- 手动运行 Brainstorming 不会自动修改已有 Spec。
- Tasks 获批只代表规划完成，实际编码需单独发起任务执行请求。
- `templete` 是项目现有文件名约定，请勿自行改名。

完整示例见 [`specs/lazyspec`](./specs/lazyspec/)。
