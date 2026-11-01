# Shared feature verification and repair

Read for planning and execution, after `risk-policy.md`. This is a shared workflow contract, not a runtime or permission grant. `spec.md` planning is owned by `writing-spec/SKILL.md`; execution and delivery finalization by `executing-plan/SKILL.md`.

## Executable success criteria

Each executable task in `spec.md` has a concrete implementation objective, a referenced acceptance ID, and a lightweight basic verification method (a syntax/compile check, command probe, or focused basic test). Do not require comprehensive test suites or full-suite execution on every task; reserve those for final Feature Verification. An exit code alone or “implementation complete / tests pass” is not a behavioral oracle. Keep acceptance IDs and full-coverage checks; use at most three descriptive bullets plus references where possible.

## Feature Verification artifact

`spec.md` carries its verification plan inline: the `验证` column of `验收标准` names the check that proves each outcome. That column is part of the approved contract and may not be weakened after approval. Do not create a separate verification file or a `Planned Checks` section.

A shared command may cover several criteria. Group outcomes only when their individual coverage remains explicit; retain distinct scenarios needed for exceptions or failure paths. Include full test suite execution, composed user flows, and risk-specific checks. Put required manual experience checks here, not in tasks.

`执行记录` is the mutable result section. It starts as `状态：未执行`. After a run, record exactly four lines:

- `状态`：`passed / failed / blocked / pending-human`
- `验证`：tested Git commit (or explicitly no commit) · verification time
- `结果`：covered `R` IDs and observed results; list each failure with expected and actual
- `未决`：unresolved issues, or `无`

Do not record fingerprints, per-check logs, secrets, or raw sensitive output. Failed required checks take precedence, then blocked, then pending human; only all satisfied required checks allow `passed`. Freshness is `current` or `stale`; a skipped check or missing environment is not success.

Choose verification methods that establish the required outcomes; existing tests, focused checks, inspection, or other attributable evidence may suffice. Planned methods are defaults unless explicitly mandated by the user or a binding project requirement. Record equivalent substitutions and their coverage without reapproval; never lower the success standard. Once current evidence covers all required outcomes and no relevant concern remains, stop verification. Broaden or repeat checks only for new changes, failures, or unresolved concerns; do not add tests that merely mirror low-impact reversible edits.

Related implementation or acceptance-contract changes make previous evidence stale. Reuse task evidence only when the tested state and covered outcome still match; rerun checks affected by integration changes. Updating `执行记录` itself does not invalidate code evidence. If results cannot be attributed to the current state, treat them as stale.

## Trigger and handoff

- After all feature tasks, including nested tasks, are checked, automatically run Feature-level Verification within the authorized scope. Completion of a selected subset only reports that subset; if it also completes the entire feature, run the feature checks. Never repair unrelated tasks beyond a user's selected scope without authorization.
- An execution request for an already checked plan still completes missing or stale verification. A status/question request is read-only and does not run checks or mutate records. Explicit verification-only requests run checks and report issues without authorizing implementation repairs.
- Human acceptance explicitly required by the user, binding project rules, or an outcome that available evidence cannot establish remains pending-human until confirmed. Risk alone does not mandate an extra sign-off. Record any confirmation against the tested state.
- Handoff separately reports task completion, feature status/freshness, evidence and remaining work. A checked task list alone is not a verified feature.
- A `passed` and `current` result is verification success, not merge approval. Execution proceeds to the user review and delivery finalization procedure in [executing-plan](../../executing-plan/SKILL.md#merge-and-automatic-delivery-finalization).
- Continue reporting likely existing Memory impact candidates without silently changing their status. Impact reporting never writes under project-memory/; use an explicit distillation or maintenance request and its approval workflow for changes.
- Follow explicit user/project commit requirements. Commit rules live in the executing Skill. Commit later repairs without rewriting history or including unrelated changes.

## Lifecycle states and negative guardrails

LazySpec defines formal lifecycle states for Specs:
- `proposed`: Active proposal or work-in-progress.
- `delivered`: Fully implemented, verified, and living truth of current system capabilities.
- `archived`: Mature foundation truth retained as a historical snapshot.
- `superseded`: Overturned by a newer Spec; retains bidirectional links and redirect warnings.
- `obsolete`: Discontinued or disproven mechanism retained as a negative guardrail.

Archive/retirement paths, warnings, and preservation operations belong to [maintain-memory](../../maintain-memory/SKILL.md); Spec delivery and supersession operations belong to executing-plan. Capsule statuses are a separate contract in the active Memory format; Spec states do not add Capsule states.

## Execution ownership

Use `executing-plan/SKILL.md` for the execution strategy, including approvals, worktree setup, spec baseline first commit, task scope, per-TODO atomic commit, verification, checkbox, user review gate, dev merge, worktree cleanup, handoff, and temporary progress rules. It follows the shared Feature Verification and failure routing rules in this reference. Multi-Spec orchestration owns cross-Spec parallel scheduling, branch isolation, and [coordinated integration and delivery](../../orchestrating-specs/SKILL.md#coordinated-integration-and-delivery), using executing-plan's finalization procedure; it does not govern intra-Spec task execution or grant delegation authority.

## Failure routing and repair

Diagnose before changing artifacts. Route to the earliest contract that must change:

| Cause | Destination | Action |
|---|---|---|
| Code violates the approved contract | Current execution task | Repair and retest within authorized scope, without reapproval |
| Missing task, wrong ordering, or inadequate verification detail; upstream contract valid | `spec.md` execution details | Update non-material execution details and continue; ask only if the success contract or reserved decision changes |
| Invalid architecture, interface, behavior, scope, or acceptance criterion | `spec.md` contract | Revise the contract, inspect affected tasks, and approve material choices |
| Unavailable environment, permission, or dependency | Current stage | Mark blocked and report the missing condition; do not change product requirements |

Never weaken approved success criteria, remove a required check, or relabel a failure just to pass. A material revision requires approval of the complete revised `spec.md` with a delta.

During an authorized implementation run, continue repairs while progressing. For the same issue, after two consecutive rounds without new evidence or improvement, reassess the hypothesis and method. Continue only with a concrete new diagnostic approach within the authorized budget; otherwise stop and report. Report attempts, evidence, and the unresolved decision. Rewording an explanation, renaming an issue, or repeating the same failed approach is not a new diagnostic approach. Honor explicit attempt/time/cost limits. Stop immediately for working-tree conflicts, missing authority, or a necessary user decision.

Only affected approvals and evidence become invalid. Preserve completed task text: completion changes only its checkbox; later remedial work is appended as a clearly identified repair task. A scoped implementation-only repair may be appended as an execution record without renewed approval; a task-plan gap follows the materiality decision above. Never rewrite completed task descriptions or existing commits.

## Delivery convergence

A delivered Spec is the living truth of the capability, not a record of the process. Finalization therefore deletes the `任务` section and compresses `执行记录` to at most five lines. The delivered artifact must contain no `//TODO`, no unchecked task, and no implementation history; Git history retains the executed plan and evidence.
