# Execution, feature verification, and learning

Read for task planning and execution in both normal and fast modes, after `risk-policy.md`. This is a workflow contract, not a runtime or permission grant.

## Executable success criteria

Each executable TODO has a concrete implementation objective, a scenario/input with an observable expected result, and a feasible verification method. A discovered command or specific test entry point is useful when available, not a mandatory new test. Label new tests as to-be-implemented until they exist. An exit code alone or “implementation complete / tests pass” is not a behavioral oracle. Keep normal-mode acceptance links and full-plan coverage checks; use at most three descriptive bullets plus links where possible.

## Feature Verification artifact

Append `## Feature Verification` to `tasks.md` (normal) or `plan.md` (fast). This is not a TODO and is excluded from checkbox counts. Do not create a separate verification file. Separate the approved **Planned Checks** from the mutable **Latest Result** so recording evidence does not revise the plan.

Planned Checks maps every acceptance outcome to a scenario, expected result, and check/evidence method. Link normal-mode requirement anchors; fast references Objective, Constraints, and task criteria. Include composed user flows and risk-specific checks. Group outcomes only when their individual coverage remains explicit. Put required manual experience checks here, not in coding TODOs.

Latest Result starts as “未执行” with no success claim. After a run, record:

- Each outcome's actual check, observed result, evidence location, and unresolved issue; distinguish passed, failed, blocked, and pending-human items.
- Verification time, tested Git commit (or explicitly no commit), relevant uncommitted changes identified by paths and diff/content fingerprint, and the corresponding contract revision/fingerprint. Record evidence with enough context to reproduce or inspect it; do not store secrets or raw sensitive logs.
- Overall status `passed / failed / blocked / pending-human` and freshness `current / stale`. Failed required checks take precedence, then blocked required checks, then pending human checks. Only all satisfied required checks allow passed. A skipped check or missing environment is not success.

Choose verification methods that establish the required outcomes; existing tests, focused checks, inspection, or other attributable evidence may suffice. Planned methods are defaults unless explicitly mandated by the user or a binding project requirement. Record equivalent substitutions and their coverage without reapproval; never lower the success standard. Once current evidence covers all required outcomes and no relevant concern remains, stop verification. Broaden or repeat checks only for new changes, failures, or unresolved concerns; do not add tests that merely mirror low-impact reversible edits.

Related implementation or acceptance-contract changes make previous evidence stale. Reuse task evidence only when the tested state and covered outcome still match; rerun checks affected by integration changes. Updating the report itself does not invalidate code evidence. If results cannot be attributed to the current state, treat them as stale.

## Trigger and handoff

- After all feature TODOs, including nested tasks, are checked, automatically run Feature-level Verification within the authorized scope. Completion of a selected subset only reports that subset; if it also completes the entire feature, run the feature checks. Never repair unrelated tasks beyond a user's selected scope without authorization.
- An execution request for an already checked plan still completes missing or stale verification. A status/question request is read-only and does not run checks or mutate records. Explicit verification-only requests run checks and report issues without authorizing implementation repairs.
- Human acceptance explicitly required by the user, binding project rules, or an outcome that available evidence cannot establish remains pending-human until confirmed. Risk alone does not mandate an extra sign-off. Record any confirmation against the tested state.
- Handoff separately reports TODO completion, feature status/freshness, evidence and remaining work. A checked task list alone is not a verified feature.
- Follow explicit user/project commit requirements. Otherwise normal mode groups related verified TODOs into coherent, independently reviewable commits; no per-TODO or separate evidence commit is mandatory. Commit later repairs without rewriting history or including unrelated changes. Fast does not acquire a new mandatory commit policy.

## Execution strategy

These rules apply to normal `tasks.md` plans; fast plan.md execution follows `fast` and this same loop.

