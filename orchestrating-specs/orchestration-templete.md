# 多 Spec 编排

## 编排目标

[用一至两句说明本次多 Spec 交付的整体目标]

## 涉及的 Spec

| Spec | 路径 | 批准状态 | 完成条件 |
|---|---|---|---|
| [feature_name] | specs/[feature_name]/ | 已批准 | Feature Verification passed |

## 依赖关系与执行顺序

[Spec 之间的依赖关系与执行顺序，如 A → B → C；无依赖则说明依据]

## 可并行执行的部分

[可并行执行的 Spec 或阶段；无则写“无”]

## 分支与合并策略

[记录依赖链的堆叠分支、独立分支的共同基础与合并顺序；遵循编排 Skill 中的分支规则]

## 跨 Spec 协调约束

[共享接口、数据、时序等 Spec 之间的协调约束；只描述跨 Spec 协调，不规定单个 Spec 内部任务如何执行]

## 跨 Spec 集成验证

[最终跨 Spec Integration Verification：场景、预期结果、检查方式]

## 生命周期状态

- [ ] 编排已获用户批准
- [ ] 各 Spec Feature Verification 全部 passed
- [ ] 跨 Spec Integration Verification passed
- [ ] Memory 沉淀门完成（需要的写入已获批准并完成，或用户明确确认无需沉淀）
- [ ] 用户确认最终交付
- [ ] 已删除 orchestration.md
