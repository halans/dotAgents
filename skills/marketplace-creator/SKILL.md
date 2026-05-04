---
name: marketplace-creator
description: >
  Generates a valid Anthropic Claude Code plugin marketplace manifest
  (.claude-plugin/marketplace.json) from user input or an existing repository
  layout. Use this skill whenever the user wants to create, scaffold, or update
  a Claude Code plugin marketplace, publish a set of Claude plugins to a team
  or organization, or is asking about the marketplace.json structure, plugin
  sources, or how to distribute Claude Code plugins. Also use when the user
  wants to add plugins to an existing marketplace or validate their
  marketplace.json against the spec.
---

# Marketplace Creator

A skill for generating and validating `.claude-plugin/marketplace.json` — the Anthropic-standard manifest for distributing Claude Code plugins to teams, organizations, or the public.

Full schema reference: `references/marketplace-schema.md` — read it when you need field-level detail about any source type, optional field, or validation error.

---

## What you are building

A **plugin marketplace** is a repository (or directory) that contains a `.claude-plugin/marketplace.json` file. That file declares:

1. **Who owns the marketplace** (name, optional email)
2. **What plugins it contains** (one or more plugin entries with names and sources)

Users install it with something like:

```
claude plugin install @marketplace-name
```

or by pointing Claude Code at the GitHub URL.

---

## Gather requirements

Before writing the manifest, collect:

1. **Marketplace name** — kebab-case, becomes the `@name` identifier
2. **Owner name** and (optional) email
3. **Plugins to list** — for each plugin:
   - Name (kebab-case)
   - Where it lives (same repo, different GitHub repo, monorepo, npm, or a bare git URL)
   - Any pinned version, branch, or tag
4. **Optional**: description, `pluginRoot` convention, cross-marketplace dependencies

If the user provides a repository layout (e.g., shows you a directory tree), infer plugin paths from it rather than asking.

---

## Workflow

### 1. Determine plugin sources

Map each plugin to the right source type (read `references/marketplace-schema.md → Plugin sources` for full field specs):

| Situation | Source type |
|-----------|-------------|
| Plugin lives in the same Git repo | `"./path/to/plugin"` (relative string) |
| Plugin is in another GitHub repo | `{ "source": "github", "repo": "owner/repo" }` |
| Plugin is a subdirectory of a monorepo | `{ "source": "git-subdir", "url": "...", "path": "..." }` |
| Plugin is published to npm | `{ "source": "npm", "package": "..." }` |
| Plugin is in any other git host | `{ "source": "url", "url": "..." }` |

> Relative path sources only work when the marketplace is distributed via Git (GitHub, GitLab, or git URL). Warn the user if they're using relative paths with URL-based distribution.

### 2. Check reserved names

Verify the marketplace `name` is not reserved. Reserved names:

`claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`

Also block names that impersonate official Anthropic properties (e.g., `official-claude-plugins`, `anthropic-tools-v2`). If the user chose a reserved name, suggest an alternative and ask them to confirm before proceeding.

### 3. Write the manifest

Output destination: `.claude-plugin/marketplace.json` relative to the project root (or wherever the user says their marketplace root is).

Use this base template and populate with what you gathered:

```json
{
  "$schema": "https://code.claude.com/schemas/marketplace.json",
  "name": "{{name}}",
  "description": "{{description}}",
  "version": "1.0.0",
  "owner": {
    "name": "{{owner.name}}",
    "email": "{{owner.email}}"
  },
  "plugins": []
}
```

Omit optional fields (`email`, `description`, `version`, `metadata`, `allowCrossMarketplaceDependenciesOn`) if the user did not provide values for them — never invent values.

For each plugin, write an entry following the schema in `references/marketplace-schema.md → Plugin entry fields`. Omit `strict` unless the user explicitly requests it (the default `true` is almost always correct).

### 4. Validate

After writing the file, run these checks:

- [ ] Valid JSON (parseable)
- [ ] `name` is kebab-case with no spaces
- [ ] No duplicate plugin names in the `plugins` array
- [ ] All relative source paths start with `./` and do not contain `..`
- [ ] `plugins` array is non-empty (warn if empty, but don't block)
- [ ] No reserved marketplace names

Report any failures and fix them before presenting the result to the user.

---

## Output

After writing the file, present:

1. The file path created
2. The full JSON contents in a fenced code block
3. A brief summary: marketplace name, owner, number of plugins listed, source types used
4. Any warnings (e.g., empty plugins list, URL-only distribution with relative paths)

**Example output summary:**

```
Created .claude-plugin/marketplace.json
  Marketplace: @acme-internal (owned by Acme Platform Team)
  Plugins: 3
    - code-formatter (relative path)
    - security-scanner (github: acme-corp/scanner)
    - doc-generator (npm: @acme/doc-gen)
```

---

## Updating an existing marketplace

If `.claude-plugin/marketplace.json` already exists:

1. Read and parse the current file
2. Preserve all existing fields the user did not ask to change
3. Only modify the specific fields or plugins the user requested
4. Re-validate after editing
5. Show a diff summary (what changed) alongside the full updated file

---

## Common patterns

**Team-internal marketplace (everything in one repo):**
Use `metadata.pluginRoot` to avoid repeating a path prefix, then use short relative names:

```json
{
  "metadata": { "pluginRoot": "./plugins" },
  "plugins": [
    { "name": "formatter", "source": "./formatter" },
    { "name": "linter", "source": "./linter" }
  ]
}
```

**Public marketplace pulling from multiple repos:**

```json
{
  "plugins": [
    {
      "name": "code-formatter",
      "source": { "source": "github", "repo": "acme/formatter", "ref": "v2.1.0" }
    },
    {
      "name": "doc-gen",
      "source": { "source": "npm", "package": "@acme/doc-gen", "version": "^3.0.0" }
    }
  ]
}
```

**Monorepo with sparse checkout:**

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": {
        "source": "git-subdir",
        "url": "https://github.com/acme/monorepo.git",
        "path": "tools/claude-plugins/my-plugin",
        "ref": "main"
      }
    }
  ]
}
```
