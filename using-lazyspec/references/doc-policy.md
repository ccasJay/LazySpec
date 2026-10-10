# Minimum-Sufficient Documentation

- Default to the shortest document that remains reviewable, verifiable, and executable.
- In v2 binary architecture, put information in exactly two artifacts: `spec.md` defines observable behavior (EARS requirements) and implementation decisions (architecture, key decisions, alternatives considered, invariants); `plan.md` identifies executable coding action items (behavioral TODOs), verification gates, and feature verification.
- Users and Agents share one document body; do not add a separate approval summary. Refer to requirement IDs instead of restating upstream content. Record each decision, rationale, constraint, or procedure once.
- Expand a section only when omitting it would create a material implementation ambiguity or the user explicitly requests more detail. An explicit request expands only the relevant section; it does not enable a separate verbose mode.
- Treat phase length targets as soft limits. Before exceeding one, remove repetition, merge closely related items, or recommend splitting an oversized Spec. Never truncate distinct approved behavior merely to meet a target.

