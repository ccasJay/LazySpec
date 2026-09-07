---
name: writing-design
description: Create or revise a LazySpec design.md from complete Requirements. Choose implementation details autonomously within the success contract and surface material decisions for review.
---

# Writing Design

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [doc-policy.md](../using-lazyspec/references/doc-policy.md) before this workflow; resolve them relative to this Skill directory. risk-policy.md separates risk-based verification from decision-based approval and defines model autonomy within the user's scope; approval-policy.md is the single source of explicit-approval, materiality, invalidation, summary-contract, and approval-asking semantics; doc-policy.md keeps the document minimum-sufficient.

## Language

- Keep the instructional prose in this Skill and its supporting resources in English.
- Write all user-visible prose in generated `design.md` content in Chinese, including the overview, design decisions, research findings, testing strategy, and explanatory text under each section.
- Keep `Overview`, `Key Design Decisions`, `Testing Strategy`, and any selected conditional section names in English as structural keywords.
- Preserve project-specific names, technical terms, code identifiers, filenames, URLs, Markdown syntax, and diagram syntax when necessary.

Before starting, read the complete `specs/{feature_name}/requirements.md`, then read `design-prompt.md` and `design-templete.md`. Resolve the Prompt and Template relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve the upstream Spec and the new `design.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before reading or writing Specs. These rules apply unchanged in a Plugin cache and an Agent Skills installation. Use the current Requirements draft without marking it approved. Stop only for unresolved material choices or explicit user phase gates. Re-evaluate risk before drafting under risk-policy.md.

## Human-First Review Summary

- Put `## 审批摘要` immediately after the document title and before `## Overview`, with the Chinese subsections `方案`, `关键决策`, and `风险与待确认`.
- Treat this summary as the user-facing approval contract under approval-policy.md. The detailed design may elaborate Agent-facing implementation mechanics, but MUST remain consistent with and bounded by the approved summary.
- Include every material choice involving public behavior or interfaces, data, dependencies, compatibility or migration, security or privacy, external or irreversible effects, failure and recovery behavior, or material risk. Keep internal file layout, helpers, test organization, and equivalent implementation refinements out of the summary.
- Render `关键决策` as a compact table with the columns `决策`, `选择与理由`, and `影响`. Reuse each summary decision's exact short title in its corresponding `Key Design Decisions` subsection so the relationship is unambiguous without adding traceability noise.
- Adapt summary length to cognitive complexity rather than a fixed numerical budget, following approval-policy.md's one-screen and splitting rules.
- Resolve every material open decision before requesting approval. Use `风险与待确认` to state known risks and explicitly record that no material decision remains unresolved.
- Before approval, verify that the body contains no material decision missing from or conflicting with the summary; a missing material decision or a summary/body conflict blocks approval under approval-policy.md.
- For a legacy Design document without `审批摘要`, add the summary only when that document is next revised. Creating Design from an approved legacy Requirements document does not require rewriting Requirements.

## Approval

Finish the Design draft and continue toward combined review unless an unresolved material decision or explicit user phase gate requires approval here. Internal implementation details remain the model's choice within the contract. When approval is needed, follow approval-policy.md's asking protocol and ask: "审批摘要是否准确覆盖了设计方案、关键决策及风险？" For any non-approval response, remain in Design; apply approval-policy.md's explicit-approval, revision-delta, and invalidation semantics.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/design.md' file if it doesn't already exist
- The model MUST create the minimum sufficient implementation-ready design at 'specs/{feature_name}/design.md'
- The document MUST put the Human-First `审批摘要` before `Overview` and keep the detailed design consistent with and bounded by that summary
- The document MUST include the English structural sections `Overview`, `Key Design Decisions`, and `Testing Strategy`; all prose within them MUST be Chinese
- `Architecture`, `Components and Interfaces`, `Data Models`, `Error Handling`, `Research Findings`, and diagrams are conditional sections; keep any selected section name in English, include it only when it materially affects implementation, and omit inapplicable sections entirely
- The model MUST identify unresolved external or project-specific facts that materially affect the design and research only those facts; skip research when the approved Requirements and repository already settle the design
- The model SHOULD NOT create separate research files; cite relevant sources in the conversation and incorporate only decision-relevant findings into the design
- Address all current Requirements (approved or explicitly identified as drafts) by referencing their IDs or logical groups without restating their acceptance criteria
- The model SHOULD record a decision and rationale only when a meaningful implementation choice or trade-off exists
- The model SHOULD choose the smallest representation that makes the design unambiguous: ASCII diagrams for topology, ownership, lifecycle, state transitions, and multi-participant sequences; tables for repeated mappings; TypeScript for data contracts; and prose for rationale, invariants, failure semantics, and compatibility guarantees
- The model MUST NOT repeat requirements, repository facts, obvious framework behavior, or implementation detail that does not help a coding agent make a decision
- Excluding the Human-First `审批摘要`, the model SHOULD target 100–180 lines for a typical detailed design body. A simple design may be shorter; never add content to reach the lower bound. This is a soft limit: consolidate repetition or recommend splitting an oversized Spec before exceeding it, but retain details needed to avoid implementation ambiguity
- The model MAY ask the user for input on specific technical decisions during the design process
- Modify the design summary and body when the user requests changes; silence or an explanation neither approves nor automatically requires edits
- Apply risk-policy.md after material edits; verified non-material refinements preserve approval
- Continue drafting Tasks when no unresolved material decision or user-requested phase gate blocks it; never mark an unapproved draft approved
- The model MUST continue the feedback-revision cycle until explicit approval is received
- The model MUST incorporate all user feedback into the design document before proceeding
- The model MUST offer to return to feature requirements clarification if gaps are identified during design

### Diagram Policy

- Prefer an ASCII diagram when relationships or flows involving at least three meaningful nodes are materially clearer visually than as short prose
- Put ASCII diagrams in fenced `text` blocks, use printable ASCII characters, and keep one primary reading direction per diagram
- Give each diagram one purpose, use exact component, interface, event, and state names, and label edges whose meaning is not obvious
- Split a diagram when crossing edges, excessive width, or mixed abstraction levels make its interpretation ambiguous
- Do not encode mandatory constraints, invariants, failure behavior, compatibility guarantees, or requirement acceptance criteria only in a diagram; state the minimum non-geometric contract immediately beside it
- Do not duplicate relationships already clear from the diagram in narrative prose
- Use Mermaid only when the user explicitly requests it or when a materially important relationship remains ambiguous after splitting the ASCII diagram

### Research Limitations

If the model cannot access needed information:

- The model SHOULD report material missing information in the conversation rather than adding a placeholder section to the design
- The model SHOULD suggest alternative approaches based on available information
- The model MAY ask the user to provide additional context or documentation
- The model SHOULD continue with available information rather than blocking progress

### Design Complexity

If the design becomes too complex or unwieldy:

- The model SHOULD first remove upstream restatement and consolidate related decisions
- The model SHOULD suggest breaking it down into smaller, more manageable components
- The model SHOULD focus on core functionality first
- The model MAY suggest a phased approach to implementation
- The model SHOULD return to requirements clarification to prioritize features if needed
