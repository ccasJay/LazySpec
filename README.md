# LazySpec

一套面向编码代理的 Spec 驱动开发 Skills，以二元架构将功能想法转化为高密度、可审阅、可执行、可验证的交付闭环，并实现自动化交付收口与三权分立的项目经验治理。

## 工作流程

```text
v2 二元链路：/grill-me 决策探针 → spec.md 审批 → plan.md (TDD) 审批 → 连续执行 → 自动交付收口
生命周期演进：proposed (立项提议) → delivered (交付生效) → archived (成熟封存) → superseded (显式废黜) / obsolete (负向警示护栏)
经验治理流：distill-feature (特性契约) / distill-learning (随时踩坑提炼) / maintain-memory (治理与索引自愈)
fast 链路：讨论 → plan.md → 一次审批 → 连续执行 → 功能验收
```

- **Spec 制定 (`writing-spec`)**：通过 `/grill-me` 风格结构化决策探针，针对业务目标、范围、架构边界与关键技术分歧快速收敛，一次性生成 `specs/<feature-name>/spec.md`（包含业务目标、EARS 验收标准、架构决策、强制的“曾考虑的备选方案”与否定性保证）。
- **Plan 制定 (`writing-plan`)**：基于已批准的 `spec.md` 生成 `specs/<feature-name>/plan.md`，按完整行为单元（Behavioral Unit）拆解任务，内置测试先行（TDD）验证入口与 `## Feature Verification` 端到端集成检查。
- **自动交付收口 (`executing-plan`)**：连续执行并运行 Feature Verification，验收通过后自动将 `spec.md` 状态置为 `delivered`，原位清洗计划假设语态为现态事实决策；若声明废黜关系，自动双向回写旧 Spec 的 `superseded` 状态与重定向警示。
- **负向警示护栏**：对于证伪或废弃的规范（`obsolete`），移入 `specs/retired/` 并打上 `[!CAUTION]`，在立项时主动探测拦截，坚决防止未来 Agent 重蹈覆辙。
- **记忆三权分立**：
  - `distill-feature`：提炼交付特性的系统能力契约（Feature Capsule）。
  - `distill-learning`：随时提炼工程教训、修复经验与负向护栏（Learning Capsule）。
  - `maintain-memory`：负责归档、废黜维护、失效清理与索引自愈。

## 安装与接入

### Agent Skills

```bash
npx skills add ccasJay/LazySpec --skill '*' -g
```

安装完成后，日常统一从 `using-lazyspec` 进入。

### Claude Code Plugin

兼容性基线为 Claude Code `2.1.229`。克隆本仓库后，在仓库根目录校验 `.claude-plugin/plugin.json`，再以仓库绝对路径加载本地 Plugin：

```bash
claude --version
claude plugin validate .
claude --plugin-dir /absolute/path/to/LazySpec
```

进入 Claude Code 后可用 `/help` 查看已加载命令；日常推荐使用统一入口：

```text
/lazyspec:using-lazyspec
```

核心技能列表（9 个精简专属技能）：

```text
/lazyspec:using-lazyspec     # 统一入口路由与生命周期护栏检查
/lazyspec:writing-spec       # 制定规范 (需求 + 架构决策 + 备选方案)
/lazyspec:writing-plan       # 制定计划 (TDD 行为任务与验收标准)
/lazyspec:executing-plan     # 连续执行任务并自动交付收口
/lazyspec:distill-feature    # 特性记忆沉淀 (Feature Capsule)
/lazyspec:distill-learning   # 随时提炼工程经验教训 (Learning Capsule)
/lazyspec:maintain-memory    # 规范全生命周期治理与记忆库自愈
/lazyspec:fast               # 单文件轻量快速通道
/lazyspec:orchestrating-specs# 多 Spec 联合执行编排
```

## 快速开始

```text
# 创建 Spec
使用 using-lazyspec 为“用户认证”创建一个 Spec。

# 制定执行计划
使用 using-lazyspec 为 specs/user-authentication/ 制定执行计划。

# 执行计划并完成交付
使用 using-lazyspec 执行 specs/user-authentication/plan.md 中的全部任务。

# fast 模式创建轻量新功能
使用 using-lazyspec 以 fast 模式为“导出 CSV”创建 plan 并执行。

# 沉淀特性记忆或踩坑经验
使用 distill-feature 沉淀已交付的 specs/user-authentication/。
使用 distill-learning 沉淀本次排查连接泄漏的工程教训。
```

## 产物与结构

产物保存在 `specs/<feature-name>/`：

| 文件 | 内容与职责 |
|---|---|
| `spec.md` | YAML 元数据（生命周期状态）、业务目标与范围、EARS 验收标准、架构核心决策、曾考虑的备选方案、风险与否定性保证 |
| `plan.md` | 行为单元编码任务（TDD 测试先行）、Feature Verification 端到端检查与运行结果、可选的 Learning Candidates |

### 生命周期状态机

`spec.md` 包含标准化的状态机元数据：

- `proposed`：立项草案，处于决策探针或评审中。
- `delivered`：验证通过并已合入主干的现态系统能力事实。
- `archived`：成熟稳定的基石规范，归档至 `specs/archived/`。
- `superseded`：被新规范推翻废黜，保留双向链接与警示重定向。
- `obsolete`：证伪废弃的负向警示护栏，归档至 `specs/retired/`，永久阻止未来 Agent 重复犯错。

## Skill 职责一览

| Skill | 职责说明 |
|---|---|
| [`using-lazyspec`](./using-lazyspec/SKILL.md) | 统一路由门面、负向警示护栏探测、阶段流转控制 |
| [`writing-spec`](./writing-spec/SKILL.md) | /grill-me 结构化决策探针，生成合并版 `spec.md` |
| [`writing-plan`](./writing-plan/SKILL.md) | 拆解行为单元任务（测试先行），生成 `plan.md` |
| [`executing-plan`](./executing-plan/SKILL.md) | 连续执行、端到端功能验收、自动原位转正与废黜指针同步 |
| [`distill-feature`](./distill-feature/SKILL.md) | 沉淀已交付特性的系统能力契约 (Feature Capsule) |
| [`distill-learning`](./distill-learning/SKILL.md) | 随时沉淀经验教训与负向护栏 (Learning Capsule) |
| [`maintain-memory`](./maintain-memory/SKILL.md) | 生命周期演进、归档治理、废黜维护与索引自愈 |
| [`fast`](./fast/SKILL.md) | 单文件极简通道，轻量讨论并一次性执行 plan.md |
| [`orchestrating-specs`](./orchestrating-specs/SKILL.md) | 多 Spec 依赖编排、堆叠分支与跨 Spec 集成验证 |
