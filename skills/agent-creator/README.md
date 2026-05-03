# agent-creator

A guide for creating custom AI agents — specialized instances with a defined persona, tool access, and deterministic workflows.

## How to install

```
npx skills add halans/dotAgents --skill agent-creator
```

## What it does

- Guides you through defining an agent's purpose and minimal tool set
- Scaffolds the agent directory and `.agent.md` template via `init_agent.py`
- Provides patterns for writing focused, deterministic system prompts
- Validates the finished agent with `quick_validate.py`

## When to use it

Use this skill when you want to create a new agent (or update an existing one) that operates as a self-contained specialist owning a complete workflow end-to-end.

## Usage

```
Create an agent that reviews pull requests and posts a summary comment
```

```
Build an agent that reads a CSV and writes a formatted markdown report
```

## Output

A validated `.agent.md` file inside a named directory under `agents/`, ready to run as a dedicated AI instance.

## Reference

- [`SKILL.md`](SKILL.md) — creation process and system prompt guidelines
- [`references/agent-patterns.md`](references/agent-patterns.md) — common agent patterns with examples
- [`references/tool-selection-guide.md`](references/tool-selection-guide.md) — how to pick the minimal tool set
- [`scripts/init_agent.py`](scripts/init_agent.py) — scaffolds the agent directory and template
- [`scripts/quick_validate.py`](scripts/quick_validate.py) — validates agent structure and frontmatter
