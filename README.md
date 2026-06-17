# gfl-marketplace

The Greenfield Labs Claude Code plugin marketplace.

## Plugins

- `ramp@gfl-marketplace` — adaptive learning mode, knowledge graphs, spaced repetition
- `tools@gfl-marketplace` — global toolbox (audit, cleanup, doctor, history, etc.)

## Setup

Register in `~/.claude/settings.json`:
```json
"extraKnownMarketplaces": {
  "gfl-marketplace": {
    "source": { "source": "github", "repo": "gf-labs/gfl-marketplace" }
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
claude --plugin-dir path/to/ramp            # develop ramp live
claude --plugin-dir path/to/claude-toolbox  # develop tools live
```

To pick up changes in the installed (cached) version: bump version in `.claude-plugin/plugin.json`,
push to GitHub, then reinstall with `/plugin install ramp@gfl-marketplace`.

Note: `/reload-plugins` (hyphen) reloads active plugins for minor in-session changes but does
not pull new code from GitHub.
