---
feature: memory-v2
status: active
summary: "current implementation memory"
source_spec: specs/memory-v2/
distilled_at: 2026-08-15
reviewed_at: 2026-08-18
tags: [memory, lifecycle]
authorities: [docs/architecture/memory.md]
supersedes: [project-memory/features/memory-v1.md]
---

# Memory V2

## Purpose

- The second implementation provides the current memory lifecycle. [S1]

## Durable Decisions

- D1 — The current capsule is the authoritative lifecycle summary. [S1]

## Guardrails

- The active capsule is the default retrieval target. [S1]

## Revisit When

- Read for current memory lifecycle work.

## Sources

- S1: `specs/memory-v2/requirements.md#req-1-1`
