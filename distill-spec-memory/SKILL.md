---
name: distill-spec-memory
description: Distill verified Feature Memory or evidence-backed Learning Memory, promote confirmed learning candidates, and maintain existing Capsules. Long-term writes require approval of the exact Capsule/index preview; routine execution only collects candidates in its task or plan artifact.
---

# Distill Spec Memory

Maintain a small corpus of current feature decisions and bounded project-specific learning. Treat Specs and Git as history; treat only an `active` Capsule as default-retrievable current guidance.

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md) for approval boundaries. Candidate collection is defined in [delivery-loop.md](../using-lazyspec/references/delivery-loop.md); read it when promoting a candidate. Resolve these links from this Skill directory.

## Language and project root

- Keep this Skill and bundled references in English.
- Write user-facing analysis, blockers, previews, approval requests, and reports in Chinese unless the user requests another language.
- Bind `ACTIVE_PROJECT_ROOT` to the user's project working directory. Resolve every Spec, Capsule, source, authority, command, and index path against it; never derive the project root from this Skill's installation path.

## Conversation output policy

- The conversation is a status and approval channel, not the full Memory payload.
- Keep the complete evidence matrix, candidate Capsule content, generated index, relationship changes, and logical write set in a preview artifact outside `ACTIVE_PROJECT_ROOT/project-memory/` (for example, a temporary file or a host-supported artifact). Do not paste those full contents into the chat.
- In chat, provide only a concise 1–3 sentence summary: what was reviewed, whether verification passed, what will be written, and the preview artifact path or link.
- When approval is required, ask the user to approve that exact preview artifact. Include its path or link and, when available, a content hash or stable identifier. Never infer approval from silence or from approval of a different preview.
- If a preview artifact cannot be exposed to the user, stop and report that limitation rather than dumping the full payload into the chat.

## Load the active contract

Before preparing or validating Memory:

1. Read `ACTIVE_PROJECT_ROOT/project-memory/README.md` completely when it exists and treat it as the project-local contract.
2. Otherwise read `references/memory-format.md` relative to this `SKILL.md` as the fallback contract.
3. Inspect `project-memory/index.md` only after loading the contract. Do not scan all Capsules as a substitute for a valid index.
4. Discover project-local index generation and validation commands from the contract and current manifest. Do not copy command names from another repository.

If the local contract conflicts with the fallback, follow the local contract and report the difference. If the local contract, generated index, and Capsule metadata disagree, stop before proposing content.

## Routing boundary

- Run only after an explicit request to create or maintain Feature/Learning Memory, a promotion request, or confirmation of a Learning Candidate. Candidate collection itself does not invoke a long-term write.
- Accept a direct request or routing from `using-lazyspec`.
- Do not automatically distill or mutate Memory when a final task completes. Task workflows collect Learning Candidates in tasks.md/plan.md and report affected Capsule candidates only.
- Treat a request for an existing Feature as maintenance review, not permission to overwrite it silently.

## Gate before preview

Keep all analysis and candidate text in the preview artifact until the gate passes; do not write under `project-memory/`:

1. Resolve the source mode and read its complete artifacts: normal `requirements.md`, `design.md`, and `tasks.md`; fast `plan.md`, without requiring or creating the three-file Spec. Inspect the candidate and current implementation/tests as applicable.
2. For Feature Memory, verify that every task checkbox, including nested checkboxes, is `[x]` or `[X]` and Feature Verification is current and passed (including required human confirmation). Legacy evidence must be re-established rather than trusting checkboxes.
3. For Learning Memory, completion of the source feature is not required. Require current, attributable results supporting each bounded observation and any recommended practice. A failed attempt can support a failure observation, not feature success or an untested fix. Keep an unverified remedy as a candidate, not active guidance.
4. Obtain explicit confirmation that the named Feature, Learning Candidate, or existing Capsule may be distilled or maintained. A promotion request supplies this intent, not approval of an unseen write set. Do not infer it from task approval, silence, or file state.
5. Check the worktree. If relevant implementation has uncommitted changes, include them in the evidence and preview; never present the previous commit as the verified implementation. A command name, old result, skipped check, or checkbox is not verification evidence.

On any failure, report the exact path, task, check, or confirmation missing and write nothing under `project-memory/`.

## Build an evidence matrix

Reconcile each candidate claim against approved intent and current implementation. Keep the complete matrix in the preview artifact; summarize its outcome in the conversation only:

| Claim | Spec anchors | Implementation evidence | Test evidence | Existing owner | Result |
|---|---|---|---|---|---|
| <claim> | <requirements/design/tasks> | <path and symbol> | <path and current result> | <Capsule and decision ID, if any> | supported / conflict / insufficient |

