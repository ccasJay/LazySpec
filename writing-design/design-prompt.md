### 2. Create Feature Design Document

After Requirements approval for medium/high risk, or after the complete low-risk Requirements draft, create the minimum sufficient implementation-ready design. Refer to requirement IDs instead of restating them, record only decisions that affect implementation, and research only unresolved facts that materially change those decisions.

Immediately after the document title and before `Overview`, add a Human-First `审批摘要` with `方案`, a compact `关键决策` table (`决策`, `选择与理由`, `影响`), and `风险与待确认`. The summary is the user-facing approval contract; the detailed design is the Agent-facing elaboration and MUST remain consistent with and bounded by it.

Include every material choice involving public behavior or interfaces, data, dependencies, compatibility or migration, security or privacy, external or irreversible effects, failure and recovery behavior, or material risk. Omit internal file layout, helpers, test organization, and equivalent implementation refinements from the summary. Reuse each summary decision's exact short title in the corresponding `Key Design Decisions` subsection.

Adapt the summary to cognitive complexity rather than a fixed item or character count and aim for a complete one-screen review. If that is impossible without hiding a material decision, stop before approval and recommend splitting the Spec; expand only after the user explicitly keeps one Spec. Resolve material open decisions before approval, state known risks, and record that no material decision remains unresolved. Re-evaluate the risk level, reasons, and named critical operations in 风险与待确认 using risk-policy.md; escalation requires its missing phase approvals.

On a material revision, update the complete summary and present a concise conversation delta for additions, changes, removals, and risk changes. A verified non-material body-only refinement does not invalidate approval. A missing material decision or a summary/body conflict blocks approval.

Use the core and conditional sections defined by `design-templete.md` and the soft length target in `SKILL.md`. Testing Strategy identifies observable acceptance outcomes, integration/failure coverage, and risk-specific or human checks needed by downstream Feature Verification; do not substitute process checks for behavior.

Write all user-visible prose in the generated `design.md` in Chinese, including the overview, design decisions, research findings, testing strategy, and explanatory text under each section. Keep the required and selected conditional section names exactly as listed in `design-templete.md` in English as structural keywords. Preserve project-specific names, technical terms, code identifiers, filenames, URLs, Markdown syntax, and diagram syntax when necessary.

Apply the Diagram Policy in `SKILL.md`. Prefer compact ASCII diagrams for implementation-relevant topology, ownership, lifecycle, state transitions, and multi-participant sequences. Keep mandatory constraints, invariants, failure behavior, and compatibility guarantees in adjacent prose or contracts rather than encoding them only through diagram geometry.
