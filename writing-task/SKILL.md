---
name: writing-task
description: Create or revise a LazySpec tasks.md only after requirements.md and design.md have explicit user approval. Use to turn an approved design into a code-focused implementation plan, obtain explicit tasks approval, and stop without implementing the planned tasks.
---

# Writing Tasks

Before starting, read the approved `specs/{feature_name}/requirements.md` and `specs/{feature_name}/design.md`, then read `task-prompt.md` and `task-templete.md`. If either upstream artifact has not received explicit user approval, stop and request the missing approval first.

Format every requirement number in each task's Requirements list as its own relative Markdown link: `[<requirement-number>.<criterion-number>](./requirements.md#req-<requirement-number>-<criterion-number>)`. Link multiple requirement numbers separately; never leave a requirement number as plain text or combine multiple numbers in one link.

Before requesting Tasks approval, validate every requirement link against `requirements.md`. Each link MUST use the exact relative-path format above, MUST NOT use an absolute path or a `#L<n>` line anchor, and its target HTML anchor MUST exist exactly once. Fix plain-text references, malformed links, missing anchors, and duplicate anchors before asking for approval.

## Plan Shape and Size

- Format the plan as a numbered checkbox list with at most two hierarchy levels. Use top-level epics only when they clarify grouping; number sub-tasks with decimal notation.
- Keep the `//TODO` marker and its task text exactly as shown in the template. Completing a task changes only its checkbox state; never remove or replace the text after `//TODO`.
- Prefer a flat, minimal sequence of discrete coding steps that build incrementally and validate core behavior early.
- Give each task a concrete writing, modification, or automated-testing objective. Add only the descriptive sub-bullets needed to identify affected components or files, essential behavior, and verification; normally use no more than 3, excluding the Requirements link line.
- Link only the acceptance criteria directly implemented by the task, normally no more than 5. Split an oversized task when that creates meaningful independent work rather than using a long reference list.
- Ensure every acceptance criterion is linked by at least one task across the complete plan. Perform this coverage check internally; do not add a traceability matrix or duplicate coverage summary.
- Assume Requirements and Design remain available during implementation. Do not repeat their behavior, rationale, interfaces, or step-by-step details in Tasks.
- Include only work a coding agent can complete by writing, modifying, or testing code. Exclude user testing, deployment, metrics gathering, running manual end-to-end flows, training, documentation, business-process changes, and communication work; automated end-to-end tests are allowed.
- Use test-driven ordering where appropriate and leave every step integrated, with no hanging or orphaned code.
- If a requirement or design gap prevents an actionable task, offer to return to the relevant upstream phase instead of padding the task with assumptions.
- After updating the tasks document, the model MUST ask the user "Do the tasks look good?" using the AskUserQuestion tool (Claude Code).
- The AskUserQuestion tool MUST be used; set metadata.source to the exact string 'spec-tasks-review'
- The model MUST make modifications to the tasks document if the user requests changes or does not explicitly approve.
- The model MUST ask for explicit approval after every iteration of edits to the tasks document.
- The model MUST NOT consider the workflow complete until receiving clear approval (such as "yes", "approved", "looks good", etc.).
- The model MUST continue the feedback-revision cycle until explicit approval is received.
- The model MUST stop once the task document has been approved.

**This workflow is ONLY for creating design and planning artifacts. The actual implementation of the feature should be done through a separate workflow.**

- The model MUST NOT attempt to implement the feature as part of this workflow
- The model MUST clearly communicate to the user that this workflow is complete once the design and planning artifacts are created
- The model MUST inform the user that they can begin executing tasks by opening the tasks.md file, or by asking to execute a specific task from tasks.md (e.g. "start task 1.1" / "execute next task").
