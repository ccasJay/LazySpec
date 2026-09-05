# Risk and approval policy

Read before planning, revising, or executing a feature. This policy governs approval timing across all seven skills; it does not grant execution permissions. Resolve this reference from the installed `using-lazyspec` skill, never the user's project directory.

## Classification

Use the highest applicable level, not a numerical score:

| Level | Conditions | Normal planning approval | Feature verification |
|---|---|---|---|
| low | Local, readily reversible; no public interface, persistent data, or permission-boundary changes | Draft Requirements → Design → Tasks, then one combined approval | All acceptance outcomes and directly affected regression checks |
| medium | Cross-component behavior, public interfaces, or compatible data changes with bounded impact | Separate Requirements, Design, and Tasks approvals | Also integration, compatibility, and failure paths |
| high | Permissions, sensitive data, destructive migrations, irreversible effects, or broad impact | Separate phase approvals; confirm critical operations before execution and final acceptance evidence afterward | Also relevant security, recovery, and impact-boundary checks |

Brainstorming proposes a level; Design re-evaluates it. Keep the existing BrainstormingContext schema: carry the initial assessment in constraints. A native planning input without a risk assessment is assessed when Requirements starts. Default to medium unless low is justified; clarify uncertain high-impact consequences before approving a plan. Do not add irrelevant tests merely to satisfy a level.

Record the level, reasons, and named critical operations in Requirements and Design's `风险与待确认`; Design records any assessment change. Tasks links to this assessment instead of duplicating it. Fast records it in Constraints and Approach. Before execution, reconcile discrepancies using the highest applicable level.

## Approval timing

- Low risk permits unapproved upstream **drafts**, not assumed approval. Continue drafting in phase order without intermediate approval requests. At Tasks, present both complete approval summaries, their consistency with their bodies, and the complete task plan including planned feature checks as one approval object. Explicit approval approves all three together.
- Medium and high retain separate phase approvals. Missing approval blocks advancement. At any level, silence, file existence, or selecting an approach does not approve a document. A rejected combined package remains in planning; apply feedback and present the revised package.
- Approval of normal planning ends planning; execution requires a separate request. Fast retains one plan and one plan approval followed by continuous execution, at every risk level. Never create a three-document Spec merely because fast is high risk.
- Prior approval of a BrainstormingContext or CodexPlanArtifact remains input approval, not Spec approval. The low-risk package is a separate approval object; medium/high request Requirements approval separately.
- On escalation, pause affected work, show changed reasons, effects, and verification needs, and obtain missing approvals. During low-risk drafting, escalation to medium/high requires approving Requirements before advancing through Design and Tasks; existing drafts are not approvals. Do not downgrade to evade a confirmation already triggered.
- Confirm only concrete critical operations not already explicitly authorized at their current scope. General plan approval is not permission for an unnamed destructive operation. High-risk final acceptance approves the evidence for the current implementation, not an old result.
- Material changes invalidate affected approvals and downstream evidence, not unrelated completed work. A non-material implementation refinement that preserves the approved summaries, scope, and success criteria needs no reapproval. Explicit plan changes still require approval at the applicable package or phase gate.

## Existing artifacts

Do not bulk-migrate Specs. On the next execution request, assess risk and add missing feature-verification structure. Derive missing success criteria from approved behavior only; if this introduces a material decision, revise and approve at the applicable gate before affected execution. Keep source TODO text intact. Administrative evidence updates and candidate collection are not planning revisions and do not request plan approval again.
