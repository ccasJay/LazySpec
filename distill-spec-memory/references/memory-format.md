# Project Memory Format

Use this fallback contract when the active project has no `project-memory/README.md`. Resolve every stored path against `ACTIVE_PROJECT_ROOT` and use project-root-relative POSIX paths.

## Project layout

```text
project-memory/
├── index.md
└── features/
    └── <feature-name>.md
```

Keep one current decision Capsule per completed Feature. Do not add Topic aggregation, sessions, draft Memory, copied Specs, or a JSON index.

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
- Include approved intent plus implementation or test evidence. Omit current control-flow narration, generic lessons, progress history, and facts cheaper to recover from code.
- Active and needs-review bodies may change only through a complete evidence review and approved preview. Git and Specs preserve earlier versions.

## Status invariants

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
```

Sort rows deterministically by feature. Keep exactly one row per Capsule. The index status, paths, tags, summary, Source Spec, and reviewed date must equal frontmatter.

## Validation checklist

- Validate required and conditional metadata, path containment, dates, and authority existence.
- Validate section order, unique decision IDs, source definitions, citations, and resolvable source paths.
- Validate index/Capsule bijection and deterministic generated content.
- Validate reciprocal supersession and reject cycles.
- Report completed-checkbox Specs without Capsules as candidates only; never create Memory automatically.
- Treat the approved Capsule set and generated index as one logical write set.
