# mcpb-creator

A guide for creating production-ready Model Context Protocol Bundles (MCPB) — distributable MCP servers with proper manifest structure, tool definitions, and security measures.

## How to install

```
npx skills add halans/dotAgents --skill mcpb-creator
```

## What it does

- Guides you through defining tools, inputs, outputs, and dependencies
- Scaffolds the bundle structure via `init_mcpb.py` (manifest, server, README, package.json)
- Provides patterns for tool handlers, input validation, path sanitisation, and timeouts
- Validates the finished bundle with `validate_mcpb.py`

## When to use it

Use this skill when you want to build an MCP server as a self-contained, distributable bundle that AI agents can discover and invoke.

## Usage

```
Create an MCP bundle that exposes file read and search tools
```

```
Build an MCPB that wraps the GitHub API
```

## Output

A validated bundle directory containing `manifest.json`, `server/index.js`, `package.json`, and `README.md`, ready to run via stdio JSON-RPC.

## Reference

- [`SKILL.md`](SKILL.md) — 8-step creation workflow and best practices
- [`references/mcpb-overview.md`](references/mcpb-overview.md) — architecture and integration patterns
- [`references/manifest-spec.md`](references/manifest-spec.md) — complete manifest.json field reference
- [`references/implementation-guide.md`](references/implementation-guide.md) — security, testing, and common patterns
- [`scripts/init_mcpb.py`](scripts/init_mcpb.py) — scaffolds a new bundle
- [`scripts/validate_mcpb.py`](scripts/validate_mcpb.py) — validates manifest structure
- [`assets/hello-world-node-template/`](assets/hello-world-node-template/) — minimal working example
