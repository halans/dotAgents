# dotAgents

A personal collection of AI skills and agents for use with [GitHub Copilot CLI](https://githubnext.com/projects/copilot-cli) and [Claude Code](https://code.claude.com).

## Skills

Skills are reusable knowledge modules that load into context when needed. Each lives in `skills/<name>/` and is defined by a `SKILL.md` file.

| Skill | Description |
|-------|-------------|
| [agent-creator](skills/agent-creator/) | Guide for creating custom agents with defined personas, tool access, and skill references. |
| [article-title-summarizer](skills/article-title-summarizer/) | Creates coherent summary paragraphs from lists of article titles. |
| [blog-cross-linker](skills/blog-cross-linker/) | Reads a set of blog posts and adds inline cross-links between them where content naturally references other posts. |
| [marketplace-creator](skills/marketplace-creator/) | Generates a valid `.claude-plugin/marketplace.json` manifest for distributing Claude Code plugins. |
| [mcpb-creator](skills/mcpb-creator/) | Guide for building MCP servers as distributable bundles with manifest structure, tool definitions, and security measures. |
| [skill-metadata-generator](skills/skill-metadata-generator/) | Generates a structured `metadata.json` for an existing skill directory. |
| [text-rewriter](skills/text-rewriter/) | Rewrites text to strip AI-generated patterns, puffery, and formulaic language. |

## Agents

Agents are self-contained AI instances with a defined persona, tool access, and end-to-end workflow. Each lives in `agents/<name>/` as a `*.agent.md` file.

| Agent | Description |
|-------|-------------|
| [article-summarizer](agents/article-summarizer/) | Browses one or more websites, extracts article titles from list items, and writes per-site summary paragraphs to a timestamped markdown file. |
| [text-rewriter](agents/text-rewriter/) | Rewrites text from pasted input or files, applying the text-rewriter skill rules, and saves the cleaned output. |

## Installing a skill

```bash
npx skills add halans/dotAgents --skill <skill-name>
```

## License

MIT
