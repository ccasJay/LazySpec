# Memory write workflow

Shared preparation, write, and cleanup procedure for `distill-feature` and `maintain-memory`. Approval semantics and the exact preview contract belong to [approval-policy.md](approval-policy.md#file-backed-review); Capsule schemas, status invariants, and index validation belong to the active Memory format.

## Context and format

Resolve project paths against `ACTIVE_PROJECT_ROOT`, the user's project working directory at session start. If invoked directly and that directory is ambiguous, establish it before reading or writing project artifacts. Load `project-memory/README.md` when present; otherwise load [memory-format.md](memory-format.md). Use that contract for Feature Capsules and maintenance; do not invent a reduced local schema.

## Prepare and apply

1. Verify the proposed claims or lifecycle changes against attributable project evidence and the calling Skill's prerequisites. Reconcile overlapping Capsule ownership and reciprocal supersession using the active format. Read-only audits stop at reporting unless the user also requests changes.
2. Save the complete write preview required by approval-policy.md outside `project-memory/`, for example `memory-preview.md`. For governance operations, include exact Spec moves, metadata changes, callouts, and source-link repairs in the same preview. Do not mutate the target write set during preparation.
3. Link the preview, give a concise explanation of its purpose, and request approval under approval-policy.md. If the proposal changes, update the preview before requesting approval of the new write set.
4. After approval, apply the Capsule changes and regenerate the index as one logical write set; include approved Spec operations for maintenance. Validate metadata, source paths, reciprocal links, and index/Capsule agreement under the active format. Report incomplete or failed writes; do not claim success or silently expand the approved set.
5. **Clean Up Preview Artifact**: Delete the temporary preview immediately after a successful write or when rejected/abandoned. Retain it while approval is pending or a write remains incomplete so the exact proposed set is recoverable.
