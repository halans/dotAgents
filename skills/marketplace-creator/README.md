# marketplace-creator

> Scaffold and validate a Claude Code plugin marketplace manifest in seconds.

## How to install

```bash
npx skills add halans/dotAgents --skill marketplace-creator
```

## What it does

Generates a valid `.claude-plugin/marketplace.json` — the Anthropic-standard manifest for distributing Claude Code plugins to teams, organizations, or the public.

Given a marketplace name, owner, and a list of plugins (with their GitHub repos, relative paths, monorepo subdirectories, or npm packages), this skill writes a correctly structured manifest, validates it against the spec, and reports any issues.

It also handles **updating** existing manifests without overwriting fields you didn't ask to change.

## When to use it

- Creating a new Claude Code plugin marketplace for your team or organization
- Adding plugins to an existing `.claude-plugin/marketplace.json`
- Migrating plugins from one source type to another (e.g., relative path → GitHub)
- Validating a marketplace manifest before publishing
- Asking about plugin source types, reserved names, or version pinning

## Usage examples

```
Create a marketplace.json for our internal Claude plugins — we have three plugins in subdirectories under ./plugins/
```

```
Add a new plugin to our marketplace that comes from npm package @acme/doc-gen at version ^3.0.0
```

```
Is "claude-code-plugins" a valid marketplace name?
```

```
Update our marketplace.json to pin the security-scanner plugin to tag v2.1.0
```

## Output

- **File created**: `.claude-plugin/marketplace.json`
- **Summary**: marketplace name, owner, plugin count, source types used
- **Warnings**: reserved name conflicts, empty plugin lists, relative path + URL distribution mismatches

## Reference links

- [Anthropic Claude Code plugin marketplace docs](https://code.claude.com/docs/en/plugin-marketplaces)
