---
name: executing-plan
description: Execute, resume, or verify an approved LazySpec spec.md in an isolated worktree, commit per task, await user approval, merge to dev, and automatically finalize delivery.
---

# Executing Spec

## Scope and shared policies

- Report progress and results to the user in Chinese, retaining project keywords and code identifiers.
- Execute approved `specs/{feature_name}/spec.md`. (Status questions are read-only; verification-only requests do not perform implementation repairs).
- Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [delivery-loop.md](../using-lazyspec/references/delivery-loop.md).
- Resolve `specs/{feature_name}/...` against `ACTIVE_PROJECT_ROOT`. Perform memory recall or reuse router-supplied `RelevantMemoryContext` as advisory input.

## Deterministic helpers

Run `scripts/spec_state.py <command>` with Python 3; add `--json` for machine output. The contract gate is `../using-lazyspec/scripts/lazyspec.py check`. A non-zero exit blocks: fix the reported code, never the checker. If Python 3 or the scripts are unavailable, perform the same steps manually and report the degradation.

## Execution Workflow

1. **Verify Authorization**: Confirm `spec.md` is explicitly approved and execution is authorized under approval-policy.md.
2. **Context Discovery**: Read the complete `spec.md`: `目标与范围`, `用户故事`, `验收标准` including every `验证` entry, `决策`, `风险与否定性保证`, the `任务` checklist, and the current `执行记录`.
3. **Worktree & Branch Setup**:
   - Create the isolated worktree and feature branch:
     `python3 <skill-dir>/scripts/spec_state.py worktree add --feature <feature-name> --base dev`
   - The command carries an approved but uncommitted `spec.md` into the worktree (moving it out of the main checkout) so step 4 can commit it as the baseline.
   - Switch active execution context into the returned path. All subsequent code edits, file operations, and verification commands MUST run inside this worktree.
   - Maintain `.execution-progress.md` inside the worktree for local recovery.
4. **First Commit (Spec Baseline)**:
   - Before writing or modifying any implementation code, commit the approved specification as the initial commit of the feature branch:
     `git add specs/{feature_name}/spec.md`
     `git commit -m "docs(spec): add approved specification for <feature-name>"`
   - This baseline commit anchors the approved contract, tasks, and verification plan as the first commit on this branch.
5. **Task Implementation, Basic Check & Commit**:
   - Execute all currently unchecked TODOs continuously without per-TODO confirmation, honoring the shared scope boundary for an explicitly requested subset.
   - For each task: implement the referenced acceptance criterion, then run only its lightweight basic check (syntax/compile check, command probe, or focused basic test). Do not run the full test suite or force a Red-Green TDD cycle on each individual TODO.
   - Only after the TODO passes its basic check, mark and commit it in one call:
     `python3 <skill-dir>/scripts/spec_state.py task-done --feature <feature-name> --n <n> --commit --paths <changed-files>`
   - The command changes only the checkbox token from `[ ]` to `[x]` and must preserve `//TODO` and every character after it; it refuses to commit when unrelated changes are already staged.
   - Every commit must pass its basic check; never commit broken builds. Commit unrelated edits separately.
6. **Feature Verification (Full Test Suite)**:
   - After all TODOs are completed, run the full test suite and every `验证` entry in `验收标准`, including composed flows and risk-specific checks. Enumerate them with `checks --feature <feature-name>` so no row is skipped.
   - Record actual observations with `evidence --commit-record`: `状态`, `验证` (tested commit and time), `结果`, `未决`, following delivery-loop.md. The commit keeps the reviewed evidence on the feature branch so it survives the merge. Do not record fingerprints or raw logs.
7. **User Review Gate (审核门禁)**:
   - Run `check --stage review`. A non-zero exit blocks this gate; the result is not approval.
   - Present a concise handoff and review summary to the user, reporting completed TODOs, commit history, verification evidence, and any affected memory impact candidates.
   - Request explicit user approval to review and accept the feature branch before merging. In orchestration mode, use Orchestrated Execution Handoff for coordinator-owned review and delivery. Do NOT merge to `dev` or delete the worktree without explicit user approval.

## Orchestrated Execution Handoff

When executing under an approved `specs/orchestration.md`, retain this Skill's authorization, worktree isolation, per-task commits, verification, and User Review Gate. After verification, hand off the pinned branch commit and evidence to the coordinator; use [orchestrating-specs](../orchestrating-specs/SKILL.md#coordinated-integration-and-delivery) for integration, review coordination, dev merges, delivery status updates, and cleanup. Only the coordinator runs the finalization procedure below in this mode; a worker's successful verification or received review approval does not authorize it to finalize independently. Workers keep progress in their own worktrees and report it to the coordinator, without editing the shared orchestration record.

## Merge and Automatic Delivery Finalization

For standalone execution, once Feature Verification is `passed` and `current` and the user approves the reviewed feature branch, complete these steps. Verification alone never authorizes them; if the reviewed implementation changes, refresh the affected evidence and review before merging.

1. **Merge to dev**: `git checkout dev` then `git merge --no-ff <feature-branch>`.
2. **Collapse the Execution Scaffolding**: run `python3 <skill-dir>/scripts/spec_state.py deliver --feature <feature-name>`. Effects: Delete the entire `## 任务` section; compress `## 执行记录` to at most five lines; set `status: delivered` and `delivered_at:`; leave no `//TODO`, no unchecked task, and no implementation history. Completed task history remains in Git, and the remaining sections stay the living truth of the capability.
3. **Bidirectional Supersession Sync**: for each path in `supersedes`, the same command sets that Spec to `status: superseded` with `superseded_by: specs/{feature_name}/` and prepends a `[!WARNING]` callout explaining that it is no longer current.
4. **Persist Finalization and Worktree Cleanup**: commit the finalization on `dev` without unrelated edits; run `check --stage delivered` and require a pass; then release the worktree with `spec_state.py worktree remove --feature <feature-name>`. It removes `.execution-progress.md`, refuses tracked changes, and requires `--force` for untracked files after you confirm they are generated artifacts.
5. **Handoff**: Present the final completion report to the user in Chinese, confirming merge into `dev`, worktree removal, and finalized delivery status.
