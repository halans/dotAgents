---
name: changelog-generator
description: Use when the user wants to generate a changelog, release notes, what's new document, or any summary of recent changes for end users. Trigger when the user says things like "generate a changelog", "write release notes", "what changed since the last release", "create a CHANGELOG entry", "summarize recent git commits for users", "write up the changes for v1.2.0", "prepare release documentation", or anything about translating git history into user-facing communication. Also trigger if the user is preparing a GitHub release, writing a What's New page, or asking what went into a release. Use this skill whenever the conversation involves git history and communicating changes to end users.
---

# Changelog Generator

Turn raw git history into release notes that customers actually understand.

## Overview

Developers write commit messages for developers. Users need something different: clear, benefit-focused descriptions of what changed and why they should care. This skill bridges that gap by reading git commits, categorizing them by impact, and rewriting them in plain language.

## Step 1: Determine the commit range

**Default (no range specified):**
```bash
# Find the last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)

if [ -z "$LAST_TAG" ]; then
  # No tags yet — use all commits
  git log --no-merges --pretty=format:"%H%x09%s%x09%b" --date=short
else
  # Commits since last tag
  git log ${LAST_TAG}..HEAD --no-merges --pretty=format:"%H%x09%s%x09%b" --date=short
fi
```

**User-specified range:** Use whatever the user provides — tag names (`v1.2.0..v1.3.0`), branches, `--since="3 weeks ago"`, commit hashes, etc.

If there are no commits in the range, say so clearly and stop.

## Step 2: Categorize each commit

Always use `--no-merges` to skip merge commits automatically.

For each commit subject line, determine its category:

**Conventional Commits** (subject matches `type(scope): description` or `type: description`):

| Type | Category |
|------|----------|
| `feat` | New Features |
| `fix` | Bug Fixes |
| `perf` | Improvements |
| `refactor`, `style` | Improvements |
| `docs` | Improvements (only if user-visible, e.g., new guides or API docs) |
| `chore`, `ci`, `build`, `test` | Improvements (only if meaningful to users, e.g., dependency security update) |
| `feat!`, `fix!`, or body contains `BREAKING CHANGE:` | Breaking Changes |

**Free-form commits** (no conventional prefix — infer from keywords):
- "add", "added", "implement", "create", "introduce", "new", "support", "enable" → **New Features**
- "fix", "fixed", "resolve", "bug", "patch", "correct", "crash", "error", "issue", "regression" → **Bug Fixes**
- "improve", "update", "upgrade", "enhance", "speed", "faster", "refactor", "optimize", "clean", "remove deprecated" → **Improvements**
- Unclear → **Improvements** (default)

**When to skip a commit entirely:** Skip commits that clearly have zero user impact: "rename variable", "add comment to code", "fix typo in internal test name". When in doubt, include it — over-including is safer than silently dropping something that matters.

## Step 3: Rewrite for users

This is the most important step. Translate each commit message from developer-speak into language that any user understands.

**Goal:** A non-technical user reads the entry and knows what changed and how it affects them.

**Rewriting principles:**
- Lead with the user benefit, not the technical mechanism
- Use active voice, past tense: "Added X", "Fixed Y", "Improved Z"
- Replace internal identifiers (class names, function names, file paths, column names) with feature descriptions
- Remove implementation jargon: "null pointer exception" → "crash", "race condition" → "intermittent issue", "migration" → skip or describe the user-visible effect
- If a change has no elegant user description, describe the effect: perf improvement → "loads faster", dependency update → "improved reliability"

**Transformation examples:**

| Raw commit | User-facing note |
|-----------|-----------------|
| `fix: resolve NPE in UserService.getUser() when userId null` | Fixed a crash when viewing certain user profiles |
| `feat: add CSV export to DataTable component` | You can now export any table to CSV with one click |
| `perf: lazy load feed images using IntersectionObserver` | The feed loads significantly faster, especially on slower connections |
| `chore(deps): bump postgres driver to 14.2` | Updated database driver for improved reliability and security |
| `fix: race condition in auth token refresh` | Fixed an issue where you could be unexpectedly signed out |
| `Added dark mode support to settings page` | Added dark mode — toggle it in Settings |
| `Removed legacy onboarding flow` | Simplified the onboarding experience |
| `Upgrade Node minimum to 18` | Dropped support for Node.js versions below 18 |

**Consolidate related commits:** When multiple commits clearly relate to the same user-facing change (e.g., "feat: add dark mode", "fix: dark mode icon color", "perf: dark mode transition speed"), merge them into a single clean entry: "Added dark mode with smooth transitions throughout the app".

## Step 4: Format the output

Use this structure:

```markdown
## What's New in [version or date]

### Breaking Changes
- [What broke, and what users need to do to adapt]

### New Features
- [User-facing description]

### Bug Fixes
- [User-facing description]

### Improvements
- [User-facing description]
```

**Formatting rules:**
- Put **Breaking Changes** first — users need to see these before anything else
- Omit any section that has no entries (don't include an empty "### Improvements" heading)
- Each bullet is 1–2 sentences maximum; longer is rarely better
- No numbering — bullets only

**Determine the version header:**
- If the user is cutting a named release, use that tag (e.g., `v1.3.0`)
- If noting unreleased/untagged changes, use `Unreleased` or today's date
- If you can infer the right semantic version bump from the commit types (patch for fixes only, minor for new features, major for breaking changes), suggest it

**Example output:**
```markdown
## What's New in v2.1.0

### New Features
- You can now export any report to PDF directly from the toolbar
- Added two-factor authentication support via authenticator apps

### Bug Fixes
- Fixed a crash when opening settings on accounts created before 2023
- Resolved an issue where email notifications were delayed by up to 30 minutes

### Improvements
- The dashboard now loads noticeably faster on slower connections
- Updated dependencies for improved security
```
