# Tool Selection Guide

Choose the minimal set of tools an agent needs based on its workflow.

## Tool Reference

| Tool | Purpose | Grant when the agent needs to... |
|------|---------|----------------------------------|
| `read` | Read file contents | Inspect existing files |
| `edit` | Make targeted edits to files | Modify specific parts of existing files |
| `write` | Create or overwrite files | Produce new output files |
| `search` | Search file contents | Find patterns or text within files |
| `bash` | Execute shell commands | Run scripts, CLI tools, or system commands |
| `glob` | Find files by name pattern | Locate files matching a pattern (e.g., `*.py`) |
| `grep` | Search with regex | Find content across files with regex patterns |
| `web_fetch` | Fetch URL content | Retrieve information from a specific URL |
| `web_search` | Search the web | Find information on the internet |
| `notebook_edit` | Edit Jupyter notebooks | Modify `.ipynb` files |

## Selection Principles

### Start from zero

Begin with an empty tool list. For each step in the agent's workflow, ask: "What tool does this step require?" Add only those tools.

### Read vs. Edit vs. Write

- **Read-only agents** (analyzers, reporters): `read` only
- **Agents that modify existing files**: `read` + `edit`
- **Agents that produce new files**: `read` + `write`
- **Agents that do both**: `read` + `edit` + `write`

### When to grant Bash

`bash` is the most powerful and most dangerous tool. Grant it only when the agent must:
- Run scripts or CLI tools (linters, test runners, build tools)
- Execute system commands (process management, file operations not covered by other tools)
- Install dependencies or run package managers

Never grant `bash` to agents that only need to read, write, or search files — use the dedicated tools instead.

### Search tools: Search vs. Grep vs. Glob

- `glob` — finding files by name or extension pattern
- `grep` — searching file contents with regex
- `search` — general content search within files

Most agents that need search capabilities need `grep` and/or `glob`. Use `search` when the agent needs broader content searching.

## Common Tool Sets by Agent Type

| Agent Type | Typical Tools |
|------------|---------------|
| File transformer | `read`, `write` |
| Code reviewer | `read`, `glob`, `grep` |
| Code modifier | `read`, `edit`, `glob`, `grep` |
| Report generator | `read`, `write`, `bash` |
| Research assistant | `read`, `web_search`, `web_fetch` |
| Full-stack developer | `read`, `edit`, `write`, `bash`, `glob`, `grep` |
