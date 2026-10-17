# Plan Writing Prompt

Follow these guidelines when generating `plan.md`:

1. **Behavioral Focus**: Each TODO is an independently deliverable behavior slice. Do not partition tasks mechanically by files or layers (e.g. "create models", "create controllers"). Group the interface entry, business logic, and applicable automated tests for one observable behavior together.
2. **Test-first discipline**: Identify a failing assertion or concrete command probe (Red) before the production change (Green). Existing focused checks can suffice; new tests are not mandatory for every task.
3. **Concrete scenarios**: Follow delivery-loop.md's executable success criteria. The task's scenario/input and expected observation must be visible before choosing a command; a bare command or green exit code does not explain the required behavior.

Requirement coverage is defined by writing-plan/SKILL.md; syntax and output shape come from [plan-template.md](plan-template.md).

