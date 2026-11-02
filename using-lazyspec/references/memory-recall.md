# Memory Recall

Session-only recall protocol for every ordinary LazySpec request. After binding `ACTIVE_PROJECT_ROOT` and before selecting the routed Skill, build a session-only `RelevantMemoryContext`. An explicit Memory distillation request routes to `distill-feature`; it does not receive an unrelated default recall context.

1. Run the router recall command: `lazyspec.py recall --query "<request text>" --json`. Use its `memories` array as this session's context. If Python 3 or the script is unavailable, perform steps 2-4 manually and report the degradation.
2. The command implements the recall invariants. Check only `ACTIVE_PROJECT_ROOT/project-memory/index.md`; never create an index or scan `project-memory/features/` as a fallback. It validates the generated six-column index header and Markdown-linked rows, and rejects absolute paths, `..` traversal, targets outside `project-memory/features/`, escaping symlinks, missing Capsules, invalid frontmatter, feature/path mismatch, missing `reviewed_at` or `authorities`, and Capsule/index mismatch. A malformed index produces a non-fatal Chinese maintenance warning and an empty context, not a guess or a rewrite.
3. For default recall, consider only rows whose index status is `active`. Rank valid candidates by query matches in `feature`, `tags`, `Summary`, and `Source Spec`, in that order of signal strength; break ties by the project-root-relative Memory path. Read the complete Capsule only after ranking, and select at most three Feature Capsules. If more than three match, report the selected paths and that the remaining matches were omitted.
4. Expose the result only as this session's context; never write it into a Spec or project file:

```ts
interface RelevantMemoryContext {
  readonly query: string;
  readonly memories: readonly {
    readonly path: string;
    readonly status: "active";
    readonly sourceSpec: string;
    readonly reviewedAt: string;
    readonly authorities: readonly string[];
    readonly relevantSections: readonly string[];
  }[]; // 0–3 items
}
```

5. If there is no related valid `active` row, use an empty context and continue. If the user explicitly asks to trace history or review Memory status, rerun with `--include-non-active`, select up to three matching `needs-review`, `superseded`, or `obsolete` rows separately, preserve their actual status, and attach a Chinese warning that they are not current facts. Never place a non-`active` item in `memories` or present it without the warning.
6. Pass `RelevantMemoryContext` as advisory input to the selected phase. If the request changes or disputes a listed authority, read that current authority and its relevant source/tests before relying on the Capsule. Memory may inform questions, requirements, design, tasks, or implementation, but it must not override current implementation evidence, confirm a requirement on the user's behalf, approve a Spec, bypass a task gate, or expand the user's explicit task scope. A missing index, no hit, omitted-over-three result, or maintenance warning is never a phase error.
