# Project Memory Format

Use this contract whenever preparing, writing, or validating Feature Memory. Resolve every stored path against `ACTIVE_PROJECT_ROOT` and write paths with `/` separators.

## Project Layout

```text
project-memory/
├── index.md
└── features/
    └── <feature-name>.md
```

Use the source Spec directory name as `<feature-name>`. The MVP contains no `topics/`, `sessions/`, draft Memory, copied Spec files, or JSON index.

## Feature Capsule

Use this exact field set and section order:

```markdown
---
feature: <feature-name>
status: active
source_spec: specs/<feature-name>/
distilled_at: YYYY-MM-DD
tags: [<tag>]
supersedes: []
superseded_by: []
status_reason: ""
---

# <Feature title>

## Capability

- <Final capability and explicit boundary.> [S1, S2]

## Durable Decisions

- <Decision, rationale, rejected alternative, and consequence.> [S1, S3]

## Contracts and Invariants

- <Behavior, interface, data, compatibility, or workflow constraint.> [S2, S4]

## Lessons

- <Non-obvious failure mode, compatibility finding, or verification lesson.> [S3, S4]

## Reuse Triggers

- <Future task, phrase, tag, or condition that should load this Memory.>

## Sources

- S1: `specs/<feature-name>/requirements.md#req-N-N`
- S2: `specs/<feature-name>/design.md`
- S3: `<project-root-relative-implementation-path>`
- S4: `<project-root-relative-test-path>`
```

## Field Rules

- `feature`: match the source Spec directory and Capsule filename exactly.
- `status`: use one of `active`, `needs-review`, `superseded`, or `obsolete`.
- `source_spec`: point to the source directory and end with `/`.
- `distilled_at`: use the local calendar date in ISO `YYYY-MM-DD` form.
- `tags`: use a short YAML flow sequence of stable retrieval terms; never encode prose.
- `supersedes` and `superseded_by`: use project-root-relative Capsule paths; leave `status_reason` empty only for `active`, otherwise state why the Memory is not current.

## Content and Source Rules

- End every durable claim in Capability, Durable Decisions, Contracts and Invariants, and Lessons with one or more source IDs.
- Define every cited source ID exactly once in Sources. Use project-root-relative paths and preserve requirement anchors when available.
- Include only conclusions supported by approved Spec plus implementation or test evidence, or by an explicit user ruling on a conflict.
- Omit temporary progress, completed checkbox history, routine command output, guesses, and facts that are cheaper to recover from current code.
- Summarize; never copy complete sections from Requirements, Design, or Tasks.

## Index

Create `project-memory/index.md` with exactly this heading and table shape:

```markdown
# Project Memory Index

| Memory | Summary | Tags | Status | Source Spec |
|---|---|---|---|---|
| project-memory/features/<feature-name>.md | <one-line routing summary> | <comma-separated tags> | active | specs/<feature-name>/ |
```

Keep one row per Capsule path. Escape `|` characters inside cell values. Keep Summary short and useful only for routing; do not place durable conclusions in the index. Keep Status identical to the Capsule frontmatter.

## Validation Checklist

- Confirm the Capsule path, `feature`, and `source_spec` agree.
- Confirm the frontmatter has only the defined fields and a permitted status.
- Confirm all required sections appear exactly once and in order.
- Confirm every durable claim cites defined, resolvable sources.
- Confirm the index has the fixed header, a unique Capsule row, and matching status.
- Confirm the result contains no Topic layer, sessions, draft, JSON index, or copied Spec content.
