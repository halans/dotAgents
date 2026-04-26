---
name: blog-cross-linker
description: >
  Reads a set of blog posts and adds inline cross-links between them — linking existing 
  text in one post to another when that text directly references the subject of the other.
  Use this skill whenever the user asks to cross-link blog posts, add internal links 
  between articles, link posts to each other, improve blog navigation with internal links, 
  find cross-linking opportunities, or says things like "link these to each other", 
  "which posts can reference each other?", or "add links between my articles". Always 
  invoke for any request about internal blog linking, even phrased casually. Never add 
  "See also" or "Related posts" sections — inline links only.
---

# Blog Cross-Linker

Analyzes a collection of blog posts, identifies where existing text in one post naturally 
references the subject of another, and adds precise inline links — embedded in the 
sentences already there, with no new text added and no "See also" sections appended.

## Core Principle

A link belongs in a post when **existing text** names something that another post is 
fundamentally about. The link wraps words that are already on the page. Nothing is 
appended or invented.

**Good link:** The phrase `"vibe coding"` in a post about MCP servers links to the 
post *about* vibe coding.  
**Bad link:** Adding `"See also: Vibe Coding"` at the bottom of a section.

## Step 1 — Discover Posts

Glob for all markdown files in the path and date range the user specifies. If they 
haven't specified, ask: which folder, and which years or posts to include?

Infer each post's internal URL from its filename. For Hugo blogs:
- `2025-04-11-vibe-coding.md` → `/posts/2025-04-11-vibe-coding/`

Confirm the URL pattern with the user if the blog framework is unknown.

## Step 2 — Read and Map All Posts

Read every post and note:
- **Title** and **slug**
- **Main subject(s):** what is this post fundamentally about?
- **Named entities:** tools, frameworks, protocols, events, people, and concepts mentioned by name
- **Tags/categories** from frontmatter
- **Existing internal links** (to avoid duplicates later)

Group posts into thematic clusters — posts about the same tool, the same event covered 
from different angles, or where one post introduced a concept that another later applied 
in practice. Clusters make the linking search tractable.

## Step 3 — Identify Linking Candidates

For each post, scan the text for phrases that name the main subject of another post in 
the collection. Ask: if a reader sees this phrase, would they naturally want to know more 
— and does the target post deliver exactly that?

Before proposing a link, verify all of the following:

1. **Text already exists** — the link wraps words already in the post, nothing added
2. **Target is the best destination** — the linked post is where a curious reader goes 
   to learn about the named thing
3. **Right occurrence chosen** — link the most meaningful mention; one link per concept 
   per article is usually right
4. **No existing link** — check the source post for a link already covering this text 
   or concept nearby
5. **Serves the reader** — if clicking feels like a stretch or surprise, skip it

Avoid:
- Linking generic phrases ("AI tools", "the web", "agents") that don't point to a specific post
- Linking every occurrence of a term — once per article is enough
- Linking a post to itself

## Step 4 — Present Proposals to the User

**Always show proposed links and ask for approval before editing any files.**

Present a table grouped by source file:

| Source file | Text to link | Links to | Rationale |
|---|---|---|---|
| `how-ai-is-rewriting.md` | `"vibecoding"` | `vibe-coding.md` | Vibe coding post is where this concept is explored hands-on |
| `mcp-server.md` | `vibe-coded` | `vibe-coding.md` | MCP server was built using the vibe coding approach |
| `osint-symposium.md` | `"agent mode" tools` | `how-ai-is-rewriting.md` | That post covers the agent paradigm in depth |

Let the user confirm, remove, or modify any proposal before proceeding. If they want 
to skip a link, respect it without asking again.

## Step 5 — Apply Approved Links

For each approved link, make a precise edit using enough surrounding context to uniquely 
identify the text. Markdown link syntax:

```
[link text](/posts/target-slug/)
```

Preserve any existing inline formatting around the linked text:
- `**vibe coding**` → `**[vibe coding](/posts/vibe-coding/)**`
- `*"vibecoding"*` → `*["vibecoding"](/posts/vibe-coding/)*`

Use the Grep tool with context lines to confirm the exact text before editing. If the 
match isn't unique, use more surrounding context in the Edit call.

After all edits, report: how many links were added and which files were changed.

## Handling Existing Links

Before proposing a link, check whether the same or nearby text already has an internal 
link. Duplicate links on the same text or concept within one article should be skipped. 
Grep with `-C 2` context is useful for spotting nearby links.

## URL Construction Reference

| Framework | File | URL |
|---|---|---|
| Hugo | `2025-04-11-vibe-coding.md` | `/posts/2025-04-11-vibe-coding/` |
| Jekyll | `_posts/2025-04-11-vibe-coding.md` | `/2025/04/11/vibe-coding/` |
| Generic | `vibe-coding.md` | `/blog/vibe-coding/` |

When in doubt, ask the user to confirm the URL pattern before constructing links.

## What Not to Do

- Do not add "See also", "Related", "Further reading", or any new navigational text
- Do not link on generic terms that aren't the specific focus of another post  
- Do not add more than one link to the same concept within a single article
- Do not invent new anchor text — only link text that already exists in the post
- Do not edit files without the user's explicit approval of the proposals
