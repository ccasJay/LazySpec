---
name: orchestrating-specs
description: Orchestrate joint execution of multiple user-approved Specs through a temporary specs/orchestration.md covering Spec-level ordering, dependencies, parallelism, stacked branches, coordination constraints, and cross-Spec integration verification. Use only on an explicit multi-Spec orchestration request.
---

# Orchestrating Specs

Coordinate the joint execution of several approved Specs through one temporary artifact, `specs/orchestration.md`.

## Rule
- The output content should all be in chinese, except the key word from the project

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [delivery-loop.md](../using-lazyspec/references/delivery-loop.md) before this workflow; resolve them relative to this Skill directory. risk-policy.md separates risk-based verification from decision-based approval; approval-policy.md is the single source of explicit-approval, materiality, invalidation, and approval-asking semantics; delivery-loop.md governs shared Feature Verification and repair. Each Spec's internal execution is governed by [executing-plan/SKILL.md](../executing-plan/SKILL.md).

## Project Root

Resolve every `specs/...` path against `ACTIVE_PROJECT_ROOT`, the user's project working directory bound at session start. Never derive `ACTIVE_PROJECT_ROOT` from this Skill's directory, a registered Skill location, the Plugin repository, or a Plugin cache. If invoked directly and the session working directory is unavailable or ambiguous, ask the user for the project root before reading or writing anything.

## Trigger and Preconditions

- Activate only when the user explicitly asks to jointly execute, orchestrate, or implement multiple approved Specs. Never activate merely because the project contains multiple Specs; single-Spec requests keep their existing workflow unchanged.
- Every participating Spec must have its own user-approved `specs/{feature_name}/spec.md` and `plan.md`. Approval comes from explicit confirmation in the conversation; never infer it from file existence.
- If any target Spec lacks an approved Spec and Plan, report in Chinese which Spec is incomplete and stop; do not create `orchestration.md`.
- If `specs/orchestration.md` already exists, treat the request as a revision of that orchestration; a material change invalidates its approval under approval-policy.md.

## Orchestration Document Contract

Write exactly one artifact: `specs/orchestration.md` under `ACTIVE_PROJECT_ROOT`, following [orchestration-templete.md](orchestration-templete.md) as the canonical output shape and lifecycle checklist, with all prose in Chinese.

Boundaries — `orchestration.md` describes Spec-level execution strategy only:

- It MUST NOT define new user behavior, interface requirements, or business scope, and it is not a new Spec or Plan layer. It MUST NOT override or modify any Spec's approved content.
- It MUST NOT specify how tasks inside any individual Spec are executed: task-level ordering, execution details, and verification methods remain governed by that Spec's approved `plan.md` and executing-plan/SKILL.md; shared repair routing remains in delivery-loop.md. The orchestration decides only when a Spec's turn arrives, on which branch, and alongside which other Specs.
- 堆叠分支策略：按逻辑依赖排序的 Spec 依序堆叠建分支（如 A→B→C：B 基于 A 的分支创建，C 基于 B 的分支创建），最后按相同顺序依次 merge；可并行的 Spec 从共同基础分支独立建分支，跨 Spec 集成验证通过后合并。

## Approval

The complete `orchestration.md` is the approval object. Request approval following approval-policy.md's orchestration gate and asking protocol; do not start any Spec execution before explicit approval. Revision and invalidation rules remain in that policy.

## Gap Handling

When orchestration planning or execution reveals a requirement, interface, architecture, or behavior gap between existing Specs, route it back to the affected Spec's `spec.md` or `plan.md` revision under delivery-loop.md's failure routing, and follow that Spec's own approval gates. MUST NOT fill the gap inside `orchestration.md` and execute it. When a participating Spec undergoes material revision, update the affected orchestration parts and reapprove per approval-policy.md's materiality rules.

## Execution

Only after orchestration approval:

- Execute each Spec through its own approved `spec.md` and `plan.md` as the source of truth via executing-plan/SKILL.md, using the approved orchestration's Spec-level sequencing and branch/merge strategy. Each Spec retains executing-plan's user-review and merge gate.
- Record per-Spec progress in `orchestration.md`'s lifecycle status as each Spec completes; a Spec counts as complete only when its Feature Verification passes.

## Memory Distillation Gate

- After every Spec's Feature Verification and the cross-Spec Integration Verification have passed, MUST proactively initiate the distillation step: summarize the Feature Memory material collected during each Spec's execution, present them to the user, and request confirmation of what should be preserved.
- Candidates the user confirms are routed to `distill-feature` to prepare the exact Capsule/index write preview and are written only after user approval; this Skill MUST NOT bypass that boundary or write Memory directly.
- The gate is complete when required writes are approved and finished, or the user explicitly confirms nothing needs preserving; neither may be silently skipped.

## Lifecycle and Deletion

Follow the template's lifecycle checklist; verification alone is not group completion.
- Never delete `orchestration.md` because a single Spec's tasks finished; delete only after the whole group's execution, verification, distillation, and final user confirmation are all complete.
- Deletion is the normal closing action of the lifecycle: delete only `specs/orchestration.md` itself; MUST NOT delete any Spec's `spec.md`, `plan.md`, or Feature Verification evidence.
