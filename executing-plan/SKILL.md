---
name: executing-plan
description: Execute, resume, or verify an approved LazySpec spec.md in an isolated worktree, commit per TODO, await user approval, merge to dev, and automatically finalize delivery.
---

# Executing Spec

## Scope and shared policies

- Report progress and results to the user in Chinese, retaining project keywords and code identifiers.
- Execute approved `specs/{feature_name}/spec.md`. (Status questions are read-only; verification-only requests do not perform implementation repairs).
- Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [delivery-loop.md](../using-lazyspec/references/delivery-loop.md).
- Resolve `specs/{feature_name}/...` against `ACTIVE_PROJECT_ROOT`. Perform memory recall or reuse router-supplied `RelevantMemoryContext` as advisory input.

## Execution Workflow

1. **Verify Authorization**: Confirm `spec.md` is explicitly approved and execution is authorized under approval-policy.md.
2. **Context Discovery**: Read the complete `spec.md`: `目标与范围`, `用户故事`, `验收标准` including every `验证` entry, `决策`, `风险与否定性保证`, the `任务` checklist, and the current `执行记录`.
3. **Worktree & Branch Setup**:
   - Create a dedicated Git worktree and feature branch based on `dev` (unless another base branch or name is requested):
     `git worktree add -b <feature-branch> .worktrees/<feature-name> dev`
     (default feature branch name: `codex/<feature-name>` or `feat/<feature-name>`). An approved `specs/orchestration.md` supplies cross-Spec branch and sequencing constraints instead.
   - Switch active execution context into the newly created worktree directory. All subsequent code edits, file operations, and verification commands MUST run inside this worktree.
   - Maintain `.execution-progress.md` inside the worktree for local recovery.
4. **First Commit (Spec Baseline)**:
   - Before writing or modifying any implementation code, commit the approved specification as the initial commit of the feature branch:
     `git add specs/{feature_name}/spec.md`
     `git commit -m "docs(spec): add approved specification for <feature-name>"`
   - This baseline commit anchors the approved contract, tasks, and verification plan as the first commit on this branch.
5. **Per-TODO Implementation, Basic Check & Commit Execution**:
   - Execute all currently unchecked TODOs continuously without per-TODO confirmation, honoring the shared scope boundary for an explicitly requested subset.
   - For each TODO:
     1. Implement the code required to satisfy the TODO's referenced acceptance criterion.
     2. Run only the lightweight basic check defined for this TODO (e.g., syntax/compile check, command probe, or focused basic test). Do not run the full test suite or force a Red-Green TDD cycle on each individual TODO.
     3. Only after the TODO passes its basic check, change its checkbox token from `[ ]` to `[x]`. Preserve `//TODO` and every character after it, and do not modify any other line in the contract sections.
     4. **Per-TODO Atomic Commit**: Create a dedicated Git commit immediately for this completed TODO:
        `git add <changed-files> specs/{feature_name}/spec.md`
        `git commit -m "feat(<feature-name>): implement TODO <n> - <task description>"`
        Every commit must pass its basic check; never commit broken builds.
6. **Feature Verification (Full Test Suite)**:
   - After all TODOs are completed, run the full test suite and every `验证` entry in `验收标准`, including composed flows and risk-specific checks.
   - Record actual observations in the four-line `执行记录`: `状态`, `验证` (tested commit and time), `结果`, `未决`, following delivery-loop.md. Do not record fingerprints or raw logs.
7. **User Review Gate (审核门禁)**:
   - After all TODOs are checked and Feature Verification is evaluated as `passed` with `current` freshness:
   - Present a concise handoff and review summary to the user, reporting completed TODOs, atomic commit history, verification evidence, and any affected memory impact candidates.
   - Request explicit user approval to review and accept the feature branch before merging. In orchestration mode, use Orchestrated Execution Handoff for coordinator-owned review and delivery. Do NOT merge to `dev` or delete the worktree without explicit user approval.

## Orchestrated Execution Handoff

When executing under an approved `specs/orchestration.md`, retain this Skill's authorization, worktree isolation, per-TODO commits, verification, and User Review Gate. After verification, hand off the pinned branch commit and evidence to the coordinator; use [orchestrating-specs](../orchestrating-specs/SKILL.md#coordinated-integration-and-delivery) for integration, review coordination, dev merges, delivery status updates, and cleanup. Only the coordinator runs the finalization procedure below in this mode; a worker's successful verification or received review approval does not authorize it to finalize independently. Workers keep progress in their own worktrees and report it to the coordinator, without editing the shared orchestration record.

## Merge and Automatic Delivery Finalization

For standalone execution, once Feature Verification is `passed` and `current` and the user approves the reviewed feature branch, complete these steps. Verification alone never authorizes them; if the reviewed implementation changes, refresh the affected evidence and review before merging.

1. **Merge to dev**:
   - Switch to the main repository and merge the feature branch into `dev`:
     `git checkout dev`
     `git merge --no-ff <feature-branch>`
2. **Update spec.md Status**:
   - Modify the YAML Frontmatter of `specs/{feature_name}/spec.md`:
     ```yaml
     status: delivered
     delivered_at: YYYY-MM-DD
     ```
3. **Collapse the Execution Scaffolding**:
   - Delete the entire `## 任务` section; completed task history remains in Git.
   - Compress `## 执行记录` to at most five lines: final status, tested commit and date, outcome summary, and unresolved items.
   - Keep `目标与范围`, `用户故事`, `验收标准`, `决策`, and `风险与否定性保证` as the living truth of the capability.
   - The delivered artifact must contain no `//TODO`, no unchecked task, and no implementation history.
4. **Bidirectional Supersession Sync**:
   - If `spec.md` lists `supersedes: [specs/<old-feature>/]`:
     - Open `specs/<old-feature>/spec.md`;
     - Update its frontmatter to `status: superseded` with `superseded_by: specs/{feature_name}/`;
     - Prepend a warning callout at the top of the superseded file:
       `> [!WARNING]`
       `> 本规范已被新规范废黜，请勿作为当前系统事实参考。`
5. **Persist Finalization and Worktree Cleanup**:
   - Commit the Spec status, task removal, compressed execution record, and supersession changes on `dev`, without including unrelated edits.
   - Remove the temporary `.execution-progress.md` record, then safely remove the clean worktree:
     `git worktree remove .worktrees/<feature-name>`
6. **Handoff**: Present the final completion report to the user in Chinese, confirming merge into `dev`, worktree removal, and finalized delivery status.
