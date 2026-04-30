---
name: general-project-handoff
description: This skill should be used whenever the user wants to create, update, refine, audit, or package a handoff document for continuing any complex project in a new AI conversation, another AI assistant, another agent/tool, or a future work session.
version: 1.0.0
---

# General Project Handoff Skill

## Purpose

Create or update a high-quality handoff document that lets a complex project continue in a new AI conversation, another AI assistant, another agent/tool, or a future work session without losing critical context.

The handoff is not just a summary. It is a **continuity artifact** for the next reasoning agent.

It should preserve:

- the project goal;
- the user's intent and quality bar;
- the current state;
- completed work;
- decisions and rationale;
- rejected or downgraded paths;
- known traps and mistakes to avoid;
- open questions and blockers;
- relevant files, paths, artifacts, or outputs;
- next action and stop conditions;
- a pasteable prompt for the next AI/session/tool when useful.

Prefer Markdown unless the user explicitly asks for a human-facing DOCX/PDF/report.

---

## When to Apply

Apply this skill when the user says or implies:

- "I need to open a new ChatGPT/Claude/Gemini window."
- "Write a handoff document."
- "Create a context file."
- "Summarize everything so another AI can continue."
- "Prepare onboarding for a new assistant."
- "Make a document I can upload to a new AI chat."
- "The conversation is too long; I need to restart."
- "Document our decisions and next steps."
- "Create/update HANDOFF.md."
- "Transfer context to another agent/tool/model."
- "Make a reusable project memory / continuity file."

Also apply when a long project is near context limits or contains many unresolved decisions.

---

## Core Output Rule

Write the handoff primarily for the **next AI assistant**, not only for a human reader.

Use direct second-person instructions where useful:

```text
You are taking over...
You must remember...
Do not...
When the user provides a new update, first check...
If the user asks X, respond with...
```

A strong handoff should let the next AI continue without asking the user to repeat basic context.

---

## Recommended File Format

Default to Markdown.

Use these file names unless the user requests otherwise:

```text
HANDOFF.md
PROJECT_HANDOFF.md
project-handoff.md
<context-name>_handoff.md
```

If creating a skill package, use:

```text
skill-folder/
└── SKILL.md
```

If the user wants a Claude-style skill, the file should be named exactly:

```text
SKILL.md
```

with YAML frontmatter including at least `name` and `description`.

---

## Workflow

### 1. Determine the Handoff Target

Before writing, infer who or what will consume the handoff.

Possible targets:

- a new ChatGPT/Claude/Gemini conversation;
- a coding agent;
- an external execution tool;
- a human collaborator;
- the same user later;
- a mixed audience of AI + human reviewers.

Adjust the style accordingly.

For a new AI conversation, use second-person prompt style.

For a human teammate, use more report-like style.

For both, use a hybrid: clear headings plus explicit "New AI instructions."

---

### 2. Check for Existing Handoff or Project Memory

If the working context includes an existing handoff, project memory, README, task tracker, or prior summary, use it.

If editing a project repository, first look for files such as:

```text
HANDOFF.md
PROJECT_HANDOFF.md
README.md
CLAUDE.md
AGENTS.md
CONTEXT.md
docs/handoff/*
docs/summaries/*
.context/*
.memory/*
```

If an existing handoff exists:

1. read it;
2. preserve still-valid decisions;
3. update stale status;
4. append history if useful;
5. do not erase important traps or rejected paths unless explicitly obsolete.

---

### 3. Separate Facts, Interpretations, and Decisions

Use clear labels where confusion is possible.

Example:

```markdown
Fact:
The analysis produced only 240 high-confidence cells.

Interpretation:
This is too small to support a stable downstream clustering as the sole main analysis.

Decision:
Use this result as a conservative sensitivity set, not as the primary discovery space.
```

This reduces the chance that the next AI treats interpretations as raw facts or speculative ideas as decisions.

---

### 4. Capture "Necessary and Sufficient" Context

Do not include everything from the conversation.

Include only what the next AI needs to continue correctly.

A good handoff should be:

- complete enough to avoid confusion;
- explicit enough to prevent repeated mistakes;
- concise enough that the next AI can actually absorb it.

For very complex projects, include detail, but organize it with strong headings and tables.

---

## Required Sections for a Full Handoff

Use these sections unless the project clearly needs a different structure.

### 0. Opening Instruction to the New AI

Tell the next AI to read before responding.

```markdown
# Project Handoff Prompt for New AI Assistant

> Read this entire document before responding to the user.
> You are taking over an ongoing project with important prior decisions.
> Do not treat the next user message as an isolated request.
```

For Chinese:

```markdown
# 项目交接提示词（给新 AI 读取）

> 请你先完整阅读本文档，再回答用户后续问题。
> 你现在接手的是一个已经推进了一段时间的项目。
> 不要把用户后续消息当成孤立的新问题。
```

---

### 1. Your Role

Define the next AI's role.

