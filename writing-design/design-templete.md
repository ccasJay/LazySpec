The English section names below are structural keywords and MUST remain in English; keep the risk heading `风险与待确认` in Chinese. All generated prose MUST be written in Chinese. Preserve project-specific names, technical terms, code identifiers, filenames, URLs, Markdown syntax, and Mermaid syntax when necessary.

Use one shared body for review and execution; do not add an approval summary. The design document MUST include these core sections in this order:

```markdown
# [功能名称] 设计

## Overview

[用一段简短中文说明实现方向，通过需求编号引用相关行为]

## Key Design Decisions

[每项影响实现的关键选择及其理由和影响，只记录一次；按需使用简短段落或表格]

## 风险与待确认

- 风险等级：[low / medium / high]；理由：[影响与可逆性]
- 关键操作：[需要执行前确认的具体操作，若无则写“无”]
- 风险：[已知风险，若无则写“无”]
- 待确认：无

## Testing Strategy

[通过需求编号说明验证方法、必要的集成和失败路径，以及风险专项或人工检查；具体检查清单与运行证据由 Tasks 记录]
```

Add any of these sections only when they contain implementation-relevant information:

- Architecture
- Components and Interfaces
- Data Models
- Error Handling
- Research Findings

Place conditional technical sections after the risk section and before Testing Strategy. Omit an inapplicable section entirely. Do not add empty sections or placeholders such as "None" or "Not applicable". Refer to Key Design Decisions rather than repeating choices and rationale in technical sections.
