# Approval policy

Single source of truth for approval semantics across all LazySpec gates: Requirements/Design/Tasks review, fast plan approval, Brainstorming context approval, multi-Spec orchestration review, and Memory write previews. It defines what approval means, when to ask, and how to ask; risk levels and verification depth live in [risk-policy.md](risk-policy.md). Resolve this reference from the installed `using-lazyspec` skill, never the user's project directory.

## Explicit approval semantics

- Only an explicit approval in the current conversation — a clear "yes", "approved", "looks good", selecting `Approve`, or an equivalent affirmative response — records approval of the current approval object. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval.
- For any non-approval response, remain in the current phase; apply requested changes when provided and request approval again.
- Approval covers the current approval object's material intent, decisions, and risks, plus its detailed body's consistency with it. It does not mean the user approved every non-material implementation detail, and it never claims that unseen content was approved.
- Approval of Requirements permits the Design phase; approval of Design permits the Tasks phase; approval of Tasks ends planning. Execution requires a separate explicit request, which may already have been supplied earlier. An existing request to plan and implement authorizes handoff after all three phase approvals; do not ask again merely because the phase changed.

## Materiality

- Treat observable behavior, scope and exclusions, public interfaces or data changes, compatibility, external side effects, security or privacy, failure and recovery behavior, key technical choices, and their risks as material. Treat filenames, internal helpers, code organization, test layout, and equivalent implementation refinements as non-material only when they do not alter any material item. When uncertain, classify a change as material.
- A material change invalidates the prior approval and downstream evidence, not unrelated completed work. A verified non-material body-only refinement that leaves the approved contract true and complete does not require reapproval.
- Task decomposition, dependency-preserving reordering, equivalent implementation choices, and equally strong verification methods are non-material refinements: update their records and continue without approval. Ask only when they alter the approved outcome, scope, constraints, material risk, or a choice explicitly reserved for the user.
- Escalation updates reasons, effects, and verification needs, but does not by itself create phase approvals. Pause only work requiring a new material decision or an unauthorized operation; continue independent authorized preparation. Do not downgrade to evade a confirmation already triggered.

## Approval timing

- For every normal Spec, create and review one phase at a time: Requirements → explicit Requirements approval → Design → explicit Design approval → Tasks → explicit Tasks approval. Never create a downstream phase document before the current phase is explicitly approved. Risk level and decision impact do not change this order or the three approval gates.
- Before creating a new Design, collect Design-stage input through the separate question exchange in `writing-design`, after Requirements approval. Brainstorming approval covers the requirements direction only; answering a Design question does not approve the Design draft.
- Resolve unanswered user decisions within the current phase. Do not advance past an unapproved phase or an unauthorized critical operation. Reuse explicit decisions and authorization already available in the conversation without asking twice for the same phase object.
- Prior approval of a BrainstormingContext or CodexPlanArtifact remains input approval, not Requirements approval. Approval of one Spec phase never approves a later phase.
- Confirm only concrete critical operations not already explicitly authorized at their current scope. General plan approval is not permission for an unnamed destructive operation. Human acceptance is required only when explicitly requested, mandated by binding project rules, or necessary to establish an outcome unavailable to automated evidence; when required, it covers the current implementation, not an old result.
- Fast retains one plan and one plan approval followed by continuous execution, at every risk level. A material plan change requires approval of the complete revised plan with its delta.
- Multi-Spec orchestration retains one approval gate: explicit approval of the complete `orchestration.md` before any participating Spec's execution starts. A material change — participating Spec set, joint objective, dependency/order, parallelism, branch strategy, coordination constraints, or integration verification — requires approval of the complete revised orchestration with its delta. Orchestration approval never approves new Spec content; participating Specs remain governed by their own approvals.
- A rejected phase remains in that phase: apply feedback and present the revised phase for approval before creating any downstream document.

## How to ask

Whenever a LazySpec workflow needs an answer from the user:

1. Discover and use an applicable user-question tool exposed by the current agent environment when available and permitted. Do not require a particular tool name or copy another agent's input schema. Supply only fields supported by the selected tool.
2. If no applicable tool is available, ask the user directly in the conversation and stop while awaiting the answer.

At a necessary approval gate, ask the phase's approval question as one decision. When the tool supports choices, offer mutually exclusive `Approve` and `Request changes` meanings as a single-choice question; adapt labels, descriptions, and free-form handling to its actual interface. An explicit affirmative free-form reply also counts under the approval semantics above.

## Human-First approval summary

Apply this contract to generated or revised Requirements and Design documents:

- Put a Chinese `审批摘要` at the top of each Requirements and Design document. It is the user-facing approval contract; the detailed body is the Agent-facing elaboration and MUST remain consistent with, and bounded by, the approved summary. Tasks keeps the complete task document as its approval object. Only explicit approval in the current conversation records approval of the current `审批摘要` and its consistency with the detailed body.
- Before requesting approval, verify internally that every material body item is represented directly or by one unambiguous group in `审批摘要`. A missing material item or any summary/body conflict blocks approval.
- Adapt the summary to the feature's cognitive complexity instead of enforcing a fixed item or character count. Aim for a complete one-screen review. If that is impossible without hiding material information, pause approval and recommend splitting the Spec; expand the summary only after the user explicitly chooses to keep one Spec.
- After a material revision, update the complete summary in the document and present a concise conversation delta covering additions, changes, removals, and risk changes before asking for approval again.
- Every downstream phase MUST treat an approved `审批摘要` as the upper-level material contract while continuing to read the complete Spec body for implementation detail.

## Legacy artifacts

Do not bulk-migrate existing Specs. Add `审批摘要` when a Requirements or Design document is next created or revised; an already approved legacy Requirements document may still be used to create Design without being rewritten.
