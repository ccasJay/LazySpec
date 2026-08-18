---
name: distill-spec-memory
description: Distill completed and verified LazySpec features into current, source-traceable project memory, or review and maintain existing project-memory Capsules after implementation drift. Use only when the user explicitly asks to preserve, distill, review, repair, supersede, or retire Project Memory; do not trigger from ordinary Spec creation, revision, planning, or task execution.
---

# Distill Spec Memory

Maintain a small corpus of current decision summaries. Treat Specs and Git as history; treat only an `active` Capsule as default-retrievable current guidance.

## Language and project root

- Keep this Skill and bundled references in English.
- Write user-facing analysis, blockers, previews, approval requests, and reports in Chinese unless the user requests another language.
- Bind `ACTIVE_PROJECT_ROOT` to the user's project working directory. Resolve every Spec, Capsule, source, authority, command, and index path against it; never derive the project root from this Skill's installation path.

## Load the active contract

Before preparing or validating Memory:

1. Read `ACTIVE_PROJECT_ROOT/project-memory/README.md` completely when it exists and treat it as the project-local contract.
2. Otherwise read `references/memory-format.md` relative to this `SKILL.md` as the fallback contract.
3. Inspect `project-memory/index.md` only after loading the contract. Do not scan all Capsules as a substitute for a valid index.
4. Discover project-local index generation and validation commands from the contract and current manifest. Do not copy command names from another repository.

If the local contract conflicts with the fallback, follow the local contract and report the difference. If the local contract, generated index, and Capsule metadata disagree, stop before proposing content.

## Routing boundary

- Run only after an explicit request to create or maintain Project Memory for a completed Feature.
- Accept a direct request or routing from `using-lazyspec`.
- Do not automatically distill or mutate Memory when a final task completes. A task workflow may report affected Capsule candidates only.
- Treat a request for an existing Feature as maintenance review, not permission to overwrite it silently.

## Gate before preview

Keep all analysis and candidate text in the conversation until the gate passes:

1. Resolve and read the complete `requirements.md`, `design.md`, and `tasks.md` for every source Feature involved.
2. Verify that every task checkbox, including nested checkboxes, is `[x]` or `[X]`.
3. Collect current, attributable results for the automated checks required by the Spec and affected implementation. A command name, old result, skipped check, or checkbox is not verification evidence.
4. Obtain explicit confirmation that the named Feature or existing Capsule may be distilled or maintained. Do not infer this from task approval, silence, or file state.
5. Check the worktree. If relevant implementation has uncommitted changes, include them in the evidence and preview; never present the previous commit as the verified implementation.

On any failure, report the exact path, task, check, or confirmation missing and write nothing under `project-memory/`.

## Build an evidence matrix

Reconcile each candidate claim against approved intent and current implementation. Keep this matrix in the conversation only:

| Claim | Spec anchors | Implementation evidence | Test evidence | Existing owner | Result |
|---|---|---|---|---|---|
| <claim> | <requirements/design/tasks> | <path and symbol> | <path and current result> | <Capsule and decision ID, if any> | supported / conflict / insufficient |

- Require at least one approved Spec anchor and one implementation or test source for every factual claim.
- Use current architecture documents as navigation, then verify against source and tests.
- Stop on a material conflict and ask for a ruling. A user ruling may resolve a conflict but cannot replace all evidence.
- Omit facts cheaper to recover from current code, temporary progress, command transcripts, and generic lessons.

## Select one owner for each decision

Use index feature, summary, tags, Source Spec, and authorities to select only potentially overlapping Capsules, then read those Capsules completely.

- Keep one active owner for each durable decision. Do not duplicate an existing claim merely because a new Feature touched it.
- For the same Feature, propose a maintenance revision that preserves `distilled_at`, updates `reviewed_at`, and changes only evidence-backed current guidance.
- When a new Feature changes an existing owner, include the affected Capsule revision or status transition in the same preview.
- Use `needs-review` when drift is suspected but cannot yet be reconciled. Exclude it from ordinary recall.
- Use `superseded` only when a resolvable replacement owns the whole conclusion; update reciprocal relationships atomically.
- Use `obsolete` when the conclusion is invalid and has no replacement.
- Never edit the body of `superseded` or `obsolete` Capsules. Git and source Specs preserve history for maintained active Capsules.

## Preview and approval

The preview is the approval object. Show, in Chinese:

- every complete proposed Capsule, including frontmatter, body, sources, and stable decision IDs;
- the complete generated index or exact index change;
- every status and reciprocal relationship change;
- the evidence matrix summary, conflicts, and user rulings; and
- the complete project-root-relative logical write set.

Ask for explicit approval of that exact preview. Any requested edit invalidates the previous approval: revise and show the complete preview again. Completion confirmation is not preview approval, and one preview never authorizes another Feature.

## Write and verify atomically

After approval:

1. Write only the approved Capsule, local contract, and index paths under `ACTIVE_PROJECT_ROOT/project-memory/`.
2. Run the project-local index generator when provided; otherwise produce the fallback deterministic index exactly as specified by the active contract.
3. Run the project-local Memory validator and relevant repository checks discovered from the manifest and contract.
4. Re-read every changed Capsule and the index; verify metadata, required sections, sources, status equality, authority paths, stable decision IDs, and reciprocal relationships.
5. Report partial writes or validation failures with exact file state and stop without claiming success.

Never create draft/staging Memory, Topic aggregation, session archives, copied Specs, or a second/JSON index unless the project-local contract explicitly replaces this fallback model.

## Status rules

- `active`: current and default-retrievable; omit `status_reason` and `superseded_by`.
- `needs-review`: suspected drift; require `status_reason`; allow an evidence-backed body revision before returning to `active`.
- `superseded`: terminal; require `status_reason` and reciprocal `superseded_by`.
- `obsolete`: terminal; require `status_reason` and no `superseded_by`.

Allow `active → active` maintenance, `active → needs-review`, `needs-review → active`, and `active` or `needs-review → superseded|obsolete`. Do not reactivate terminal Capsules; create a new owner instead.

## Write boundary

- Keep evidence and candidate content in the conversation before exact preview approval.
- Treat all approved Capsule revisions, status relationships, and the generated index as one logical write set.
- Do not delete, move, rename, or overwrite source Specs.
- Stop after the requested Memory operation; do not begin another Feature automatically.
