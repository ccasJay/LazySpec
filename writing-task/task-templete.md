**Compact Example Format:**

```markdown
# Implementation Plan

- [ ] //TODO 1. Implement the core interface

  - 实现目标：修改入口的参数校验逻辑
  - 成功判据：传入空名称时返回约定的校验错误，且不写入数据
  - 验证方式：待实现的参数校验测试；执行前发现项目测试命令
  - _Requirements: [1.1](./requirements.md#req-1-1)_

- [ ] //TODO 2. Integrate and verify the feature

  - 实现目标：将实现接入现有调用入口
  - 成功判据：有效请求产生一次预期写入；失败请求保持原状态
  - 验证方式：待实现的入口集成测试；覆盖成功与失败路径
  - _Requirements: [1.2](./requirements.md#req-1-2), [2.1](./requirements.md#req-2-1), [2.2](./requirements.md#req-2-2)_

## Feature Verification

风险依据：[Design 风险与待确认](./design.md#风险与待确认)

### Planned Checks

| 验收范围 | 场景与预期结果 | 验证方式 |
|---|---|---|
| [1.1](./requirements.md#req-1-1) | 空名称不写入数据并返回约定错误 | 参数校验测试（待实现） |
| [1.2](./requirements.md#req-1-2) | 有效请求通过现有入口得到约定的成功响应 | 入口集成测试（待实现） |
| [2.1](./requirements.md#req-2-1) | 一次有效请求恰好写入一次 | 入口集成测试（待实现） |
| [2.2](./requirements.md#req-2-2) | 失败请求保持原状态 | 入口失败路径测试（待实现） |

### Latest Result

未执行。运行后按 delivery-loop.md 记录逐项证据、整体状态、时效、时间和被测代码状态。
```

Adapt the example to real approved requirements; never copy its behaviors or fabricate test commands. Add risk-specific and required human checks to Planned Checks. Learning Candidates is optional and added only from execution evidence.
