---
name: distill-feature
description: Distill verified delivered features from a Spec or fast plan into compact Feature Capsules under project-memory/features/. Requires user approval of an exact preview artifact before writing.
---

# Distill Feature Memory

## Scope and Shared Policies

- Maintain durable feature capability decisions under `project-memory/features/<feature-name>.md`.
- Read [approval-policy.md](../using-lazyspec/references/approval-policy.md) and [memory-workflow.md](../using-lazyspec/references/memory-workflow.md). The shared workflow owns project-root resolution, format loading, preview preparation, approved writes, validation, and cleanup.

## Prerequisites

1. The target Spec must have `status: delivered` in its frontmatter (or all tasks checked with Feature Verification `passed` in legacy Specs). For a feature delivered in fast mode, use its approved `plan.md` and completed tasks instead of requiring a nonexistent `spec.md`.
2. Feature Verification must be `passed` and `current`, with evidence attributable to the current commit/worktree.
3. Explicit user confirmation to distill this feature into memory.

## Workflow

Build an evidence matrix reconciling claims against the approved intent (`spec.md`, fast plan, or legacy requirements/design) and actual implementation/test sources:

| Claim | Spec/Plan Anchors | Code Evidence | Test Evidence | Existing Owner | Result |
|---|---|---|---|---|---|

Use the active format's Feature Capsule schema, then complete the shared Memory write workflow.

