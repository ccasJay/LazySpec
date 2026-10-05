---
name: writing-requirement
description: Collect requirements one at a time with the user, then create or revise an EARS requirements document. Request explicit Requirements approval before LazySpec enters Design.
---

# Writing Requirements

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [doc-policy.md](../using-lazyspec/references/doc-policy.md) before this workflow; resolve them relative to this Skill directory. risk-policy.md separates risk-based verification from decision-based approval and defines model autonomy within the user's scope; approval-policy.md is the single source of explicit-approval, materiality, invalidation, summary-contract, and approval-asking semantics; doc-policy.md keeps the document minimum-sufficient.

## Language

- Keep the instructional prose in this Skill and its supporting resources in English.
- Write all user-visible prose in generated `requirements.md` content in Chinese, including the title, headings, introduction, user stories, and acceptance criteria.
- Preserve project-specific names, code identifiers, filenames, Markdown syntax, and HTML anchor IDs when necessary.

Start directly from the user's request, relevant project facts, and any existing `requirements.md`. User-provided plans are ordinary background material; they do not bypass requirement collection or approve the Requirements document. No separately approved input object or platform-specific planning protocol is required. Respect the host environment's current tool and file-writing restrictions.

Before drafting or revising requirements, read `requirement-prompt.md` and `requirement-templete.md`. Resolve both files relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve `specs/{feature_name}/requirements.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before writing. These rules apply unchanged in a Plugin cache and an Agent Skills installation.

## Requirement Collection

Follow approval-policy.md's `How to ask` protocol for every collection, clarification, and completion question. Keep collection in the current conversation; do not create a collection file or another phase approval gate.

For an existing document, collect only additions, material behavior changes, and removals. Confirm a removal's effect before deleting the requirement. Preserve unchanged requirements and their anchors without asking again. For purely editorial revisions, skip this collection workflow and revise only the requested wording under approval-policy.md's materiality and invalidation rules; do not ask a collection-completion question.

1. Inspect the user's request and directly relevant project evidence. Research discoverable facts before asking. Identify the objective, included and excluded scope, observable behavior, binding constraints, risks, and success criteria; clarify missing intent within this Requirements exchange. Assess the initial risk under risk-policy.md.
2. Propose one candidate requirement at a time. Show only what the requirement is and its concise target behavior. Use plain-language Chinese by default and lead with the user-visible result. Do not show detailed acceptance criteria, formal user stories, requirement IDs, internal fields, or implementation steps in collection questions. Leave architecture, data models, APIs, and other implementation choices to Design unless the user states a binding constraint.
3. Ask the user to confirm, modify, or reject that candidate, then wait for the actual answer before moving to another requirement. For a new document, every requirement MUST be individually asked and explicitly confirmed before inclusion, even when the initial request or a supplied plan already describes it in detail. Do not batch multiple requirements into one tool call or conversation question, or skip this exchange because the background is complete.
4. Incorporate explicit modifications into the candidate; a clear replacement supplied by the user settles that behavior. Clarify an ambiguous answer or a new dependent choice before continuing. Exclude rejected requirements. Silence, timeout, default selections, and tool acknowledgments do not confirm a requirement. Update remaining candidates from the answers rather than following a fixed questionnaire, and do not invent speculative requirements to meet a count.
5. After all candidates are resolved, ask whether the user has additional requirements or wants to finish collection and generate the draft. Wait for explicit confirmation that collection is complete. If the user adds requirements, resume the same one-at-a-time exchange and ask the completion question again when they are resolved.
6. Only after collection is complete, draft and write the complete `requirements.md` once, within the host's permissions. Do not create or incrementally update it while collection is pending. Derive user stories and EARS criteria only from confirmed behavior. If elaboration introduces a new material behavior, boundary, or choice, return to collection before writing the affected revision and reconfirm completion. Do not present inferred details as user-confirmed decisions.

Keep questions concise and decision-focused. Use meaningful mutually exclusive options when useful, explaining their consequences and marking a recommendation only when justified; use a focused free-text question when choices would be artificial. Match the user's technical depth and briefly explain necessary terms without omitting scope, constraints, risks, or success criteria.

Prefix every numbered acceptance criterion with exactly one HTML anchor on the same line, using `req-<requirement-number>-<criterion-number>` as the unique ID. The numbers MUST match the criterion's requirement and ordinal, every acceptance criterion MUST have an anchor, and each anchor ID MUST occur exactly once in `requirements.md`.

## Human-First Review Summary

- Put `## 审批摘要` immediately after the document title and before `## 引言`, with the Chinese subsections `目标`, `范围`, `核心行为`, and `风险与待确认`.
- Treat this summary as the user-facing approval contract under approval-policy.md. The detailed user stories and EARS criteria may elaborate it, but MUST NOT add, omit, broaden, narrow, or contradict a material behavior, boundary, or risk.
- Cover every materially distinct acceptance outcome in the summary. Group multiple criteria only when one concise statement preserves the same approval intent; keep HTML anchors and traceability links out of the summary.
- Resolve open requirements questions before requesting approval. Use `风险与待确认` to state known risks and explicitly record that no requirements decision remains unresolved.
- For a legacy Requirements document without `审批摘要`, add the summary only when that document is next revised. Do not rewrite already approved legacy Requirements merely because a downstream phase reads it.

