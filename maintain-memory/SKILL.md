---
name: maintain-memory
description: "Audit and govern project memory and specs lifecycle: propagate supersessions, archive mature foundation specs into specs/archived/, retire obsolete specs into specs/retired/, and heal project-memory/index.md."
---

# Maintain Memory and Specs Governance

## Scope

`maintain-memory` owns lifecycle transitions, historical archiving, and memory health across `specs/` and `project-memory/`:
1. **Supersession Propagation**: When a Spec is marked `superseded`, update corresponding Feature Capsules and `project-memory/index.md` status to `superseded`.
2. **Mature Foundation Archival (Archive)**:
   - Identify Specs with `status: delivered` that have proven stable and foundational over time.
   - Relocate them to `specs/archived/<feature-name>/`.
   - Freeze the files as read-only historical snapshots to keep the active `specs/` workspace uncluttered.
3. **Negative Guardrail Retirement (Retire / Obsolete)**:
   - Identify Specs marked `status: obsolete` (mechanisms disproven or removed).
   - **DO NOT DELETE.** Relocate them to `specs/retired/<feature-name>/`.
   - Verify that the document includes a prominent `[!CAUTION]` block explaining why the design failed/was deprecated, acting as an active negative guardrail.
4. **Index Self-Healing**:
   - Scan all active, superseded, archived, and obsolete capsules.
   - Regenerate and align `project-memory/index.md` according to the active contract.

