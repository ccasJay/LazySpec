---
feature: drifting
status: needs-review
source_spec: specs/drifting/
distilled_at: 2026-08-15
tags: [memory, review]
supersedes: []
superseded_by: []
status_reason: "Implementation drift requires review."
---

# Drifting Memory

## Capability

- This memory may describe a capability whose implementation has drifted. [S1]

## Durable Decisions

- No current decision is asserted until review. [S1]

## Contracts and Invariants

- Review is required before ordinary retrieval. [S1]

## Lessons

- Drift must be visible in the status. [S1]

## Reuse Triggers

- Read only for explicit review requests.

## Sources

- S1: `specs/drifting/requirements.md#req-1-1`
