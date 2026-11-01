# LazySpec

> 面向 AI Coding Agent 的极简单文件规范驱动开发（Spec-Driven Development）。  
> 告别脱缰乱写、只写不测与文档过时；以最小完备契约构建高密度交付闭环与长期工程记忆。

---

## 💡 为什么需要 LazySpec？

| 痛点 | 传统 Agent 编码 | LazySpec 的解法 |
|---|---|---|
| **指令模糊脱缰** | 给一句话需求就乱写，脑补过多 | **结构化决策探针**：主动抛出关键分歧与备选方案，先收敛再动工 |
| **文档写完即过时** | 繁琐的 PRD 维护成本极高，代码改完文档脱节 | **单文件最小契约**：仅需一份 `spec.md`，验收后删除任务清单并压缩执行记录为事实 |
| **只写代码不验证** | 声称“已完成”，一跑全是 Bug | **两级验证门禁**：逐 TODO 轻量基本检查，收尾全量 `Feature Verification` 验收 |
| **多会话反复踩坑** | 新会话 Agent 毫无记忆，重蹈覆辙 | **特性记忆与负向护栏**：沉淀已交付能力与决策，立项前检查废弃方案 |

---

## 🔄 核心工作流

```mermaid
flowchart LR
    A["💡 需求想法"] --> B["1. writing-spec<br/>(决策探针 + 验收与任务拆解)"]
    B -->|审批 spec.md| C["2. executing-plan<br/>(逐 TODO 基本检查 + 收尾全量测试)"]
    C -->|用户审核并批准合并| D["3. 自动交付收口<br/>(合并 + 删除任务 + 状态同步)"]
```

- **标准通道 (Standard)**：`spec.md` (定义意图、边界、用户故事、验收与任务) ➔ 一次审批 ➔ 连续执行与验收 ➔ 用户审核并批准合并 ➔ 自动交付收尾。Memory 沉淀另走预览审批流程。
- **多 Spec 编排 (Orchestration)**：通过 `orchestrating-specs` 联合处理多 Spec 就绪调度，默认优先并行实施、按真实依赖等待，并统一集成验证和合并。

---

## 📂 项目资产结构

LazySpec 在项目根目录下规范化管理两类资产：

```text
your-project/
├── specs/                          # 规范与执行工件
│   ├── user-auth/                  # 功能目录
│   │   └── spec.md                 # 单一契约（状态、用户故事、验收与验证、决策、风险、任务、执行记录）
│   ├── archived/                   # 成熟稳定的基石规范
│   └── retired/                    # 废弃/证伪方案（负向警示护栏，立项时自动拦截）
└── project-memory/                 # 跨会话长期工程记忆
    ├── index.md                    # 记忆总索引（自动治理）
    └── features/                   # 系统能力契约胶囊 (Feature Capsules)
```

---

## 🧬 Spec 生命周期

每个 `spec.md` 均拥有严格的状态机元数据，完整追踪功能演进：

| 状态 | 职责说明 | 存放路径 |
|---|---|---|
| `proposed` | 立项草案，处于决策探针收敛或方案评审阶段 | `specs/<feature>/` |
| `delivered` | 验收通过，已转正为系统现态能力事实的生效规范 | `specs/<feature>/` |
| `archived` | 成熟封存，长期稳定运行的系统基石规范 | `specs/archived/<feature>/` |
| `superseded` | 被新规范替代废黜，保留双向跳转与重定向警示 | `specs/<feature>/` |
| `obsolete` | 证伪或废弃的负向警示护栏，立项时主动探测拦截 | `specs/retired/<feature>/` |

**演进路径**：
- **正常迭代**：`proposed` ➔ `delivered` ➔ `archived`
- **迭代废黜**：`delivered` ➔ `superseded`（新规范交付时自动双向回写旧规范）
- **证伪淘汰**：`proposed` / `delivered` ➔ `obsolete`（移入 `retired/` 永久拦截旧坑）

---

## 📦 安装与接入

### 方式 1：Agent Skills（推荐通用平台）
```bash
npx skills add ccasJay/LazySpec --skill '*' -g
```

### 方式 2：Claude Code Plugin
基线版本要求 Claude Code `2.1.229+`：
```bash
# 验证插件并加载本地目录
claude plugin validate .
claude --plugin-dir /absolute/path/to/LazySpec
```

---

## 🚀 极速上手

安装完成后，日常统一通过 **`using-lazyspec`** 入口进入：

### 1. 立项与决策探针
```text
使用 using-lazyspec 为“用户邮箱验证”立项。
```
> Agent 发起结构化探针确认核心架构决策与边界，生成 `specs/user-auth/spec.md`：包含用户故事、验收标准及内联验证方式、决策、风险与任务清单。

### 2. 执行与自动收口
```text
spec.md 已批准，请执行 specs/user-auth/spec.md 中的全部任务。
```
> Agent 连续执行编码与逐 TODO 基本检查，全部完成后运行全量 `Feature Verification`；用户审核并批准合并后，合并到 `dev`，将 `spec.md` 标记为 `delivered`，删除任务清单并压缩执行记录。

Spec 只记录可验收行为、必要决策、风险与任务；验证方式内联在验收表中，篇幅按实际复杂度决定。

### 3. 特性沉淀
```text
# 将已交付特性沉淀为能力契约胶囊
使用 distill-feature 沉淀已交付的“用户邮箱验证”特性。
```

---

## 🛠️ 技能清单

统一通过 `using-lazyspec` 路由，各技能亦可按需单独使用：

| 技能名称 | 职责说明 |
|---|---|
| [`using-lazyspec`](./using-lazyspec/SKILL.md) | **统一调度入口**：路由分发、负向警示护栏探测、记忆检索 |
| [`writing-spec`](./writing-spec/SKILL.md) | **规范制定**：决策探针收敛分歧，生成含任务与验收方式的单一 `spec.md` |
| [`executing-plan`](./executing-plan/SKILL.md) | **执行收口**：连续执行编码与基本检查、收尾全量功能验收、自动交付收敛与废黜回写 |
| [`distill-feature`](./distill-feature/SKILL.md) | **特性沉淀**：将已交付特性提炼为能力契约胶囊 |
| [`maintain-memory`](./maintain-memory/SKILL.md) | **记忆治理**：生命周期演进、成熟归档与索引自愈 |
| [`orchestrating-specs`](./orchestrating-specs/SKILL.md) | **联合编排**：默认优先并行、依赖就绪即启动、统一集成与合并 |
