# Risk policy

Read before planning, revising, or executing a feature. This policy defines risk classification and verification depth; approval semantics and timing live in [approval-policy.md](approval-policy.md). Neither grants execution permissions. Resolve this reference from the installed `using-lazyspec` skill, never the user's project directory.

## Autonomy contract

User instructions and explicit authorization take precedence over Skill defaults, subject to host/system permissions. Bind work to the goal, scope, constraints, observable success evidence, and decisions reserved for the user. Within those boundaries, let the model choose research methods, internal task order, implementation details, and verification methods. Do not ask the user to choose an internal technique merely because alternatives exist.

When pausing, name the affected action, missing decision or permission, and exact rule/source; distinguish a Skill requirement from your interpretation. Continue independent authorized work. Status questions during execution do not cancel the original task; incorporate corrections into affected work and preserve unaffected results. Stop on explicit cancellation.

## Classification

Use the highest applicable level, not a numerical score:

| Level | Conditions | Normal planning approval | Feature verification |
|---|---|---|---|
| low | Local, readily reversible; no public interface, persistent data, or permission-boundary changes | Requirements, Design, and Tasks each require approval under approval-policy.md | All acceptance outcomes and directly affected regression checks |
| medium | Cross-component behavior, public interfaces, or compatible data changes with bounded impact | The same three phase approvals | Also integration, compatibility, and failure paths |
| high | Permissions, sensitive data, destructive migrations, irreversible effects, or broad impact | The same three phase approvals; confirm unauthorized critical operations and required human acceptance | Also relevant security, recovery, and impact-boundary checks |

Brainstorming proposes a level; Design re-evaluates it. Keep the existing BrainstormingContext schema: carry the initial assessment in constraints. A native planning input without a risk assessment is assessed when Requirements starts. Default to medium unless low is justified; clarify uncertain high-impact consequences before approving a plan. Do not add irrelevant tests merely to satisfy a level.

Record the level, reasons, and named critical operations in Requirements and Design's `风险与待确认`; Design records any assessment change. Tasks links to this assessment instead of duplicating it. Fast records it in Constraints and Approach. Before execution, reconcile discrepancies using the highest applicable level.

## Existing artifacts

Do not bulk-migrate Specs. On the next execution request, assess risk and add missing feature-verification structure. Derive missing success criteria from approved behavior only; if this introduces a material decision, revise and approve at the applicable gate under approval-policy.md before affected execution. Keep source TODO text intact. Administrative evidence updates and candidate collection are not planning revisions and do not request plan approval again.
