# Minimum-Sufficient Documentation

- Default to the shortest document that remains reviewable, verifiable, and executable.
- Put information in exactly one phase: Requirements define observable behavior, Design records implementation decisions, and Tasks identify coding actions and automated verification.
- Other than the bounded Human-First `审批摘要` projection defined in [approval-policy.md](approval-policy.md), refer to upstream requirement IDs instead of restating upstream content. Do not repeat the same rationale, constraint, or procedure in multiple detailed sections.
- Expand a section only when omitting it would create a material implementation ambiguity or the user explicitly requests more detail. An explicit request expands only the relevant section; it does not enable a separate verbose mode.
- Treat phase length targets as soft limits. Before exceeding one, remove repetition, merge closely related items, or recommend splitting an oversized Spec. Never truncate distinct approved behavior merely to meet a target.
