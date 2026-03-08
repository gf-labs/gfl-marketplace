# CLAUDE.md

## What this is

`gfl-marketplace` is a standalone Claude Code plugin marketplace for Greenfield Labs.
It is a **pure manifest** — no plugin code lives here. It catalogs two plugins:

- `ramp` — adaptive learning mode, knowledge graphs, spaced repetition
- `tools` — personal global toolbox (audit, cleanup, doctor, history, etc.)

Plugin sources are GitHub HTTPS URL references. On `/plugin install`, Claude Code clones
those repos into its local cache.

---

## Architecture: two layers

```
gfl-marketplace (manifest)          ramp / claude-toolbox (plugin code)
─────────────────────────           ──────────────────────────────────
.claude-plugin/marketplace.json     .claude-plugin/plugin.json
  └── "source": GitHub URL  ──────► cloned to ~/.claude/plugins/cache/
```

The marketplace and the plugins are **separate repos**. Installing a plugin fetches it from
GitHub, not from this repo.

---

## Registration in settings.json

### Your dev machine (directory source — manifest changes are live)

```json
"extraKnownMarketplaces": {
  "gfl-marketplace": {
    "source": {
      "source": "directory",
      "path": "/Users/berniegreen/Repos/gfl/gfl-marketplace"
    }
  }
}
```

`marketplace.json` is read from disk on every session. No push needed for manifest changes.

### End users (GitHub source — no local clone required)

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

Claude Code clones the marketplace repo automatically. The repo is private, so users need
GitHub auth configured (standard for private plugin repos).

---

## Installing plugins

After the marketplace is registered:

```
/plugin install ramp@gfl-marketplace
/plugin install tools@gfl-marketplace
```

This clones the plugin repo from GitHub into `~/.claude/plugins/cache/`.

---

## Development workflows

### Workflow A — Live plugin dev (recommended)

Load a plugin directly from your local repo, bypassing the marketplace and cache entirely:

```bash
claude --plugin-dir ~/Repos/gfl/ramp           # develop ramp live
claude --plugin-dir ~/Repos/gfl/claude-toolbox  # develop tools live
```

- Changes are picked up on **session restart** (no reinstall, no version bump)
- Does not affect your installed plugin cache
- Use this when actively editing commands, hooks, or scripts

### Workflow B — Test the installed version

When you want to test what an end user sees (the cached, installed version):

1. Bump version in the plugin's `.claude-plugin/plugin.json`
2. Push to GitHub
3. Force reinstall:

```
/plugin uninstall ramp@gfl-marketplace
/plugin install ramp@gfl-marketplace
```

Or clear the cache manually and reinstall:

```bash
rm -rf ~/.claude/plugins/cache
# then in a new session:
# /plugin install ramp@gfl-marketplace
```

### Workflow C — Manifest-only changes (this repo)

If you only change `marketplace.json` (add/remove a plugin, update description):

- With `directory` source (your dev machine): changes are live immediately — no action needed
- With `github` source (end users): they need to re-clone the marketplace; no documented
  live-reload for marketplace manifests — they reinstall or wait for cache expiry

---

## Key files

| File | Role |
|------|------|
| `.claude-plugin/marketplace.json` | Plugin catalog — the only file that matters |
| `CLAUDE.md` | This file — dev reference |
| `README.md` | Setup guide for end users |

---

## Adding a plugin

1. Plugin repo must have `.claude-plugin/plugin.json`
2. Push it to GitHub (public or private with auth)
3. Add entry to `.claude-plugin/marketplace.json` with its HTTPS `.git` URL
4. Commit + push this repo
5. `/plugin install plugin-name@gfl-marketplace`

---

## Schema notes

- `$schema` field is required
- `description` lives at top level (not nested under `metadata`)
- Plugin sources use `{"source": "url", "url": "https://github.com/org/repo.git"}` for GitHub
- Do not use SSH URLs (`git@github.com:...`) — HTTPS only
