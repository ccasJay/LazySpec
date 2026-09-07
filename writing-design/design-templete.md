The section names below are structural keywords and MUST remain in English. All generated prose under these sections MUST be written in Chinese. Preserve project-specific names, technical terms, code identifiers, filenames, URLs, Markdown syntax, and Mermaid syntax when necessary.

Every generated Design document MUST begin with the Human-First approval contract shown below, immediately after the document title and before the English structural sections:

```markdown
## 审批摘要

### 方案

[用一至两句说明总体实现方向]

### 关键决策

| 决策 | 选择与理由 | 影响 |
|---|---|---|
| [与详细决策章节相同的短标题] | [所选方案及原因] | [用户、系统、兼容性或风险影响] |

### 风险与待确认

- 风险等级：[low / medium / high]；理由：[影响与可逆性]
- 关键操作：[需要执行前确认的具体操作，若无则写“无”]
- 风险：[已知风险，若无则写“无”]
- 待确认：无
```

The design document MUST include these core sections:

- Overview
- Key Design Decisions
- Testing Strategy

Add any of these sections only when they contain implementation-relevant information:

- Architecture
- Components and Interfaces
- Data Models
- Error Handling
- Research Findings

Omit an inapplicable section entirely. Do not add empty sections or placeholders such as "None" or "Not applicable".
