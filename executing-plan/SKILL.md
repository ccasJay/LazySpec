---
name: executing-plan
description: Execute, resume, or verify approved LazySpec plan.md files, and automatically finalize delivery (updating spec.md status to delivered, in-place cleansing hypothetical language into current-tense decisions, and syncing bidirectional supersessions).
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
3. **Branch Setup**: Create or switch to feature branch `codex/<feature-name>` unless another name is requested. Maintain `.execution-progress.md` for local recovery.
4. **Behavioral TDD Execution**:
   - For each TODO, identify the verification entry point (failing test or command probe) before editing code.
   - Implement the minimal code to satisfy the scenario and make the verification pass.
   - Upon verification success, check off the task token: `- [ ] //TODO` -> `- [x] //TODO`.
5. **Feature Verification**: Run the end-to-end Planned Checks defined in `plan.md`. Record actual observations, timestamps, and commit/worktree fingerprints in Latest Result.

## Automatic Delivery Finalization

Once all TODOs are checked and Feature Verification is evaluated as `passed` with `current` freshness:

1. **Update spec.md Status**:
   - Modify the YAML Frontmatter of `specs/{feature_name}/spec.md`:
     ```yaml
     status: delivered
     delivered_at: YYYY-MM-DD
     ```
2. **In-place Phrasing Cleansing (dsh Style)**:
   - Rewrite any proposal or future-tense phrasing (e.g. "拟议", "计划", "should", "proposed") in `spec.md` into current-tense factual architectural decisions.
3. **Bidirectional Supersession Sync**:
   - If `spec.md` lists `supersedes: [specs/<old-feature>/]`:
     - Open `specs/<old-feature>/spec.md` (or legacy `design.md`);
     - Update its frontmatter to `status: superseded` with `superseded_by: specs/{feature_name}/`;
     - Prepend a warning callout at the top of the superseded file:
       `> [!WARNING]\n> 本规范已被 [specs/{feature_name}/spec.md](../{feature_name}/spec.md) 废黜，请勿作为当前系统事实参考。`
4. **Cleanup**: Remove `.execution-progress.md`.
5. **Handoff**: Present a concise delivery summary, highlighting delivered capabilities, verification pass evidence, and any affected superseded Specs or memory impact candidates.
