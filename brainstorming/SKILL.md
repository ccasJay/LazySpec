---
name: brainstorming
description: Explore and clarify a feature in the current session before LazySpec creates its first requirements.md, or when the user explicitly requests brainstorming for an existing Spec. Use to inspect relevant project context, compare three approaches, obtain explicit approval, and prepare an approved session-only context for writing-requirement.
---

# Brainstorming

Turn a feature idea into an explicitly approved direction that LazySpec can use as the input to `writing-requirement`. Keep every result in the current conversation context only.

## Rule
- The output content should all be in chinese, except the key word from the project

## Human-First Interaction

- Use plain-language Chinese by default and lead with the user-visible result. Explain the implementation mechanism only when it changes the current choice.
- Ask each question to make exactly one decision. Say what the decision affects before listing the options.
- Name options by the result the user will notice, then describe the main experience, cost, risk, or compatibility trade-off.
- If the user actively uses technical terms or asks for deeper detail, match that level without becoming verbose or losing the result-first framing.
- Briefly explain every necessary technical term the first time it appears.
- Hide type names, internal field names, Requirement IDs, file paths, and Agent work protocols by default. Show them only when they affect the user's choice or the user explicitly asks for them.
- Do not omit the feature's scope, observable behavior, constraints, risks, or success criteria when simplifying the language.
- Before sending a question, comparison, or approval view, self-check that the decision, option consequences, and recommendation reason are easy to understand. Rewrite the message before sending if they are not.

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
     [用一句白话说明现在只需要决定什么，以及这个决定会影响什么]

     1. [按用户结果命名的推荐选项]（推荐）— [会得到什么，以及主要代价或风险]
     2. [按用户结果命名的第二选项] — [会得到什么，以及主要代价或风险]
     3. [按用户结果命名的第三选项] — [会得到什么，以及主要代价或风险]
     4. 其他 — 用自己的话回答
     ```

   - Put the recommended option first and explain the recommendation concisely.
   - Prefer an applicable question-and-answer tool when one is available. If the tool automatically adds a free-form `Other` choice, provide exactly the first three predefined options and use the automatic choice as option 4. If the tool cannot preserve this structure, ask the question directly in the conversation.
   - Accept either an option number or the user's free-form answer.
   - Continue until the required context is complete and no unresolved question would materially change the result.

3. Compare approaches.
   - Present exactly three viable approaches with their relevant trade-offs.
   - For each approach, show only `用户会得到什么`, `主要限制或风险`, and `适用条件` in the user-facing comparison.
   - Name each approach by its user-visible result rather than its implementation pattern.
   - Recommend one approach and explain the reason concisely in terms of the user's stated goal and constraints.
   - Include technical details only when they materially affect the selection; otherwise leave them to Design.
   - Avoid speculative features and unrelated improvements.

4. Obtain approval.
   - First ask the user to select one of the three compared approaches. Selecting an approach records only `selectedApproach`; it is not approval of the complete Brainstorming Context.
   - After the selection, present the complete user-facing Context with exactly these headings. Put included scope under `包含` and excluded scope under `不包含`; do not show internal field names in this approval view:

     ```text
     目标
     包含
     不包含
     必须遵守
     完成表现
     选定方案
     ```

   - Then ask a separate approval question with these three predefined options plus the free-form option:

     ```text
     是否批准以上需求方向并进入 Requirements？

     1. 批准并进入 Requirements（推荐）— 以上方向成为 Requirements 的输入
     2. 修改内容 — 留在 Brainstorming，根据反馈修改后重新确认
     3. 重新比较方案 — 放弃当前选择，返回三个方案的比较
     4. 其他 — 用自己的话回答
     ```

   - Prefer the applicable user-question tool under the question rules above. Only option 1 or an unambiguous affirmative answer to this separate approval question counts as approval. Approach selection, silence, timeout, explanation, or an ambiguous answer does not.
   - If the user requests changes, revise the approaches or continue clarifying one question at a time, then present the complete context and ask the separate approval question again.
   - Do not set `approved: true` or proceed to `writing-requirement` until the selected approach and the complete context receive this separate explicit approval.

5. Prepare the session handoff.
   - Map the six user-facing headings to the unchanged internal schema as follows: `目标` → `objective`; `包含` and `不包含` → `scope`; `必须遵守` → `constraints`; `完成表现` → `successCriteria`; `选定方案` → `selectedApproach`.
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
