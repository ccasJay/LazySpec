# Minimum-Sufficient Documentation

- Default to the shortest document that remains reviewable, verifiable, and executable.
- In v2 binary architecture, put information in exactly two artifacts: `spec.md` defines observable behavior (EARS requirements) and implementation decisions (architecture, key decisions, alternatives considered, invariants); `plan.md` identifies executable coding action items (behavioral TODOs), verification gates, and feature verification.
- Users and Agents share one document body; do not add a separate approval summary. Refer to requirement IDs instead of restating upstream content. Record each decision, rationale, constraint, or procedure once.
- Expand a section only when omitting it would create a material implementation ambiguity or the user explicitly requests more detail. An explicit request expands only the relevant section; it does not enable a separate verbose mode.
- Do not impose fixed length limits. Remove repetition and merge closely related items first; propose splitting only when independently reviewable scope warrants it. Never omit distinct approved behavior to shorten a document.
- Keep implementation inventories, exhaustive call-site maps, code, and detailed test commands out of Spec by default; include them only when material to the contract or explicitly requested. Plan references the Spec rather than copying it, while retaining concrete executable scenarios and complete verification coverage.