- For Feature facts, require at least one approved Spec anchor (or approved fast plan section) and one current implementation or test source for every factual claim. For Learning, require an approved intent reference plus attributable observation/check evidence, including failure evidence where relevant; do not require a feature-wide pass. Cite persisted evidence in the task/plan report and verify it against the current sources. User confirmation alone cannot validate a factual claim.
- Use current architecture documents as navigation, then verify against source and tests.
- Stop on a material conflict and ask for a ruling. A user ruling may resolve a conflict but cannot replace all evidence.
- Omit facts cheaper to recover from current code, temporary progress, command transcripts, and generic lessons. Learning must specify applicability, observed problem, evidenced explanation, validated practice or bounded negative guidance, sources, limits, and revisit conditions. A single success supports only the tested conditions.

## Select one owner for each decision

Use index feature or learning ID, summary, tags, Source Spec, and authorities to select only potentially overlapping Capsules, then read those Capsules completely.

- Keep one active owner for each durable decision. Do not duplicate an existing claim merely because a new Feature touched it.
- For the same Feature or Learning, propose a maintenance revision that preserves `distilled_at`, updates `reviewed_at`, and changes only evidence-backed current guidance.
- When a new Feature changes an existing owner, include the affected Capsule revision or status transition in the same preview.
- Use `needs-review` when drift is suspected but cannot yet be reconciled. Exclude it from ordinary recall.
- Use `superseded` only when a resolvable replacement owns the whole conclusion; update reciprocal relationships atomically.
- Use `obsolete` when the conclusion is invalid and has no replacement.
- Never edit the body of `superseded` or `obsolete` Capsules. Git and source Specs preserve history for maintained active Capsules.

## Preview and approval

The preview artifact is the approval object. Make it available to the user, and summarize it in Chinese in the chat without reproducing its full contents:

- Include every complete proposed Capsule, including frontmatter, body, sources, and stable decision IDs in the preview artifact;
- include the complete generated index or exact index change;
- include every status and reciprocal relationship change;
- include the evidence matrix summary, conflicts, and user rulings; and
- include the complete project-root-relative logical write set.

Ask for explicit approval of that exact preview artifact, unless the current conversation already explicitly approved this identical complete candidate and exact Capsule/index write set. Do not ask twice for the same authorized write. Any requested edit invalidates the previous approval: revise the artifact, provide its new path or identifier, and summarize the changes. Completion confirmation is not preview approval, and one preview never authorizes another Feature.

## Write and verify atomically

After approval:

1. Write only the approved Capsule, local contract, and index paths under `ACTIVE_PROJECT_ROOT/project-memory/`.
2. Run the project-local index generator when provided; otherwise produce the fallback deterministic index exactly as specified by the active contract.
3. Run the project-local Memory validator and relevant repository checks discovered from the manifest and contract.
4. Re-read every changed Capsule and the index; verify metadata, required sections, sources, status equality, authority paths, stable decision IDs, and reciprocal relationships.
5. Report partial writes or validation failures with exact file state and stop without claiming success.

Never create draft/staging Memory under project-memory/, Topic aggregation, session archives, copied Specs, or a second/JSON index unless the project-local contract explicitly replaces this fallback model. Learning Capsules use project-memory/learnings/; unapproved candidates stay in the source tasks.md/plan.md. Do not automatically edit AGENTS.md, skills, permissions, or project configuration.

## Status rules

- `active`: current and default-retrievable; omit `status_reason` and `superseded_by`.
- `needs-review`: suspected drift; require `status_reason`; allow an evidence-backed body revision before returning to `active`.
- `superseded`: terminal; require `status_reason` and reciprocal `superseded_by`.
- `obsolete`: terminal; require `status_reason` and no `superseded_by`.

Allow `active → active` maintenance, `active → needs-review`, `needs-review → active`, and `active` or `needs-review → superseded|obsolete`. Do not reactivate terminal Capsules; create a new owner instead.

## Write boundary

- Keep evidence and candidate content in the linked preview artifact before exact preview approval; do not paste the full payload into the conversation.
- Treat all approved Capsule revisions, status relationships, and the generated index as one logical write set.
- Do not delete, move, rename, or overwrite source Specs.
- Stop after the requested Memory operation; do not begin another Feature automatically.
- If a project-local contract does not support Learning Capsules, prepare its minimal extension in the same preview for explicit approval before writing; never silently override it or migrate unrelated legacy Capsules.
