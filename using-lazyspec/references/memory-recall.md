# Memory Recall

Session-only recall protocol for every ordinary LazySpec request. After binding `ACTIVE_PROJECT_ROOT` and before selecting the phase Skill, build a session-only `RelevantMemoryContext`. For metadata validation, load project-memory/README.md when present, otherwise [memory-format.md](../../distill-spec-memory/references/memory-format.md); use the index alone for candidate discovery, not a Capsule directory scan. An explicit Memory distillation request routes directly to `distill-spec-memory`; it does not receive an unrelated default recall context.

1. Check only `ACTIVE_PROJECT_ROOT/project-memory/index.md`. If it does not exist, use an empty context and continue the original route. Do not create an index or scan `project-memory/features/` as a fallback.
2. Parse the generated six-column index header and Markdown-linked rows. If the marker, header, columns, path, or status is malformed, report a non-fatal Chinese maintenance warning, use an empty context (or retain only independently valid rows), and continue the original route. Never guess a path, synthesize a missing row, or rewrite the index during recall.
3. For default recall, consider only rows whose index status is `active`. Resolve each Memory link against `ACTIVE_PROJECT_ROOT`; reject absolute paths, `..` traversal, paths outside the allowed roots `project-memory/features/` and `project-memory/learnings/`, missing Capsules, invalid frontmatter or kind/path mismatch (legacy kind defaults to feature), symlinks escaping the project, missing `reviewed_at` or `authorities`, or Capsule/index mismatches. Report each rejected row and do not scan other files to compensate.
4. Rank valid candidates by query matches in `feature` (or Learning `learning` ID), `tags`, `Summary`, and `Source Spec`, in that order of signal strength; break ties by the project-root-relative Memory path. Read the complete Capsule only after ranking, and select at most three across both kinds combined. Check Learning applicability and limits before using it; omit inapplicable guidance without treating a candidate in tasks.md/plan.md as Memory. If more than three match, report the selected paths and that the remaining matches were omitted.
5. Expose the result only as this session's context; never write it into a Spec or project file:

```ts
interface RelevantMemoryContext {
  readonly query: string;
  readonly memories: readonly {
    readonly path: string;
    readonly kind: "feature" | "learning"; // legacy Capsules default to feature
    readonly status: "active";
    readonly sourceSpec: string;
    readonly reviewedAt: string;
    readonly authorities: readonly string[];
    readonly relevantSections: readonly string[];
  }[]; // 0–3 items
}
```

6. If there is no related valid `active` row, use an empty context and continue. If the user explicitly asks to trace history or review Memory status, select up to three matching `needs-review`, `superseded`, or `obsolete` rows separately, preserve their actual status, and attach a Chinese warning that they are not current facts. Never place a non-`active` item in `memories` or present it without the warning.
7. Pass `RelevantMemoryContext` as advisory input to the selected phase. If the request changes or disputes a listed authority, read that current authority and its relevant source/tests before relying on the Capsule. Memory may inform questions, requirements, design, tasks, or implementation, but it must not override current implementation evidence, approve a phase, reorder Brainstorming → Requirements → Design → Tasks, bypass a task gate, or expand the user's explicit task scope. A missing index, no hit, omitted-over-three result, or maintenance warning is never a phase error.
