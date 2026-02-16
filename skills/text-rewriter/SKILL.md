---
name: text-rewriter
description: Rewrites text to remove AI-generated linguistic patterns, puffery, and formulaic language. Use when the user wants to rewrite, clean up, or de-AI any text — from pasted input or files.
---

# Text Rewriter

## Overview

Rewrite text to remove AI tells and linguistic patterns using the comprehensive rule set in `references/ai-writing-guide.md`.

## Workflow

1. **Determine input source** — identify whether the user has pasted text directly or provided a file path.
2. **If file path**, read the file to get the source text.
3. **Read `references/ai-writing-guide.md`** for the full rule set. Load it into context before rewriting.
4. **Rewrite the text** applying all rules from the guide.
5. **Determine output path:**
   - For file input: save to the same directory with `-rewritten` appended before the extension (e.g., `report.md` → `report-rewritten.md`).
   - For pasted text: ask the user for an output file path.
6. **Save rewritten text** to the output file.
7. **Display a summary** of changes made.

## Rewriting Rules

When rewriting, follow the ai-writing-guide strictly:

- **Remove all forbidden phrases and patterns** listed in the guide's "non-negotiables" section. Every single one. No exceptions.
- **Apply the "do this instead" replacement strategies** — use the guide's suggested alternatives for each pattern category.
- **Use the "quick templates"** as safe structural patterns when restructuring sentences.
- **Preserve original meaning, facts, and structure** — rewrite for style, not substance. Do not add information, change conclusions, or alter the author's intent.
- **Run every item in the guide's "final self-check"** before saving. If any check fails, revise until it passes.

## Output Format

The saved file contains **only the rewritten text** — no metadata, annotations, diff markers, or commentary.

After saving, display a brief summary listing:
- **Key patterns removed** (e.g., "Removed 3 instances of 'delve', 2 instances of 'it's worth noting'")
- **Notable changes** (e.g., "Replaced rhetorical questions with direct statements")
- **Output file path**
