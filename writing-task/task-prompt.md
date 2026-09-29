### 3. Create Task List

From explicitly approved Requirements and Design with no unresolved blocking decision, create the shortest actionable checklist that implements them. Each task should identify a coding objective, only the essential affected components or files, and automated verification. Refer to Requirements and Design instead of repeating their content.

Read the shared risk-policy.md and delivery-loop.md through this Skill. Add Feature Verification (Planned Checks and Latest Result) after the task list; evidence recording is separate from plan approval.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/tasks.md' file if it doesn't already exist
- The model MUST return to the design step if the user indicates any changes are needed to the design
- The model MUST return to the requirement step if the user indicates that we need additional requirements
- The model MUST create an implementation plan at 'specs/{feature_name}/tasks.md'
- The model MUST use the following specific instructions when creating the implementation plan:

```
Convert the design into the fewest TODOs needed to cover the approved acceptance criteria. Each TODO delivers one complete, independently verifiable behavior, including implementation, entry-point integration, automated tests, and its success, validation, and failure paths even across files or components. Split only for independently deliverable behavior or separate behavior with distinct dependencies, risks, or observable outcomes; never split solely by file, architectural layer, or test type. Give each TODO scenario-based observable success criteria and an executable verification entry point, and leave the code integrated and usable with no orphaned work. Focus only on writing, modifying, or testing code.
```
