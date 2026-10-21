---
name: writing-plan
description: Create or revise a LazySpec plan.md with behavioral TODOs, basic per-TODO checks, and final full-suite Feature Verification checks after spec.md approval. Request explicit Plan approval before LazySpec enters implementation.
---

# Writing Plan

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), [doc-policy.md](../using-lazyspec/references/doc-policy.md), and [delivery-loop.md](../using-lazyspec/references/delivery-loop.md) before this workflow; resolve them relative to the directory containing this `SKILL.md`. risk-policy.md separates risk-based verification from decision-based approval; approval-policy.md is the single source of explicit approval; doc-policy.md maintains the binary spec architecture; delivery-loop.md defines executable success criteria, basic per-TODO verification, and final full-suite Feature Verification.

## Language and paths

- Output all user-facing text and generated `plan.md` content in Chinese, preserving project code keywords, command names, and Markdown/HTML anchors.
- Resolve supporting resources (`plan-prompt.md`, `plan-template.md`) relative to the directory containing this `SKILL.md`.
- Resolve upstream `specs/{feature_name}/spec.md` and the target `specs/{feature_name}/plan.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root.
- Require explicit approval of `spec.md` before creating `plan.md`. Never infer approval from file existence.

## Plan Structure and Engineering Discipline

1. **Behavioral Slices (Superpowers Inspired)**:
   - Read [plan-prompt.md](plan-prompt.md) for behavioral slicing and two-tier verification (basic per-TODO checks, full test suite at completion), and [plan-template.md](plan-template.md) for TODO syntax and document shape.
   - Apply delivery-loop.md's executable success criteria to every task; do not duplicate the shared verification contract.
2. **Requirement Linkage**:
   - Link each acceptance criterion implemented by the TODO to `spec.md`:
     `[<req-num>.<crit-num>](./spec.md#spec-req-<req-num>-<crit-num>)`.
   - Every acceptance criterion in `spec.md` MUST be covered by at least one task.
3. **Feature Verification Appendix**:
   - Populate the template's Feature Verification appendix under delivery-loop.md; use the normal-mode requirement anchors above.

## Approval Gate

1. Finish writing `specs/{feature_name}/plan.md`.
2. Present the saved file link to the user and request explicit approval under approval-policy.md:
   `"请审阅执行计划 specs/<feature>/plan.md；是否批准其中的任务拆解与验收范围？"`
3. Await explicit approval before handoff to `executing-plan`.

