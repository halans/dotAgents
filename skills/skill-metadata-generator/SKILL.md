---
name: skill-metadata-generator
description: Generates a structured metadata.json file for an existing skill directory. Use when you need to create or update a skill's machine-readable metadata for agent discovery, compatibility declarations, and capability descriptions. Triggers on requests like "generate metadata for this skill", "create a metadata.json", "add metadata to my skill", or any time a skill directory lacks a metadata.json or has one that needs updating.
---

# Skill Metadata Generator

You generate a well-structured `metadata.json` file for an existing skill by reading its directory and applying a consistent derivation process.

Good skill metadata makes capabilities machine-discoverable: agents can match user queries to the right skill via triggers and tags, understand what the skill expects and produces via input/output schemas, and reason about compatibility and dependencies without reading the full SKILL.md.

## How you work

1. **Locate the skill directory.** Accept a path from the user. If none is given, ask for it. Verify that a `SKILL.md` exists at that path.

2. **Read the skill thoroughly.**
   - Parse the YAML frontmatter (`name`, `description`, any declared tools).
   - Read the full SKILL.md body: identity statement, workflow steps, rules, output section.
   - List the contents of `references/`, `scripts/`, `assets/`, and `templates/` if they exist.
   - If a `metadata.json` already exists, read it — preserve fields like `version`, `license`, `author`, and `repository` rather than overwriting them.

3. **Derive each field** using the rules in `references/metadata-schema.md`. Pay particular attention to:
   - **`triggers`**: mine the description and body for every phrase a user might type that should invoke this skill. Think about how users describe the *problem*, not the *solution* — include both.
   - **`tags`**: distil triggers to 3–8 high-signal kebab-case concepts for filtering and discovery.
   - **`usage.prompt`**: write this as a model-facing instruction, not a user-facing description.
   - **`inputSchema` / `outputSchema`**: infer from what the skill accepts and what it produces. Use JSON Schema format.

4. **Confirm version handling.** If no prior `metadata.json` exists, use `"1.0.0"`. If one exists, preserve the current version unless the user asks to bump it.

5. **Write `metadata.json`** to the skill root directory. Use 2-space indentation and consistent key ordering (follow the schema in `references/metadata-schema.md`).

6. **Show a summary** of what was generated — key fields, trigger count, and any fields left as `null` that the user may want to fill in (e.g. `author`, `repository`, `license`).

## Rules

- Never invent a `repository` URL, `author`, or `license` — leave them as `null` if not found in an existing `metadata.json` or explicit user input.
- Preserve all fields from an existing `metadata.json` that you cannot re-derive (e.g. `author`, `repository`, `license`, `version`).
- `name` must match the skill directory name exactly.
- `triggers` must be phrases a real user would type — not internal implementation terms. Aim for 8–12 triggers.
- `tags` must be lowercase, hyphenated, and specific (not generic terms like `"ai"` or `"tool"`).
- Do not modify `SKILL.md` or any other file — only write `metadata.json`.
- Follow the full schema in `references/metadata-schema.md`. Consult it before writing the file.

## Output

A `metadata.json` file written to the skill root, followed by a brief confirmation showing:
- Output path
- Fields populated vs. left null
- Trigger count and tag list
