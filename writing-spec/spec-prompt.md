# Spec Writing Prompt

Follow these guidelines when generating `spec.md`:

1. **Integrated Truth**: Do not divide the document into disconnected requirements and design silos. Connect observable behavior directly with the architectural decisions that support it.
2. **EARS Acceptance Criteria**: Write criteria in EARS format (Easy Approach to Requirements Syntax: Ubiquitous, Event-driven, State-driven, Unwanted-behavior, Optional). Ensure every criterion is testable.
3. **Mandatory Alternatives**: Every major architectural choice must explain at least one real competing alternative and why it lost. Never omit `## 曾考虑的备选方案`.
4. **Anchors**: Prefix every acceptance criterion with `<a id="spec-req-<num>-<num>"></a>`.
5. **Living Document**: Use present tense for current designs; keep the document concise, authoritative, and reviewable by both humans and agents.

