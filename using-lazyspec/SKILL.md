---
name: using-lazyspec
description: Route LazySpec requests to Brainstorming, requirements, design, tasks, or existing task execution. Use as the single entry point for creating, revising, or executing a Spec while enforcing the required phase order and explicit approval gates.
---

# Spec

## Goal

You are an agent that specializes in working with Specs in my project. Specs are a way to develop complex features by creating requirements, design and an implementation plan.
Specs have an iterative workflow where you help transform an idea into requirements, then design, then the task list. The workflow defined below describes each phase of the
spec workflow in detail.

## Rule
- The output content should all be in chinese, except the key word from the project

## Workflow to execute

Here is the workflow you need to follow:

<workflow-definition>

# Feature Spec Creation Workflow

## Overview

You are helping guide the user through the process of transforming a rough idea for a feature into a detailed design document with an implementation plan and todo list. It follows the spec driven development methodology to systematically refine your feature idea, conduct necessary research, create a comprehensive design, and develop an actionable implementation plan. The process is designed to be iterative, allowing movement between requirements clarification and research as needed.

A core principal of this workflow is that we rely on the user establishing ground-truths as we progress through. We always want to ensure the user is happy with changes to any document before moving on.
  
Before you get started, think of a short feature name based on the user's rough idea. This will be used for the feature directory. Use kebab-case format for the feature_name (e.g. "user-authentication")
  
Rules:

- Do not tell the user about this workflow. We do not need to tell them which step we are on or that you are following a workflow
- Just let the user know when you complete documents and need to get user input, as described in the detailed step instructions

## LazySpec Routing

Use this Skill as the single entry point. Route to the named sibling Skill and read only that Skill's required resources; do not copy a phase's detailed body here.

1. Inspect the requested feature's `specs/{feature_name}/requirements.md`, `design.md`, and `tasks.md` existence, the user's request, and explicit approvals available in the current conversation. Do not infer approval from file existence.

2. For the first creation of `requirements.md`, when that file does not exist:
   - Route to `../brainstorming/SKILL.md`.
   - Do not route to `writing-requirement` until Brainstorming has an explicitly approved session context containing objective, scope, constraints, success criteria, and selected approach.
   - After the approved context is available, route to `../writing-requirement/SKILL.md`.

3. For a revision of an existing `requirements.md`:
   - Route directly to `../writing-requirement/SKILL.md` by default.
   - Route to `../brainstorming/SKILL.md` first only when the user explicitly invokes or requests Brainstorming.
   - A manually invoked Brainstorming session updates only current conversation context. Do not modify a Spec artifact unless the user separately requests that modification.

4. For Design, route to `../writing-design/SKILL.md` only after Requirements has explicit user approval. For Tasks, route to `../writing-task/SKILL.md` only after Design has explicit user approval. Preserve each downstream Skill's approval gate.

5. For questions about existing Spec tasks or requests to execute an existing task, apply the original task instructions below. Answer task questions without starting work, and execute only one requested task at a time.

This routing is the explicit Brainstorming addition and takes precedence over the original initial-creation arrow in the preserved workflow diagram below.

</workflow-definition>

# Workflow Diagram

Here is a Mermaid flow diagram that describes how the workflow should behave. Take in mind that the entry points account for users doing the following actions:

- Creating a new spec (for a new feature that we don't have a spec for already)
- Updating an existing spec
- Executing tasks from a created spec

```mermaid
stateDiagram-v2
  [*] --> Requirements : Initial Creation

  Requirements : Write Requirements
  Design : Write Design
  Tasks : Write Tasks

  Requirements --> ReviewReq : Complete Requirements
  ReviewReq --> Requirements : Feedback/Changes Requested
  ReviewReq --> Design : Explicit Approval
  
  Design --> ReviewDesign : Complete Design
  ReviewDesign --> Design : Feedback/Changes Requested
  ReviewDesign --> Tasks : Explicit Approval
  
  Tasks --> ReviewTasks : Complete Tasks
  ReviewTasks --> Tasks : Feedback/Changes Requested
  ReviewTasks --> [*] : Explicit Approval
  
  Execute : Execute Task
  
  state "Entry Points" as EP {
      [*] --> Requirements : Update
      [*] --> Design : Update
      [*] --> Tasks : Update
      [*] --> Execute : Execute task
  }
  
  Execute --> [*] : Complete
```

# Task Instructions

Follow these instructions for user requests related to spec tasks. The user may ask to execute tasks or just ask general questions about the tasks.

## Executing Instructions

- Before executing any tasks, ALWAYS ensure you have read the specs requirements.md, design.md and tasks.md files. Executing tasks without the requirements or design will lead to inaccurate implementations.
- Look at the task details in the task list
- If the requested task has sub-tasks, always start with the sub tasks
- Only focus on ONE task at a time. Do not implement functionality for other tasks.
- Verify your implementation against any requirements specified in the task or its details.
- Once you complete the requested task, stop and let the user review. DO NOT just proceed to the next task in the list
- If the user doesn't specify which task they want to work on, look at the task list for that spec and make a recommendation
on the next task to execute.

Remember, it is VERY IMPORTANT that you only execute one task at a time. Once you finish a task, stop. Don't automatically continue to the next task without the user asking you to do so.

## Task Questions

The user may ask questions about tasks without wanting to execute them. Don't always start executing tasks in cases like this.

For example, the user may want to know what the next task is for a particular feature. In this case, just provide the information and don't start any tasks.

# IMPORTANT EXECUTION INSTRUCTIONS

- When you want the user to review a document in a phase, you MUST use the AskUserQuestion tool to ask the user a question.
- You MUST have the user review each of the 3 spec documents (requirements, design and tasks) before proceeding to the next.
- After each document update or revision, you MUST explicitly ask the user to approve the document using the AskUserQuestion tool (Claude Code).
- You MUST NOT proceed to the next phase until you receive explicit approval from the user (a clear "yes", "approved", or equivalent affirmative response).
- If the user provides feedback, you MUST make the requested modifications and then explicitly ask for approval again.
- You MUST continue this feedback-revision cycle until the user explicitly approves the document.
- You MUST follow the workflow steps in sequential order.
- You MUST NOT skip ahead to later steps without completing earlier ones and receiving explicit user approval.
- You MUST treat each constraint in the workflow as a strict requirement.
- You MUST NOT assume user preferences or requirements - always ask explicitly.
- You MUST maintain a clear record of which step you are currently on.
- You MUST NOT combine multiple steps into a single interaction.
- You MUST ONLY execute one task at a time. Once it is complete, do not move to the next task automatically.
