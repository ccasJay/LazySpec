---
name: writing-requirement
description: Create or revise EARS requirements from approved brainstorming or native planning input. Draft toward combined review, asking earlier only for unresolved material decisions or user-requested phase gates.
---

# Writing Requirements

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [doc-policy.md](../using-lazyspec/references/doc-policy.md) before this workflow; resolve them relative to this Skill directory. risk-policy.md separates risk-based verification from decision-based approval and defines model autonomy within the user's scope; approval-policy.md is the single source of explicit-approval, materiality, invalidation, summary-contract, and approval-asking semantics; doc-policy.md keeps the document minimum-sufficient.

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
- Treat this summary as the user-facing approval contract under approval-policy.md. The detailed user stories and EARS criteria may elaborate it, but MUST NOT add, omit, broaden, narrow, or contradict a material behavior, boundary, or risk.
- Cover every materially distinct acceptance outcome in the summary. Group multiple criteria only when one concise statement preserves the same approval intent; keep HTML anchors and traceability links out of the summary.
- Resolve every material open question before requesting approval. Use `风险与待确认` to state known risks and explicitly record that no material decision remains unresolved.
- For a legacy Requirements document without `审批摘要`, add the summary only when that document is next revised. Do not rewrite already approved legacy Requirements merely because a downstream phase reads it.

## Approval

Finish the Requirements draft and continue toward combined review unless an unresolved material decision or user-requested phase gate requires approval here. Reuse explicit decisions already supplied by the user. When approval is needed, follow approval-policy.md's asking protocol and ask: "审批摘要是否准确覆盖了需求的目标、范围、核心行为与风险？" For any non-approval response, remain in Requirements; apply approval-policy.md's explicit-approval, revision-delta, and invalidation semantics.

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
- Continue drafting Design when no unresolved material decision or user-requested phase gate blocks it; never mark an unapproved draft approved
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
