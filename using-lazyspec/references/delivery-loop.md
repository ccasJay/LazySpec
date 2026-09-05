# Execution, feature verification, and learning

Read for task planning and execution in both normal and fast modes, after `risk-policy.md`. This is a workflow contract, not a runtime or permission grant.

## Executable success criteria

Each executable TODO has a concrete implementation objective, a scenario/input with an observable expected result, and a discovered command or specific test entry point. Label new tests as to-be-implemented until they exist. An exit code alone or “implementation complete / tests pass” is not a behavioral oracle. Keep normal-mode acceptance links and full-plan coverage checks; use at most three descriptive bullets plus links where possible.

## Feature Verification artifact

Append `## Feature Verification` to `tasks.md` (normal) or `plan.md` (fast). This is not a TODO and is excluded from checkbox counts. Do not create a separate verification file. Separate the approved **Planned Checks** from the mutable **Latest Result** so recording evidence does not revise the plan.

Planned Checks maps every acceptance outcome to a scenario, expected result, and check/evidence method. Link normal-mode requirement anchors; fast references Objective, Constraints, and task criteria. Include composed user flows and risk-specific checks. Group outcomes only when their individual coverage remains explicit. Put required manual experience checks here, not in coding TODOs.

Latest Result starts as “未执行” with no success claim. After a run, record:

- Each outcome's actual check, observed result, evidence location, and unresolved issue; distinguish passed, failed, blocked, and pending-human items.
- Verification time, tested Git commit (or explicitly no commit), relevant uncommitted changes identified by paths and diff/content fingerprint, and the corresponding contract revision/fingerprint. Record evidence with enough context to reproduce or inspect it; do not store secrets or raw sensitive logs.
- Overall status `passed / failed / blocked / pending-human` and freshness `current / stale`. Failed required checks take precedence, then blocked required checks, then pending human checks. Only all satisfied required checks allow passed. A skipped check or missing environment is not success.

Related implementation or acceptance-contract changes make previous evidence stale. Reuse task evidence only when the tested state and covered outcome still match; rerun checks affected by integration changes. Updating the report itself does not invalidate code evidence. If results cannot be attributed to the current state, treat them as stale.

## Trigger and handoff

- After all feature TODOs, including nested tasks, are checked, automatically run Feature-level Verification within the authorized scope. Completion of a selected subset only reports that subset; if it also completes the entire feature, run the feature checks. Never repair unrelated tasks beyond a user's selected scope without authorization.
- An execution request for an already checked plan still completes missing or stale verification. A status/question request is read-only and does not run checks or mutate records. Explicit verification-only requests run checks and report issues without authorizing implementation repairs.
- High-risk automated success remains pending-human until the user confirms current acceptance evidence. Other required human checks also remain pending-human until confirmed. Record the confirmation against the tested state.
- Handoff separately reports TODO completion, feature status/freshness, evidence and remaining work. A checked task list alone is not a verified feature.
- Normal mode retains per-TODO commits. Commit later repairs separately without rewriting history; record final verification/candidates in a separate scoped evidence commit after task commits. Fast does not acquire a new mandatory commit policy.

## Failure routing and repair

Diagnose before changing artifacts. Route to the earliest contract that must change:

| Cause | Destination | Action |
|---|---|---|
| Code violates valid requirements and design | Current execution task | Repair and retest within authorized scope, without reapproval |
| Missing task, wrong ordering, or inadequate verification steps; upstream contracts valid | Tasks | Revise affected plan, show delta, approve before continuing |
| Invalid architecture, interface, or data-design assumption | Design | Revise Design and inspect affected Tasks; apply risk-specific approvals |
| Missing, conflicting, or incorrect behavior, scope, or acceptance criterion | Requirements | Revise Requirements and inspect affected Design/Tasks; approve affected contracts |
| Unavailable environment, permission, or dependency | Current stage | Mark blocked and report the missing condition; do not change product requirements |

Never weaken approved success criteria, remove a required check, or relabel a failure just to pass. In fast, route the same causes to Objective/Constraints, Approach, or Tasks inside plan.md. A material revision requires approval of the complete revised plan with a delta; do not create Requirements/Design/Tasks files.

During an authorized implementation run, continue repairs while progressing. For the same issue, stop after two consecutive repair-and-retest rounds with neither new diagnostic evidence nor observable improvement. Report attempts, evidence, and the unresolved decision. Reset the counter only on real new evidence or improvement, not a renamed issue or rephrased explanation. Stop immediately for working-tree conflicts, missing authority, or a necessary user decision.

Only affected approvals and evidence become invalid. Preserve completed TODO text: completion changes only its checkbox; later remedial work is appended as a clearly identified repair task. A scoped implementation-only repair may be appended as an execution record without renewed approval; a task-plan gap uses the Tasks gate above. Never rewrite completed task descriptions or existing commits.

## Learning Candidates

After verification or a valuable blocked/failed attempt, inspect the run for reusable, project-specific evidence. If none exists, add nothing. Otherwise append `## Learning Candidates` to the same task/plan document. Each candidate records applicability, observed problem, evidenced explanation, validated practice (or explicitly unverified proposal), sources, limits, and revisit conditions.

Candidates are not long-term Memory and must not be recalled as active guidance. Show a concise handoff and link the complete candidate. Only when the user requests promotion or confirms a candidate, route to distill-spec-memory to prepare the exact Capsule/index write preview. Approval of the complete candidate plus exact write set authorizes that write once; changes invalidate it. Collection alone never writes under project-memory/ or changes AGENTS.md, skills, permissions, or configuration.

An unfinished feature can support a bounded failure observation; it cannot support a claim of feature success or an untested remedy. One success supports only its evidenced conditions. Continue reporting likely existing Memory impact candidates without silently changing their status.
