---
name: writing-design
description: Create or revise a LazySpec design.md only after requirements.md has explicit user approval. Use to research, draft, review, and obtain approval for a feature design; read the design prompt and template resources, and do not begin Tasks before design approval.
---

# Writing Design

Before starting, read the approved `specs/{feature_name}/requirements.md`, then read `design-prompt.md` and `design-templete.md`. Resolve the Prompt and Template relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve the upstream Spec and the new `design.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before reading or writing Specs. These rules apply unchanged in a Plugin cache and an Agent Skills installation. If Requirements has not received explicit user approval in the current conversation, stop and request completion of that approval first; never infer approval from the file's existence.

## Approval

After every Design update or revision, request approval using this protocol:

1. If `AskUserQuestion` is available, call it with exactly this supported input shape and no extra fields:

   ```json
   {
     "questions": [{
       "question": "Does the design look good? If so, we can move on to the implementation plan.",
       "header": "Review",
       "options": [
         {"label": "Approve", "description": "Approve Design and allow routing to Tasks."},
         {"label": "Request changes", "description": "Keep the current phase and revise Design from my feedback."}
       ],
       "multiSelect": false
     }]
   }
   ```

2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields that tool supports.
3. Otherwise, ask the same approval question directly in the conversation and stop while awaiting the answer.

Only explicit approval in the current conversation records Design approval. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval. For any non-approval response, remain in Design; apply requested changes when provided and request approval again.

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