```markdown
## 1. Your Role

You are not starting from scratch. You are taking over an ongoing project.

Your role is:
- project continuity keeper;
- technical/methodological reviewer;
- reasoning partner;
- prompt writer for downstream tools or collaborators;
- quality-control assistant.

You should:
1. preserve prior decisions;
2. identify whether new outputs change the strategy;
3. write clear next-step instructions;
4. avoid reopening settled questions unless new evidence requires it.

You should not:
1. restart from scratch;
2. ask the user to repeat documented context;
3. revive rejected strategies as if they were still valid;
4. overstate uncertain conclusions.
```

---

### 2. Project in One Sentence

Give the next AI a compact project identity.

Template:

```markdown
## 2. Project in One Sentence

This project aims to [goal] using [inputs/tools/materials] by [main strategy], with the current focus on [active stage].
```

---

### 3. Background and Quality Bar

Explain why the project matters and what level of care is needed.

Include:

- user's intended deliverable;
- expert review expectations;
- domain constraints;
- important terminology;
- quality bar;
- consequences of getting decisions wrong.

---

### 4. Data / Materials / Inputs / Artifacts

List the project inputs and outputs.

Use a table:

```markdown
| Item | Location / Name | Purpose | Status |
|---|---|---|---|
| Main dataset | ... | ... | Available |
| Analysis object | ... | ... | Generated |
| Report | ... | ... | Drafted |
```

Include exact paths, file names, IDs, or links if available.

---

### 5. Current Workflow or Roadmap

State the working plan and dependencies.

```markdown
| Stage | Purpose | Depends on | Status |
|---|---|---|---|
| Stage 1 | ... | — | Done |
| Stage 2 | ... | Stage 1 | In progress |
| Stage 3 | ... | Stage 2 | Not started |
```

Add dependency warnings:

```text
Do not start Stage 4 before Stage 2 has selected the final object.
```

---

### 6. Completed Work

Summarize completed work with specific results.

Use concrete numbers, filenames, outputs, or decisions.

Avoid vague claims like "analysis was done."

Prefer:

```markdown
Completed:
- F1 preprocessing completed: 107,146 cells retained after QC.
- Epithelial subset saved: 6,703 cells.
- Normal epithelial: 4,721; tumor epithelial: 1,982.
```

For non-data projects:

```markdown
Completed:
- Requirements draft v2 reviewed.
- Authentication approach chosen: JWT, not cookie sessions.
- Pricing model A rejected due to operational complexity.
```

---

### 7. Decisions Already Made

This section prevents the next AI from reopening settled issues.

Template:

```markdown
## 7. Decisions Already Made

1. Use [strategy] as the primary path.
   - Rationale:
   - Alternatives rejected:

2. Treat [object/result] as [main/supplement/sensitivity/exploratory].
   - Rationale:

3. Use the wording "[careful term]" instead of "[overstated term]".
```

---

### 8. Rejected / Downgraded / Failed Paths

Capture traps explicitly.

Template:

```markdown
## 8. Rejected or Downgraded Paths

### Path: [name]

What was tried:
...

Result:
...

Why it is not the main path:
...

Current status:
Use only as [supplement / sensitivity / historical context / do not repeat].
```

This is one of the most important sections.

---

### 9. Current Active Problem

State the current unresolved issue.

Include:

- what triggered it;
- why it matters;
- what evidence exists;
- what decision is needed;
- what should not be done prematurely.

---

### 10. Recommended Next Step

Give an unambiguous next action.

```markdown
## 10. Recommended Next Step

The next step is:

[clear action]

Do not proceed to [later stage] until [condition] is met.

Required outputs:
- ...
- ...
```

---

### 11. Copy-Paste Prompt for the Next AI / Tool / Collaborator

If the user will send instructions elsewhere, provide a direct block.

````markdown
## 11. Copy-Paste Prompt for the Next Action

```text
Please continue with the following strategy:

1. ...
2. ...
3. ...

Required outputs:
- ...

Stop and ask before proceeding if:
- ...
```
````

The prompt should be:

- actionable;
- bounded;
- explicit about outputs;
- explicit about what not to do;
- explicit about stop conditions.

---

### 12. Future Roadmap

Show how upcoming work depends on current decisions.

```markdown
| Future step | Input required | Purpose | Do not start until |
|---|---|---|---|
| ... | ... | ... | ... |
```

---

### 13. Risk Register

Use a table.

```markdown
| Risk | Status | Why it matters | Mitigation |
|---|---|---|---|
| Tool disagreement | Active | May misclassify result | Use multi-evidence strategy |
| Technical artifact | Active | Could become false main result | Mark as artifact and exclude |
| Overfitting | Potential | Weak generalization | External validation |
```

---

### 14. Wording Rules

Provide careful language rules.

```markdown
Use:
- candidate
- supported by
- consistent with
- sensitivity analysis

Avoid:
- confirmed
- proves
- causal
- definitive
```

Tailor to the project.

---

### 15. How to Handle Future User Updates

Tell the next AI how to reason about new outputs.

