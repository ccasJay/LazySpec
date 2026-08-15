---
feature: memory-v1
status: superseded
source_spec: specs/memory-v1/
distilled_at: 2026-08-15
tags: [memory, lifecycle]
supersedes: []
superseded_by: [project-memory/features/memory-v2.md]
status_reason: "Replaced by the second implementation memory."
---

# Memory V1

## Capability

- The first implementation provides the original memory lifecycle. [S1]

## Durable Decisions

- The original lifecycle is retained as historical context. [S1]

## Contracts and Invariants

- Historical capsules remain traceable. [S1]

## Lessons

- A later capsule must explicitly replace an older one. [S1]

## Reuse Triggers

- Read when tracing the first implementation.

## Sources

- S1: `specs/memory-v1/requirements.md#req-1-1`
