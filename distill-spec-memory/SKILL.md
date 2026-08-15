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

## Completion Gate

Run `gate` before producing any candidate claim, preview, or write. Keep the gate result in the current session; do not encode it by creating a file.

1. **Spec completeness:** resolve `specs/<feature-name>/requirements.md`, `design.md`, and `tasks.md` under `ACTIVE_PROJECT_ROOT`. Each must be a readable regular file. Read each file completely before deciding that the gate passes. A missing, unreadable, or truncated file is a blocking condition.
2. **Task completion:** parse every task checkbox in `tasks.md`, including nested checkboxes. Every checkbox must be `[x]` or `[X]`; report each remaining `[ ]` with its line number and task text. Never infer completion from a task marker, a commit message, or file existence.
3. **Verification evidence:** collect the relevant automated checks named by the Feature's Tasks and Design. Each required check must have a current, attributable pass result in the session or be explicitly supplied and confirmed by the user. A command name without its result, a stale result, a skipped check, or an untestable claim is missing evidence.
4. **Completion confirmation:** obtain a separate, explicit confirmation in the current conversation that this Feature may be distilled. Approval of a task, Spec document, or a later Capsule preview is not completion confirmation. Do not infer it from silence, file state, or an ambiguous “done”.

If any item fails, return a Chinese blocking report listing the failed item, exact path or task/check evidence, and the next information needed. Stop immediately. Do not create `project-memory/`, a Capsule, an index update, or any `draft`/temporary Memory file. Existing Memory must remain untouched.

## Reconciliation and Evidence Matrix

After `gate` passes, read the complete Requirements, Design, and Tasks again as the approved intent set. Then inspect only the implementation and automated tests that are directly relevant to the candidate claims. Keep an in-session Evidence Matrix with one row per claim:

| Claim | Spec anchors | Implementation evidence | Test evidence | User ruling | Result |
|---|---|---|---|---|---|
| <candidate durable claim> | <requirements/design/tasks path and anchor> | <project-root-relative path and symbol/line> | <project-root-relative test path and result> | <only when resolving a conflict> | supported / conflict / insufficient |

Every candidate must have at least one approved intent anchor and one observable implementation or test source. A user ruling may resolve a documented conflict, but it cannot replace all Spec or implementation/test evidence. Keep this matrix in the conversation only; never write it as a project file.

- If the Spec and implementation/tests agree, mark the claim `supported` and retain all relevant source references.
- If they disagree, show both sides with their exact paths/anchors and ask the user to rule. Mark the claim `conflict`, stop before preview generation, and write nothing until the ruling is explicit.
- If the evidence is absent, unreachable, stale, or only a guess, mark the claim `insufficient`, report what is missing, and stop before preview generation. Never downgrade an unsupported claim into a confirmed fact.

## Deduplication and Conflict Check

After reconciliation, inspect `project-memory/index.md` if it exists. Use its rows to select only Capsules whose feature, tags, source Spec, or summary can overlap the candidate; read those Capsules completely. Do not scan every Capsule as a substitute for an index and do not create a replacement index during this check.

Classify each overlap before preview:

- An existing Capsule for the same Feature is an existing result, not permission to overwrite it. Report whether the request is a maintenance correction, a status transition, or a duplicate distillation and stop for the appropriate approval path.
- An `active` Capsule with materially overlapping claims is a potential duplicate or conflict. Show the existing sources and the candidate Evidence Matrix rows; do not silently merge, overwrite, or choose precedence.
- `needs-review`, `superseded`, and `obsolete` Capsules are historical context by default. Use them for conflict analysis only when the request or source relationship makes them relevant, and state their non-current status.
- If the index is malformed, a selected Capsule is missing, or index and Capsule metadata disagree, report the maintenance error and stop. Do not guess a path, status, or replacement relationship.

If an overlap requires a user ruling, or if no unique source-backed candidate remains after deduplication, stop before preview and write nothing. Only a clean, source-backed result may proceed to the existing `preview → approve → write → verify` sequence.

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
