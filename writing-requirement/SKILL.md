---
name: writing-requirement
description: Create or revise a LazySpec requirements.md after approved brainstorming context is available for a new feature, or when editing existing requirements. Use to produce EARS requirements, obtain explicit approval, and hand off only approved requirements to writing-design.
---

# Writing Requirements

## Language

- Keep the instructional prose in this Skill and its supporting resources in English.
- Write all user-visible prose in generated `requirements.md` content in Chinese, including the title, headings, introduction, user stories, and acceptance criteria.
- Preserve project-specific names, code identifiers, filenames, Markdown syntax, and HTML anchor IDs when necessary.

For a new feature, require a complete, explicitly approved `BrainstormingContext` from the current session before creating `requirements.md`. It must contain the confirmed objective, scope, constraints, success criteria, and selected approach. If it is missing, incomplete, unapproved, or lost, return to `brainstorming`; do not infer or restore it from disk.

For an existing `requirements.md`, use the existing document and explicit user feedback. Do not automatically rerun Brainstorming.

Before drafting or revising requirements, read `requirement-prompt.md` and `requirement-templete.md`. Resolve both files relative to the directory containing this `SKILL.md`, never relative to the process working directory or repository root. Resolve `specs/{feature_name}/requirements.md` against `ACTIVE_PROJECT_ROOT`, defined by `using-lazyspec` as the user's project working directory at session start. Never use this Skill's directory, its repository, or a Plugin cache as the project root. If invoked directly and the session working directory is unavailable or ambiguous, ask for the project root before writing. These rules apply unchanged in a Plugin cache and an Agent Skills installation.

Prefix every numbered acceptance criterion with exactly one HTML anchor on the same line, using `req-<requirement-number>-<criterion-number>` as the unique ID. The numbers MUST match the criterion's requirement and ordinal, every acceptance criterion MUST have an anchor, and each anchor ID MUST occur exactly once in `requirements.md`.

## Approval

After every Requirements update or revision, request approval using this protocol:

1. If `AskUserQuestion` is available, call it with exactly this supported input shape and no extra fields:

   ```json
   {
     "questions": [{
       "question": "Do the requirements look good? If so, we can move on to the design.",
       "header": "Review",
       "options": [
         {"label": "Approve", "description": "Approve Requirements and allow routing to Design."},
         {"label": "Request changes", "description": "Keep the current phase and revise Requirements from my feedback."}
       ],
       "multiSelect": false
     }]
   }
   ```

2. Otherwise, if the environment provides an equivalent user-question tool, use it with the same single-choice meaning and only fields that tool supports.
3. Otherwise, ask the same approval question directly in the conversation and stop while awaiting the answer.

Only explicit approval in the current conversation records Requirements approval. File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval. For any non-approval response, remain in Requirements; apply requested changes when provided and request approval again.

## Content Boundaries and Size

- Write only observable behavior, user-visible constraints, and verifiable outcomes. Do not include architecture, component boundaries, file changes, implementation steps, or speculative improvements.
- Consolidate overlapping behavior into one requirement instead of creating separate requirements for normal flow, edge cases, user experience, technical constraints, and success criteria when they describe the same outcome.
- Target at most 8 requirements, 2–5 acceptance criteria per requirement, and 30 acceptance criteria in total.
- Treat these targets as soft limits. Exceed them only when merging would lose distinct approved behavior; first consider narrowing or splitting the Spec, and explain any necessary exception in the conversation rather than the document.
- Keep the introduction to one short paragraph. Do not add summaries, glossaries, traceability tables, or repeated context unless the user explicitly needs them.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/requirements.md' file under the project folder if it doesn't already exist
- The model MUST generate an initial version of the requirements document based on the user's rough idea WITHOUT asking sequential questions first
- The model MUST express EARS semantics naturally in Chinese and MUST NOT copy the literal English EARS keywords `WHEN`, `THEN`, or `SHALL` into the generated document.
- The model MUST format the initial requirements.md document with:
- A clear introduction section that summarizes the feature
- A hierarchical numbered list of requirements where each contains:
  - A user story written in Chinese using the role-goal-benefit structure
  - A numbered list of acceptance criteria in EARS format (Easy Approach to Requirements Syntax)
- The model SHOULD include an edge case, user-experience constraint, technical constraint, or success criterion only when it creates a distinct observable and verifiable outcome
- The model MUST make modifications to the requirements document if the user requests changes or does not explicitly approve
- The model MUST ask for explicit approval after every iteration of edits to the requirements document
- The model MUST NOT proceed to the design document until receiving clear approval (such as "yes", "approved", "looks good", etc.)
- The model MUST continue the feedback-revision cycle until explicit approval is received
- The model SHOULD identify only gaps that would materially change observable behavior; it MUST NOT suggest speculative expansion by default
- The model MAY ask targeted questions about specific aspects of the requirements that need clarification
- The model MAY suggest options when the user is unsure about a particular aspect
- The model MUST proceed to the design phase after the user accepts the requirements

## Troubleshooting

### Requirements Clarification Stalls

If the requirements clarification process seems to be going in circles or not making progress:

- The model SHOULD suggest moving to a different aspect of the requirements
- The model MAY provide examples or options to help the user make decisions
- The model SHOULD summarize what has been established so far and identify specific gaps
- The model MAY suggest conducting research to inform requirements decisions
