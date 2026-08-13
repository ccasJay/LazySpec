# requirement-templete

## Requirements Template

```markdown
# Requirements Document

## Introduction

[One short paragraph describing the objective and scope]

## Requirements

### Requirement 1: [Observable outcome]

**User Story:** As a [role], I want [feature], so that [benefit]

#### Acceptance Criteria

1. <a id="req-1-1"></a> WHEN [event] THEN [system] SHALL [response]
2. <a id="req-1-2"></a> IF [precondition] THEN [system] SHALL [response]

### Requirement 2: [Distinct observable outcome]

**User Story:** As a [role], I want [feature], so that [benefit]

#### Acceptance Criteria

1. <a id="req-2-1"></a> WHEN [event] THEN [system] SHALL [response]
2. <a id="req-2-2"></a> WHEN [event] AND [condition] THEN [system] SHALL [response]
```

## Usage Guidelines

- Replace [placeholder] with actual content
- Use HTML anchors for traceability: <a id="req-1-1"></a>
- Focus on observable and verifiable behavior
- Keep total acceptance criteria under 30