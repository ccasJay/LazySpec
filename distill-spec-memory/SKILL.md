---
name: distill-spec-memory
description: Distill a completed and verified LazySpec feature into durable project memory with source traceability and explicit write approval. Use only when the user explicitly asks to preserve, archive, or distill a finished Feature Spec directory into `project-memory/`; do not use for ordinary Spec creation, revision, planning, or task execution.
---

# Distill Spec Memory

## Language

- Keep this Skill and its references in English.
- Write all user-facing analysis, blockers, previews, approval requests, and completion reports in Chinese unless the user explicitly requests another language.
- Preserve project names, code identifiers, paths, status values, and Markdown syntax.

## Project Root

Bind `ACTIVE_PROJECT_ROOT` to the user's project working directory at the start of the session. Resolve `specs/<feature-name>/` and `project-memory/` against that root. Never derive the project root from this Skill directory, a Plugin cache, an Agent Skills installation, or the current location of `SKILL.md`. If the project root or feature name is ambiguous, ask before reading or writing.

Resolve `references/memory-format.md` relative to the directory containing this `SKILL.md`. Read it before preparing a Memory preview or validating a write.

## Routing Boundary

- Run only after an explicit request to distill a finished Feature Spec into project Memory.
- Accept routing from `using-lazyspec` or a direct invocation of this Skill.
- Do not trigger from ordinary Brainstorming, Requirements, Design, Tasks, task questions, or task execution.
- Do not automatically distill a Feature when its final task is completed.

## Workflow

Follow this sequence without skipping a gate:

1. Identify the target `specs/<feature-name>/` and keep all candidate work in the current session.
2. Confirm that the Feature is complete and that its verification evidence is current. Stop without writing when a completion condition is missing.
3. Reconcile the approved Spec with directly relevant implementation and test evidence. Escalate material conflicts to the user instead of choosing a side silently.
4. Read `references/memory-format.md`, inspect `project-memory/index.md` when it exists, and select only existing Capsules relevant to duplicate or conflict checks.
5. Produce a concise candidate Capsule containing durable knowledge only. Preserve a source reference for every durable claim.
6. Preview the candidate Capsule, proposed index row, status changes, conflicts, and sources in the conversation. Do not create a draft file.
7. Write the approved logical change set under `ACTIVE_PROJECT_ROOT/project-memory/`, then validate paths, structure, sources, uniqueness, and index consistency.

Preserve this ordering and the zero-write behavior until every completion, evidence, and approval gate has passed.

## Memory Contract

- Use exactly one `project-memory/index.md` as the human- and Agent-readable index.
- Store one approved Feature Capsule at `project-memory/features/<feature-name>.md`.
- Use project-root-relative POSIX paths in metadata and index fields.
- Keep the Capsule materially smaller than its source Spec; record capabilities, durable decisions, contracts and invariants, non-obvious lessons, reuse triggers, and sources instead of repeating Spec prose.
- Do not create Topic aggregation, session archives, JSON indexes, or copies of Requirements, Design, or Tasks in the MVP.
- Do not delete, move, rename, or overwrite the source Spec.

## Write Boundary

- Keep analysis, evidence reconciliation, and previews in the conversation until the user explicitly approves the current preview.
- Treat the Capsule and matching index row as one logical change set.
- Report every file actually changed. Never claim success when validation fails or a partial write leaves Memory inconsistent.
- Stop after completing the requested distillation. Do not begin another Feature automatically.
