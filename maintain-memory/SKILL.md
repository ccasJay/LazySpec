---
name: maintain-memory
description: "Audit and govern project memory and specs lifecycle: propagate supersessions, archive mature foundation specs into specs/archived/, retire obsolete specs into specs/retired/, and heal project-memory/index.md."
---

# Maintain Memory and Specs Governance

## Shared policies

Read [approval-policy.md](../using-lazyspec/references/approval-policy.md), [memory-workflow.md](../using-lazyspec/references/memory-workflow.md), and the lifecycle definitions in [delivery-loop.md](../using-lazyspec/references/delivery-loop.md#lifecycle-states-and-negative-guardrails). Follow the shared workflow for project-root and format resolution, read-only audits, and any approved write set.

## Scope

`maintain-memory` owns lifecycle transitions, historical archiving, and memory health across `specs/` and `project-memory/`:
1. **Supersession Propagation**: When a Spec is marked `superseded`, update corresponding Feature Capsules and `project-memory/index.md` status to `superseded`.
2. **Mature Foundation Archival (Archive)**:
   - Identify Specs with `status: delivered` that have proven stable and foundational over time.
   - Relocate them to `specs/archived/<feature-name>/`.
   - Set the Spec status to `archived` and repair source references affected by the move.
   - Freeze the files as read-only historical snapshots to keep the active `specs/` workspace uncluttered.
3. **Negative Guardrail Retirement (Retire / Obsolete)**:
   - Identify Specs marked `status: obsolete` (mechanisms disproven or removed).
   - **DO NOT DELETE.** Relocate them to `specs/retired/<feature-name>/`.
   - Verify that the document includes a prominent `[!CAUTION]` block explaining why the design failed/was deprecated, acting as an active negative guardrail.
4. **Index Self-Healing**:
   - Scan both Capsule roots using the active Memory format; `archived` is a Spec state, not a Capsule state.
   - Regenerate and align `project-memory/index.md` according to the active contract.

Prepare lifecycle changes, Capsule updates, index regeneration, and affected source-link repairs as one preview under the shared workflow. Normal delivery's Spec-to-Spec supersession update belongs to `executing-plan`; this Skill propagates approved effects to Memory and handles archival/retirement. Do not infer a Memory write authorization from delivery completion.

