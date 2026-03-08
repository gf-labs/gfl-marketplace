# CLAUDE.md

## What this is

`gfl-marketplace` is a standalone Claude Code plugin marketplace for Greenfield Labs.
It is a **pure manifest** — no plugin code lives here. It catalogs two plugins:

- `ramp` — adaptive learning mode, knowledge graphs, spaced repetition
- `tools` — personal global toolbox (audit, cleanup, doctor, history, etc.)

Plugin sources are GitHub HTTPS URL references. On `/plugin install`, the plugin system
clones those repos into its local cache.

## How local development works

**Marketplace changes are live.** This repo is registered in `~/.claude/settings.json` as
a local `directory` source, so Claude Code reads `marketplace.json` from disk on every
session. No push needed for manifest changes to take effect.

**Plugin code changes use `--plugin-dir`.** For active development of ramp or tools, bypass
the marketplace entirely and load the plugin live from its local repo:
```bash
claude --plugin-dir ~/Repos/gfl/ramp           # develop ramp live
claude --plugin-dir ~/Repos/gfl/claude-toolbox  # develop tools live
```
No install, no cache rebuild, no push. Changes are live immediately.

When using the installed (cached) version, Claude Code caches by plugin version. To pick up
code changes from GitHub:
1. Bump version in the plugin's `.claude-plugin/plugin.json`
2. Push to GitHub
3. Reinstall: `/plugin install ramp@gfl-marketplace`

`/reload-plugins` reloads active plugins but only picks up minor in-session changes — it won't
pull new code from GitHub. For most plugin changes, prefer `--plugin-dir` during development.

## Settings.json registration

```json
"extraKnownMarketplaces": {
  "gfl-marketplace": {
    "source": {
      "source": "github",
      "repo": "gf-labs/gfl-marketplace"
    }
  }
}
```

No local clone needed. Claude fetches the catalog from GitHub. Push changes to `marketplace.json`
before expecting them to take effect.

## Adding a plugin

1. Plugin repo must have `.claude-plugin/plugin.json`
2. Push it to GitHub
3. Add entry to `.claude-plugin/marketplace.json` with its HTTPS Git URL
4. `/plugin install plugin-name@gfl-marketplace`

## Key files

| File | Role |
|------|------|
| `.claude-plugin/marketplace.json` | Plugin catalog — the only file that matters |
| `README.md` | Setup and local dev reference |

## Schema notes (from anthropics/claude-plugins-official)

- `$schema` field is required
- `description` lives at top level (not nested under `metadata`)
- URL sources use HTTPS `.git` URLs (not SSH)
- Optional `sha` field available for pinning to a specific commit
