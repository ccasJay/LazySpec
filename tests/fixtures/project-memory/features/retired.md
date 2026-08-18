---
feature: retired
status: obsolete
summary: "retired memory"
source_spec: specs/retired/
distilled_at: 2026-08-15
reviewed_at: 2026-08-18
tags: [memory, retired]
authorities: [docs/architecture/retired.md]
status_reason: "The capability is no longer supported."
---

# Retired Memory

## Purpose

- The retired capability is kept only for historical traceability. [S1]

## Durable Decisions

- D1 — No replacement exists for this retired capability. [S1]

## Guardrails

- Obsolete memory is excluded from ordinary retrieval. [S1]

## Revisit When

- Read only for explicit historical requests.

## Sources

- S1: `specs/retired/requirements.md#req-1-1`
