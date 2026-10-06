---
name: writing-design
description: Create or revise a LazySpec design.md from complete Requirements. Collect Design-stage user decisions, choose routine implementation details within the success contract, and surface material decisions for review.
---

# Writing Design

## Shared policies

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [doc-policy.md](../using-lazyspec/references/doc-policy.md) before this workflow; resolve them relative to this Skill directory. risk-policy.md separates risk-based verification from decision-based approval and defines model autonomy within the user's scope; approval-policy.md is the single source of explicit-approval, materiality, invalidation, complete-file review, and approval-asking semantics; doc-policy.md keeps the document minimum-sufficient.

## Language

- Keep the instructional prose in this Skill and its supporting resources in English.
- Write all user-visible prose in generated `design.md` content in Chinese, including the overview, design decisions, research findings, testing strategy, and explanatory text under each section.
- Keep `Overview`, `Key Design Decisions`, `Testing Strategy`, and any selected conditional section names in English as structural keywords.
- Preserve project-specific names, technical terms, code identifiers, filenames, URLs, Markdown syntax, and diagram syntax when necessary.

Before starting, read the complete `specs/{feature_name}/requirements.md`, then read `design-prompt.md` and `design-templete.md`. Resolve the Prompt and Template relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve the upstream Spec and the new `design.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before reading or writing Specs. These rules apply unchanged in a Plugin cache and an Agent Skills installation. Require explicit approval of the current Requirements before collecting Design decisions or creating `design.md`; do not infer approval from file existence. Re-evaluate risk before drafting under risk-policy.md.

## Design Decision Collection

Before creating a new Design, inspect Requirements and relevant project code, then hold a separate Design-stage user-question exchange. Do not treat requirement collection or Requirements approval as a choice of architecture, interfaces, data model, dependencies, compatibility strategy, security controls, or recovery behavior.

- Before asking, examine the approved Requirements, relevant code, and explicit prior decisions for unresolved choices about architecture, public interfaces, data, dependencies, compatibility, external effects, security, and recovery. Research discoverable project facts. Distinguish material or user-reserved choices from routine internal techniques the model can choose; prioritize the choices whose alternatives materially change the design or its risks. Keep this decision check in the conversation, not a new artifact.
- For each choice requiring the user's decision, explain what it affects, recommend a viable option with a concise reason, and compare the main consequences or trade-offs in user-facing terms. Ask one focused question at a time using the current environment's applicable user-question tool under approval-policy.md, and wait for the answer. Do not ask for a choice already made explicitly.
- After each answer, check whether the current choice is resolved and whether it exposes another material or user-reserved choice. Clarify an ambiguous answer before moving on; an answer of “none” to additional preferences does not close an unresolved material choice. Do not draft affected Design sections while such a choice remains open. For a new Design with no competing choice, ask at least one design-focused question inviting additional design constraints or preferences, allow an explicit answer of none, and wait before drafting.
- Record the user's explicit design decisions and constraints for the Design draft. Do not infer a design choice from Requirements approval. If a proposed design choice changes observable behavior or scope, return to Requirements for that decision before fixing it in Design.
- Resolve choices reserved for the user before drafting their affected sections. Choose routine internal techniques autonomously; do not manufacture alternatives or repeat an already explicit decision. Design decision collection is distinct from approval of the completed Design document.

## Document Contract

- Use one body for user review and Agent execution, following approval-policy.md's complete-file contract. Do not add an approval summary.
- Record each key choice, rationale, and impact once in `Key Design Decisions`, including material choices about public behavior or interfaces, data, dependencies, compatibility or migration, security or privacy, external or irreversible effects, failure and recovery behavior, and risk. Reference those decisions from technical sections instead of repeating them.
- Put the risk assessment in a standalone `## 风险与待确认` after `Key Design Decisions`. Resolve open design decisions before requesting approval, state known risks, and explicitly record that no design decision remains unresolved.
- Read a legacy Design document as it stands; do not migrate it solely to adopt this format. Creating Design from approved legacy Requirements does not require rewriting Requirements.

## Approval

Finish and check the saved Design file, then link to it and request explicit Design approval before creating any Tasks document. Let the user review the complete file; do not paste it into the conversation. Internal implementation details remain the model's choice within the contract. Follow approval-policy.md's file-backed review and asking protocols and ask: "请审阅设计文件；是否批准其中的方案、关键决策、风险与测试策略？" For any non-approval response, remain in Design; apply approval-policy.md's explicit-approval, revision-delta, and invalidation semantics.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/design.md' file if it doesn't already exist
- The model MUST create the minimum sufficient implementation-ready design at 'specs/{feature_name}/design.md'
- The document MUST include `Overview`, `Key Design Decisions`, the standalone Chinese `风险与待确认`, and `Testing Strategy` in that order; all prose within them MUST be Chinese
- `Architecture`, `Components and Interfaces`, `Data Models`, `Error Handling`, `Research Findings`, and diagrams are conditional sections; keep any selected section name in English, include it only when it materially affects implementation, and omit inapplicable sections entirely
- The model MUST identify unresolved external or project-specific facts that materially affect the design and research only those facts; skip research when the approved Requirements and repository already settle the design
- The model SHOULD NOT create separate research files; cite relevant sources in the conversation and incorporate only decision-relevant findings into the design
- Address all current Requirements (approved or explicitly identified as drafts) by referencing their IDs or logical groups without restating their acceptance criteria
- The model SHOULD record a decision and rationale only when a meaningful implementation choice or trade-off exists
- The model SHOULD choose the smallest representation that makes the design unambiguous: ASCII diagrams for topology, ownership, lifecycle, state transitions, and multi-participant sequences; tables for repeated mappings; TypeScript for data contracts; and prose for rationale, invariants, failure semantics, and compatibility guarantees
- The model MUST NOT repeat requirements, repository facts, obvious framework behavior, or implementation detail that does not help a coding agent make a decision
- The model SHOULD keep the complete design document within 180 lines where practical, with no minimum length. This is a soft upper limit: remove repetition or recommend splitting an oversized Spec before exceeding it, but retain details needed to avoid implementation ambiguity; never pad a simple design
- The model MUST collect Design-stage input as specified in Design Decision Collection before creating a new Design; ask again on revision only when a new material or user-reserved design choice arises
- Modify the design document when the user requests changes; silence or an explanation neither approves nor automatically requires edits
- Apply risk-policy.md after material edits; verified non-material refinements preserve approval
- Do not create or draft Tasks until the current Design has explicit approval; never mark an unapproved draft approved
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
