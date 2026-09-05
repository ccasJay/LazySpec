---
name: fast
description: Create or resume a lightweight LazySpec fast/快速 plan when no requirements.md exists. Approve one plan, execute its authorized tasks, verify the feature, and collect learning candidates with risk-based controls.
---

# Fast

Turn a new feature idea into an approved `plan.md` and execute it in one continuous run, skipping the full LazySpec phase pipeline. Use this Skill for first-time fast creation and subsequent execution, verification, or revision of that fast plan; never use it to revise an existing three-document Spec.

## Shared risk policy

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md) before this workflow; resolve it relative to this Skill directory. It determines low-risk combined approval versus medium/high phase gates, and fast critical-operation confirmation. Also read [delivery-loop.md](../using-lazyspec/references/delivery-loop.md) for executable success criteria, Feature Verification, repair, and Learning Candidates.

## Rule
- The output content should all be in chinese, except the key word from the project

## Project Root

Resolve every `specs/{feature_name}/...` path against `ACTIVE_PROJECT_ROOT`, the user's project working directory bound at session start. Never derive `ACTIVE_PROJECT_ROOT` from this Skill's directory, a registered Skill location, the Plugin repository, or a Plugin cache. If invoked directly and the session working directory is unavailable or ambiguous, ask the user for the project root before reading or writing anything.

## Pre-conditions

Before any discussion, inspect the target feature under `ACTIVE_PROJECT_ROOT`:

1. If `specs/{feature_name}/requirements.md` exists, stop. Report in Chinese that this feature already has a Spec and must use the normal LazySpec chain (`brainstorming` / `writing-requirement` and onward); do not create or modify a `plan.md`.
2. If `specs/{feature_name}/plan.md` exists, inspect it and the current request. On an explicit execution request, resume the authorized tasks and missing/stale Feature Verification after confirming applicable plan approval from the conversation; never infer approval from checkboxes. On a verification-only request, run and report checks under delivery-loop.md without implementation repairs. For a status question, report read-only. Otherwise ask whether to resume or revise; never silently overwrite the plan.
3. Only when neither file exists, proceed to discussion.

## Discussion

Discuss interactively and keep it lightweight:

- Establish the objective, scope, constraints, and a concrete implementation approach. Ask only one question at a time when information is missing or ambiguous.
- For every user-facing question, provide exactly three concrete, mutually exclusive predefined options and a fourth free-form option. Put the recommended option first, mark it as recommended, and explain the recommendation concisely; describe the relevant trade-off for each other option. Accept an option number or a free-form answer. Prefer an applicable question-and-answer tool when one is available; if the tool adds its own free-form `Other` choice, provide exactly the first three options.
- Before writing `plan.md`, explicitly present the recommended implementation approach and explain why it best fits the confirmed objective, scope, and constraints. Do not make the user infer the recommendation from option order or from the eventual plan.
- When a different approach would materially change the implementation, present the viable alternatives with their relevant trade-offs and ask the user to choose, with the recommended approach first. Otherwise, state the single recommended approach and proceed without forcing a three-approach comparison.
- Stop asking once no unresolved question would materially change the plan.

## Writing plan.md

Write exactly one artifact: `specs/{feature_name}/plan.md` under `ACTIVE_PROJECT_ROOT`, with these sections (all prose in Chinese):

1. **Objective** — one or two sentences describing the observable outcome.
2. **Constraints** — only constraints that change implementation decisions.
3. **Approach** — the selected implementation approach and its key decisions.
4. **Tasks** — a numbered checkbox list; format every task line as `- [ ] //TODO <number>. <task text>` with at most two hierarchy levels and decimal numbering for sub-tasks. Use at most 3 descriptive sub-bullets: implementation objective, scenario/input with observable success criteria, and discovered command or specific test entry point (new tests explicitly to-be-implemented).
5. **Feature Verification** — Planned Checks covering Objective, Constraints, task criteria, composed flows and risk, plus an initially unexecuted Latest Result. Follow delivery-loop.md; this is not a TODO.

Record risk level, reasons, and critical operations in Constraints/Approach. During execution append Learning Candidates only when useful evidence exists.

Keep the plan minimal and directly executable. Exclude user testing, deployment, documentation, and communication work from coding Tasks; automated tests are allowed. Necessary human acceptance checks belong in Feature Verification. Do not create `requirements.md`, `design.md`, `tasks.md`, or any other artifact.

## Approval

After writing or revising `plan.md`, request approval using this protocol:

1. If `AskUserQuestion` is available, call it with only its supported `questions` input. Use one question object with `question`, `header`, `options`, and `multiSelect`; use `Review` as the header, the two single-choice options `Approve` and `Request changes`, and `multiSelect: false`. Do not add unsupported top-level or question fields.
2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields supported by that tool.
3. Otherwise, ask the approval question directly in the conversation and stop while awaiting the answer.

Only explicit approval in the current conversation (a clear "yes", "approved", selecting `Approve`, or equivalent affirmative response) records approval. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval. For requested plan changes, revise `plan.md` from the feedback and request approval again. Silence or an explanation is not approval and does not require speculative edits. Evidence/candidate updates do not revise the approved plan. Never start execution before explicit approval.

## Execution

After explicit approval, execute the plan continuously:

- For the initial approved run, execute every task in order until all are complete; do not pause between tasks for confirmation. On a later request explicitly limited to a task subset, honor that subset and the shared verification scope boundary.
- Verify each task's implementation against its stated behavior and verification before moving on.
- When a task completes, change only its checkbox token in `plan.md` from `[ ]` to `[x]`. Preserve `//TODO` and every character after it exactly; never remove, replace, or rewrite the task text.
- Follow delivery-loop.md for failures: autonomously repair implementation errors within scope while progressing; route genuine plan gaps to Objective/Constraints, Approach, or Tasks and approve the revised plan before continuing. Apply the two-round no-progress stopping condition and risk-policy.md critical-operation confirmations.

## Handoff

When all checkboxes are checked, run Feature-level Verification and collect valuable Learning Candidates under delivery-loop.md, then report in Chinese:

- TODO completion separately from feature status/freshness, current evidence, required human acceptance, and remaining work. Pending or blocked verification is not feature success.
- Inspect only the Project Memory index (`project-memory/index.md`) for Capsules whose feature, tags, summary, Source Spec, or authorities overlap the changed paths, and report likely impact candidates. Do not create, edit, or re-status Memory without a separate explicit distillation or maintenance request.
- Note that the feature used fast mode and has no `requirements.md` / `design.md` / `tasks.md`; suggest the normal chain if the feature later needs a full Spec.
