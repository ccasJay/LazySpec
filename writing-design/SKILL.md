---
name: writing-design
description: Create or revise a LazySpec design.md only after requirements.md has explicit user approval. Use to research, draft, review, and obtain approval for a feature design; read the design prompt and template resources, and do not begin Tasks before design approval.
---

# Writing Design

Before starting, read the approved `specs/{feature_name}/requirements.md`, then read `design-prompt.md` and `design-templete.md`. If Requirements has not received explicit user approval, stop and request completion of that approval first.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/design.md' file if it doesn't already exist
- The model MUST create the minimum sufficient implementation-ready design at 'specs/{feature_name}/design.md'
- The document MUST include Overview, Key Design Decisions, and Testing Strategy
- Architecture, Components and Interfaces, Data Models, Error Handling, research findings, and diagrams are conditional sections; include only those that materially affect implementation and omit inapplicable sections entirely
- The model MUST identify unresolved external or project-specific facts that materially affect the design and research only those facts; skip research when the approved Requirements and repository already settle the design
- The model SHOULD NOT create separate research files; cite relevant sources in the conversation and incorporate only decision-relevant findings into the design
- The model MUST address all approved requirements by referencing their IDs or logical groups without restating their acceptance criteria
- The model SHOULD record a decision and rationale only when a meaningful implementation choice or trade-off exists
- The model SHOULD use Mermaid only when a relationship or sequence is materially clearer as a diagram than as short prose
- The model MUST NOT repeat requirements, repository facts, obvious framework behavior, or implementation detail that does not help a coding agent make a decision
- The model SHOULD target 100–180 lines for a typical design. A simple design may be shorter; never add content to reach the lower bound. This is a soft limit: consolidate repetition or recommend splitting an oversized Spec before exceeding it, but retain details needed to avoid implementation ambiguity
- The model MAY ask the user for input on specific technical decisions during the design process
- After updating the design document, the model MUST ask the user "Does the design look good? If so, we can move on to the implementation plan." using the AskUserQuestion tool (Claude Code).
- The AskUserQuestion tool MUST be used; set metadata.source to the exact string 'spec-design-review'
- The model MUST make modifications to the design document if the user requests changes or does not explicitly approve
- The model MUST ask for explicit approval after every iteration of edits to the design document
- The model MUST NOT proceed to the implementation plan until receiving clear approval (such as "yes", "approved", "looks good", etc.)
- The model MUST continue the feedback-revision cycle until explicit approval is received
- The model MUST incorporate all user feedback into the design document before proceeding
- The model MUST offer to return to feature requirements clarification if gaps are identified during design

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
