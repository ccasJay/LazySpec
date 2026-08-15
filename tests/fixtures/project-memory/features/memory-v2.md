---
feature: memory-v2
status: active
source_spec: specs/memory-v2/
distilled_at: 2026-08-15
tags: [memory, lifecycle]
supersedes: [project-memory/features/memory-v1.md]
superseded_by: []
status_reason: ""
---

# Memory V2

## Capability

- The second implementation provides the current memory lifecycle. [S1]

## Durable Decisions

- The current capsule is the authoritative lifecycle summary. [S1]

## Contracts and Invariants

- The active capsule is the default retrieval target. [S1]

## Lessons

- Replacement must be represented in both directions. [S1]

## Reuse Triggers

- Read for current memory lifecycle work.

## Sources

- S1: `specs/memory-v2/requirements.md#req-1-1`
