# gfl-marketplace

Personal Claude Code plugin marketplace for Greenfield Labs.

## Plugins

- `ramp@gfl-marketplace` — adaptive learning mode, knowledge graphs, spaced repetition
- `tools@gfl-marketplace` — personal global toolbox (audit, cleanup, doctor, history, etc.)

---

## Setup

### Step 1 — Register the marketplace

Add to `~/.claude/settings.json`:

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

> **Note:** This repo is private. GitHub auth must be configured for your Claude Code
> installation (standard for private plugin repos).

### Step 2 — Install plugins

In any Claude Code session:

```
/plugin install ramp@gfl-marketplace
/plugin install tools@gfl-marketplace
```

---

## How it works

The marketplace is a pure manifest — no plugin code lives here. When you run
`/plugin install`, Claude Code:

1. Reads `marketplace.json` from this repo
2. Finds the plugin's GitHub URL source
3. Clones the plugin repo into `~/.claude/plugins/cache/`

---

## Local development (plugin authors)

To develop a plugin locally with changes reflected immediately, bypass the marketplace
and load the plugin directly:

```bash
claude --plugin-dir ~/Repos/gfl/ramp           # develop ramp live
claude --plugin-dir ~/Repos/gfl/claude-toolbox  # develop tools live
```

Changes are picked up on session restart. No reinstall or version bump required.

To test the installed (cached) version, reinstall after pushing changes:

```
/plugin uninstall ramp@gfl-marketplace
/plugin install ramp@gfl-marketplace
```

---

## Developer registration (directory source)

On your dev machine, use a local `directory` source so manifest changes are live immediately:

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
