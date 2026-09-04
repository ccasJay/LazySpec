---
name: writing-requirement
description: Create or revise a LazySpec requirements.md after approved brainstorming context is available for a new feature, or when editing existing requirements. Use to produce EARS requirements, obtain explicit approval, and hand off only approved requirements to writing-design.
---

# Writing Requirements

## Language

- Keep the instructional prose in this Skill and its supporting resources in English.
- Write all user-visible prose in generated `requirements.md` content in Chinese, including the title, headings, introduction, user stories, and acceptance criteria.
- Preserve project-specific names, code identifiers, filenames, Markdown syntax, and HTML anchor IDs when necessary.

For a new feature, require one explicitly approved input from the current session before creating `requirements.md`: either a complete `BrainstormingContext` or a non-empty, explicitly approved `CodexPlanArtifact` received from the `using-lazyspec` Codex Plan Mode adapter. A standard `BrainstormingContext` must contain the confirmed objective, scope, constraints, success criteria, and selected approach. A `CodexPlanArtifact` is valid only with `source: "codex-plan-mode"`, a non-empty `content`, and `approved: true`; it does not need those five fields, fixed sections, or an extra header. If the selected input is missing, incomplete, unapproved, invalid, or lost, do not create or update `requirements.md`; return to the router for the appropriate clarification or standard `brainstorming` path. Never infer or restore either input from disk.

When the input is a `CodexPlanArtifact`, use its complete `content` as the Requirements context. Preserve the original Markdown, line breaks, and long text exactly while passing it through the session; do not summarize, rewrite, normalize, truncate, or require a schema before deriving observable requirements. Plan approval is not Requirements approval. If the plan leaves a material gap, remain in Requirements and ask a targeted clarification question before drafting or advancing.

For an existing `requirements.md`, use the existing document and explicit user feedback. Do not automatically rerun Brainstorming.

Before drafting or revising requirements, read `requirement-prompt.md` and `requirement-templete.md`. Resolve both files relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve `specs/{feature_name}/requirements.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before writing. These rules apply unchanged in a Plugin cache and an Agent Skills installation.

Prefix every numbered acceptance criterion with exactly one HTML anchor on the same line, using `req-<requirement-number>-<criterion-number>` as the unique ID. The numbers MUST match the criterion's requirement and ordinal, every acceptance criterion MUST have an anchor, and each anchor ID MUST occur exactly once in `requirements.md`.

## Human-First Review Summary

- Put `## 审批摘要` immediately after the document title and before `## 引言`, with the Chinese subsections `目标`, `范围`, `核心行为`, and `风险与待确认`.
- Treat this summary as the user-facing approval contract. The detailed user stories and EARS criteria may elaborate it, but MUST NOT add, omit, broaden, narrow, or contradict a material behavior, boundary, or risk.
- Cover every materially distinct acceptance outcome in the summary. Group multiple criteria only when one concise statement preserves the same approval intent; keep HTML anchors and traceability links out of the summary.
- Adapt summary length to cognitive complexity rather than a fixed numerical budget. Aim for a complete one-screen review. If that is impossible without concealing material information, stop before approval and recommend splitting the Spec; expand only after the user explicitly keeps one Spec.
- Resolve every material open question before requesting approval. Use `风险与待确认` to state known risks and explicitly record that no material decision remains unresolved.
- On a material revision, replace the summary with the complete current version and present a concise additions/changes/removals/risk delta in the conversation. A material change invalidates prior approval; a verified non-material body-only refinement does not.
- For a legacy Requirements document without `审批摘要`, add the summary only when that document is next revised. Do not rewrite already approved legacy Requirements merely because a downstream phase reads it.

## Approval

After creating Requirements or making a material revision, request approval using this protocol:

1. If `AskUserQuestion` is available, call it with exactly this supported input shape and no extra fields:

   ```json
   {
     "questions": [{
       "question": "审批摘要是否准确覆盖了需求的目标、范围、核心行为与风险？",
       "header": "Review",
       "options": [
         {"label": "Approve", "description": "批准当前摘要表达的实质需求，并允许进入 Design。"},
         {"label": "Request changes", "description": "留在 Requirements，根据反馈更新摘要与正文。"}
       ],
       "multiSelect": false
     }]
   }
   ```

2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields that tool supports.
3. Otherwise, ask the same approval question directly in the conversation and stop while awaiting the answer.

Only explicit approval in the current conversation records approval of the current `审批摘要` and its consistency with the detailed Requirements body. It does not mean the user approved every non-material implementation detail. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval. For any non-approval response, remain in Requirements; apply requested changes when provided and request approval again. Any material change invalidates prior approval; a verified non-material body-only refinement does not.

## Content Boundaries and Size

- Write only observable behavior, user-visible constraints, and verifiable outcomes. Do not include architecture, component boundaries, file changes, implementation steps, or speculative improvements.
- Consolidate overlapping behavior into one requirement instead of creating separate requirements for normal flow, edge cases, user experience, technical constraints, and success criteria when they describe the same outcome.
- Target at most 8 requirements, 2–5 acceptance criteria per requirement, and 30 acceptance criteria in total.
- Treat these targets as soft limits. Exceed them only when merging would lose distinct approved behavior; first consider narrowing or splitting the Spec, and explain any necessary exception in the conversation rather than the document.
- Keep the introduction to one short paragraph. Other than the required `审批摘要`, do not add summaries, glossaries, traceability tables, or repeated context unless the user explicitly needs them.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/requirements.md' file under the project folder if it doesn't already exist
- The model MUST generate an initial version of the requirements document based on the user's rough idea WITHOUT asking sequential questions first
- The model MUST express EARS semantics naturally in Chinese and MUST NOT copy the literal English EARS keywords `WHEN`, `THEN`, or `SHALL` into the generated document.
- The model MUST format the initial requirements.md document with:
- A Human-First `审批摘要` before the introduction, followed by a clear introduction section that summarizes the feature
- A hierarchical numbered list of requirements where each contains:
  - A user story written in Chinese using the role-goal-benefit structure
  - A numbered list of acceptance criteria in EARS format (Easy Approach to Requirements Syntax)
- The model SHOULD include an edge case, user-experience constraint, technical constraint, or success criterion only when it creates a distinct observable and verifiable outcome
- The model MUST make modifications to the requirements summary and body if the user requests changes or does not explicitly approve
- The model MUST ask for explicit approval after every material iteration of edits to the requirements document; verified non-material body-only refinements preserve approval
- The model MUST NOT proceed to the design document until receiving clear approval (such as "yes", "approved", "looks good", etc.)
- The model MUST continue the feedback-revision cycle until explicit approval is received
- The model SHOULD identify only gaps that would materially change observable behavior; it MUST NOT suggest speculative expansion by default
- The model MAY ask targeted questions about specific aspects of the requirements that need clarification
- The model MAY suggest options when the user is unsure about a particular aspect
- The model MUST proceed to the design phase after the user accepts the requirements

## Troubleshooting

### Requirements Clarification Stalls

If the requirements clarification process seems to be going in circles or not making progress:

- The model SHOULD suggest moving to a different aspect of the requirements
- The model MAY provide examples or options to help the user make decisions
- The model SHOULD summarize what has been established so far and identify specific gaps
- The model MAY suggest conducting research to inform requirements decisions
