---
name: agent-creator
description: Guide for creating custom agents. Use when users want to create a new agent (or update an existing agent) that operates as a specialized AI Agent instance with a defined persona, tool access, and optional skill references. Agents are defined in .agent.md files with YAML frontmatter and a system prompt body.
---

# Agent Creator

This skill provides guidance for creating custom agents.

## About Agents

Agents are specialized AI Agent instances defined by a system prompt and a set of allowed tools. While skills provide modular knowledge and workflows, agents are the executable layer that puts skills to work within a focused persona and behavioral contract.

Think of agents as "job descriptions" — they define who the AI Agent becomes, what tools it can use, and how it should behave for a specific task.

### Agents vs. Skills

| Aspect | Skill | Agent |
|--------|-------|-------|
| File | `SKILL.md` | `*.agent.md` |
| Purpose | Knowledge and workflows | Executable persona with tool access |
| Frontmatter | `name`, `description` | `name`, `description`, `tools` |
| Body | Instructions and reference material | System prompt defining behavior |
| Loading | Loaded into context on trigger | Runs as a dedicated AI Agent instance |
| Composition | Standalone | Can reference and use skills |

Use a **skill** when the goal is reusable knowledge that can be composed into many contexts. Use an **agent** when the goal is a self-contained specialist that owns a complete workflow end-to-end.

### Anatomy of an Agent

Every agent is a single `.agent.md` file inside a named directory:

```
agent-name/
└── agent-name.agent.md
```

The `.agent.md` file has two parts:

1. **YAML frontmatter** — metadata and tool declarations
2. **Markdown body** — the system prompt

#### Frontmatter

```yaml
---
name: agent-name
description: What this agent does and when to use it.
tools:
  - read
  - edit
  - search
---
```

Required fields:
- `name` — kebab-case identifier (must match directory name)
- `description` — clear explanation of what the agent does and when to invoke it
- `tools` — list of tools the agent is allowed to use

#### Available Tools

Select only the tools the agent needs. See `references/tool-selection-guide.md` for detailed guidance.

Common tools: `read`, `edit`, `write`, `search`, `bash`, `glob`, `grep`, `web_fetch`, `web_search`, `notebook_edit`.

#### System Prompt (Body)

The markdown body is the agent's system prompt. It defines:

1. **Identity** — one sentence stating what the agent is
2. **Workflow** — numbered steps the agent follows
3. **Rules** — constraints and behavioral guidelines
4. **Output** — what the agent produces and how it presents results

## Core Principles

### Single Responsibility

Each agent should do one thing well. If an agent's description requires "and" to explain what it does, consider splitting it into two agents or extracting shared logic into a skill.

### Minimal Tool Surface

Grant only the tools the agent actually needs. An agent that only reads and analyzes files should not have `bash` or `write`. This limits blast radius and makes the agent's capabilities predictable.

### Skill Composition

Agents can reference existing skills to inherit domain knowledge without duplicating it. In the system prompt, reference the skill by name and point to its resources:

```markdown
You follow the `text-rewriter` skill and its `references/ai-writing-guide.md` rule set exactly.
```

This keeps agents lean — the agent owns the workflow and persona, while the skill owns the domain knowledge.

### Deterministic Workflows

Write the agent's workflow as explicit numbered steps. Each step should be a clear action, not a vague goal. The agent should be able to follow the steps mechanically.

**Good:** "1. Read the file at the provided path. 2. Extract all function signatures. 3. Write a summary to `output.md`."

**Vague:** "1. Understand the code. 2. Do something useful with it."

## Agent Creation Process

1. Define the agent's purpose with concrete examples
2. Select the minimal tool set
3. Initialize the agent (run `init_agent.py`)
4. Write the system prompt
5. Test and iterate

### Step 1: Define the Agent's Purpose

Gather concrete examples of how the agent will be used. Ask:

- "What specific task should this agent handle end-to-end?"
- "What would a user say to invoke this agent?"
- "What inputs does it accept and what outputs does it produce?"
- "Does an existing skill provide the domain knowledge this agent needs?"

Conclude when the agent's scope and behavior are clear.

### Step 2: Select the Minimal Tool Set

Based on the agent's workflow, determine which tools it needs. See `references/tool-selection-guide.md` for guidance on choosing tools.

The principle is least privilege — only grant tools the agent will actually use in its workflow.

### Step 3: Initialize the Agent

Run the `init_agent.py` script to create the agent directory and template:

```bash
scripts/init_agent.py <agent-name> --path <output-directory>
```

The script creates:
- Agent directory with the correct name
- Template `.agent.md` file with frontmatter and TODO placeholders

After initialization, customize the generated template.

### Step 4: Write the System Prompt

The system prompt is the markdown body of the `.agent.md` file. Structure it as:

1. **Opening identity statement** — "You are a [role] that [core capability]."
2. **"How you work" section** — numbered workflow steps
3. **Rules/constraints section** — behavioral guidelines and guardrails
4. **Output section** — what the agent produces and how it presents results

See `references/agent-patterns.md` for common patterns and examples.

#### System Prompt Guidelines

- **Use imperative form** — "Read the file" not "You should read the file"
- **Be specific about file handling** — state naming conventions, output locations, and formats
- **Reference skills explicitly** — name the skill and its resource files
- **Keep it concise** — a system prompt should typically be 20-50 lines
- **Avoid redundancy** — if a skill already documents the rules, reference it rather than restating

### Step 5: Test and Iterate

Test the agent against the concrete examples from Step 1. Common issues:

- Agent uses tools it shouldn't have — reduce the tool list
- Agent misses steps — make workflow more explicit
- Agent produces unexpected output — add output format specification
- Agent doesn't leverage skill knowledge — add explicit skill reference in system prompt
