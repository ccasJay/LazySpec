# Minimum-Sufficient Documentation

- Default to the shortest document that remains reviewable, verifiable, and executable.
- LazySpec has exactly one planning artifact per feature: `spec.md`. It carries observable behavior, material decisions, risks, the approved task list, and each criterion's verification method. Do not create `plan.md` or a separate verification file.
- Users and Agents share one document body; do not add a separate approval summary. Refer to `S`/`R` IDs instead of restating upstream content. Record each decision, rationale, constraint, or procedure once.
- Use the canonical section shapes: one-line goals, one-line user stories, and tables for acceptance criteria, decisions, and risks. Prose is for a decision's reason, not for background, motivation, or value narration.
- Budget: `目标与范围` two lines, at most 12 acceptance rows, 5 decisions, 3 risk rows, 12 tasks, and 5 execution-record lines. When a section exceeds its budget, merge duplicate criteria and delete narration first; split the feature into separate Specs only when independently reviewable scope warrants it. Never omit distinct approved behavior to shorten a document.
- Keep implementation inventories, exhaustive call-site maps, code, and test code out of `spec.md` by default; include them only when material to the contract or explicitly requested.
