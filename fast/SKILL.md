---
name: fast
description: Create and execute a lightweight LazySpec plan for a brand-new feature without the full Brainstorming → Requirements → Design → Tasks pipeline. Use when the user asks for the fast/快速 mode, or when routed by using-lazyspec for a feature that has no existing requirements.md, to discuss interactively, write specs/{feature_name}/plan.md, obtain one explicit approval, and then execute all planned tasks continuously.
---

# Fast

Turn a new feature idea into an approved `plan.md` and execute it in one continuous run, skipping the full LazySpec phase pipeline. Use this Skill only for first-time creation of a feature; never use it to revise an existing Spec.

## Rule
- The output content should all be in chinese, except the key word from the project

## Project Root

Resolve every `specs/{feature_name}/...` path against `ACTIVE_PROJECT_ROOT`, the user's project working directory bound at session start. Never derive `ACTIVE_PROJECT_ROOT` from this Skill's directory, a registered Skill location, the Plugin repository, or a Plugin cache. If invoked directly and the session working directory is unavailable or ambiguous, ask the user for the project root before reading or writing anything.

## Pre-conditions

Before any discussion, inspect the target feature under `ACTIVE_PROJECT_ROOT`:

1. If `specs/{feature_name}/requirements.md` exists, stop. Report in Chinese that this feature already has a Spec and must use the normal LazySpec chain (`brainstorming` / `writing-requirement` and onward); do not create or modify a `plan.md`.
2. If `specs/{feature_name}/plan.md` exists, stop. Report in Chinese that a fast plan already exists, and ask whether to continue executing its remaining unchecked tasks or to discard it and discuss a new plan. Never silently overwrite an existing `plan.md`.
3. Only when neither file exists, proceed to discussion.

## Discussion

Discuss interactively and keep it lightweight:

- Establish the objective, scope, constraints, and a concrete implementation approach. Ask only one question at a time when information is missing or ambiguous.
- For every user-facing question, provide exactly three concrete, mutually exclusive predefined options and a fourth free-form option. Put the recommended option first, mark it as recommended, and explain the recommendation concisely; describe the relevant trade-off for each other option. Accept an option number or a free-form answer. Prefer an applicable question-and-answer tool when one is available; if the tool adds its own free-form `Other` choice, provide exactly the first three options.
- Before writing `plan.md`, explicitly present the recommended implementation approach and explain why it best fits the confirmed objective, scope, and constraints. Do not make the user infer the recommendation from option order or from the eventual plan.
- When a different approach would materially change the implementation, present the viable alternatives with their relevant trade-offs and ask the user to choose, with the recommended approach first. Otherwise, state the single recommended approach and proceed without forcing a three-approach comparison.
- Stop asking once no unresolved question would materially change the plan.

## Writing plan.md

Write exactly one artifact: `specs/{feature_name}/plan.md` under `ACTIVE_PROJECT_ROOT`, with these sections:

1. **Objective** — one or two sentences describing the observable outcome.
2. **Constraints** — only constraints that change implementation decisions.
3. **Approach** — the selected implementation approach and its key decisions.
4. **Tasks** — a numbered checkbox list; format every task line as `- [ ] //TODO <number>. <task text>` with at most two hierarchy levels and decimal numbering for sub-tasks. Give each task a concrete writing, modification, or automated-testing objective, with at most 3 descriptive sub-bullets identifying affected components or files, essential behavior, and verification.

Keep the plan minimal and directly executable. Exclude user testing, deployment, documentation, and communication work; automated tests are allowed. Do not create `requirements.md`, `design.md`, `tasks.md`, or any other artifact.

## Approval

After writing or revising `plan.md`, request approval using this protocol:

1. If `AskUserQuestion` is available, call it with only its supported `questions` input. Use one question object with `question`, `header`, `options`, and `multiSelect`; use `Review` as the header, the two single-choice options `Approve` and `Request changes`, and `multiSelect: false`. Do not add unsupported top-level or question fields.
2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields supported by that tool.
3. Otherwise, ask the approval question directly in the conversation and stop while awaiting the answer.

Only explicit approval in the current conversation (a clear "yes", "approved", selecting `Approve`, or equivalent affirmative response) records approval. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval. For any non-approval response, revise `plan.md` from the feedback and request approval again. Never start execution before explicit approval.

## Execution

After explicit approval, execute the plan continuously:

- Execute every task in order until all are complete; do not pause between tasks for confirmation.
- Verify each task's implementation against its stated behavior and verification before moving on.
- When a task completes, change only its checkbox token in `plan.md` from `[ ]` to `[x]`. Preserve `//TODO` and every character after it exactly; never remove, replace, or rewrite the task text.
- If a task is blocked by a genuine plan gap, stop, report the gap in Chinese, and ask whether to revise the plan (which requires approval again) before continuing.

## Handoff

When all checkboxes are checked, stop and report in Chinese:

- What was implemented and how it was verified.
- Inspect only the Project Memory index (`project-memory/index.md`) for Capsules whose feature, tags, summary, Source Spec, or authorities overlap the changed paths, and report likely impact candidates. Do not create, edit, or re-status Memory without a separate explicit distillation or maintenance request.
- Note that the feature used fast mode and has no `requirements.md` / `design.md` / `tasks.md`; suggest the normal chain if the feature later needs a full Spec.
