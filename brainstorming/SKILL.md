---
name: brainstorming
description: Explore and clarify a feature in the current session before LazySpec creates its first requirements.md, or when the user explicitly requests brainstorming for an existing Spec. Use to inspect relevant project context, compare three approaches, obtain explicit approval, and prepare an approved session-only context for writing-requirement.
---

# Brainstorming

Turn a feature idea into an explicitly approved direction that LazySpec can use as the input to `writing-requirement`. Keep every result in the current conversation context only.

## Workflow

1. Inspect the project context.
   - Read only the project files, documentation, and existing Spec context directly related to the feature.
   - Determine whether the requested scope is suitable for one Spec.
   - If the scope contains multiple independent subsystems, propose a decomposition and brainstorm one bounded subsystem at a time.

2. Clarify the idea.
   - Establish the objective, scope, constraints, and success criteria.
   - Ask only one question at a time when information is missing or ambiguous.
   - For every user-facing question, provide exactly three concrete, mutually exclusive predefined options and a fourth free-form option using this structure:

     ```text
     [Question]

     1. [Recommended option] (Recommended) — [concise reason]
     2. [Second option] — [relevant trade-off]
     3. [Third option] — [relevant trade-off]
     4. Other — provide your own answer
     ```

   - Put the recommended option first and explain the recommendation concisely.
   - Prefer an applicable question-and-answer tool when one is available. If the tool automatically adds a free-form `Other` choice, provide exactly the first three predefined options and use the automatic choice as option 4. If the tool cannot preserve this structure, ask the question directly in the conversation.
   - Accept either an option number or the user's free-form answer.
   - Continue until the required context is complete and no unresolved question would materially change the result.

3. Compare approaches.
   - Present exactly three viable approaches with their relevant trade-offs.
   - Recommend one approach and explain the reason concisely.
   - Avoid speculative features and unrelated improvements.

4. Obtain approval.
   - Ask the user to explicitly select or approve an approach using the same three predefined options plus option 4 for a free-form answer.
   - If the user requests changes, revise the approaches or continue clarifying one question at a time.
   - Do not proceed to `writing-requirement` until the selected approach and the complete context are explicitly approved.

5. Prepare the session handoff.
   - Retain only the final approved result in the current conversation context with all of these fields:

     ```text
     objective
     scope
     constraints
     successCriteria
     selectedApproach
     approved: true
     ```

   - Keep each field concise. Exclude rejected approaches, exploratory reasoning, raw notes, and information already captured by another field.
   - Pass the selected approach as a constraint on Requirements; do not turn its implementation details into user-facing requirements.
   - Set `approved` to `true` only after explicit user approval.
   - When this skill ran before the first `requirements.md`, allow `using-lazyspec` to route the approved context to `writing-requirement`.
   - When the user manually invoked this skill during an existing Requirements, Design, Tasks, or task-execution stage, stop after updating the session context. Modify a Spec artifact only after a separate explicit user request.

## Session-Only Boundary

- Do not create a Brainstorming document, Design document, temporary file, or any other persistent artifact.
- Do not use a file as storage or recovery for the approved context.
- If the context is interrupted or lost before `writing-requirement` consumes it, run this workflow again and obtain fresh approval.
- Do not commit to Git, invoke `writing-plans`, write requirements directly, or enter implementation.
