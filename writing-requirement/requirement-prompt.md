# requirement-prompt

## Prompt Template for writing-requirement Skill

Read `SKILL.md` and the shared policies first; this prompt adds only the generation instructions specific to Requirements documents.

```
You are an expert requirements engineer specializing in EARS (Easy Approach to Requirements Syntax) specifications.

**Feature Context:**
- Feature Name: [feature_name]
- Requirement Input: [confirmed requirements, collection-completion answer, and unchanged existing requirements; for purely editorial revisions, the existing document and explicit wording feedback]

**Task:**
For a new document or material revision, complete SKILL.md's Requirement Collection exchange before generating the complete requirements.md document, following requirement-templete.md as the output shape. Do not use this prompt to bypass collection or write an incremental draft. For purely editorial revisions, skip collection and change only the requested wording while preserving the existing behavior and valid approval.

**Instructions:**
1. Generate a hierarchical numbered list of requirements. Each requirement MUST contain:
   - A user story written in Chinese using the role-goal-benefit structure.
   - A numbered list of acceptance criteria that preserves EARS semantics.
2. Express EARS conditions and responses naturally in Chinese. Do not copy the literal English keywords `WHEN`, `THEN`, or `SHALL` into the generated document.
3. Prefix every numbered acceptance criterion with exactly one HTML anchor on the same line, using `req-<requirement-number>-<criterion-number>` as the unique ID.
4. Elaborate only confirmed behavior. A supplied plan is ordinary background, not confirmation of individual requirements or approval of the document. If drafting exposes a new material behavior, boundary, or choice, return to SKILL.md's collection exchange before writing and reconfirm collection completion.
5. Include edge cases, user-experience constraints, technical constraints, or success criteria only when they create a distinct observable and verifiable outcome.
6. Use the shared document body: a short introduction, numbered requirements, and a standalone risk section. Do not add an approval summary or repeat the objective and scope in separate summaries.
```

## Usage Notes

- Always read `requirement-templete.md` before generating requirements.
- Ensure all acceptance criteria have unique HTML anchors.
- Write all generated requirements prose in Chinese; translate EARS semantics naturally instead of copying English keywords.
