# Plan Writing Prompt

Follow these guidelines when generating `plan.md`:

1. **Behavioral Focus**: Do not partition tasks mechanically by files or layers (e.g. "create models", "create controllers"). Group all related changes and automated tests for one observable behavior into a single cohesive TODO.
2. **Explicit Verification Entry Points**: Every task must clearly specify how to verify it (a specific test command, automated test entry point, or deterministic command probe).
3. **Full Spec Coverage**: Every acceptance criterion defined in `spec.md` must be referenced by at least one task using relative anchor links.
4. **Preserve Checkbox Syntax**: Strict format `- [ ] //TODO <num>. <title>`.

