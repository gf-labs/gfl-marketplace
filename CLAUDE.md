# CLAUDE.md

## What this is

`gfl-marketplace` is a standalone Claude Code plugin marketplace for Greenfield Labs.
It is a **pure manifest** — no plugin code lives here. It catalogs two plugins:

- `ramp` — adaptive learning mode, knowledge graphs, spaced repetition
- `tools` — session lifecycle management (orient, checkpoint, archive, health checks)

Plugin sources are GitHub HTTPS URL references. On `/plugin install`, the plugin system
clones those repos into its local cache.

## How local development works

**Two ways to register this marketplace** (the `github` source is canonical — it's what end
users get; see "Settings.json registration" below):

- **`github` source** — Claude Code fetches `marketplace.json` from GitHub. Push manifest
  changes before they take effect. This is how the catalog is meant to be consumed.
- **`directory` source** (optional, local dev) — point Claude Code at this repo on disk and it
  reads `marketplace.json` from disk every session, so manifest edits are live with no push.

**Plugin code changes use `--plugin-dir`.** For active development of ramp or tools, bypass
the marketplace entirely and load the plugin live from its local repo:
```bash
claude --plugin-dir path/to/ramp            # develop ramp live
claude --plugin-dir path/to/claude-toolbox  # develop tools live
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
| `.claude-plugin/marketplace.json` | Plugin catalog — the manifest everything else exists to protect |
| `scripts/validate-marketplace.py` | Validates the manifest against the catalog's house conventions |
| `.github/workflows/validate.yml` | CI gate — runs the validator on every change |
| `README.md` | Public front door — what/why/how, install, troubleshooting, contributing |

## Schema notes

The manifest follows the official schema (`anthropics/claude-plugins-official`) with a few
deliberately strict **house conventions** the CI validator enforces (see README "House conventions"):

- **`$schema`** — optional in the official schema (Claude Code ignores it at load time); we
  require it for editor autocomplete. The published URL is an *identifier*, not a fetchable
  document — it 404s by design, and is the exact value `anthropics/claude-plugins-official` uses.
- **`description`** — kept top-level; the schema also accepts it under `metadata`.
- **Sources** — we standardize on `url` (HTTPS `github.com`, `.git` suffix). The schema is
  broader: it also allows `github`/`git-subdir`/`npm`, and `url` accepts SSH and bare URLs.
- **`sha`** — optional; pins a plugin to an exact commit. We track each plugin's default branch.