## Approval

For a new document or material revision, finish the Requirements draft, present its `审批摘要` and body for review, and request explicit Requirements approval before creating any Design document. Confirming individual requirements or finishing collection does not approve the complete document. Reuse collection answers when preparing the review; do not repeat unchanged decisions. Follow approval-policy.md's asking protocol and ask: "审批摘要是否准确覆盖了需求的目标、范围、核心行为与风险？" For any non-approval response, remain in Requirements; apply approval-policy.md's explicit-approval, revision-delta, and invalidation semantics. Purely editorial revisions preserve any still-valid prior document approval under that policy; never infer approval for an unapproved draft.

## Content Boundaries and Size

- Write only observable behavior, user-visible constraints, and verifiable outcomes. Do not include architecture, component boundaries, file changes, implementation steps, or speculative improvements.
- Consolidate overlapping behavior into one requirement instead of creating separate requirements for normal flow, edge cases, user experience, technical constraints, and success criteria when they describe the same outcome.
- Target at most 8 requirements, 2–5 acceptance criteria per requirement, and 30 acceptance criteria in total.
- Treat these targets as soft limits. Exceed them only when merging would lose distinct approved behavior; first consider narrowing or splitting the Spec, and explain any necessary exception in the conversation rather than the document.
- Keep the introduction to one short paragraph. Other than the required `审批摘要`, do not add summaries, glossaries, traceability tables, or repeated context unless the user explicitly needs them.

**Constraints:**

- The model MUST create `specs/{feature_name}/requirements.md` under the project root only after the requirement collection above is complete and file writing is permitted.
- The model MUST express EARS semantics naturally in Chinese and MUST NOT copy the literal English EARS keywords `WHEN`, `THEN`, or `SHALL` into the generated document.
- The model MUST format the initial requirements.md document with:
- A Human-First `审批摘要` before the introduction, followed by a clear introduction section that summarizes the feature
- A hierarchical numbered list of requirements where each contains:
  - A user story written in Chinese using the role-goal-benefit structure
  - A numbered list of acceptance criteria in EARS format (Easy Approach to Requirements Syntax)
- The model SHOULD include an edge case, user-experience constraint, technical constraint, or success criterion only when it creates a distinct observable and verifiable outcome
- Do not create or draft Design until the current Requirements has explicit approval; never mark an unapproved draft approved
- The model MUST continue the feedback-revision cycle until explicit approval is received
- The model SHOULD identify unanswered requirements questions; it MUST NOT suggest speculative expansion by default
- The model MUST resolve material requirements choices through the collection exchange before writing them into the document.
- The model MAY suggest options when the user is unsure about a particular aspect
- After explicit Requirements approval, the model MAY proceed to Design only when the user's existing request covers further planning; otherwise wait for a request to continue

## Troubleshooting

### Requirements Clarification Stalls

If the requirements clarification process seems to be going in circles or not making progress:

- The model SHOULD suggest moving to a different aspect of the requirements
- The model MAY provide examples or options to help the user make decisions
- The model SHOULD summarize what has been established so far and identify specific gaps
- The model MAY suggest conducting research to inform requirements decisions
