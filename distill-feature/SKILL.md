---
name: distill-feature
description: Distill verified delivered feature specifications into compact Feature Capsules under project-memory/features/. Requires user approval of an exact preview artifact before writing.
---

# Distill Feature Memory

## Scope and Shared Policies

- Maintain durable feature capability decisions under `project-memory/features/<feature-name>.md`.
- Read [approval-policy.md](../using-lazyspec/references/approval-policy.md). Writing to `project-memory/` strictly requires explicit user approval of a complete preview artifact outside the project-memory tree.
- Resolve all project paths against `ACTIVE_PROJECT_ROOT`. Load project contract `project-memory/README.md` if present, otherwise load fallback `../distill-spec-memory/references/memory-format.md`.

## Prerequisites

1. The target Spec must have `status: delivered` in its frontmatter (or all tasks checked with Feature Verification `passed` in legacy Specs).
2. Verification evidence must be attributable to the current commit/worktree.
3. Explicit user confirmation to distill this feature into memory.

## Workflow

1. **Build Evidence Matrix**:
   Reconcile claims against `spec.md` (or legacy requirements/design) and actual implementation/test sources:
   | Claim | Spec Anchors | Code Evidence | Test Evidence | Existing Owner | Result |
   |---|---|---|---|---|---|
2. **Generate Preview Artifact**:
   Write a complete preview artifact outside `project-memory/` showing:
   - Full text of candidate `project-memory/features/<feature-name>.md`;
   - Exact diff or updated row for `project-memory/index.md`;
   - Reciprocal status transitions if overriding an existing capsule.
3. **Request Approval**:
   Summarize concisely in chat (1-3 sentences) with a link to the preview artifact. Ask for explicit approval.
4. **Atomic Write & Verify**:
   Upon approval, write the capsule, regenerate/update `project-memory/index.md`, and verify metadata.

