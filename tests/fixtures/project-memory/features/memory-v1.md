---
feature: memory-v1
status: superseded
summary: "first implementation memory"
source_spec: specs/memory-v1/
distilled_at: 2026-08-15
reviewed_at: 2026-08-18
tags: [memory, lifecycle]
authorities: [docs/architecture/memory.md]
superseded_by: [project-memory/features/memory-v2.md]
status_reason: "Replaced by the second implementation memory."
---

# Memory V1

## Purpose

- The first implementation provides the original memory lifecycle. [S1]

## Durable Decisions

- D1 — The original lifecycle is retained as historical context. [S1]

## Guardrails

- Historical capsules remain traceable. [S1]

## Revisit When

- Read when tracing the first implementation.

## Sources

- S1: `specs/memory-v1/requirements.md#req-1-1`
