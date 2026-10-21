# Plan Writing Prompt

Follow these guidelines when generating `plan.md`:

1. **Behavioral Focus**: Each TODO is an independently deliverable behavior slice. Do not partition tasks mechanically by files or layers (e.g. "create models", "create controllers"). Group the interface entry and core business logic for one observable behavior together.
2. **Two-tier verification (Basic per-TODO, Full at completion)**: Keep per-TODO verification lightweight—each TODO only needs a basic check (such as a smoke command probe, syntax/compile check, or a focused basic test) rather than full test suites or mandatory Red-Green TDD cycles. Reserve comprehensive automated tests and full test suite execution for `## Feature Verification` after all TODOs are completed.
3. **Concrete scenarios**: Follow delivery-loop.md's executable success criteria. The task's scenario/input and expected observation must be visible before choosing a command; a bare command or green exit code does not explain the required behavior.

Requirement coverage is defined by writing-plan/SKILL.md; syntax and output shape come from [plan-template.md](plan-template.md).

