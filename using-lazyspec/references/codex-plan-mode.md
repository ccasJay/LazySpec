# Codex Plan Mode Adapter

Codex native Plan Mode serves only as a Brainstorming input source before creating a new feature; it is not a new LazySpec stage. The adapter relies only on mode markers explicitly provided by the Codex runtime; it does not guess environment variables, filenames, user wording, or other signals.

```ts
interface RuntimeMode {
  readonly platform: "codex" | "non-codex" | "unknown";
  readonly planMode: "active" | "inactive" | "unknown";
}

interface CodexPlanArtifact {
  readonly source: "codex-plan-mode";
  readonly content: string;
  readonly approved: true;
}

type BrainstormingInput =
  | BrainstormingContext
  | CodexPlanArtifact;
```

Establish a `CodexPlanArtifact` only when `RuntimeMode.platform` is `codex`, `RuntimeMode.planMode` is `active`, the plan's original text `content.trim()` is non-empty, and the user has explicitly approved that native plan. The adapter does not require fixed sections, fields, or an extra header; the `content` passed to Requirements must be the complete original text as approved. `CodexPlanArtifact` and the runtime markers remain in the current session only; do not serialize them or write them into project files.

On first creation when `requirements.md` does not exist, a valid Codex Plan Mode artifact routes directly to `writing-requirement`, with its `RouteDecision.stage` remaining `"requirements"`; do not invoke standard `brainstorming`. Do not invoke `writing-requirement` before the plan is approved. When the environment is known to be non-Codex, or Codex is not in Plan Mode, continue with standard `brainstorming`; when the platform or mode cannot be confirmed, do not automatically choose either branch — stop and require the user to explicitly switch to standard Brainstorming or supply a valid Codex Plan Mode plan.

The adapter must fail closed on invalid or incomplete input: when the plan is missing or empty, prompt to complete a non-empty plan and approve it explicitly; when a plan has been generated but not approved, state that user approval has not yet been obtained; when the platform or mode is unknown, state that the runtime status cannot be confirmed. In all these cases, remain in the current session: do not invoke `writing-requirement`, and do not create or update `requirements.md`. The only next steps are completing and approving the current plan, or the user explicitly switching to standard Brainstorming. When the plan's original text is modified, the user requests replanning, or the artifact's content changes, the old `CodexPlanArtifact` and its approval status become invalid immediately and must receive explicit approval again.

The Codex Plan Mode adapter maintains session-only input; it must not create `plan.md`, a Brainstorming document, or any other persistent intermediate artifact. Explicit replanning of an existing Spec likewise updates only the current session Context; when `requirements.md` already exists and the user has not explicitly requested replanning, continue directly into `writing-requirement` and do not automatically modify existing Spec files because of the adapter.
