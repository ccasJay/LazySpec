---
name: writing-design
description: Create or revise a LazySpec design.md from Requirements with risk-based approval gates. Low risk drafts toward combined approval; medium/high require approved Requirements before Design.
---

# Writing Design

## Shared risk policy

Read [risk-policy.md](../using-lazyspec/references/risk-policy.md) before this workflow; resolve it relative to this Skill directory. It determines low-risk combined approval versus medium/high phase gates, and fast critical-operation confirmation.

## Language

- Keep the instructional prose in this Skill and its supporting resources in English.
- Write all user-visible prose in generated `design.md` content in Chinese, including the overview, design decisions, research findings, testing strategy, and explanatory text under each section.
- Keep `Overview`, `Key Design Decisions`, `Testing Strategy`, and any selected conditional section names in English as structural keywords.
- Preserve project-specific names, technical terms, code identifiers, filenames, URLs, Markdown syntax, and diagram syntax when necessary.

Before starting, read the complete `specs/{feature_name}/requirements.md`, then read `design-prompt.md` and `design-templete.md`. Resolve the Prompt and Template relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve the upstream Spec and the new `design.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before reading or writing Specs. These rules apply unchanged in a Plugin cache and an Agent Skills installation. For medium/high risk, if Requirements has not received explicit user approval in the current conversation, stop and request that approval first; never infer approval from file existence. For low risk, use the current Requirements draft without marking it approved. Re-evaluate risk before drafting; escalation follows risk-policy.md.

## Human-First Review Summary

- Put `## 审批摘要` immediately after the document title and before `## Overview`, with the Chinese subsections `方案`, `关键决策`, and `风险与待确认`.
- Treat this summary as the user-facing approval contract. The detailed design may elaborate Agent-facing implementation mechanics, but MUST remain consistent with and bounded by the approved summary.
- Include every material choice involving public behavior or interfaces, data, dependencies, compatibility or migration, security or privacy, external or irreversible effects, failure and recovery behavior, or material risk. Keep internal file layout, helpers, test organization, and equivalent implementation refinements out of the summary.
- Render `关键决策` as a compact table with the columns `决策`, `选择与理由`, and `影响`. Reuse each summary decision's exact short title in its corresponding `Key Design Decisions` subsection so the relationship is unambiguous without adding traceability noise.
- Adapt summary length to cognitive complexity rather than a fixed numerical budget. Aim for a complete one-screen review. If that is impossible without concealing a material decision, stop before approval and recommend splitting the Spec; expand only after the user explicitly keeps one Spec.
- Resolve every material open decision before requesting approval. Use `风险与待确认` to state known risks and explicitly record that no material decision remains unresolved.
- Before approval, verify that the body contains no material decision missing from or conflicting with the summary. Any material revision invalidates prior approval; a verified non-material body-only refinement does not.
- On a material revision, replace the summary with the complete current version and present a concise additions/changes/removals/risk delta in the conversation.
- For a legacy Design document without `审批摘要`, add the summary only when that document is next revised. Creating Design from an approved legacy Requirements document does not require rewriting Requirements.

## Approval

For low risk, finish the unapproved Design draft and continue to Tasks for combined approval. For medium/high risk, after creating Design or making a material revision, request approval using this protocol:

1. If `AskUserQuestion` is available, call it with exactly this supported input shape and no extra fields:

   ```json
   {
     "questions": [{
       "question": "审批摘要是否准确覆盖了设计方案、关键决策及风险？",
       "header": "Review",
       "options": [
         {"label": "Approve", "description": "批准当前摘要表达的实质设计，并允许进入 Tasks。"},
         {"label": "Request changes", "description": "留在 Design，根据反馈更新摘要与正文。"}
       ],
       "multiSelect": false
     }]
   }
   ```

2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields that tool supports.
3. Otherwise, ask the same approval question directly in the conversation and stop while awaiting the answer.

Only explicit approval in the current conversation records approval of the current `审批摘要` and its consistency with the detailed Design body. It does not mean the user approved every non-material implementation detail. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval. For any non-approval response, remain in Design; apply requested changes when provided and request approval again. Any material change invalidates prior approval; a verified non-material body-only refinement does not.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/design.md' file if it doesn't already exist
- The model MUST create the minimum sufficient implementation-ready design at 'specs/{feature_name}/design.md'
- The document MUST put the Human-First `审批摘要` before `Overview` and keep the detailed design consistent with and bounded by that summary
- The document MUST include the English structural sections `Overview`, `Key Design Decisions`, and `Testing Strategy`; all prose within them MUST be Chinese
- `Architecture`, `Components and Interfaces`, `Data Models`, `Error Handling`, `Research Findings`, and diagrams are conditional sections; keep any selected section name in English, include it only when it materially affects implementation, and omit inapplicable sections entirely
- The model MUST identify unresolved external or project-specific facts that materially affect the design and research only those facts; skip research when the approved Requirements and repository already settle the design
- The model SHOULD NOT create separate research files; cite relevant sources in the conversation and incorporate only decision-relevant findings into the design
- Address all current Requirements (approved for medium/high, draft for low) by referencing their IDs or logical groups without restating their acceptance criteria
- The model SHOULD record a decision and rationale only when a meaningful implementation choice or trade-off exists
- The model SHOULD choose the smallest representation that makes the design unambiguous: ASCII diagrams for topology, ownership, lifecycle, state transitions, and multi-participant sequences; tables for repeated mappings; TypeScript for data contracts; and prose for rationale, invariants, failure semantics, and compatibility guarantees
- The model MUST NOT repeat requirements, repository facts, obvious framework behavior, or implementation detail that does not help a coding agent make a decision
- Excluding the Human-First `审批摘要`, the model SHOULD target 100–180 lines for a typical detailed design body. A simple design may be shorter; never add content to reach the lower bound. This is a soft limit: consolidate repetition or recommend splitting an oversized Spec before exceeding it, but retain details needed to avoid implementation ambiguity
- The model MAY ask the user for input on specific technical decisions during the design process
- Modify the design summary and body when the user requests changes; silence or an explanation neither approves nor automatically requires edits
- Apply risk-policy.md after material edits: low-risk package approval or medium/high Design approval; verified non-material body-only refinements preserve approval
- For medium/high risk, the model MUST NOT proceed to the implementation plan until receiving clear approval; low risk may advance an unapproved draft under risk-policy.md
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
