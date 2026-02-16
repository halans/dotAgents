#!/usr/bin/env python3
"""
Quick validation script for agents - validates .agent.md structure and frontmatter
"""

import sys
import re
import yaml
from pathlib import Path


def validate_agent(agent_path):
    """Basic validation of an agent"""
    agent_path = Path(agent_path)

    # Find .agent.md file
    agent_files = list(agent_path.glob('*.agent.md'))
    if not agent_files:
        return False, "No .agent.md file found"
    if len(agent_files) > 1:
        return False, f"Multiple .agent.md files found: {[f.name for f in agent_files]}. Each agent directory should contain exactly one."

    agent_md = agent_files[0]

    # Check filename matches directory name
    expected_filename = f"{agent_path.name}.agent.md"
    if agent_md.name != expected_filename:
        return False, f"Agent file '{agent_md.name}' should be named '{expected_filename}' to match directory name"

    # Read and validate frontmatter
    content = agent_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'tools'}

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    for field in ('name', 'description', 'tools'):
        if field not in frontmatter:
            return False, f"Missing required field '{field}' in frontmatter"

    # Validate name
    name = frontmatter['name']
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > 64:
        return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Validate name matches directory
    if name != agent_path.name:
        return False, f"Name '{name}' in frontmatter does not match directory name '{agent_path.name}'"

    # Validate description
    description = frontmatter['description']
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if not description:
        return False, "Description cannot be empty"
    if '<' in description or '>' in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate tools
    tools = frontmatter['tools']
    if not isinstance(tools, list):
        return False, f"Tools must be a list, got {type(tools).__name__}"
    if len(tools) == 0:
        return False, "Tools list cannot be empty — agents need at least one tool"
    for tool in tools:
        if not isinstance(tool, str):
            return False, f"Each tool must be a string, got {type(tool).__name__}: {tool}"

    # Check that body (system prompt) exists after frontmatter
    body = content[match.end():].strip()
    if not body:
        return False, "Agent has no system prompt (empty body after frontmatter)"

    return True, "Agent is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <agent_directory>")
        sys.exit(1)

    valid, message = validate_agent(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
