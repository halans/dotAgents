#!/usr/bin/env python3
"""
Agent Initializer - Creates a new agent from template

Usage:
    init_agent.py <agent-name> --path <path>

Examples:
    init_agent.py code-reviewer --path agents
    init_agent.py data-analyst --path .github/agents
    init_agent.py doc-writer --path /custom/location
"""

import sys
from pathlib import Path


AGENT_TEMPLATE = """---
name: {agent_name}
description: "TODO: Clear explanation of what this agent does and when to invoke it. Be specific about the task it handles end-to-end."
tools:
  - read
  # TODO: Keep only the tools this agent needs. Remove unused tools.
  # Common tools: read, edit, write, search, bash, glob, grep, web_fetch, web_search, notebook_edit
---

You are a {agent_title_lower} that [TODO: one sentence describing core capability].

## How you work

1. [TODO: First step — e.g., "Accept input from the user — either pasted directly or as a file path."]
2. [TODO: Second step — e.g., "Read the file to get the source content."]
3. [TODO: Third step — e.g., "Apply transformation rules."]
4. [TODO: Fourth step — e.g., "Save the output."]
5. [TODO: Fifth step — e.g., "Show a brief summary of what changed."]

## Rules

- [TODO: Add behavioral constraints and guardrails]
- [TODO: Reference any skills this agent uses, e.g., "Follow the `skill-name` skill and its `references/guide.md` rule set exactly."]

## Output

[TODO: Describe what the agent produces and how it presents results.]
"""


def title_case_name(name):
    """Convert hyphenated name to Title Case for display."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def init_agent(agent_name, path):
    """
    Initialize a new agent directory with template .agent.md file.

    Args:
        agent_name: Name of the agent (kebab-case)
        path: Path where the agent directory should be created

    Returns:
        Path to created agent directory, or None if error
    """
    agent_dir = Path(path).resolve() / agent_name

    if agent_dir.exists():
        print(f"Error: Agent directory already exists: {agent_dir}")
        return None

    try:
        agent_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created agent directory: {agent_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    agent_title = title_case_name(agent_name)
    agent_content = AGENT_TEMPLATE.format(
        agent_name=agent_name,
        agent_title_lower=agent_title.lower()
    )

    agent_md_path = agent_dir / f'{agent_name}.agent.md'
    try:
        agent_md_path.write_text(agent_content)
        print(f"Created {agent_name}.agent.md")
    except Exception as e:
        print(f"Error creating .agent.md: {e}")
        return None

    print(f"\nAgent '{agent_name}' initialized successfully at {agent_dir}")
    print("\nNext steps:")
    print("1. Update the description in frontmatter")
    print("2. Select the minimal set of tools the agent needs")
    print("3. Write the system prompt (workflow, rules, output)")
    print("4. Test the agent against concrete use cases")

    return agent_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_agent.py <agent-name> --path <path>")
        print("\nAgent name requirements:")
        print("  - Kebab-case identifier (e.g., 'code-reviewer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 64 characters")
        print("  - Must match directory name exactly")
        print("\nExamples:")
        print("  init_agent.py code-reviewer --path agents")
        print("  init_agent.py data-analyst --path .github/agents")
        print("  init_agent.py doc-writer --path /custom/location")
        sys.exit(1)

    agent_name = sys.argv[1]
    path = sys.argv[3]

    print(f"Initializing agent: {agent_name}")
    print(f"   Location: {path}")
    print()

    result = init_agent(agent_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
