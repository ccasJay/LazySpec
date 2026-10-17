---
name: writing-spec
description: Probe requirements and architectural decisions using /grill-me structured questions, reconcile related uncommitted Specs, then draft a unified spec.md containing EARS criteria, architecture decisions, and alternatives considered. Request explicit Spec approval before LazySpec enters planning.
---

# Writing Spec

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [doc-policy.md](../using-lazyspec/references/doc-policy.md) before this workflow; resolve them relative to the directory containing this `SKILL.md`. risk-policy.md separates risk-based verification from decision-based approval; approval-policy.md governs explicit approvals, materiality, and the single-body contract; doc-policy.md keeps the binary spec minimum-sufficient.

## Language and paths

- Keep instructional prose in this Skill and its resources in English.
- Write all user-visible prose in generated `spec.md` content in Chinese, including the title, headings, goal/scope, EARS criteria, architecture decisions, alternatives considered, and risks.
- Preserve project-specific names, code identifiers, filenames, and Markdown/HTML anchor IDs.
- Resolve supporting resources (`spec-prompt.md`, `spec-template.md`) relative to the directory containing this `SKILL.md`.
- Resolve `specs/{feature_name}/spec.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before writing.

## Uncommitted Spec Boundary Check

Before design probing for a new or revised Spec, inspect staged, unstaged, and untracked changes from `ACTIVE_PROJECT_ROOT`:

```sh
git status --porcelain=v1 -z --untracked-files=all -M -- specs/
```

- Treat the output as NUL-delimited records, including both index and working-tree status. For renames, use the destination path and consume the following source-path field. Select other added, modified, or renamed `specs/<feature>/spec.md` files that currently exist; exclude the current Spec, deleted files, and `specs/archived/` and `specs/retired/`. Limit this check to the current working tree; do not search other branches or worktrees. If Git is unavailable or the project is not a Git repository, report the limitation in Chinese and continue with visible project evidence.
- Read each candidate's complete current working-tree content, rather than only its diff or staged version. Use goals, responsibilities, interfaces, data, and constraints to identify related Specs; skip unrelated ones. Include incomplete drafts and completed designs. File existence or `status: proposed` establishes neither approval nor implementation; other drafts are designs to coordinate, not automatically binding constraints or available capabilities. Apply approval-policy.md to any approval established in the conversation.
- For related Specs, check overlapping responsibilities, conflicting interface or data ownership, circular dependencies, reliance on another Spec's internals, and contradictory constraints. Prefer explicit ownership and dependencies through defined contracts. Preserve necessary dependencies; do not introduce abstractions or split features merely to claim decoupling.
- Resolve conflicts in the current Spec first, defining its responsibilities, exclusions, dependency contracts, and relevant absence/failure behavior. Reference the owning Spec instead of duplicating its contract. If resolution requires materially changing another Spec, explain the conflict and proposed coordinated change and ask under approval-policy.md before that dependent work; do not modify other Specs by default or silently choose a conflicting design. Continue independent design work where possible.
- Keep inspected paths and content versions in session context. After saving the current Spec and before requesting approval, rerun discovery and compare current candidate contents; reassess new, changed, renamed, or removed peers and any resulting boundary decisions. Resolve material conflicts before presenting the file for approval. Record relevant boundaries and dependencies concisely within the current Spec's architecture section; with no related Specs, continue normally without an extra section or table. Do not create another artifact, status field, approval phase, or orchestration workflow for this check.

## Structured Probing (/grill-me Style)

Instead of mechanical, one-by-one incremental confirmations, `writing-spec` conducts a structured decision interview:

1. **Inspect and Research**: Complete the Uncommitted Spec Boundary Check, then inspect the user's request, project architecture, and relevant existing codebase facts before asking.
2. **Identify Branches of Decision Tree**:
   - Scope and boundaries (what is in, what is explicitly out);
   - Core behavior and observable outcomes (EARS scenarios);
   - Architecture and component relationships;
   - Competing approaches and technical trade-offs (Alternatives Considered);
   - Invariants, risks, and negative guarantees.
3. **Ask One Focused Decision Question at a Time**:
   - Use the available user-question tool (following approval-policy.md's `How to ask`).
   - Format questions as structured single-choice or multi-choice options with a justified `(Recommended)` prefix on the best option.
   - Explain the trade-offs and consequences concisely.
   - Wait for the actual answer before proceeding down that branch of the design tree.
4. **Conclude Probing**: Once material requirements and design decisions reach a shared understanding, ask whether the user has additional constraints or is ready to generate `spec.md`.

## Document Contract

Read [spec-prompt.md](spec-prompt.md) for content rules and [spec-template.md](spec-template.md) for the canonical frontmatter and document shape before drafting. Together they define the combined requirements/design document; do not maintain another schema here. Record the risk assessment required by risk-policy.md in the template's risk section.

## Approval Gate

1. Write the complete `specs/{feature_name}/spec.md` under `ACTIVE_PROJECT_ROOT`.
2. Complete the pre-approval recheck in Uncommitted Spec Boundary Check, then present the saved file link to the user and request explicit approval under approval-policy.md:
   `"请审阅规范文件 specs/<feature>/spec.md；是否批准其中的目标、范围、验收标准、架构决策与备选方案？"`
3. Await explicit approval before transitioning to `writing-plan`.

