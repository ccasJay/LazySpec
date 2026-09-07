# Risk and approval policy

Read before planning, revising, or executing a feature. This policy governs approval timing across all seven skills; it does not grant execution permissions. Resolve this reference from the installed `using-lazyspec` skill, never the user's project directory.

## Autonomy contract

User instructions and explicit authorization take precedence over Skill defaults, subject to host/system permissions. Bind work to the goal, scope, constraints, observable success evidence, and decisions reserved for the user. Within those boundaries, let the model choose research methods, internal task order, implementation details, and verification methods. Do not ask the user to choose an internal technique merely because alternatives exist.

When pausing, name the affected action, missing decision or permission, and exact rule/source; distinguish a Skill requirement from your interpretation. Continue independent authorized work. Status questions during execution do not cancel the original task; incorporate corrections into affected work and preserve unaffected results. Stop on explicit cancellation.

## Classification

Use the highest applicable level, not a numerical score:

| Level | Conditions | Normal planning approval | Feature verification |
|---|---|---|---|
| low | Local, readily reversible; no public interface, persistent data, or permission-boundary changes | Draft Requirements → Design → Tasks, then one combined approval | All acceptance outcomes and directly affected regression checks |
| medium | Cross-component behavior, public interfaces, or compatible data changes with bounded impact | Combined plan review; ask earlier only for unresolved material decisions | Also integration, compatibility, and failure paths |
| high | Permissions, sensitive data, destructive migrations, irreversible effects, or broad impact | Combined plan review; confirm unauthorized critical operations and required human acceptance | Also relevant security, recovery, and impact-boundary checks |

Brainstorming proposes a level; Design re-evaluates it. Keep the existing BrainstormingContext schema: carry the initial assessment in constraints. A native planning input without a risk assessment is assessed when Requirements starts. Default to medium unless low is justified; clarify uncertain high-impact consequences before approving a plan. Do not add irrelevant tests merely to satisfy a level.

Record the level, reasons, and named critical operations in Requirements and Design's `风险与待确认`; Design records any assessment change. Tasks links to this assessment instead of duplicating it. Fast records it in Constraints and Approach. Before execution, reconcile discrepancies using the highest applicable level.

## Approval timing

- Every risk level permits unapproved upstream **drafts**, not assumed approval. Continue drafting in phase order without intermediate approval requests. At Tasks, present both complete approval summaries, their consistency with their bodies, and the complete task plan including planned feature checks as one approval object. Explicit approval approves all three together.
- Risk determines verification depth, not the number of approval pauses. Ask before an unresolved material decision or an unauthorized critical operation; otherwise continue preparing the reviewable package. Honor explicitly requested phase-by-phase review. At any level, silence, file existence, or selecting an approach does not approve a document. A rejected combined package remains in planning; apply feedback and present the revised package.
- Approval of normal planning alone ends planning; execution requires an explicit request, which may already have been supplied earlier. An existing request to plan and implement authorizes handoff after unresolved decisions are settled; do not ask again merely because the phase changed. Fast retains one plan and one plan approval followed by continuous execution, at every risk level. Never create a three-document Spec merely because fast is high risk.
- Prior approval of a BrainstormingContext or CodexPlanArtifact remains input approval, not approval of newly introduced Spec decisions. Reuse explicit decisions and authorization already available in context; request approval only for the complete package or material delta not yet approved. Never claim that unseen content was approved.
- On escalation, update reasons, effects, and verification needs. Pause only work requiring a new material decision or unauthorized operation; continue independent authorized preparation. Escalation alone does not create phase approvals. Do not downgrade to evade a confirmation already triggered.
- Confirm only concrete critical operations not already explicitly authorized at their current scope. General plan approval is not permission for an unnamed destructive operation. Human acceptance is required only when explicitly requested, mandated by binding project rules, or necessary to establish an outcome unavailable to automated evidence. When required, it covers the current implementation, not an old result.
- Material changes invalidate affected approvals and downstream evidence, not unrelated completed work. A non-material implementation refinement that preserves the approved summaries, scope, and success criteria needs no reapproval. Task decomposition, dependency-preserving reordering, equivalent implementation choices, and equally strong verification methods are non-material refinements: update their records and continue without approval. Ask only when they alter the approved outcome, scope, constraints, material risk, or a choice explicitly reserved for the user.

## Existing artifacts

Do not bulk-migrate Specs. On the next execution request, assess risk and add missing feature-verification structure. Derive missing success criteria from approved behavior only; if this introduces a material decision, revise and approve at the applicable gate before affected execution. Keep source TODO text intact. Administrative evidence updates and candidate collection are not planning revisions and do not request plan approval again.
