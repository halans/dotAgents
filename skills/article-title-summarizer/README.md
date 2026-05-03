# article-title-summarizer

Synthesizes a list of article titles into a single, coherent summary paragraph — capturing dominant themes, trends, and topics without mechanically listing them.

## How to install

```
npx skills add halans/dotAgents --skill article-title-summarizer
```

## What it does

- Identifies recurring themes and subject clusters across a title list
- Produces exactly one neutral, present-tense paragraph (3–6 sentences)
- Derives kebab-case tags from the identified themes
- Outputs a markdown file with YAML frontmatter (`tags`) followed by the summary

## When to use it

Use this skill when you have a list of article titles and want a readable paragraph that conveys what the collection covers — for digests, newsletters, research overviews, or reading list summaries.

## Usage

```
Summarize these article titles into a single paragraph: [list of titles]
```

```
Generate an overview paragraph for this reading list
```

## Output

A markdown string with YAML frontmatter containing a `tags` list, followed by one summary paragraph. No bullet points, no headers, no title quoting.

```markdown
---
tags:
  - ai-governance
  - agent-security
---

Coverage spans...
```

## Reference

- [`SKILL.md`](SKILL.md) — workflow, rules, and quality checks