```markdown
When the user pastes a new result, first ask:

1. Which project stage does this belong to?
2. Does it support or contradict the current strategy?
3. Does it trigger a branch decision?
4. Is there a methodological flaw?
5. Are required outputs missing?
6. Should the project continue, pause, or revise?
7. What exact reply should be sent to the external tool or collaborator?
```

---

### 16. If-User-Asks Patterns

Include response templates for likely questions.

```markdown
### If the user asks "Did we make a mistake?"

Answer:
Not necessarily. The earlier step tested an assumption. The result shows whether that route should remain primary, become supplemental, or be abandoned.

### If the user asks "Can we move to the next stage?"

Answer:
Only if [condition] is satisfied. Otherwise request [missing output] first.

### If the user asks "Should X be the main result?"

Answer:
Use X as the main result only if it satisfies [criteria]. Otherwise treat it as exploratory or supplemental.
```

---

### 17. Final Guardrail

End with a single memorable rule.

```markdown
## Final Guardrail

The most important thing to remember is:

[one-sentence rule]

All future decisions should be checked against this rule.
```

---

## Lightweight Handoff Format

For quick transfers, use:

```markdown
# Quick Handoff

## Summary
[1–3 sentences about current state]

## Current Task State
[What is in progress]

## Key Decisions
- ...

## What Worked
- ...

## What Did Not Work / Traps to Avoid
- ...

## Relevant Files / Artifacts
- ...

## Blockers / Open Questions
- ...

## Next Steps
1. ...
2. ...

## Pasteable Resume Prompt
[What the next AI should read/do first]
```

---

## Session-Log Handoff Format

For long-running projects, use timestamped entries.

```markdown
---

## Handoff: YYYY-MM-DD HH:MM

### Current Task State
...

### Key Decisions
...

### Modified / Relevant Files
...

### Blockers / Open Questions
...

### Next Steps
...

### Critical Context / Gotchas
...

### Model Summary
- 8–12 bullets summarizing what the next AI must know.

### Handoff Context
Paste this into the next session:
1. Read this latest handoff entry.
2. Focus on...
3. Do not...
```

Append new entries instead of overwriting if maintaining a history is important.

---

## Context-Transfer File Format

When the user wants a file to upload to a new conversation, write the content to a Markdown file and give the user the download path/link.

A strong context-transfer file should include:

```markdown
## Context Transfer

### Summary
[1–3 sentences]

### Key Decisions
...

### Traps to Avoid
...

### Working Agreements
...

### Relevant Files
...

### Open Work
...

### Prompt for New Chat
...
```

The "Prompt for New Chat" should provide background context, not blindly command the new AI to act without verifying any referenced files.

---

## Quality Checklist

Before finalizing, verify:

- [ ] The document is written for the next AI, not only for a human.
- [ ] The new AI's role is explicit.
- [ ] The project is summarized in one sentence.
- [ ] Current state is concrete and specific.
- [ ] Completed work is separated from planned work.
- [ ] Decisions include rationale.
- [ ] Failed/downgraded paths are recorded.
- [ ] Current active problem is clear.
- [ ] Next step is unambiguous.
- [ ] Direct copy-paste prompt is included if useful.
- [ ] Future dependencies are clear.
- [ ] Risks and mitigations are included.
- [ ] Wording rules prevent overclaiming.
- [ ] Future update handling is specified.
- [ ] Final guardrail summarizes the core strategy.
- [ ] Format is Markdown unless user asked otherwise.

---

## Common Mistakes to Avoid

### Mistake 1: Writing a human report instead of an AI prompt

Bad:

```text
This project analyzes X. Several steps have been completed.
```

Better:

```text
You are taking over a project analyzing X. You must preserve these decisions and avoid reopening rejected paths.
```

---

### Mistake 2: Omitting rejected paths

Bad:

```text
Next, continue with strategy B.
```

Better:

```text
Strategy A was tested and downgraded because...
Do not revive Strategy A unless new evidence appears.
Continue with Strategy B.
```

---

### Mistake 3: No stop conditions

Bad:

```text
Run the next analysis.
```

Better:

```text
Run the next analysis. Stop and ask if matching rate is below 90%, if output object is missing, or if the result contradicts the current main strategy.
```

---

### Mistake 4: Overclaiming uncertain results

Bad:

```text
X is confirmed.
```

Better:

```text
X is supported by current evidence, but remains a candidate until validated by...
```

---

### Mistake 5: Missing file paths or object names

If a file, table, dataset, branch, or object matters, name it exactly.

---

## Notes on Skill Design

When packaging this as a `SKILL.md`:

- include YAML frontmatter with `name` and `description`;
- make the description specific and trigger-rich;
- keep the main body focused;
- move extremely long examples to `references/` if using a full skill folder;
- include templates that can be copied directly;
- make the skill tool-agnostic unless the user's workflow requires a specific tool.

---

## Final Success Criterion

The handoff succeeds if:

> A new AI can read it once, understand the project state, avoid known traps, and correctly advise the user's next step without asking for already-documented context.
