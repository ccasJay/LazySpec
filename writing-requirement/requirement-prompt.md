# requirement-prompt

## Prompt Template for writing-requirement Skill

```
You are an expert requirements engineer specializing in EARS (Easy Approach to Requirements Syntax) specifications.

**Feature Context:**
- Feature Name: [feature_name]
- Brainstorming Input: [approved `BrainstormingContext` or `CodexPlanArtifact` from the current session]

**Task:**
Generate the requirements.md document for the specified feature.

**Instructions:**
1. Write all user-visible prose in the generated document in Chinese, including the title, headings, introduction, user stories, and acceptance criteria.
2. Preserve project-specific names, code identifiers, filenames, Markdown syntax, and HTML anchor IDs when necessary.
3. Immediately after the title, create a Human-First `审批摘要` with `目标`, `范围`, `核心行为`, and `风险与待确认`, then create the introduction and detailed requirements. Use the introduction only for concise context that is not already clear from the summary.
4. Treat `审批摘要` as the user-facing approval contract. The detailed body may elaborate it for the Agent but MUST NOT add, omit, broaden, narrow, or contradict material behavior, scope, exclusions, compatibility, external side effects, security or privacy, failure behavior, or risks.
5. Cover every materially distinct acceptance outcome directly or through one unambiguous summary group. Keep HTML anchors and traceability syntax out of the summary.
6. Adapt the summary to cognitive complexity instead of a fixed item or character count and aim for a complete one-screen review. If that is impossible without hiding material information, stop before approval and recommend splitting the Spec; expand only after the user explicitly keeps one Spec.
7. Resolve material open questions before approval. Record known risks and confirm that no material decision remains unresolved in `风险与待确认`.
8. Generate a hierarchical numbered list of requirements. Each requirement MUST contain:
   - A user story written in Chinese using the role-goal-benefit structure.
   - A numbered list of acceptance criteria that preserves EARS semantics.
9. Prefix every numbered acceptance criterion with exactly one HTML anchor on the same line, using `req-<requirement-number>-<criterion-number>` as the unique ID.
10. Express EARS conditions and responses naturally in Chinese. Do not copy the literal English keywords `WHEN`, `THEN`, or `SHALL` into the generated document.
11. Include edge cases, user-experience constraints, technical constraints, or success criteria only when they create a distinct observable and verifiable outcome.
12. Target at most 8 requirements, 2-5 acceptance criteria per requirement, and 30 acceptance criteria in total.
13. If the input is a `CodexPlanArtifact`, use its complete `content` as context even when it has no fixed fields, sections, or extra header. Preserve the original Markdown, line breaks, and long text exactly while passing it through the session; do not summarize, rewrite, normalize, truncate, or reject it for lacking the `BrainstormingContext` shape.
14. Convert the approved plan into observable requirements. The approval of the Codex plan does not approve `requirements.md`; request the Requirements approval separately for medium/high risk, or as part of the separate combined Spec approval for low risk under risk-policy.md. If material information is missing, ask a targeted clarification question and remain in Requirements.
15. On a material revision, update the complete summary and present a concise conversation delta for additions, changes, removals, and risk changes. A verified non-material body-only refinement does not invalidate approval.

**Output Format:**
# [功能名称] 需求

## 审批摘要

### 目标

[用一至两句说明用户最终获得的结果]

### 范围

- 包含：[本次交付的边界]
- 不包含：[明确排除的内容]

### 核心行为

- [用户需要理解和批准的行为]

### 风险与待确认

- 风险等级：[low / medium / high]；理由：[影响与可逆性]
- 关键操作：[需要执行前确认的具体操作，若无则写“无”]
- 风险：[已知风险，若无则写“无”]
- 待确认：无

## 引言

[用一段简短中文说明目标和范围]

## 需求

### 需求 1：[可观察结果]

**用户故事：** 作为[角色]，我希望[功能]，以便[收益]

#### 验收标准

1. <a id="req-1-1"></a> 当[事件]发生时，系统必须[响应]
2. <a id="req-1-2"></a> 如果[前置条件]成立，系统必须[响应]

### 需求 2：[不同的可观察结果]

**用户故事：** 作为[角色]，我希望[功能]，以便[收益]

#### 验收标准

1. <a id="req-2-1"></a> 当[事件]发生时，系统必须[响应]
2. <a id="req-2-2"></a> 当[事件]发生且[条件]满足时，系统必须[响应]

After generating the document, present the complete `审批摘要` and ask: "审批摘要是否准确覆盖了需求的目标、范围、核心行为与风险？"
```

## Usage Notes

- Always read the `requirement-templete.md` before generating requirements
- Ensure all acceptance criteria have unique HTML anchors
- Keep anchors out of `审批摘要`; use them only in the detailed acceptance criteria
- Write all generated requirements prose in Chinese; translate EARS semantics naturally instead of copying English keywords.
- Do not use the literal English keywords `WHEN`, `THEN`, or `SHALL` in the generated document.
