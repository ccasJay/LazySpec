# requirement-templete

## Requirements Template

```markdown
# [功能名称] 需求

## 审批摘要

### 目标

[用一至两句说明用户最终获得的结果]

### 范围

- 包含：[本次交付的边界]
- 不包含：[明确排除的内容]

### 核心行为

- [用户需要理解和批准的行为；可无歧义地归组多条详细验收标准]

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
```

## Usage Guidelines

- Replace [placeholder] with actual content
- Treat `审批摘要` as the user-facing approval contract and keep the detailed body consistent with and bounded by it
- Adapt the summary to cognitive complexity and aim for a complete one-screen review; recommend splitting the Spec when that is impossible without hiding material information
- Keep HTML anchors and traceability syntax out of `审批摘要`
- Use HTML anchors for traceability: <a id="req-1-1"></a>
- Focus on observable and verifiable behavior
- Keep total acceptance criteria under 30
- Write all generated document prose in Chinese; preserve project-specific terms and identifiers when necessary
- Express EARS semantics naturally in Chinese without copying `WHEN`, `THEN`, or `SHALL`
