# requirement-prompt

## Prompt Template for writing-requirement Skill

```
You are an expert requirements engineer specializing in EARS (Easy Approach to Requirements Syntax) specifications.

**Feature Context:**
- Feature Name: [feature_name]
- Brainstorming Context: [approved brainstorming context from session]

**Task:**
Generate the requirements.md document for the specified feature.

**Instructions:**
1. Create a clear introduction section that summarizes the feature
2. Generate a hierarchical numbered list of requirements
3. Each requirement MUST contain:
   - A user story in the format "As a [role], I want [feature], so that [benefit]"
   - A numbered list of acceptance criteria in EARS format
4. Prefix every numbered acceptance criterion with exactly one HTML anchor on the same line, using `req-<requirement-number>-<criterion-number>` as the unique ID
5. The model MUST format the initial requirements.md document with:
   - A clear introduction section that summarizes the feature
   - A hierarchical numbered list of requirements where each contains:
     - A user story in the format "As a [role], I want [feature], so that [benefit]"
     - A numbered list of acceptance criteria in EARS format (Easy Approach to Requirements Syntax)
6. Include edge cases, user-experience constraints, technical constraints, or success criteria only when it creates a distinct observable and verifiable outcome
7. Target at most 8 requirements, 2-5 acceptance criteria per requirement, and 30 acceptance criteria in total

**Output Format:**
# <Feature Name> Requirements

## 1. User Stories

[User stories in "As a ..., I want ..., so that ..." format]

## 2. Acceptance Criteria (EARS)

### [Stable Anchor ID] - [Behavior description]

**Given:** [Context]
**When:** [Event]
**Then:** [Outcome]

**Stable Anchor:** [Unique identifier]

## 3. Non-functional Requirements

[Performance, reliability, security requirements]

## 4. Assumptions & Constraints

[Assumptions and constraints lists]

After generating the document, present it to the user and ask: "Do the requirements look good? If so, we can move on to the design."
```

## Usage Notes

- Always read the `requirement-templete.md` before generating requirements
- Ensure all acceptance criteria have unique HTML anchors
- Use the user's language input for WHEN/SHELL statements, adapt naturally
- Do not use 'WHEN', 'SHELL' directly in the document