# Marketplace Schema Reference

Full specification for `.claude-plugin/marketplace.json` based on the Anthropic Claude Code plugin marketplace documentation.

Source: https://code.claude.com/docs/en/plugin-marketplaces

---

## Top-level structure

```json
{
  "$schema": "...",
  "name": "my-marketplace",
  "description": "Brief description",
  "version": "1.0.0",
  "owner": {
    "name": "Team Name",
    "email": "team@example.com"
  },
  "metadata": {
    "pluginRoot": "./plugins"
  },
  "allowCrossMarketplaceDependenciesOn": ["other-marketplace"],
  "plugins": []
}
```

### Required top-level fields

| Field | Type | Rules |
|-------|------|-------|
| `name` | string | Kebab-case, no spaces. Public-facing — users see it as `@marketplace-name`. |
| `owner.name` | string | Maintainer or team name. |
| `plugins` | array | At least one plugin entry recommended. |

### Optional top-level fields

| Field | Type | Description |
|-------|------|-------------|
| `$schema` | string | JSON Schema URL for editor autocomplete. Ignored by Claude Code at load time. |
| `description` | string | Brief human-readable description of the marketplace. |
| `version` | string | Semantic version of the marketplace manifest itself. |
| `owner.email` | string | Contact email for the maintainer. |
| `metadata.pluginRoot` | string | Base directory prepended to relative plugin source paths. Lets you write `"source": "formatter"` instead of `"source": "./plugins/formatter"`. |
| `allowCrossMarketplaceDependenciesOn` | array of strings | Names of other marketplaces that plugins here may depend on. Dependencies from unlisted marketplaces are blocked at install. |

### Reserved marketplace names (cannot be used)

`claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`

Names that impersonate official marketplaces (e.g. `official-claude-plugins`, `anthropic-tools-v2`) are also blocked.

---

## Plugin entry fields

Each object in the `plugins` array.

### Required

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Kebab-case plugin identifier. Public-facing. |
| `source` | string \| object | Where to fetch the plugin from (see [Plugin sources](#plugin-sources)). |

### Optional metadata

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Brief plugin description. |
| `version` | string | Pins the plugin to this version string. Omit to use git commit SHA. |
| `author.name` | string | Plugin author name. |
| `author.email` | string | Plugin author email. |
| `homepage` | string | Plugin documentation or homepage URL. |
| `repository` | string | Source code repository URL. |
| `license` | string | SPDX identifier (e.g. `MIT`, `Apache-2.0`). |
| `keywords` | array | Tags for discovery and categorization. |
| `category` | string | Plugin category. |
| `tags` | array | Tags for searchability. |
| `strict` | boolean | `true` (default): `plugin.json` is authority, marketplace entry supplements. `false`: marketplace entry is the full definition, no `plugin.json` needed. |

### Optional component paths

| Field | Type | Description |
|-------|------|-------------|
| `skills` | string \| array | Paths to skill directories containing `<name>/SKILL.md`. |
| `commands` | string \| array | Paths to flat `.md` skill files or directories. |
| `agents` | string \| array | Paths to agent files. |
| `hooks` | string \| object | Hooks configuration or path to hooks file. |
| `mcpServers` | string \| object | MCP server configurations or path to MCP config. |
| `lspServers` | string \| object | LSP server configurations or path to LSP config. |

---

## Plugin sources

### Relative path (string)

For plugins in the same repository. Must start with `./`. Resolves relative to marketplace root (the directory containing `.claude-plugin/`), not the `.claude-plugin/` subdirectory itself.

```json
{ "source": "./plugins/my-plugin" }
```

> Only works with Git-based marketplace distribution (GitHub, GitLab, git URL). Does **not** work with URL-based (`https://example.com/marketplace.json`) distribution.

---

### GitHub (`source: "github"`)

```json
{
  "source": {
    "source": "github",
    "repo": "owner/repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4..."
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `repo` | Yes | `owner/repo` format |
| `ref` | No | Branch or tag (defaults to default branch) |
| `sha` | No | Full 40-char SHA to pin to exact commit |

---

### Git URL (`source: "url"`)

```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4..."
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | Full git URL (`https://` or `git@`). `.git` suffix optional. |
| `ref` | No | Branch or tag |
| `sha` | No | Full 40-char SHA |

---

### Git subdirectory (`source: "git-subdir"`)

Sparse-clones only the specified subdirectory. Ideal for monorepos.

```json
{
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4..."
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | Git URL, `owner/repo` shorthand, or SSH URL |
| `path` | Yes | Subdirectory path within the repo |
| `ref` | No | Branch or tag |
| `sha` | No | Full 40-char SHA |

---

### npm (`source: "npm"`)

```json
{
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `package` | Yes | Package name or scoped package (`@org/name`) |
| `version` | No | Version or range (`2.1.0`, `^2.0.0`, `~1.5.0`) |
| `registry` | No | Custom npm registry URL |

---

## Version resolution order

Claude Code resolves plugin version from the **first** of these that is set:

1. `version` in the plugin's `plugin.json`
2. `version` in the marketplace plugin entry
3. Git commit SHA of the plugin's source

Avoid setting `version` in both places — `plugin.json` always wins silently.

---

## Validation errors reference

| Error | Cause |
|-------|-------|
| `File not found: .claude-plugin/marketplace.json` | Missing manifest file |
| `Invalid JSON syntax` | Malformed JSON |
| `Duplicate plugin name "x"` | Two plugin entries share a name |
| `plugins[0].source: Path contains ".."` | Relative path escapes marketplace root |
| `YAML frontmatter failed to parse` | Invalid YAML in a skill/agent/command file |
| `Invalid JSON syntax` (hooks.json) | Malformed hooks file — blocks entire plugin |

**Warnings (non-blocking):**
- `Marketplace has no plugins defined`
- `No marketplace description provided`
- `Plugin name "x" is not kebab-case` — blocked by Claude.ai marketplace sync
