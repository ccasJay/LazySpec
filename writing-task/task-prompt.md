### 3. Create Task List

After Design approval for medium/high risk, or after the complete low-risk Design draft, create the shortest actionable checklist that implements it. Each task should identify a coding objective, only the essential affected components or files, and automated verification. Refer to Requirements and Design instead of repeating their content.

Read the shared risk-policy.md and delivery-loop.md through this Skill. Add Feature Verification (Planned Checks and Latest Result) after the task list; evidence recording is separate from plan approval.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/tasks.md' file if it doesn't already exist
- The model MUST return to the design step if the user indicates any changes are needed to the design
- The model MUST return to the requirement step if the user indicates that we need additional requirements
- The model MUST create an implementation plan at 'specs/{feature_name}/tasks.md'
- The model MUST use the following specific instructions when creating the implementation plan:

```
Convert the design into incremental coding tasks with scenario-based observable success criteria and executable verification entry points. Each task must leave the code integrated and usable, with no orphaned work. Focus only on writing, modifying, or testing code.
```
