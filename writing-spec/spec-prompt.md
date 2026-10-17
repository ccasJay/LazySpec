# Spec Writing Prompt

Follow these guidelines when generating `spec.md`:

1. **Integrated Truth**: Do not divide the document into disconnected requirements and design silos. Connect observable behavior directly with the architectural decisions that support it.
2. **EARS Acceptance Criteria**: Write criteria in EARS format (Easy Approach to Requirements Syntax: Ubiquitous, Event-driven, State-driven, Unwanted-behavior, Optional). Ensure every criterion is testable.
3. **Mandatory Alternatives**: Every major architectural choice must explain at least one real competing alternative and why it lost.
4. **Anchors**: Prefix every acceptance criterion with `<a id="spec-req-<num>-<num>"></a>`.
5. **Living Document**: Use present tense for current designs; keep the document concise, authoritative, and reviewable by both humans and agents.
6. **Metadata**: Use the frontmatter in [spec-template.md](spec-template.md) for a new Spec. `delivered_at` is added during delivery; lifecycle meanings and transitions are defined by the shared delivery rules and their owning Skills. Keep stable Markdown/HTML anchors across revisions.

