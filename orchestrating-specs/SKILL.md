---
name: orchestrating-specs
description: Orchestrate joint execution of multiple user-approved Specs through a temporary specs/orchestration.md covering Spec-level ordering, dependencies, parallelism, stacked branches, coordination constraints, and cross-Spec integration verification. Use only on an explicit multi-Spec orchestration request.
---

# Orchestrating Specs

Coordinate the joint execution of several Specs that each completed planning and hold user approval. This Skill writes one temporary artifact, `specs/orchestration.md`, describing only cross-Spec execution strategy. It is not a new Requirements, Design, or Tasks layer, it never defines new user behavior, and it never interferes with how tasks inside any individual Spec are executed.

## Rule
- The output content should all be in chinese, except the key word from the project

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [delivery-loop.md](../using-lazyspec/references/delivery-loop.md) before this workflow; resolve them relative to this Skill directory. risk-policy.md separates risk-based verification from decision-based approval; approval-policy.md is the single source of explicit-approval, materiality, invalidation, and approval-asking semantics; delivery-loop.md governs each Spec's internal task execution, Feature Verification, repair, and Learning Candidates.

## Project Root

Resolve every `specs/...` path against `ACTIVE_PROJECT_ROOT`, the user's project working directory bound at session start. Never derive `ACTIVE_PROJECT_ROOT` from this Skill's directory, a registered Skill location, the Plugin repository, or a Plugin cache. If invoked directly and the session working directory is unavailable or ambiguous, ask the user for the project root before reading or writing anything.

## Trigger and Preconditions

- Activate only when the user explicitly asks to jointly execute, orchestrate, or implement multiple approved Specs. Never activate merely because the project contains multiple Specs; single-Spec requests keep their existing workflow unchanged.
- Every participating Spec must have its own user-approved `specs/{feature_name}/requirements.md`, `design.md`, and `tasks.md`. Approval comes from explicit confirmation in the conversation; never infer it from file existence.
- If any target Spec lacks an approved three-document Spec — including features with only a fast `plan.md` — report in Chinese which Spec is incomplete and stop; do not create `orchestration.md`.
- If `specs/orchestration.md` already exists, treat the request as a revision of that orchestration; a material change invalidates its approval under approval-policy.md.

## Orchestration Document Contract

Write exactly one artifact: `specs/orchestration.md` under `ACTIVE_PROJECT_ROOT`, following [orchestration-templete.md](orchestration-templete.md) as the output shape, with all prose in Chinese. It MUST cover:

1. 本次多 Spec 交付的整体目标；
2. 涉及的 Spec（路径与批准状态）；
3. Spec 之间的依赖关系；
4. 执行顺序；
5. 可并行执行的部分；
6. 跨 Spec 协调约束；
7. 每个 Spec 的完成条件（其 Feature Verification passed）；
8. 最终跨 Spec Integration Verification。

Boundaries — `orchestration.md` describes Spec-level execution strategy only:

- It MUST NOT define new user behavior, interface requirements, or business scope, and it is not a new Requirements, Design, or Tasks layer.
- It MUST NOT specify how tasks inside any individual Spec are executed: task-level ordering, execution details, verification methods, and repair routing remain governed by that Spec's approved `tasks.md` and delivery-loop.md. The orchestration decides only when a Spec's turn arrives, on which branch, and alongside which other Specs.
- 堆叠分支策略：按逻辑依赖排序的 Spec 依序堆叠建分支（如 A→B→C：B 基于 A 的分支创建，C 基于 B 的分支创建），最后按相同顺序依次 merge；可并行的 Spec 从共同基础分支独立建分支，跨 Spec 集成验证通过后合并。

## Approval

The complete `orchestration.md` is the approval object. Request approval following approval-policy.md's asking protocol; do not start any Spec execution before explicit approval. Material changes — participating Spec set, joint objective, dependency/order, parallelism, branch strategy, coordination constraints, or integration verification — invalidate approval: revise, present the delta, and request approval again.

## Gap Handling

When orchestration planning or execution reveals a requirement, interface, architecture, or behavior gap between existing Specs, route it back to the affected Spec's Requirements, Design, or Tasks revision under delivery-loop.md's failure routing, and follow that Spec's own approval gates. MUST NOT fill the gap inside `orchestration.md` and execute it. When a participating Spec undergoes material revision, update the affected orchestration parts and reapprove per approval-policy.md's materiality rules.

## Execution

Only after orchestration approval:

- Execute each Spec through its own approved Requirements, Design, and Tasks as the source of truth via delivery-loop.md. The orchestration only coordinates — it MUST NOT override or modify any Spec's approved content.
- The orchestration decides Spec-level sequencing, branch stacking, and merge order; each Spec's internal task execution remains fully governed by that Spec's `tasks.md` and delivery-loop.md.
- Branch and merge strategy follows the approved orchestration (overriding the default single-Spec `codex/<feature-name>` branch rule); without an orchestration, single-Spec defaults are unchanged.
- Record per-Spec progress in `orchestration.md`'s lifecycle status as each Spec completes; a Spec counts as complete only when its Feature Verification passes.

## Memory Distillation Gate

- After every Spec's Feature Verification and the cross-Spec Integration Verification have passed, MUST proactively initiate the distillation step: summarize the Learning Candidates and Feature Memory material collected during each Spec's execution, present them to the user, and request confirmation of what should be preserved.
- Candidates the user confirms are routed to `distill-spec-memory` to prepare the exact Capsule/index write preview and are written only after user approval; this Skill MUST NOT bypass that boundary or write Memory directly.
- The gate is complete when required writes are approved and finished, or the user explicitly confirms nothing needs preserving; neither may be silently skipped.

## Lifecycle and Deletion

Lifecycle: 多个 Spec 已批准 → 创建 `orchestration.md` → 用户批准编排 → 按编排执行各 Spec → 所有 Spec Feature Verification passed → 跨 Spec Integration Verification passed → Memory 沉淀门 → 用户确认最终交付 → 删除 `orchestration.md`。

- Completion means every step finished: Spec execution finished or verification passed alone is not completion; MUST NOT skip the distillation gate or the final confirmation.
- Never delete `orchestration.md` because a single Spec's Tasks finished; delete only after the whole group's execution, verification, distillation, and final user confirmation are all complete.
- Deletion is the normal closing action of the lifecycle: delete only `specs/orchestration.md` itself; MUST NOT delete any Spec's Requirements, Design, Tasks, or Feature Verification evidence (distillation products live in `project-memory/` and are unaffected by the deletion).
