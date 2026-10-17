# Shared feature verification, repair, and learning

Read for task planning and for execution in both normal and fast modes, after `risk-policy.md`. This is a shared workflow contract, not a runtime or permission grant. Normal `plan.md` execution is owned by `executing-plan/SKILL.md`; fast `plan.md` execution is owned by `fast/SKILL.md`.

## Executable success criteria

Each executable TODO has a concrete implementation objective, a scenario/input with an observable expected result, and a feasible verification method. A discovered command or specific test entry point is useful when available, not a mandatory new test. Label new tests as to-be-implemented until they exist. An exit code alone or “implementation complete / tests pass” is not a behavioral oracle. Keep normal-mode acceptance links and full-plan coverage checks; use at most three descriptive bullets plus links where possible.

## Feature Verification artifact

Append `## Feature Verification` to `plan.md`. This is not a TODO and is excluded from checkbox counts. Do not create a separate verification file. Separate the approved **Planned Checks** from the mutable **Latest Result** so recording evidence does not revise the plan.

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
- A `passed` and `current` result is verification success, not merge approval. Normal mode proceeds to the user review and delivery finalization procedure in [executing-plan](../../executing-plan/SKILL.md#merge-and-automatic-delivery-finalization). Fast completes its own handoff without creating or updating `spec.md` and without inheriting normal-mode merge or status-transition rules.
- Follow explicit user/project commit requirements. Mode-specific commit rules live in the executing Skill. Commit later repairs without rewriting history or including unrelated changes; fast does not acquire a new mandatory commit policy.

## Lifecycle states and negative guardrails

LazySpec defines formal lifecycle states for Specs:
- `proposed`: Active proposal or work-in-progress.
- `delivered`: Fully implemented, verified, and living truth of current system capabilities.
- `archived`: Mature foundation truth retained as a historical snapshot.
- `superseded`: Overturned by a newer Spec; retains bidirectional links and redirect warnings.
- `obsolete`: Discontinued or disproven mechanism retained as a negative guardrail.

Archive/retirement paths, warnings, and preservation operations belong to [maintain-memory](../../maintain-memory/SKILL.md); Spec delivery and supersession operations belong to executing-plan. Capsule statuses are a separate contract in the active Memory format; Spec states do not add Capsule states.


## Mode-specific execution

Use `executing-plan/SKILL.md` for the normal `plan.md` execution strategy, including approvals, worktree setup, spec baseline first commit, TODO scope, per-TODO atomic commit, verification, checkbox, user review gate, dev merge, worktree cleanup, handoff, and temporary progress rules. Use `fast/SKILL.md` for fast `plan.md` execution. Both modes follow the shared Feature Verification, failure routing, and Learning Candidates rules in this reference. Multi-Spec orchestration controls cross-Spec sequencing and branches only; it does not govern intra-Spec task execution or grant delegation authority.

## Failure routing and repair

Diagnose before changing artifacts. Route to the earliest contract that must change:

| Cause | Destination | Action |
|---|---|---|
| Code violates valid spec and design decisions | Current execution task | Repair and retest within authorized scope, without reapproval |
| Missing task, wrong ordering, or inadequate verification steps; upstream contracts valid | Plan (`plan.md`) | Update non-material execution details and continue; ask only if the success contract or reserved decision changes |
| Invalid architecture, interface, behavior, scope, or acceptance criterion | Spec (`spec.md`) | Revise Spec and inspect affected Plan; approve material choices |
| Unavailable environment, permission, or dependency | Current stage | Mark blocked and report the missing condition; do not change product requirements |

Never weaken approved success criteria, remove a required check, or relabel a failure just to pass. In fast, route the same causes to Objective/Constraints, Approach, or Tasks inside plan.md. A material revision requires approval of the complete revised plan with a delta.

During an authorized implementation run, continue repairs while progressing. For the same issue, after two consecutive rounds without new evidence or improvement, reassess the hypothesis and method. Continue only with a concrete new diagnostic approach within the authorized budget; otherwise stop and report. Report attempts, evidence, and the unresolved decision. Rewording an explanation, renaming an issue, or repeating the same failed approach is not a new diagnostic approach. Honor explicit attempt/time/cost limits. Stop immediately for working-tree conflicts, missing authority, or a necessary user decision.

Only affected approvals and evidence become invalid. Preserve completed TODO text: completion changes only its checkbox; later remedial work is appended as a clearly identified repair task. A scoped implementation-only repair may be appended as an execution record without renewed approval; a task-plan gap follows the materiality decision above. Never rewrite completed task descriptions or existing commits.

## Learning Candidates

After verification or a valuable blocked/failed attempt, inspect the run for reusable, project-specific evidence. If none exists, add nothing. Otherwise append `## Learning Candidates` to the same plan document. Each candidate records applicability, observed problem, evidenced explanation, validated practice (or explicitly unverified proposal), sources, limits, and revisit conditions.

Candidates are not long-term Memory and must not be recalled as active guidance. Show a concise handoff and link the complete candidate. Only when the user requests promotion or confirms a candidate, route to distill-learning and its shared Memory write workflow under approval-policy.md. Collection alone never writes under project-memory/ or changes AGENTS.md, skills, permissions, or configuration.

An unfinished feature can support a bounded failure observation; it cannot support a claim of feature success or an untested remedy. One success supports only its evidenced conditions. Continue reporting likely existing Memory impact candidates without silently changing their status.
