---
name: using-lazyspec
description: Route LazySpec binary planning (spec.md, plan.md), execution and automated delivery, fast mode, and memory governance. Apply risk-based approval and evidence-backed repair boundaries.
---

# LazySpec

## Rule
- The output content should all be in chinese, except the key word from the project

## Resource Loading

Load only resources required by the selected route.

| Route | Required resources |
|---|---|
| spec | risk-policy, approval-policy, doc-policy |
| plan | risk-policy, approval-policy, doc-policy, delivery-loop |
| execute | risk-policy, approval-policy, delivery-loop |
| fast | risk-policy, approval-policy, delivery-loop |
| orchestration | risk-policy, approval-policy, delivery-loop |
| memory-recall | memory-recall |
| memory-distill | approval-policy, memory-workflow |
| memory-maintain | approval-policy, memory-workflow, delivery-loop |

Rules:
- Load the routed Skill after selecting the route.
- Load conditional resources only when their route or condition applies.
- Do not preload every reference at session start.
- A routed Skill may load its own prompt/template/resources.
- Resolve every reference from this Skill's `references/` directory; if a resource is unavailable, report the missing resource rather than inventing a policy.

[approval-policy.md](references/approval-policy.md) owns approval semantics and user questions; [risk-policy.md](references/risk-policy.md) owns risk classification and verification depth; [delivery-loop.md](references/delivery-loop.md) owns shared verification, repair, lifecycle state definitions. `executing-plan` owns normal-mode execution and delivery finalization; `fast` owns fast execution. [doc-policy.md](references/doc-policy.md) owns documentation scope; [memory-workflow.md](references/memory-workflow.md) owns Memory write preparation and cleanup; [memory-recall.md](references/memory-recall.md) owns recall. Load each only for its route.

## Routing Protocol
Use this Skill as the single entry point. Route by logical Skill name and read only that Skill's required resources; do not copy a phase's detailed body here.

Before inspecting or writing any Spec artifact, bind `ACTIVE_PROJECT_ROOT` to the user's project working directory at the start of the current agent session. Resolve every `specs/{feature_name}/...` path against that directory. Never derive `ACTIVE_PROJECT_ROOT` from this Skill's directory, a registered Skill location, the Plugin repository, or a Plugin cache. If the session working directory is unavailable or ambiguous, ask the user for the project root before writing; never default to the Plugin installation directory.

Resolve every routed Skill with this platform-neutral protocol:

1. Prefer the current environment's registered Skill invocation mechanism. Use the logical names `writing-spec`, `writing-plan`, `executing-plan`, `distill-feature`, `maintain-memory`, `fast`, `orchestrating-specs`; a Claude Code Plugin may expose them as `lazyspec:<logical-name>`, while an Agent Skills installation may expose the unnamespaced logical name.
2. If no registered Skill invocation mechanism is available, or the logical Skill is not registered, read its sibling `SKILL.md` using the fallback mapping below. Resolve the path relative to this `using-lazyspec/SKILL.md`, never relative to the process working directory or repository root.
3. After resolving the target, follow that Skill's instructions and resolve its supporting files by the target Skill's own resource rules.

| Logical name | Registered Claude Code name | Relative fallback |
|---|---|---|
| `writing-spec` | `lazyspec:writing-spec` | `../writing-spec/SKILL.md` |
| `writing-plan` | `lazyspec:writing-plan` | `../writing-plan/SKILL.md` |
| `executing-plan` | `lazyspec:executing-plan` | `../executing-plan/SKILL.md` |
| `distill-feature` | `lazyspec:distill-feature` | `../distill-feature/SKILL.md` |
| `maintain-memory` | `lazyspec:maintain-memory` | `../maintain-memory/SKILL.md` |
| `fast` | `lazyspec:fast` | `../fast/SKILL.md` |
| `orchestrating-specs` | `lazyspec:orchestrating-specs` | `../orchestrating-specs/SKILL.md` |

### Negative Guardrails Inspection

Before routing to `writing-spec` or initiating new feature planning:
- Inspect `specs/retired/` (or obsolete entries in `project-memory/`).
- If the requested capability or approach matches a retired/obsolete specification or negative guardrail, issue an immediate warning in Chinese citing the retirement reason and require user confirmation before proceeding, preventing the agent from repeating past mistakes.

### Memory Distillation & Governance Routing

- Route to `distill-feature` when the user explicitly requests distilling an already delivered feature into a Feature Capsule, using its Spec or verified fast plan.
- Route to `maintain-memory` for memory and specs maintenance, supersession propagation, foundation archival, or index self-healing.
- Do not infer a distillation request from task completion; exact Memory write approval remains separate.

### Fast Mode Routing

- For new features, route to `fast` only when the user explicitly asks for fast mode (keywords such as `fast` or `快速`, or a direct `fast` / `lazyspec:fast` invocation). Also route explicit requests to execute, verify, or revise an existing fast plan.md to fast; this resumes its existing mode rather than inferring fast for a new feature.
- Fast creation and subsequent plan operations are allowed only when the target feature has no `specs/{feature_name}/spec.md`. If `spec.md` already exists, keep the request on the normal chain, report in Chinese why fast mode was declined, and route by the ordinary rules below.
- A `fast` request is an ordinary LazySpec request: apply Memory Recall Routing before routing, and pass `RelevantMemoryContext` to `fast` as advisory input.

### Multi-Spec Orchestration Routing

- Route to `orchestrating-specs` only when the user explicitly asks to jointly execute, orchestrate, or implement multiple approved Specs. Never infer an orchestration request from the mere existence of multiple Specs; single-Spec requests keep the normal chain unchanged.
- An orchestration request is an ordinary LazySpec request: apply Memory Recall Routing before routing, and pass `RelevantMemoryContext` to `orchestrating-specs` as advisory input.
- `specs/orchestration.md` coordinates cross-Spec execution only; its boundaries and lifecycle are owned by `orchestrating-specs`.

### Memory Recall Routing

For every ordinary LazySpec request, after binding `ACTIVE_PROJECT_ROOT` and before selecting the phase Skill, build a session-only `RelevantMemoryContext` by following [memory-recall.md](references/memory-recall.md) exactly.

Inspect the requested feature's `specs/{feature_name}/spec.md` and `plan.md` under `ACTIVE_PROJECT_ROOT`, the user's request, and explicit approvals available in the current conversation. Do not infer approval from file existence.

### Phase Chain (Binary Architecture)

1. **Phase 1: Spec Creation / Revision**:
   - For a new feature or revision of `spec.md`, route directly to `writing-spec`.
2. **Phase 2: Plan Creation / Revision**:
   - Only after explicit approval of `spec.md`, route to `writing-plan`.
3. **Phase 3: Execution, Review, and Delivery Finalization**:
   - For normal `plan.md` execution, resume, or verification requests, route to `executing-plan` after checking Spec/Plan approvals and execution authorization under approval-policy.md. It owns the worktree, commit, user-review, merge, and finalization procedure.

## Task Instructions

- Answer task-information requests read-only without modifying code, Spec files, checkbox state, or the temporary progress record.
