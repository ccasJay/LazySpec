---
name: distill-learning
description: Distill reusable engineering lessons, failure observations, and negative guardrails into Learning Capsules under project-memory/learnings/. Can be invoked at any time without waiting for full feature delivery.
---

# Distill Learning Memory

## Scope and Shared Policies

- Capture project-specific engineering practices, diagnostic discoveries, and negative guardrails under `project-memory/learnings/<learning-id>.md`.
- Read [approval-policy.md](../using-lazyspec/references/approval-policy.md). Writing to `project-memory/` strictly requires explicit user approval of a complete preview artifact outside `project-memory/`.
- Full feature completion is NOT required. Attributable failure observations or debugging solutions may be distilled whenever valuable evidence emerges.

## Capsule Sections

A Learning Capsule strictly conforms to:
- `## Applicability`: Precise scope, triggers, and technologies affected.
- `## Observation`: Observed problem, symptoms, or behavior.
- `## Validated Practice`: Proven remedy, workaround, or negative constraint.
- `## Limits`: Conditions where the guidance does not apply.
- `## Revisit When`: Triggers to review or retire this guidance.
- `## Sources`: Attributable code, test, plan, or execution evidence items.

## Workflow

1. **Evidence Verification**: Verify that the observed problem and remedy have concrete, attributable evidence in the current repository.
2. **Preview Artifact**: Prepare preview with candidate capsule content and proposed `index.md` row (e.g., temporary `memory-preview.md` or environment artifact outside `project-memory/`).
3. **Approval Gate**: Request user approval of the preview artifact.
4. **Atomic Write**: Write to `project-memory/learnings/<learning-id>.md` and update `index.md`.
5. **Clean Up Preview Artifact**: Immediately delete the temporary preview artifact (e.g., `memory-preview.md`) upon successful write to ensure no ephemeral files remain in the workspace.

