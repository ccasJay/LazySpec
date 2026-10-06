---
name: executing-task
description: Execute, resume, or verify approved normal LazySpec tasks.md plans with per-TODO context discovery and a temporary local progress record. Not for fast plan.md execution.
---

# Executing Tasks

## Scope and shared rules

- Report to the user in Chinese, retaining project keywords and code identifiers as needed.
- Handle ordinary three-document Specs only. Route `plan.md` work to `fast`; task-status questions are read-only and must not start checks or change files. A verification-only request may run checks and update Feature Verification, but does not authorize implementation repairs.
- Read [risk-policy.md](../using-lazyspec/references/risk-policy.md), [approval-policy.md](../using-lazyspec/references/approval-policy.md), and [delivery-loop.md](../using-lazyspec/references/delivery-loop.md). Reuse resources already loaded by `using-lazyspec`. The shared delivery loop owns Feature Verification evidence, failure routing, and Learning Candidates; this Skill owns normal-mode execution and the temporary progress record.
- Bind `ACTIVE_PROJECT_ROOT` to the user's project working directory at the start of the agent session. Resolve `specs/{feature_name}/...` against that root, never against this Skill's installation directory. If invoked directly, perform [memory-recall.md](../using-lazyspec/references/memory-recall.md) before execution; reuse `RelevantMemoryContext` when the router already supplied it. Memory is advisory and never overrides current Spec or code evidence.

## Entry and context discovery

1. Confirm the requested `tasks.md` and TODO number, when specified. Require explicit approval of the current Requirements, Design, and Tasks under approval-policy.md; file existence, checkboxes, and an execution request do not approve unseen changes. Reconcile risk at the highest applicable level. Do not create a progress file or change code before the execution scope is authorized.
2. Read complete Requirements, Design's `Overview`, `Key Design Decisions`, and `风险与待确认`, and the complete `tasks.md` checklist and Planned Checks. This establishes the feature boundary and all requested TODOs without requiring every Design technical section up front. For legacy documents, locate the equivalent material content wherever it is recorded without rewriting them or giving a summary separate authority. If the requested contract remains uncertain or sections conflict, read the affected complete artifact and resolve the contract before acting.
3. For each TODO, follow every linked acceptance criterion to `requirements.md`; find the Design decisions and sections governing those criteria; then inspect the relevant source, callers, tests, and project instructions. Use code search and targeted reads rather than a fixed repository tour. Before editing, state to yourself the TODO's objective, affected behavior, expected result, verification entry point, and dependencies. Expand to other Spec sections or code when the change crosses tasks, a link is missing, or the current context cannot establish the contract. Never infer a missing requirement or lower an approved success criterion.
4. Track which acceptance outcomes and Design sections have been checked. Before claiming Feature Verification `passed`, inspect any still-uncovered contract sections and ensure the complete current feature contract and composed flows are covered. Reuse unchanged context and attributable evidence; reread only changed or uncertain material.

## Normal execution

- An explicit request to execute `tasks.md` covers all currently unchecked TODOs, including nested TODOs, without per-TODO confirmation. A request naming one TODO number covers only that TODO and its children. Start with subtasks where present. If the file or number is unresolved, ask for the exact target before modifying files. An already checked plan on an execution request still needs missing or stale Feature Verification.
- Before the first file modification, including creation of `.execution-progress.md`, create a feature branch named `codex/<feature-name>` unless the user requested another name. Reuse a branch already belonging to this work; choose a unique `codex/` name if the default belongs to unrelated work, and report it. Do not commit unrelated pre-existing changes. An approved `specs/orchestration.md` supplies the cross-Spec branch and sequencing constraints instead; it never overrides this Spec's task contract.
- Treat listed order as the default. Reorder or group independent TODOs only when dependencies, approved outcomes, and user scope remain intact; briefly record the reason without renumbering or rewriting completed TODOs. Parallel work requires host/user permission and clear ownership. If permitted, one coordinator writes the Spec's progress file.
- For each TODO, implement within its authorized scope, run a focused check against its stated scenario and relevant regressions, and repair implementation failures using delivery-loop.md. Only after the TODO passes, change its checkbox token from `[ ]` to `[x]`; preserve `//TODO` and every character after it. Group related verified TODOs into coherent, reviewable commits unless the user or project set a different policy; no per-TODO commit is mandatory. Keep unrelated working-tree changes out of commits.
- Continue through the requested scope without intentional pauses. Stop and report the exact blocker for a working-tree or merge conflict, commit failure, missing authority or user decision, user interruption, or delivery-loop.md's no-progress boundary. A selected subset does not authorize repairs to unrelated TODOs.
- After all feature TODOs are checked, run Feature Verification under delivery-loop.md. A partial execution reports only its authorized subset unless it completes the feature. Report TODO completion separately from feature status, freshness, evidence, and remaining work. When the requested TODO scope is complete, inspect only `project-memory/index.md` for Capsules whose feature, tags, summary, Source Spec, or authorities overlap changed paths; report likely impact candidates without creating, editing, or changing Memory status absent a separate request.

## Temporary execution progress

Use one local, Git-ignored Markdown file at `specs/{feature_name}/.execution-progress.md` for an authorized execution run. Never stage or commit it. It is a recovery hint, not an approval object, a checkbox authority, or durable verification evidence. Do not copy complete Spec text, raw command logs, or secrets into it. Create it after branch selection and before TODO work or Feature Verification, including execution requests where every TODO is already checked; a verification-only request with no existing file does not create one.

Keep the record compact with these fields:

| Section | Contents |
|---|---|
| Run | Spec path, requested scope, branch, HEAD, current Requirements/Design/Tasks content fingerprints, update time |
| Current TODO | Number, state (`pending`, `in-progress`, `verified`, or `blocked`), linked requirement IDs, relevant Design sections, code/test paths |
| Recovery | Focused check and attributable evidence reference, blocker or unresolved decision, next concrete action |
| Feature | TODO completion and Feature Verification status/freshness, referring to the durable result in `tasks.md` |

- Update the record when a TODO starts, its context changes materially, verification completes, a commit changes HEAD, execution blocks, or a run resumes. Record concise references rather than duplicating evidence. Update fingerprints after Spec/checkbox changes. The file's absence or corruption must not block reconstruction from the approved Spec, code, Git state, and tests.
- On resume, compare the recorded scope, branch, HEAD, fingerprints, TODO states, and evidence with current `tasks.md`, code, and Feature Verification. If the branch differs, locate the authorized work and return to its branch when safe; stop on a conflict or missing branch decision. If the contract changed, apply approval-policy.md's materiality rules and invalidate affected evidence; obtain approval for a material revision before executing it. Reconstruct or correct stale entries before continuing; never mark a TODO complete, reuse verification, or claim approval solely from this file. A status-only request does not update it.
- Keep the file across partial completion, failure, `blocked`, `pending-human`, interruption, or a material contract revision awaiting approval. A verification-only run may update an existing file. Delete only this file when every feature TODO is checked and Feature Verification is attributable to the current code/contract with status `passed` and freshness `current`; if a completed run left the file behind, reconcile and remove it. Do not delete `tasks.md`, approval records, or verification evidence.
