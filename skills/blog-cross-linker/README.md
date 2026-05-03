# blog-cross-linker

Reads a set of blog posts and adds inline cross-links between them — embedding links in existing text, never appending "See also" sections.

## How to install

```
npx skills add halans/dotAgents --skill blog-cross-linker
```

## What it does

- Reads all markdown posts in a folder and maps each post's subjects and named entities
- Identifies where existing text in one post names the subject of another
- Presents a proposals table for your approval before touching any files
- Applies approved links as precise inline markdown edits

## When to use it

Use this skill when you want to improve internal navigation across a blog by linking posts to each other — whether you call it "cross-linking", "internal links", "interlinking", or just "link these posts together".

## Usage

```
Cross-link all the posts in content/posts/
```

```
Which of my articles can link to each other?
```

```
Add internal links between my blog posts
```

## Output

Modified markdown files with inline links added to approved locations. After editing, a summary reports how many links were added and which files were changed.

## Reference

- [`SKILL.md`](SKILL.md) — full 5-step workflow, linking rules, and URL construction reference
