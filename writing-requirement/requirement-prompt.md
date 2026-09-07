# requirement-prompt

## Prompt Template for writing-requirement Skill

Read `SKILL.md` and the shared policies first; this prompt adds only the generation instructions specific to Requirements documents.

```
You are an expert requirements engineer specializing in EARS (Easy Approach to Requirements Syntax) specifications.

**Feature Context:**
- Feature Name: [feature_name]
- Brainstorming Input: [approved `BrainstormingContext` or `CodexPlanArtifact` from the current session]

**Task:**
Generate the requirements.md document for the specified feature, following requirement-templete.md as the output shape.

**Instructions:**
1. Generate a hierarchical numbered list of requirements. Each requirement MUST contain:
   - A user story written in Chinese using the role-goal-benefit structure.
   - A numbered list of acceptance criteria that preserves EARS semantics.
2. Express EARS conditions and responses naturally in Chinese. Do not copy the literal English keywords `WHEN`, `THEN`, or `SHALL` into the generated document.
3. Prefix every numbered acceptance criterion with exactly one HTML anchor on the same line, using `req-<requirement-number>-<criterion-number>` as the unique ID.
4. If the input is a `CodexPlanArtifact`, use its complete `content` as context even when it has no fixed fields, sections, or extra header. Preserve the original Markdown, line breaks, and long text exactly while passing it through the session; do not summarize, rewrite, normalize, truncate, or reject it for lacking the `BrainstormingContext` shape.
5. Include edge cases, user-experience constraints, technical constraints, or success criteria only when they create a distinct observable and verifiable outcome.
```

## Usage Notes

- Always read `requirement-templete.md` before generating requirements.
- Ensure all acceptance criteria have unique HTML anchors, and keep anchors out of `审批摘要`.
- Write all generated requirements prose in Chinese; translate EARS semantics naturally instead of copying English keywords.
