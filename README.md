# dotAgents

A collection of AI agents and reusable skills. Build composable AI workflows with clear personas, tool access, and domain knowledge separation.

## Overview

dotAgents (.github, .claude, etc) provides a structured approach to building AI-powered automation through two core primitives:

- **Skills** — Reusable knowledge modules and workflows that can be composed into multiple contexts
- **Agents** — Executable AI instances with defined personas, tool access, and specific behavioral contracts

Think of skills as libraries of domain knowledge, and agents as specialized workers that apply that knowledge to complete specific tasks end-to-end.

## Core Concepts

### Agents vs. Skills

| Aspect | Skill | Agent |
|--------|-------|-------|
| File | `SKILL.md` | `*.agent.md` |
| Purpose | Knowledge and workflows | Executable persona with tool access |
| Frontmatter | `name`, `description` | `name`, `description`, `tools` |
| Body | Instructions and reference material | System prompt defining behavior |
| Loading | Loaded into context on trigger | Runs as a dedicated AI instance |
| Composition | Standalone | Can reference and use skills |

**Use a skill** when the goal is reusable knowledge that can be composed into many contexts.

**Use an agent** when the goal is a self-contained specialist that owns a complete workflow end-to-end.

## Project Structure

```
dotAgents/
├── agents/                    # Agent definitions
│   └── text-rewriter/
│       └── text-rewriter.agent.md
├── skills/                    # Reusable skill modules
│   ├── agent-creator/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── agent-patterns.md
│   │   │   └── tool-selection-guide.md
│   │   └── scripts/
│   │       ├── init_agent.py
│   │       └── quick_validate.py
│   └── text-rewriter/
│       ├── SKILL.md
│       └── references/
│           └── ai-writing-guide.md
└── instructions/              # (Reserved for future use)
```

## Getting Started

### Creating a New Agent

1. **Define the agent's purpose** with concrete examples of how it will be used
2. **Select minimal tools** the agent needs (read, edit, write, search, etc.)
3. **Initialize the agent** using the provided script:

```bash
python skills/agent-creator/scripts/init_agent.py <agent-name> --path agents
```

4. **Customize the template** by editing the generated `.agent.md` file:
   - Update the description in frontmatter
   - Select only the tools the agent needs
   - Write the system prompt (workflow, rules, output)

5. **Validate the agent**:

```bash
python skills/agent-creator/scripts/quick_validate.py agents/<agent-name>
```

### Agent Anatomy

Every agent is defined in a `.agent.md` file with two parts:

#### 1. YAML Frontmatter (Metadata)

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

#### 2. Markdown Body (System Prompt)

The system prompt defines:
- **Identity** — one sentence stating what the agent is
- **Workflow** — numbered steps the agent follows
- **Rules** — constraints and behavioral guidelines
- **Output** — what the agent produces and how it presents results

## Example: Text Rewriter Agent

The text-rewriter agent demonstrates the framework's composability:

- **Agent**: [`agents/text-rewriter/text-rewriter.agent.md`](agents/text-rewriter/text-rewriter.agent.md)
  - Accepts text input (pasted or file path)
  - Applies rewriting rules
  - Saves cleaned output
  
- **Skill**: [`skills/text-rewriter/SKILL.md`](skills/text-rewriter/SKILL.md)
  - Provides the workflow and rules
  - References comprehensive writing guide
  
- **Reference**: [`skills/text-rewriter/references/ai-writing-guide.md`](skills/text-rewriter/references/ai-writing-guide.md)
  - 245-line guide with specific patterns to remove
  - Replacement strategies
  - Quality checks

The agent references the skill, keeping the agent definition lean while leveraging deep domain knowledge.

## Core Principles

### Single Responsibility
Each agent should do one thing well. If an agent's description requires "and" to explain what it does, consider splitting it or extracting shared logic into a skill.

### Minimal Tool Surface
Grant only the tools the agent actually needs. This limits blast radius and makes capabilities predictable.

### Skill Composition
Agents reference existing skills to inherit domain knowledge without duplication. The agent owns the workflow and persona; the skill owns the domain knowledge.

### Deterministic Workflows
Write agent workflows as explicit numbered steps. Each step should be a clear action, not a vague goal.

## Available Scripts

### Initialize Agent
```bash
python skills/agent-creator/scripts/init_agent.py <agent-name> --path <output-directory>
```
Creates a new agent directory with template `.agent.md` file.

### Validate Agent
```bash
python skills/agent-creator/scripts/quick_validate.py <agent-directory>
```
Validates agent structure, frontmatter format, and required fields.

## Contributing

When creating new agents or skills:

1. Follow the established patterns in `skills/agent-creator/references/agent-patterns.md`
2. Use the agent-creator skill's tools for initialization and validation
3. Keep agents focused on specific tasks
4. Extract reusable knowledge into skills
5. Validate all agents before committing

## License

(Add your license information here)
