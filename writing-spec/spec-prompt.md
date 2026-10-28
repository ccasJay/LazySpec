# Spec Writing Prompt

Follow these guidelines when generating `spec.md`:

1. **Integrated Truth**: Do not divide the document into disconnected requirements and design silos. Connect observable behavior directly with the architectural decisions that support it.
2. **EARS Acceptance Criteria**: Write criteria in EARS format (Easy Approach to Requirements Syntax: Ubiquitous, Event-driven, State-driven, Unwanted-behavior, Optional). Ensure every criterion is testable.
3. **Decisions and alternatives**: Record only decisions and boundaries that materially affect implementation. Include a real rejected alternative and its reason only when the trade-off matters to review or future maintenance; omit it otherwise.
4. **Anchors**: Prefix every acceptance criterion with `<a id="spec-req-<num>-<num>"></a>`.
5. **Minimum sufficient**: Record each behavior, constraint, decision, and risk once. Refer to acceptance IDs instead of repeating their text in architecture or risk sections. Default to omitting file inventories, exhaustive call-site maps, implementation code, and test commands unless their absence creates material ambiguity or the user requires them. Preserve material compatibility exceptions, distinct semantics, and cross-Spec ownership and dependencies. Use present tense and do not impose a fixed length limit.
6. **Metadata**: Use the frontmatter in [spec-template.md](spec-template.md) for a new Spec. `delivered_at` is added during delivery; lifecycle meanings and transitions are defined by the shared delivery rules and their owning Skills. Keep stable Markdown/HTML anchors across revisions.

