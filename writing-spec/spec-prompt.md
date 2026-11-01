# Spec Writing Prompt

Follow these guidelines when generating `spec.md`. It is LazySpec's only planning artifact: one approved file carries the contract, the task list, and the verification method.

1. **One artifact**: Never create `plan.md`, a verification file, or any other planning artifact. `spec.md` holds behavior, decisions, risks, tasks, and verification.
2. **User stories**: Give every story a stable `S<n>` ID and exactly one line: `作为…，我希望…，以便…`. Write the story once; the acceptance table references its ID instead of repeating the text.
3. **EARS acceptance criteria**: One table row per criterion. `类型` is the EARS category (普遍, 事件, 状态, 异常, 可选); `当` is the trigger or condition; `系统应` is the observable result. Keep exceptions and failure paths as separate rows; never merge them into a happy path. IDs are `R<story>.<n>` and stay stable across revisions.
4. **Inline verification**: The `验证` column is the approved check for that criterion (command, probe, or named end-to-end check). A shared command may cover several criteria; add one `组合：…` line only for composed flows. State the full test suite command once, on the relevant row or the combination line. Do not add a separate verification table or `Planned Checks` section.
5. **Decisions**: Record only choices that materially affect implementation: architecture, interfaces, data ownership, compatibility. One row per decision with a one-line reason. Fill `放弃` only when a rejected alternative matters to review or maintenance; otherwise write `无`.
6. **Risks**: Record the assessed level with its reason and the critical operations that need explicit authorization. Add invariants only when acceptance criteria do not already express them, and reference `R` IDs instead of repeating text.
7. **Tasks**: One line per task: `- [ ] //TODO <n>. <behavioral action> → R<id>；检查：<basic check>`. Each task is an independently deliverable behavior slice, not a file or layer. Do not copy the scenario or acceptance text; reference the `R` ID. Reserve full test suites and end-to-end execution for the final verification pass.
8. **Execution record**: Keep the four fixed lines (`状态`, `验证`, `结果`, `未决`). While executing, update only `执行记录`; the only permitted change inside the contract sections is the task checkbox `[ ]` → `[x]`. Do not record fingerprints, per-check timestamps, or raw logs.
9. **Single source**: Write each behavior, decision, risk, and check exactly once and refer to IDs elsewhere. Do not write background, motivation, value narration, implementation steps, file inventories, call-site maps, code, or test code.
10. **Shape and budget**: Keep `目标与范围` to two lines, at most 12 acceptance rows, 5 decisions, 3 risk rows, 12 tasks, and 5 execution-record lines. When a section exceeds its budget, merge duplicate criteria and delete narration first; if still over, split the feature into separate Specs. Never drop a distinct acceptance behavior to shorten the document.

Use [spec-template.md](spec-template.md) for frontmatter and section shape, and keep lifecycle metadata plus stable `S`/`R` IDs across revisions.
