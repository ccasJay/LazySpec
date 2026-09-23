### 2. Create Feature Design Document

From explicitly approved Requirements with no unresolved blocking decision, create the minimum sufficient implementation-ready design. Refer to requirement IDs instead of restating them, record only decisions that affect implementation, and research only unresolved facts that change those decisions.

Use the core and conditional sections defined by `design-templete.md` and the soft length target in `SKILL.md`. Testing Strategy identifies observable acceptance outcomes, integration/failure coverage, and risk-specific or human checks needed by downstream Feature Verification; do not substitute process checks for behavior.

Write all user-visible prose in the generated `design.md` in Chinese, including the overview, design decisions, research findings, testing strategy, and explanatory text under each section. Keep the required and selected conditional section names exactly as listed in `design-templete.md` in English as structural keywords. Preserve project-specific names, technical terms, code identifiers, filenames, URLs, Markdown syntax, and diagram syntax when necessary.

Apply the Diagram Policy in `SKILL.md`. Prefer compact ASCII diagrams for implementation-relevant topology, ownership, lifecycle, state transitions, and multi-participant sequences. Keep mandatory constraints, invariants, failure behavior, and compatibility guarantees in adjacent prose or contracts rather than encoding them only through diagram geometry.
