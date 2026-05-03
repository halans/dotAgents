# text-rewriter

Rewrites text to remove AI-generated linguistic patterns, puffery, and formulaic language — without changing the original meaning.

## How to install

```
npx skills add halans/dotAgents --skill text-rewriter
```

## What it does

- Strips overused AI phrases, hedging language, and filler constructs
- Applies the rule set in `references/ai-writing-guide.md`
- Accepts pasted text or a file path as input
- Saves the rewritten output alongside the original (e.g. `report.md` → `report-rewritten.md`)

## When to use it

Use this skill when text sounds robotic, overwritten, or templated — whether it came from an AI or a human imitating one.

## Usage

Paste text directly or provide a file path:

```
Rewrite this: "It's worth noting that leveraging this approach can unlock significant value..."
```

```
Rewrite the file at docs/proposal.md
```

## Output

A saved file containing only the rewritten text. No metadata, annotations, or diff markers.

After saving, a brief summary lists patterns removed and notable changes made.

## Reference

- [`SKILL.md`](SKILL.md) — workflow and rewriting rules
- [`references/ai-writing-guide.md`](references/ai-writing-guide.md) — full list of forbidden phrases and replacement strategies
