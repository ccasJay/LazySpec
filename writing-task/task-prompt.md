### 3. Create Task List

After the user approves Design, create the shortest actionable checklist that implements it. Each task should identify a coding objective, only the essential affected components or files, and automated verification. Refer to Requirements and Design instead of repeating their content.

**Constraints:**

- The model MUST create a 'specs/{feature_name}/tasks.md' file if it doesn't already exist
- The model MUST return to the design step if the user indicates any changes are needed to the design
- The model MUST return to the requirement step if the user indicates that we need additional requirements
- The model MUST create an implementation plan at 'specs/{feature_name}/tasks.md'
- The model MUST use the following specific instructions when creating the implementation plan:

```
Convert the design into incremental coding tasks with early automated verification. Each task must leave the code integrated and usable, with no orphaned work. Focus only on writing, modifying, or testing code.
```
