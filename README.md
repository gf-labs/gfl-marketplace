# gfl-marketplace

Personal Claude Code plugin marketplace for Greenfield Labs.

## Plugins

- `ramp@gfl-marketplace` — adaptive learning mode, knowledge graphs, spaced repetition
- `tools@gfl-marketplace` — personal global toolbox (audit, cleanup, doctor, history, etc.)

## Setup

Register in `~/.claude/settings.json`:
```json
"extraKnownMarketplaces": {
  "gfl-marketplace": {
    "source": { "source": "directory", "path": "/Users/berniegreen/Repos/gfl/gfl-marketplace" }
  }
}
```

Then in any Claude Code session:
```
/plugin install ramp@gfl-marketplace
/plugin install tools@gfl-marketplace
```

## Local development

This marketplace is a local directory source — `marketplace.json` is read directly from disk.
Manifest changes are live immediately with no push.

For active plugin development (editing commands, hooks, or scripts in ramp or claude-toolbox),
use `--plugin-dir` to load the plugin live from its local repo, bypassing the marketplace cache:

```bash
claude --plugin-dir ~/Repos/gfl/ramp           # develop ramp live
claude --plugin-dir ~/Repos/gfl/claude-toolbox  # develop tools live
```
