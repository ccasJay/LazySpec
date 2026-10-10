---
name: writing-spec
description: Probe requirements and architectural decisions using /grill-me structured questions, then draft a unified spec.md containing EARS criteria, architecture decisions, and alternatives considered. Request explicit Spec approval before LazySpec enters planning.
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

## Structured Probing (/grill-me Style)

Instead of mechanical, one-by-one incremental confirmations, `writing-spec` conducts a structured decision interview:

1. **Inspect and Research**: Inspect the user's request, project architecture, and relevant existing codebase facts before asking.
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

The generated `specs/{feature_name}/spec.md` combines requirements and design into a single living truth:

1. **YAML Frontmatter**:
   ```yaml
   ---
   status: proposed
   created_at: YYYY-MM-DD
   supersedes: []
   superseded_by: null
   ---
   ```
2. **Body Structure**:
   - `# <Feature Name> Spec`
   - `## 目标与范围 (Goal & Scope)`: Concise user-visible goals, non-goals, and boundary definition.
   - `## 需求与验收标准 (Requirements & Acceptance Criteria)`: Numbered requirements with user stories and EARS criteria. Each criterion MUST have a unique HTML anchor `spec-req-<num>-<num>`.
   - `## 架构与核心决策 (Architecture & Key Decisions)`: Structural diagrams, data contracts, API boundaries, and runtime invariants.
   - `## 曾考虑的备选方案 (Alternatives Considered)`: MANDATORY section detailing alternative designs evaluated and the exact reasons they were rejected (Why not X?).
   - `## 风险与否定性保证 (Risks & Invariants)`: Known risks, failure containment, and invariants that must never be violated.

## Approval Gate

1. Write the complete `specs/{feature_name}/spec.md` under `ACTIVE_PROJECT_ROOT`.
2. Present the saved file link to the user and request explicit approval under approval-policy.md:
   `"请审阅规范文件 specs/<feature>/spec.md；是否批准其中的目标、范围、验收标准、架构决策与备选方案？"`
3. Await explicit approval before transitioning to `writing-plan`.
