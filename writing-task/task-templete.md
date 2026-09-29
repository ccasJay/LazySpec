**Compact Example Format:**

```markdown
# Implementation Plan

- [ ] //TODO 1. 实现创建记录行为

  - 实现目标：一并完成入口参数校验、数据写入、响应接入及对应自动化测试，即使它们位于不同文件
  - 成功判据：空名称返回约定错误且不写入；有效名称得到成功响应且恰好写入一次；写入失败时保持原状态
  - 验证方式：待实现的创建入口测试，覆盖有效、空名称及写入失败场景；执行前发现项目测试命令
  - _Requirements: [1.1](./requirements.md#req-1-1), [1.2](./requirements.md#req-1-2), [2.1](./requirements.md#req-2-1), [2.2](./requirements.md#req-2-2)_

- [ ] //TODO 2. 实现按 ID 查询记录行为

  - 实现目标：完成查询入口、读取逻辑及对应自动化测试；此行为可与创建记录分别交付和验证
  - 成功判据：已存在的 ID 返回对应记录；不存在的 ID 返回约定的未找到结果
  - 验证方式：待实现的查询入口测试，覆盖命中与未命中场景；执行前发现项目测试命令
  - _Requirements: [3.1](./requirements.md#req-3-1), [3.2](./requirements.md#req-3-2)_

## Feature Verification

风险依据：[Design 风险与待确认](./design.md#风险与待确认)

### Planned Checks

| 验收范围 | 场景与预期结果 | 验证方式 |
|---|---|---|
| [1.1](./requirements.md#req-1-1) | 空名称不写入数据并返回约定错误 | 创建入口测试（待实现） |
| [1.2](./requirements.md#req-1-2) | 有效请求通过创建入口得到约定的成功响应 | 创建入口测试（待实现） |
| [2.1](./requirements.md#req-2-1) | 一次有效请求恰好写入一次 | 创建入口测试（待实现） |
| [2.2](./requirements.md#req-2-2) | 写入失败时保持原状态 | 创建入口失败路径测试（待实现） |
| [3.1](./requirements.md#req-3-1) | 已存在的 ID 返回对应记录 | 查询入口测试（待实现） |
| [3.2](./requirements.md#req-3-2) | 不存在的 ID 返回约定的未找到结果 | 查询入口测试（待实现） |

### Latest Result

未执行。运行后按 delivery-loop.md 记录逐项证据、整体状态、时效、时间和被测代码状态。
```

The first TODO is one behavior slice across entry point, storage, response, and tests; the second is a separately deliverable behavior. Adapt the example to real approved requirements; never copy its behaviors or fabricate test commands. Add risk-specific and required human checks to Planned Checks. Learning Candidates is optional and added only from execution evidence.