- Before executing, understand the complete `requirements.md`, `design.md`, and `tasks.md` contract. Reuse unchanged content already in context; read missing or changed sections. Never execute with missing or uncertain contract context.
- Before implementing, confirm the current normal Spec has the applicable combined or phase approvals under approval-policy.md. An execution request alone does not approve unseen material plan changes.
- When the user explicitly requests execution of a `tasks.md` plan, execute all currently unchecked TODOs, including their sub-tasks, without waiting for per-task approval or another user instruction. If the user explicitly names one TODO number, limit execution to that TODO and its sub-tasks. Look at the task details in the task list; start with sub-tasks if present.
- Before the first file modification, create a new feature branch by default using `codex/<feature-name>` (or the user's explicitly requested branch name). If the default branch name already belongs to unrelated work, use a unique `codex/` branch name and report the choice. Do not commit unrelated pre-existing changes.
- When executing under an approved `specs/orchestration.md`, follow its cross-Spec branch stacking, sequencing, and coordination constraints, which override the default single-Spec branch rule. The orchestration coordinates Spec-level execution only: it MUST NOT override or modify any Spec's approved content, and it does not govern intra-Spec task execution — task-level ordering, verification methods, and repair routing remain defined by that Spec's `tasks.md` and this loop.
- Verify implementation against any requirements specified in the task or its details.
- After each TODO passes its verification, change only its checkbox token from `[ ]` to `[x]`. Preserve `//TODO` and every character after it exactly; do not remove, replace, or rewrite the task text. Group related verified work into coherent commits unless the user specifies another commit policy. Exclude unrelated working-tree changes.
- Continue through all requested unchecked TODOs without an intentional pause. Verification failures follow Failure routing and repair below: diagnose, repair within authorization while progressing, or route to the earliest invalid contract. Stop for the no-progress threshold, merge or working-tree conflict, commit failure, missing authority/user decision, or user interruption; report the exact blocker.
- When all requested TODOs are complete, inspect only the Project Memory index for Capsules whose feature, tags, summary, Source Spec, or authorities overlap the changed paths. Report likely impact candidates in the handoff, but do not create, edit, or re-status Memory without a separate explicit distillation or maintenance request.
- If the task file has no unchecked TODOs, complete missing or stale Feature Verification on an execution request. For partial execution, report only the authorized subset unless all feature TODOs are now complete. Follow Feature Verification artifact and Learning Candidates below for the in-file report. If the requested task file or TODO cannot be resolved, ask for the exact path or number before modifying files.

Ensure the complete current contract is understood; reuse unchanged content already available in context and read missing or changed sections rather than rereading every artifact. If context is incomplete or freshness uncertain, read the relevant complete artifact before acting. Choose research depth and tools based on unresolved facts, not a fixed exploration sequence.

Treat listed task order as a default. Reorder independent tasks or group related work when dependencies, approved outcomes, and user scope are preserved; briefly record the reason. Do not renumber or rewrite completed TODO text. Parallel work must also be permitted by the host/user and have clear ownership; this policy does not grant delegation authority.

## Failure routing and repair

Diagnose before changing artifacts. Route to the earliest contract that must change:

| Cause | Destination | Action |
|---|---|---|
| Code violates valid requirements and design | Current execution task | Repair and retest within authorized scope, without reapproval |
| Missing task, wrong ordering, or inadequate verification steps; upstream contracts valid | Tasks | Update non-material execution details and continue; ask only if the success contract or reserved decision changes |
| Invalid architecture, interface, or data-design assumption | Design | Revise Design and inspect affected Tasks; approve material choices, continue equivalent internal refinements |
| Missing, conflicting, or incorrect behavior, scope, or acceptance criterion | Requirements | Revise Requirements and inspect affected Design/Tasks; approve affected contracts |
| Unavailable environment, permission, or dependency | Current stage | Mark blocked and report the missing condition; do not change product requirements |

Never weaken approved success criteria, remove a required check, or relabel a failure just to pass. In fast, route the same causes to Objective/Constraints, Approach, or Tasks inside plan.md. A material revision requires approval of the complete revised plan with a delta; do not create Requirements/Design/Tasks files.

During an authorized implementation run, continue repairs while progressing. For the same issue, after two consecutive rounds without new evidence or improvement, reassess the hypothesis and method. Continue only with a concrete new diagnostic approach within the authorized budget; otherwise stop and report. Report attempts, evidence, and the unresolved decision. Rewording an explanation, renaming an issue, or repeating the same failed approach is not a new diagnostic approach. Honor explicit attempt/time/cost limits. Stop immediately for working-tree conflicts, missing authority, or a necessary user decision.

Only affected approvals and evidence become invalid. Preserve completed TODO text: completion changes only its checkbox; later remedial work is appended as a clearly identified repair task. A scoped implementation-only repair may be appended as an execution record without renewed approval; a task-plan gap follows the materiality decision above. Never rewrite completed task descriptions or existing commits.

## Learning Candidates

After verification or a valuable blocked/failed attempt, inspect the run for reusable, project-specific evidence. If none exists, add nothing. Otherwise append `## Learning Candidates` to the same task/plan document. Each candidate records applicability, observed problem, evidenced explanation, validated practice (or explicitly unverified proposal), sources, limits, and revisit conditions.

Candidates are not long-term Memory and must not be recalled as active guidance. Show a concise handoff and link the complete candidate. Only when the user requests promotion or confirms a candidate, route to distill-spec-memory to prepare the exact Capsule/index write preview. Approval of the complete candidate plus exact write set authorizes that write once; changes invalidate it. Collection alone never writes under project-memory/ or changes AGENTS.md, skills, permissions, or configuration.

An unfinished feature can support a bounded failure observation; it cannot support a claim of feature success or an untested remedy. One success supports only its evidenced conditions. Continue reporting likely existing Memory impact candidates without silently changing their status.
