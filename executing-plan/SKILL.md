---
name: executing-plan
description: Execute, resume, or verify approved LazySpec plan.md files in an isolated worktree, commit per TODO, await user approval, merge to dev, and automatically finalize delivery.
---

# Executing Plan

## Scope and shared policies

- Report progress and results to the user in Chinese, retaining project keywords and code identifiers.
- Execute approved `specs/{feature_name}/plan.md` plans. (Status questions are read-only; verification-only requests do not perform implementation repairs).
- Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [delivery-loop.md](../using-lazyspec/references/delivery-loop.md).
- Resolve `specs/{feature_name}/...` against `ACTIVE_PROJECT_ROOT`. Perform memory recall or reuse router-supplied `RelevantMemoryContext` as advisory input.

## Execution Workflow

1. **Verify Authorization**: Confirm `spec.md` and `plan.md` are explicitly approved under approval-policy.md.
2. **Context Discovery**: Read complete `spec.md` (goal, EARS criteria, architecture decisions, invariants) and the `plan.md` checklist with Planned Checks.
3. **Worktree & Branch Setup**:
   - Create a dedicated Git worktree and feature branch based on `dev` (unless another base branch or name is requested):
     `git worktree add -b <feature-branch> .worktrees/<feature-name> dev`
     (default feature branch name: `codex/<feature-name>` or `feat/<feature-name>`). An approved `specs/orchestration.md` supplies cross-Spec branch and sequencing constraints instead.
   - Switch active execution context into the newly created worktree directory. All subsequent code edits, file operations, and verification commands MUST run inside this worktree.
   - Maintain `.execution-progress.md` inside the worktree for local recovery.
4. **First Commit (Spec Baseline)**:
   - Before writing or modifying any implementation code, commit the approved specification assets as the initial commit of the feature branch:
     `git add specs/{feature_name}/spec.md specs/{feature_name}/plan.md`
     `git commit -m "docs(spec): add approved specification and plan for <feature-name>"`
   - This baseline commit anchors the approved requirements and plan as the first commit on this branch.
5. **Behavioral TDD & Per-TODO Commit Execution**:
   - Execute all currently unchecked TODOs continuously without per-TODO confirmation.
   - For each TODO:
     1. Identify the verification entry point (failing test or command probe) before editing code (Red).
     2. Implement the minimal code to satisfy the scenario and make the verification pass (Green).
     3. Only after the TODO passes, change its checkbox token from `[ ]` to `[x]`. Preserve `//TODO` and every character after it.
     4. **Per-TODO Atomic Commit**: Create a dedicated Git commit immediately for this completed TODO:
        `git add <changed-files> specs/{feature_name}/plan.md`
        `git commit -m "feat(<feature-name>): implement TODO <n> - <task description>"`
        Every commit must be a green, test-passing atomic commit; never commit broken builds.
6. **Feature Verification**: Run the end-to-end Planned Checks defined in `plan.md`. Record actual observations, timestamps, and commit/worktree fingerprints in Latest Result.
7. **User Review Gate (审核门禁)**:
   - After all TODOs are checked and Feature Verification is evaluated as `passed` with `current` freshness:
   - Present a concise handoff and review summary to the user, reporting completed TODOs, atomic commit history, verification evidence, and any affected memory impact candidates.
   - Request explicit user approval to review and accept the feature branch before merging. Do NOT merge to `dev` or delete the worktree without explicit user approval.

## Merge and Automatic Delivery Finalization

Once the user approves the reviewed feature branch:

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
3. **In-place Phrasing Cleansing**:
   - Cleanses proposal/hypothetical phrasing (e.g. "拟议", "计划", "should", "proposed") in `spec.md` into current-tense factual architectural decisions (Decision).
4. **Bidirectional Supersession Sync**:
   - If `spec.md` lists `supersedes: [specs/<old-feature>/]`:
     - Open `specs/<old-feature>/spec.md`;
     - Update its frontmatter to `status: superseded` with `superseded_by: specs/{feature_name}/`;
     - Prepend a warning callout at the top of the superseded file:
       `> [!WARNING]`
       `> 本规范已被新规范废黜，请勿作为当前系统事实参考。`
5. **Worktree Cleanup**:
   - Safely remove the worktree and clean up the temporary progress record:
     `git worktree remove .worktrees/<feature-name>`
     (and delete `.execution-progress.md`).
6. **Handoff**: Present the final completion report to the user in Chinese, confirming merge into `dev`, worktree removal, and finalized delivery status.
