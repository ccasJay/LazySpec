---
kind: learning
learning: bounded-retry
status: active
summary: "限定重复校验失败的重试经验"
source_spec: specs/retry-example/
distilled_at: 2026-09-05
reviewed_at: 2026-09-05
tags: [retry, validation]
authorities: [tests/test_delivery_contracts.py]
---

# 重复失败的边界（合成测试样例）

## Applicability

- 仅适用于这个合成样例的重复校验失败，不代表生产环境结论。[S1, S2]

## Observation

- 失败结果没有变化时，单纯改写报告不能使证据更新。[S2, S3]

## Validated Practice

- L1 — 样例校验拒绝把过期证据标记为当前通过结果。[S2, S3]

## Limits

- 未证明任何生产修复有效，源功能可以仍未完成。[S1, S2]

## Revisit When

- 样例的证据时效规则改变时复核。

## Sources

- S1: `specs/retry-example/plan.md#approach`
- S2: `specs/retry-example/plan.md#feature-verification`
- S3: `tests/test_delivery_contracts.py`
