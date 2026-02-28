---
name: article-title-summarizer
description: Creates coherent summary paragraphs from lists of article titles. Use when the user provides multiple article titles and requests a summary, overview paragraph, or narrative synthesis of the content themes. Ideal for literature reviews, content aggregation, research summaries, or generating descriptive text from reading lists.
---

# Article Title Summarizer

This skill provides guidance for synthesizing a list of article titles into a single, coherent summary paragraph.

## Purpose

Given a list of article titles, produce one paragraph that captures the dominant themes, trends, and topics across the list — not a mechanical enumeration of titles, but a narrative synthesis a reader could use to understand what the collection covers.

## Workflow

1. Read all titles in full before writing anything.
2. Identify recurring themes, subject clusters, and notable outliers.
3. Draft a single paragraph that:
   - Opens with the dominant theme or focus area of the collection
   - Weaves in secondary themes and notable sub-topics
   - Notes any significant patterns (e.g., a trend, a debate, a technology shift)
   - Closes with the overall scope or breadth of the collection
4. Compile a tags list from the identified themes (2–8 tags, kebab-case, lowercase).
5. Review the draft against the rules below before finalizing.

## Rules

### Structure
- **One paragraph only.** No bullet points, no headers, no numbered lists in the output.
- **3–6 sentences.** Long enough to be informative; short enough to be scannable.
- **No title quoting.** Do not reproduce article titles verbatim in the paragraph. Paraphrase themes instead.

### Tone
- Neutral and descriptive. Do not editorialize or express opinions about the articles.
- Present tense. ("The articles explore...", not "The articles explored...")
- Third person. Do not address the reader directly.

### Content
- Synthesize themes — do not list topics mechanically.
- If a strong majority of titles share a single theme, lead with that theme.
- If titles are diverse, open with the unifying thread (domain, audience, era) before listing sub-themes.
- Do not refer to the list of titles as a named collection, edition, or time-bound set (e.g., avoid "this month's articles", "the February collection", "recent AI coverage", "this week's titles"). Refer to the content and themes directly.
- Do not speculate about article content beyond what the titles indicate.

## Output Format

The output is a markdown file with YAML frontmatter followed by the summary paragraph:

```markdown
---
tags:
  - ai-governance
  - agent-security
  - creative-work
---

Coverage spans...
```

### Tags rules
- Derive tags directly from the identified themes — one tag per distinct theme.
- 2–8 tags maximum.
- Kebab-case, lowercase (e.g., `ai-safety`, `self-improving-models`).
- No generic tags like `ai` or `technology` alone — be specific.

## Quality checks (run before finalizing)
- [ ] Does the file start with valid YAML frontmatter containing a `tags` list?
- [ ] Is the body exactly one paragraph?
- [ ] Does it avoid quoting any title verbatim?
- [ ] Does every claim trace back to at least one title in the list?
- [ ] Is the tone neutral (no praise, no criticism)?
- [ ] Is it 3–6 sentences?
