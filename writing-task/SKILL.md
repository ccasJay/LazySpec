---
name: writing-task
description: Create or revise a LazySpec tasks.md with executable success criteria and feature checks. Obtain combined low-risk Spec approval or medium/high Tasks approval, then stop without implementation.
---

# Writing Tasks

## Shared risk policy

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md) before this workflow; resolve it relative to this Skill directory. It determines low-risk combined approval versus medium/high phase gates, and fast critical-operation confirmation. Also read [delivery-loop.md](../using-lazyspec/references/delivery-loop.md) for executable success criteria, Feature Verification, repair, and Learning Candidates.

## Rule
- The output content should all be in chinese, except the key word from the project

Before starting, read the complete `specs/{feature_name}/requirements.md` and `specs/{feature_name}/design.md`, then read `task-prompt.md` and `task-templete.md`. Resolve the Prompt and Template relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve the upstream Specs and the new `tasks.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before reading or writing Specs. These rules apply unchanged in a Plugin cache and an Agent Skills installation. For medium/high risk, if either upstream artifact has not received explicit user approval in the current conversation, stop and request the missing approval first; never infer approval from file existence. Low risk uses both complete drafts and obtains combined approval here.

Format every requirement number in each task's Requirements list as its own relative Markdown link: `[<requirement-number>.<criterion-number>](./requirements.md#req-<requirement-number>-<criterion-number>)`. Link multiple requirement numbers separately; never leave a requirement number as plain text or combine multiple numbers in one link.

Before requesting Tasks approval, validate every requirement link against `requirements.md`. Each link MUST use the exact relative-path format above, MUST NOT use an absolute path or a `#L<n>` line anchor, and its target HTML anchor MUST exist exactly once. Fix plain-text references, malformed links, missing anchors, and duplicate anchors before asking for approval.

## Approval

After every Tasks plan revision, request approval using this protocol. For low risk the object is both Requirements/Design summaries and their body consistency plus the complete Tasks plan including Planned Checks; adapt the question and option descriptions to name this combined package. For medium/high risk the object is Tasks. Evidence updates and Learning Candidates alone do not require Tasks approval:

1. If `AskUserQuestion` is available, call it with exactly this supported input shape and no extra fields:

   ```json
   {
     "questions": [{
       "question": "Do the tasks look good?",
       "header": "Review",
       "options": [
         {"label": "Approve", "description": "Approve Tasks and finish the planning workflow."},
         {"label": "Request changes", "description": "Keep the current phase and revise Tasks from my feedback."}
       ],
       "multiSelect": false
     }]
   }
   ```

2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields that tool supports.
3. Otherwise, ask the same approval question directly in the conversation and stop while awaiting the answer.

Only explicit approval in the current conversation records Tasks approval (and all three documents for a low-risk combined package). File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval. For any non-approval response, remain in Tasks; apply requested changes when provided and request approval again. Approval ends planning and MUST NOT start implementation.

## Plan Shape and Size

- Format every task line as `- [ ] //TODO <number>. <task text>` in a numbered checkbox list with at most two hierarchy levels. Use top-level epics only when they clarify grouping; number sub-tasks with decimal notation.
- Keep the `//TODO` marker and its task text exactly as shown in the template. Completing a task changes only the checkbox token from `[ ]` to `[x]`; never remove, replace, or rewrite `//TODO` or any text after it.
- Prefer a flat, minimal sequence of discrete coding steps that build incrementally and validate core behavior early.
- Give each task a concrete implementation objective, scenario/input with observable success criteria, and discovered command or specific test entry point. Label new tests as to-be-implemented. Normally use no more than 3 descriptive bullets, excluding the Requirements link line. An exit code or “tests pass” alone is not a success criterion.
- Link only the acceptance criteria directly implemented by the task, normally no more than 5. Split an oversized task when that creates meaningful independent work rather than using a long reference list.
- Ensure every acceptance criterion is linked by at least one task across the complete plan. Perform this task-link coverage check internally; do not add a second traceability matrix. Feature Verification separately maps acceptance outcomes to checks and actual evidence.
- Assume Requirements and Design remain available during implementation. Do not repeat their behavior, rationale, interfaces, or step-by-step details in Tasks.
- Include only work a coding agent can complete by writing, modifying, or testing code in the coding TODO list. Exclude user testing, deployment, metrics gathering, running manual end-to-end flows, training, documentation, business-process changes, and communication work; automated end-to-end tests are allowed.
- Use test-driven ordering where appropriate and leave every step integrated, with no hanging or orphaned code.
- If a requirement or design gap prevents an actionable task, route to the earliest affected phase under delivery-loop.md rather than padding the task with assumptions.
- Append Feature Verification with approved Planned Checks and an initially unexecuted Latest Result, following delivery-loop.md. Cover all acceptance outcomes, composed flows, risk requirements, and necessary human checks outside the coding TODO list. Add Learning Candidates only when execution yields useful evidence.
- Modify the tasks plan when the user requests changes; a non-approval response alone does not require speculative edits.
- Request explicit approval after every revision of the task plan, not after execution evidence or candidate updates.
- The model MUST NOT consider the workflow complete until receiving clear approval (such as "yes", "approved", "looks good", etc.).
- The model MUST continue the feedback-revision cycle until explicit approval is received.
- The model MUST stop once the task document has been approved.

**This workflow is ONLY for creating design and planning artifacts. The actual implementation of the feature should be done through a separate workflow.**

- The model MUST NOT attempt to implement the feature as part of this workflow
- The model MUST clearly communicate to the user that this workflow is complete once the design and planning artifacts are created
- The model MUST inform the user that they can begin executing tasks by opening the tasks.md file, or by asking to execute a specific task from tasks.md (e.g. "start task 1.1" / "execute next task").
