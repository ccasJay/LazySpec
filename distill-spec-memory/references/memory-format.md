# Project Memory Format

Use this fallback contract when the active project has no `project-memory/README.md`. Resolve every stored path against `ACTIVE_PROJECT_ROOT` and use project-root-relative POSIX paths.

## Project layout

```text
project-memory/
├── index.md
├── features/
│   └── <feature-name>.md
└── learnings/
    └── <learning-id>.md
```

Keep one current decision Capsule per completed Feature and one owner per durable learning conclusion. Do not add Topic aggregation, sessions, draft Memory under project-memory/, copied Specs, or a JSON index. Candidates belong in source tasks.md/plan.md and are never default-retrievable.

## Feature Capsule format

Existing Capsules without `kind` remain Feature Capsules. Optional `kind: feature` is accepted, not required; no bulk migration. A verified fast feature may use approved plan.md sections as Spec sources.

## Capsule format

Use this required metadata and section order:

```markdown
---
feature: <feature-name>
status: active
summary: "<short routing summary>"
source_spec: specs/<feature-name>/
distilled_at: YYYY-MM-DD
reviewed_at: YYYY-MM-DD
tags: [<stable-tag>]
authorities: [<current-architecture-or-source-path>]
---

# <Feature title>

## Purpose

- <Why this decision set exists and its boundary.> [S1, S2]

## Durable Decisions

- D1 — <Decision, rationale, rejected alternative or consequence.> [S2, S3]

## Guardrails

- <Negative guarantee, compatibility rule, or ownership constraint.> [S1, S4]

## Revisit When

- <Observable condition that should trigger review.>

## Sources

- S1: `specs/<feature-name>/requirements.md#req-N-N`
- S2: `specs/<feature-name>/design.md`
- S3: `<project-root-relative-implementation-path>`
- S4: `<project-root-relative-test-path>`
```

Conditional metadata is omitted when unused:

- `status_reason`: required for every non-`active` status.
- `supersedes`: non-empty Capsule path sequence when this Capsule replaces another.
- `superseded_by`: required non-empty Capsule path sequence only for `superseded`.

## Field and content rules

- `feature`, filename, and `source_spec` directory name must match.
- `status` is `active`, `needs-review`, `superseded`, or `obsolete`.
- `summary` is routing text, not a durable conclusion.
- Preserve the first successful `distilled_at`; set `reviewed_at` whenever all current claims are reverified.
- `tags` contains stable search terms. `authorities` points to current architecture or source owners and must not contain historical-only documents.
- Use unique stable `D<N>` IDs within each Capsule.
- End every factual bullet in Purpose, Durable Decisions, and Guardrails with defined source IDs.
- Keep Revisit When operational and observable. Do not use age or word count alone as a trigger.
- Include approved intent (normal Spec or fast plan) plus implementation or test evidence. Omit current control-flow narration, generic lessons, progress history, and facts cheaper to recover from code.
- Active and needs-review bodies may change only through a complete evidence review and approved preview. Git and Specs preserve earlier versions.

## Status invariants

These statuses apply to both Feature and Learning Capsules.

- `active` is current and default-retrievable; omit `status_reason` and `superseded_by`.
- `needs-review` is excluded from ordinary recall and requires a non-empty reason.
- `superseded` is terminal and requires a reason plus reciprocal `superseded_by`/`supersedes` paths.
- `obsolete` is terminal, requires a reason, and has no `superseded_by`.

Allow `active → active` maintenance, `active → needs-review`, `needs-review → active`, and `active|needs-review → superseded|obsolete`. Never reactivate terminal Capsules.

## Deterministic index

Generate one `project-memory/index.md` from Capsule metadata:

```markdown
# Project Memory Index

<!-- Generated from Capsule metadata; do not edit manually. -->

| Memory | Summary | Tags | Status | Source Spec | Reviewed |
|---|---|---|---|---|---|
| [project-memory/features/<feature-name>.md](./features/<feature-name>.md) | <summary> | <tags> | active | [specs/<feature-name>/](../specs/<feature-name>/) | YYYY-MM-DD |
| [project-memory/learnings/<learning-id>.md](./learnings/<learning-id>.md) | <summary> | <tags> | active | [specs/<source-feature>/](../specs/<source-feature>/) | YYYY-MM-DD |
```

For feature-only legacy indexes preserve sorting by feature. For mixed indexes sort by kind (feature before learning), then feature/learning ID, then project-root-relative path. Keep the same six-column header; Memory paths distinguish kinds. Keep exactly one row per Capsule. The index status, paths, tags, summary, Source Spec, and reviewed date must equal frontmatter.

## Validation checklist

- Validate required and conditional metadata, path containment, dates, and authority existence.
- Validate section order, unique decision IDs, source definitions, citations, and resolvable source paths.
- Validate index/Capsule bijection and deterministic generated content.
- Validate reciprocal supersession and reject cycles.
- Report completed-checkbox Specs without Capsules as candidates only; never create Memory automatically. Feature promotion still requires current passed verification. Learning promotion requires bounded claim evidence and exact write approval, not source feature completion.
- Treat the approved Capsule set and generated index as one logical write set.

## Learning Capsule format

Use this metadata and section order for new learning Capsules:

```markdown
---
kind: learning
learning: <learning-id>
status: active
summary: "<short routing summary>"
source_spec: specs/<primary-source-feature>/
distilled_at: YYYY-MM-DD
reviewed_at: YYYY-MM-DD
tags: [<stable-tag>]
authorities: [<current-source-or-test-path>]
---

# <Learning title>

## Applicability

- <Project conditions where this guidance applies.> [S1, S2]

## Observation

- <Observed problem and evidenced explanation; distinguish unknown causes.> [S2, S3]

## Validated Practice

- L1 — <Validated action or bounded negative guidance, not an untested remedy.> [S2, S3]

## Limits

- <Conditions not established by the evidence and exclusions.> [S2, S3]

## Revisit When

- <Observable source, environment, or behavior change requiring review.>

## Sources

- S1: `specs/<source-feature>/plan.md#approach`
- S2: `specs/<source-feature>/plan.md#feature-verification`
- S3: `<current-source-or-test-path>`
```

- `kind: learning` is required, and `learning` equals the filename stem. `source_spec` identifies the primary originating feature and need not match the learning ID. Additional source features belong in Sources, each traceable to approved intent and attributable evidence.
- The metadata, dates, authority existence, four statuses, and reciprocal supersession rules are shared with Feature Capsules. Learning uses stable unique `L<N>` IDs rather than `D<N>` IDs. Cite defined sources for factual bullets in Applicability, Observation, Validated Practice, and Limits.
- A failed or incomplete source feature is permitted when current evidence proves the bounded observation and practice. A failure does not prove a proposed fix; user confirmation cannot replace evidence. Never label a feature verified through a Learning Capsule.
- Reject kind/path mismatches, absolute paths, traversal (including symlinks escaping the project), duplicate IDs, invalid source links, stale unsupported claims, and index/metadata discrepancies. Recall accepts only active, applicable guidance, at most three Capsules across both kinds combined.
- Keep the six-column index and one row per Capsule. Feature and Learning conclusions must not create duplicate active owners; reconcile overlap in one approved preview. Candidate collection or suspected drift alone does not authorize status changes.
