# requirement-templete

## Requirements Template

```markdown
# [功能名称] 需求

## 引言

[用一段简短中文说明目标、包含的范围和必要的排除项]

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

## 风险与待确认

- 风险等级：[low / medium / high]；理由：[影响与可逆性]
- 关键操作：[需要执行前确认的具体操作，若无则写“无”]
- 风险：[已知风险，若无则写“无”]
- 待确认：无
```

## Usage Guidelines

- Replace [placeholder] with actual content.
- Use one shared body for review and execution; do not add an approval summary.
- Use HTML anchors for traceability: <a id="req-1-1"></a>
- Focus on observable and verifiable behavior.
- Write all generated document prose in Chinese; preserve project-specific terms and identifiers when necessary.
