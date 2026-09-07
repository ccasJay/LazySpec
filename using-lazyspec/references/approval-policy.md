# Approval policy

Single source of truth for approval semantics across all LazySpec gates: Requirements/Design/Tasks review, fast plan approval, Brainstorming context approval, and Memory write previews. It defines what approval means, when to ask, and how to ask; risk levels and verification depth live in [risk-policy.md](risk-policy.md). Resolve this reference from the installed `using-lazyspec` skill, never the user's project directory.

## Explicit approval semantics

- Only an explicit approval in the current conversation — a clear "yes", "approved", "looks good", selecting `Approve`, or an equivalent affirmative response — records approval of the current approval object. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval.
- For any non-approval response, remain in the current phase; apply requested changes when provided and request approval again.
- Approval covers the current approval object's material intent, decisions, and risks, plus its detailed body's consistency with it. It does not mean the user approved every non-material implementation detail, and it never claims that unseen content was approved.
- Approval of planning alone ends planning; execution requires a separate explicit request, which may already have been supplied earlier. An existing request to plan and implement authorizes handoff once unresolved decisions are settled; do not ask again merely because the phase changed.

## Materiality

- Treat observable behavior, scope and exclusions, public interfaces or data changes, compatibility, external side effects, security or privacy, failure and recovery behavior, key technical choices, and their risks as material. Treat filenames, internal helpers, code organization, test layout, and equivalent implementation refinements as non-material only when they do not alter any material item. When uncertain, classify a change as material.
- A material change invalidates the prior approval and downstream evidence, not unrelated completed work. A verified non-material body-only refinement that leaves the approved contract true and complete does not require reapproval.
- Task decomposition, dependency-preserving reordering, equivalent implementation choices, and equally strong verification methods are non-material refinements: update their records and continue without approval. Ask only when they alter the approved outcome, scope, constraints, material risk, or a choice explicitly reserved for the user.
- Escalation updates reasons, effects, and verification needs, but does not by itself create phase approvals. Pause only work requiring a new material decision or an unauthorized operation; continue independent authorized preparation. Do not downgrade to evade a confirmation already triggered.

## Approval timing

- Risk determines verification depth, not the number of approval pauses. Every risk level permits unapproved upstream drafts, not assumed approval: continue drafting Requirements → Design → Tasks in phase order without intermediate approval requests, then present both approval summaries, their consistency with their bodies, and the complete task plan including planned feature checks as one combined approval object. Explicit approval approves all three together. Honor explicitly requested phase-by-phase review when the user asks for it.
- Ask for approval earlier only for an unresolved material decision, an unauthorized critical operation, or a user-requested phase gate. Never cross an unresolved material decision or an unauthorized operation. Drafting and authorized internal refinements may proceed without phase approval.
- Prior approval of a BrainstormingContext or CodexPlanArtifact remains input approval, not approval of newly introduced Spec decisions. Reuse explicit decisions and authorization already available in context; request approval only for the complete package or a material delta not yet approved.
- Confirm only concrete critical operations not already explicitly authorized at their current scope. General plan approval is not permission for an unnamed destructive operation. Human acceptance is required only when explicitly requested, mandated by binding project rules, or necessary to establish an outcome unavailable to automated evidence; when required, it covers the current implementation, not an old result.
- Fast retains one plan and one plan approval followed by continuous execution, at every risk level. A material plan change requires approval of the complete revised plan with its delta.
- A rejected combined package remains in planning: apply feedback and present the revised package.

## How to ask

At a necessary approval gate:

1. If `AskUserQuestion` is available, call it with only its supported `questions` input and no extra fields. Use exactly one question object with `question`, `header`, `options`, and `multiSelect`; use `Review` as the header, exactly the two single-choice options `Approve` and `Request changes`, and `multiSelect: false`:

   ```json
   {
     "questions": [{
       "question": "<the asking phase's approval question>",
       "header": "Review",
       "options": [
         {"label": "Approve", "description": "<phase-specific description>"},
         {"label": "Request changes", "description": "<phase-specific description>"}
       ],
       "multiSelect": false
     }]
   }
   ```

   Do not add unsupported top-level or question fields. Each option uses only `label` and `description`; the question text and option descriptions are the asking phase's choice.
2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields that tool supports.
3. Otherwise, ask the phase's approval question directly in the conversation and stop while awaiting the answer.

## Human-First approval summary

Apply this contract to generated or revised Requirements and Design documents:

- Put a Chinese `审批摘要` at the top of each Requirements and Design document. It is the user-facing approval contract; the detailed body is the Agent-facing elaboration and MUST remain consistent with, and bounded by, the approved summary. Tasks keeps the complete task document as its approval object. Only explicit approval in the current conversation records approval of the current `审批摘要` and its consistency with the detailed body.
- Before requesting approval, verify internally that every material body item is represented directly or by one unambiguous group in `审批摘要`. A missing material item or any summary/body conflict blocks approval.
- Adapt the summary to the feature's cognitive complexity instead of enforcing a fixed item or character count. Aim for a complete one-screen review. If that is impossible without hiding material information, pause approval and recommend splitting the Spec; expand the summary only after the user explicitly chooses to keep one Spec.
- After a material revision, update the complete summary in the document and present a concise conversation delta covering additions, changes, removals, and risk changes before asking for approval again.
- Every downstream phase MUST treat an approved `审批摘要` as the upper-level material contract while continuing to read the complete Spec body for implementation detail.

## Legacy artifacts

Do not bulk-migrate existing Specs. Add `审批摘要` when a Requirements or Design document is next created or revised; an already approved legacy Requirements document may still be used to create Design without being rewritten.
