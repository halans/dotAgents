# skill-metadata-generator

Generates a structured `metadata.json` file for an existing skill directory, making it machine-readable for agent discovery, compatibility declarations, and capability descriptions.

## How to install

```
npx skills add halans/dotAgents --skill skill-metadata-generator
```

## What it does

- Reads a skill's `SKILL.md` frontmatter and body to derive all metadata fields
- Lists `references/`, `scripts/`, `assets/`, and `templates/` directories automatically
- Extracts triggers from the description and workflow, and distils tags from those triggers
- Infers input/output schemas from the skill's workflow and output sections
- Preserves existing `metadata.json` fields (version, license, author, repository) on update

## When to use it

Use this skill when a skill directory is missing `metadata.json`, or when an existing one needs regenerating after the skill has been updated.

## Usage

```
Generate metadata for skills/text-rewriter
```

```
Create a metadata.json for my skill at ~/projects/my-skill
```

```
Update the metadata for this skill
```

## Output

A `metadata.json` written to the skill root. After writing, a summary shows which fields were populated and which were left `null` (e.g. `license`, `author`, `repository`) for the user to fill in.

## Reference

- [`SKILL.md`](SKILL.md) — derivation workflow and rules
- [`references/metadata-schema.md`](references/metadata-schema.md) — full field reference with required/recommended/optional tiers and derivation rules
