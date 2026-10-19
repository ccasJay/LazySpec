---
name: orchestrating-specs
description: Orchestrate joint execution of multiple user-approved Specs through a temporary specs/orchestration.md prioritizing parallel Spec execution, explicit implementation dependencies, isolated worktrees, and coordinated integration and merges. Use only on an explicit multi-Spec orchestration request.
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
- Scheduling, branch isolation, and integration follow the policies below; individual Spec task decomposition remains unchanged.

## Parallel Scheduling

Default to parallel Spec implementation. Record this scheduling policy in `orchestration.md`; dispatch work only after orchestration approval:

- Derive implementation prerequisites from approved Specs/Plans. An agreed interface contract or a business relationship is not automatically a finish-to-start dependency. Use the Specs' defined contracts and local verification substitutes where applicable; unresolved contracts return through Gap Handling. Record each necessary wait with its concrete artifact, readiness condition, and reason; reject circular implementation prerequisites for design correction.
- Identify incompatible edits and shared mutable resources (including test databases, ports, and migrations). Prefer isolated worktrees and test resources; shared files alone do not justify serializing whole Specs. Record remaining exclusive-resource constraints, rather than silently adding an implementation dependency.
- Assign one executor, feature branch, and isolated worktree per active Spec, and one coordinator. Record a concrete concurrency limit within available authorized executor capacity and any user limits. Use parallel executors only where available and authorized; otherwise report the limitation and record feasible scheduling without claiming concurrent execution. Do not infer delegation permission from orchestration approval alone.
- Dispatch ready Specs up to that limit, and fill freed capacity as soon as prerequisites and exclusive resources allow; do not wait for an entire batch. A blocked or review-pending Spec must not hold unrelated ready Specs; only unsatisfied prerequisites or exclusive resources block dependents. An upstream artifact can release dependents before a dev merge only when the approved readiness condition is met, its verification is current, and its commit is pinned.
- Branch independently from the recorded common base by default. Use stacked branches only for concrete implementation prerequisites: pin the required upstream verified commit, create the dependent branch from it, and merge upstream before downstream. Changes to that artifact require reassessing dependent code and verification; do not rewrite published commit history automatically.

## Coordinated Integration and Delivery

- Executors run executing-plan through Feature Verification and hand off their branch commit, evidence, unresolved issues, and review status. The coordinator alone writes `orchestration.md`, integrates branches, and performs dev merges and delivery finalization. Executors do not switch the main checkout, merge to dev, change delivery status, or remove worktrees independently.
- Combine pinned participating commits in a separate integration worktree and run the approved cross-Spec checks before dev merges. Record the tested base, branch commits, actual results, and freshness in `orchestration.md`. Local verification with substitutes is not integration success. Keep implementation-ready, verified, review-approved, and merged states distinct; integration alone is not approval.
- After current feature and integration verification and explicit review/merge approval covering each branch, serialize merges and use executing-plan's finalization procedure for each Spec. A grouped approval may cover explicitly identified branches and commits; orchestration approval alone does not approve merges. Merge dependencies first. If a branch, relevant base, or integration resolution changes, refresh affected checks and review under the existing evidence/approval rules before merging; never mark a Spec delivered merely because its worker finished.
- Retain dependent and integration worktrees until no remaining work needs them. Clean them only after the reviewed changes and evidence are preserved and the worktrees can be safely removed. Continue the Memory and final group-confirmation gates below.

## Approval

The complete `orchestration.md` is the approval object. Request approval following approval-policy.md's orchestration gate and asking protocol; do not start any Spec execution before explicit approval. Revision and invalidation rules remain in that policy.

## Gap Handling

When orchestration planning or execution reveals a requirement, interface, architecture, or behavior gap between existing Specs, route it back to the affected Spec's `spec.md` or `plan.md` revision under delivery-loop.md's failure routing, and follow that Spec's own approval gates. MUST NOT fill the gap inside `orchestration.md` and execute it. When a participating Spec undergoes material revision, update the affected orchestration parts and reapprove per approval-policy.md's materiality rules.

## Execution

Only after orchestration approval:

- Execute each Spec through its own approved `spec.md` and `plan.md` as the source of truth via executing-plan/SKILL.md, using the approved orchestration's Spec-level sequencing and branch/merge strategy. Each Spec retains executing-plan's user-review and merge gate.
- Record each Spec's executor/worktree, prerequisites, pinned commit, current verification, review, merge, and blocking status in `orchestration.md`. Apply Parallel Scheduling continuously; group delivery requires every Spec to finish coordinated integration and delivery, not just Feature Verification.

## Memory Distillation Gate

- After every Spec's Feature Verification and the cross-Spec Integration Verification have passed, MUST proactively initiate the distillation step: summarize the Feature Memory material collected during each Spec's execution, present them to the user, and request confirmation of what should be preserved.
- Candidates the user confirms are routed to `distill-feature` to prepare the exact Capsule/index write preview and are written only after user approval; this Skill MUST NOT bypass that boundary or write Memory directly.
- The gate is complete when required writes are approved and finished, or the user explicitly confirms nothing needs preserving; neither may be silently skipped.

## Lifecycle and Deletion

Follow the template's lifecycle checklist; verification alone is not group completion.
- Never delete `orchestration.md` because a single Spec's tasks finished; delete only after the whole group's execution, verification, distillation, and final user confirmation are all complete.
- Deletion is the normal closing action of the lifecycle: delete only `specs/orchestration.md` itself; MUST NOT delete any Spec's `spec.md`, `plan.md`, or Feature Verification evidence.
