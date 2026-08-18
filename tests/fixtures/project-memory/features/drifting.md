---
feature: drifting
status: needs-review
summary: "memory awaiting review"
source_spec: specs/drifting/
distilled_at: 2026-08-15
reviewed_at: 2026-08-18
tags: [memory, review]
authorities: [docs/architecture/drifting.md]
status_reason: "Implementation drift requires review."
---

# Drifting Memory

## Purpose

- This memory may describe a capability whose implementation has drifted. [S1]

## Durable Decisions

- D1 — No current decision is asserted until review. [S1]

## Guardrails

- Review is required before ordinary retrieval. [S1]

## Revisit When

- Read only for explicit review requests.

## Sources

- S1: `specs/drifting/requirements.md#req-1-1`
