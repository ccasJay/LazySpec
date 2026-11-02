---
name: using-lazyspec
description: Route LazySpec single-artifact planning (spec.md), execution and automated delivery, and memory governance. Apply risk-based approval and evidence-backed repair boundaries.
---

# LazySpec

## Rule
- The output content should all be in chinese, except the key word from the project

## Resource Loading

Load only resources required by the selected route.

| Route | Required resources |
|---|---|
| spec | risk-policy, approval-policy, doc-policy, delivery-loop |
| execute | risk-policy, approval-policy, delivery-loop |
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

[approval-policy.md](references/approval-policy.md) owns approval semantics and user questions; [risk-policy.md](references/risk-policy.md) owns risk classification and verification depth; [delivery-loop.md](references/delivery-loop.md) owns shared verification, repair, lifecycle state definitions. `writing-spec` owns the single planning artifact and its approval; `executing-plan` owns execution and delivery finalization. [doc-policy.md](references/doc-policy.md) owns documentation scope; [memory-workflow.md](references/memory-workflow.md) owns Memory write preparation and cleanup; [memory-recall.md](references/memory-recall.md) owns recall. Load each only for its route.

## Deterministic helpers

`scripts/lazyspec_core/` holds the shared implementation; every skill calls it through its own entry script. Run with Python 3; a non-zero exit blocks and means fix the code, never the checker.

- `scripts/lazyspec.py check --feature <f> --stage plan|review|delivered` — contract gate.
- `scripts/lazyspec.py recall --query <text>` — bounded Memory recall.
- `scripts/lazyspec.py scan-retired` — obsolete Specs and reasons.

If Python 3 or the scripts are unavailable, follow the policy manually.

## Routing Protocol
Use this Skill as the single entry point. Route by logical Skill name and read only that Skill's required resources; do not copy a routed Skill's detailed body here.

Before inspecting or writing any Spec artifact, bind `ACTIVE_PROJECT_ROOT` to the user's project working directory at the start of the current agent session. Resolve every `specs/{feature_name}/...` path against that directory. Never derive `ACTIVE_PROJECT_ROOT` from this Skill's directory, a registered Skill location, the Plugin repository, or a Plugin cache. If the session working directory is unavailable or ambiguous, ask the user for the project root before writing; never default to the Plugin installation directory.

Resolve every routed Skill with this platform-neutral protocol:

1. Prefer the current environment's registered Skill invocation mechanism. Use the logical names `writing-spec`, `executing-plan`, `distill-feature`, `maintain-memory`, `orchestrating-specs`; a Claude Code Plugin may expose them as `lazyspec:<logical-name>`, while an Agent Skills installation may expose the unnamespaced logical name.
2. If no registered Skill invocation mechanism is available, or the logical Skill is not registered, read its sibling `SKILL.md` using the fallback mapping below. Resolve the path relative to this `using-lazyspec/SKILL.md`, never relative to the process working directory or repository root.
3. After resolving the target, follow that Skill's instructions and resolve its supporting files by the target Skill's own resource rules.

| Logical name | Registered Claude Code name | Relative fallback |
|---|---|---|
| `writing-spec` | `lazyspec:writing-spec` | `../writing-spec/SKILL.md` |
| `executing-plan` | `lazyspec:executing-plan` | `../executing-plan/SKILL.md` |
| `distill-feature` | `lazyspec:distill-feature` | `../distill-feature/SKILL.md` |
| `maintain-memory` | `lazyspec:maintain-memory` | `../maintain-memory/SKILL.md` |
| `orchestrating-specs` | `lazyspec:orchestrating-specs` | `../orchestrating-specs/SKILL.md` |

### Negative Guardrails Inspection

Before routing to `writing-spec` or initiating new feature planning:
- Run `scripts/lazyspec.py scan-retired` to list `specs/retired/` and obsolete entries in `project-memory/`; if the command is unavailable, inspect those paths directly.
- If the requested capability or approach matches a retired/obsolete specification or negative guardrail, issue an immediate warning in Chinese citing the retirement reason and require user confirmation before proceeding, preventing the agent from repeating past mistakes.

### Memory Distillation & Governance Routing

- Route to `distill-feature` when the user explicitly requests distilling an already delivered feature into a Feature Capsule, using its Spec.
- Route to `maintain-memory` for memory and specs maintenance, supersession propagation, foundation archival, or index self-healing.
- Do not infer a distillation request from task completion; exact Memory write approval remains separate.

### Multi-Spec Orchestration Routing

- Route to `orchestrating-specs` only when the user explicitly asks to jointly execute, orchestrate, or implement multiple approved Specs. Never infer an orchestration request from the mere existence of multiple Specs; single-Spec requests keep the normal chain unchanged.
- An orchestration request is an ordinary LazySpec request: apply Memory Recall Routing before routing, and pass `RelevantMemoryContext` to `orchestrating-specs` as advisory input.
- `specs/orchestration.md` coordinates cross-Spec execution only; its boundaries and lifecycle are owned by `orchestrating-specs`.

### Memory Recall Routing

For every ordinary LazySpec request, after binding `ACTIVE_PROJECT_ROOT` and before selecting the routed Skill, build a session-only `RelevantMemoryContext` by following [memory-recall.md](references/memory-recall.md) exactly.

Inspect the requested feature's `specs/{feature_name}/spec.md` under `ACTIVE_PROJECT_ROOT`, the user's request, and explicit approvals available in the current conversation. Do not infer approval from file existence.

### Phase Chain (Single-Artifact Architecture)

1. **Phase 1: Spec Creation / Revision**:
   - For a new feature or revision of `spec.md`, route directly to `writing-spec`. The approved `spec.md` is the only planning artifact and carries user stories, acceptance criteria with inline verification, decisions, risks, and tasks.
2. **Phase 2: Execution, Review, and Delivery Finalization**:
   - For `spec.md` execution, resume, or verification requests, route to `executing-plan` after checking Spec approval and execution authorization under approval-policy.md. It owns the worktree, commit, user-review, merge, and finalization procedure.

## Task Instructions

- Answer task-information requests read-only without modifying code, Spec files, checkbox state, or the temporary progress record.
