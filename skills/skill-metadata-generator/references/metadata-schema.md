# Skill Metadata JSON Schema

A reference for the fields that make up a skill's `metadata.json`. All fields marked **required** must be present. Optional fields should be included when the information is available or derivable from the skill.

---

## Full schema

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "One-sentence explanation of what this skill does and when to use it.",
  "license": "MIT",
  "author": "Author Name or Org",
  "repository": "https://github.com/org/repo",
  "languages": ["en"],
  "compatibility": {
    "minCliVersion": "0.1.0",
    "agents": ["claude-code", "codex-cli", "cursor", "windsurf", "generic"]
  },
  "entryPoint": "SKILL.md",
  "references": [
    "references/guide.md"
  ],
  "triggers": [
    "keyword or phrase that should invoke this skill",
    "another trigger phrase"
  ],
  "tags": [
    "kebab-case-tag"
  ],
  "usage": {
    "prompt": "One or two sentences of model-facing instruction summarising how to use this skill.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "input_field": {
          "type": "string",
          "description": "Description of the expected input"
        }
      },
      "required": ["input_field"]
    },
    "outputSchema": {
      "type": "object",
      "properties": {
        "output_field": {
          "type": "string",
          "description": "Description of the produced output"
        }
      }
    }
  },
  "dependencies": {
    "tools": ["playwright", "bash"],
    "packages": [],
    "external": []
  },
  "bundled": {
    "scripts": [],
    "assets": [],
    "templates": []
  }
}
```

---

## Field reference

### Required

| Field | Type | Rules |
|-------|------|-------|
| `name` | string | Lowercase, hyphens only, max 64 chars. Must match the skill directory name. |
| `version` | string | Semantic version (`MAJOR.MINOR.PATCH`). Default `"1.0.0"` for new skills. |
| `description` | string | Mirror of the `description` in SKILL.md frontmatter. |
| `entryPoint` | string | Always `"SKILL.md"`. |
| `triggers` | array of strings | 5–15 phrases a user would type that should invoke this skill. Derive from the SKILL.md description and body. |

### Recommended

| Field | Type | Notes |
|-------|------|-------|
| `license` | string | SPDX identifier (e.g. `"MIT"`). Use `"UNLICENSED"` if unknown. |
| `author` | string | Person or org name. |
| `repository` | string | URL to source repo. Omit if private or unknown. |
| `languages` | array | ISO 639-1 codes. Default `["en"]`. |
| `tags` | array of strings | Kebab-case. More granular than triggers — used for filtering and discovery. |
| `references` | array of strings | Relative paths to every file in `references/`. Derive by listing the directory. |
| `bundled` | object | Lists `scripts`, `assets`, and `templates` as relative path arrays. |

### Optional

| Field | Type | Notes |
|-------|------|-------|
| `compatibility` | object | `minCliVersion` (semver string) and `agents` (array of agent identifiers). |
| `usage.prompt` | string | Model-facing instruction for invoking the skill. |
| `usage.inputSchema` | JSON Schema object | Describes expected inputs. |
| `usage.outputSchema` | JSON Schema object | Describes produced outputs. |
| `dependencies.tools` | array | Named tools the skill requires (e.g. `"playwright"`, `"bash"`). |
| `dependencies.packages` | array | npm/pip/etc packages. |
| `dependencies.external` | array | External APIs or services. |

---

## Derivation rules

When generating metadata from a skill directory, apply these rules:

1. **`name`** — read from SKILL.md `name` frontmatter field.
2. **`description`** — read from SKILL.md `description` frontmatter field.
3. **`version`** — check for existing `metadata.json`; if present, preserve version. If absent, use `"1.0.0"`.
4. **`entryPoint`** — always `"SKILL.md"`.
5. **`references`** — list all files in `references/` recursively. Use relative paths from the skill root.
6. **`bundled.scripts`** — list all files in `scripts/` recursively.
7. **`bundled.assets`** — list all files in `assets/` recursively.
8. **`bundled.templates`** — list all files in `templates/` recursively.
9. **`triggers`** — extract from the SKILL.md description and body: action verbs, domain nouns, user-facing phrases, and any explicit "use when" language.
10. **`tags`** — distil triggers down to 3–8 high-signal kebab-case concepts.
11. **`usage.prompt`** — summarise the SKILL.md "How you work" or equivalent section into 1–2 model-facing sentences.
12. **`usage.inputSchema`** — infer from workflow step 1 (what the skill accepts).
13. **`usage.outputSchema`** — infer from the Output section (what the skill produces).
14. **`dependencies.tools`** — scan the SKILL.md body for named tools (playwright, bash, web_fetch, etc.).
15. **`license` / `author` / `repository`** — read from existing `metadata.json` if present; otherwise leave as `null` or omit.
