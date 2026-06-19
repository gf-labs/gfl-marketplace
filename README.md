<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/lockup-dark.png">
    <img src="docs/assets/lockup.png" alt="Greenfield Labs" width="420">
  </picture>
</p>

<h1 align="center">gfl-marketplace</h1>

<p align="center"><em>The Greenfield Labs plugin marketplace for Claude Code — one place to install, update, and share the tools that make a team productive.</em></p>

<p align="center">
  <a href="https://github.com/gf-labs/gfl-marketplace/actions/workflows/validate.yml"><img src="https://github.com/gf-labs/gfl-marketplace/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-21A64A?style=flat-square" alt="license"></a>
  <img src="https://img.shields.io/badge/Claude_Code-marketplace-d97757?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code marketplace">
  <img src="https://img.shields.io/badge/plugins-2-6366f1?style=flat-square" alt="plugins">
</p>

<p align="center">Built by <a href="https://github.com/berniegreen">Bernie Green</a> · <a href="https://github.com/gf-labs">Greenfield Labs</a></p>

---

## Why this exists

Claude Code's power comes from its extension points — slash commands, hooks, subagents, MCP servers. But a clever command sitting in one developer's `~/.claude/` only becomes a *team* capability when there's a way to distribute it: install it the same way everywhere, update it in one step, and trust that everyone is running the same version.

That distribution channel is a **marketplace**. `gfl-marketplace` is the Greenfield Labs catalog — a single source you register once, after which every GFL plugin is one command away.

### What a Claude Code marketplace actually is

- **What** — a small manifest (`marketplace.json`) that lists plugins and where to fetch each one. No plugin code lives here; it's a pure catalog.
- **Why** — so a whole team installs, pins, and updates plugins consistently instead of copying files by hand.
- **How** — you register the marketplace once, then `/plugin install <name>@gfl-marketplace`. On install, Claude Code clones each plugin's source repo into its local cache.

---

## The plugins

| Plugin | Install | What it does |
|--------|---------|--------------|
| **[`ramp`](https://github.com/gf-labs/ramp)** | `/plugin install ramp@gfl-marketplace` | Adaptive, repo-grounded learning mode — knowledge graphs, spaced repetition, and a passive skill observer. Built for onboarding engineers to Claude Code and your codebase. |
| **[`tools`](https://github.com/gf-labs/claude-toolbox)** | `/plugin install tools@gfl-marketplace` | Session lifecycle management — orient, checkpoint, close out, and archive. Keeps context clean and the thread unbroken across sessions. (Repo: `claude-toolbox`.) |

---

## Install

Register the marketplace once, then install whatever you need:

```
/plugin marketplace add gf-labs/gfl-marketplace
/plugin install ramp@gfl-marketplace
/plugin install tools@gfl-marketplace
```

Prefer a declarative, version-controlled setup? Register it in `~/.claude/settings.json` instead:

```json
"extraKnownMarketplaces": {
  "gfl-marketplace": {
    "source": { "source": "github", "repo": "gf-labs/gfl-marketplace" }
  }
}
```

No local clone needed — Claude Code fetches the catalog from GitHub. Update a plugin any time with `/plugin update <name>@gfl-marketplace`.

> Some plugins have their own prerequisites — `tools`, for example, needs a `CLAUDE_TOOLBOX_ROOT` environment variable. Each plugin's own README covers its specifics.

---

## Contributing a plugin

Adding a plugin to the catalog is a four-step change to one file:

1. Make sure the plugin repo has a valid `.claude-plugin/plugin.json`.
2. Push it to GitHub.
3. Add an entry to [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) with the repo's HTTPS `.git` URL.
4. `/plugin install your-plugin@gfl-marketplace`.

A catalog entry looks like this:

```json
{
  "name": "your-plugin",
  "description": "One line on what it does",
  "source": { "source": "url", "url": "https://github.com/gf-labs/your-plugin.git" },
  "category": "productivity",
  "author": { "name": "Your Name" }
}
```

**Manifest rules** (from the official `claude-plugins-official` schema):

- `$schema` is required.
- `description` lives at the top level — not nested under `metadata`.
- URL sources use HTTPS `.git` URLs, not SSH.
- An optional `sha` field pins a plugin to a specific commit.

---

## Local development

**Catalog changes are live.** When this repo is registered as a local `directory` source, Claude Code reads `marketplace.json` from disk every session — no push needed for manifest edits to take effect. (When registered as a `github` source, push to GitHub first.)

**Plugin *code* changes use `--plugin-dir`.** To develop a plugin live, bypass the marketplace and load it straight from its repo:

```bash
claude --plugin-dir path/to/ramp            # develop ramp live
claude --plugin-dir path/to/claude-toolbox  # develop tools live
```

To pick up code changes through the *installed* (cached) path, bump the plugin's version in its `plugin.json`, push, and reinstall. `/reload-plugins` reloads active plugins for minor in-session edits but won't pull new code from GitHub — for real plugin work, prefer `--plugin-dir`.

---

## About Greenfield Labs

Greenfield Labs builds developer tooling for Claude Code with a single throughline: **tools should make a team measurably more capable, not just busier.** Both plugins in this catalog are designed to be read as much as run — each one is a worked example of a different slice of Claude Code's extension model, from slash commands and hooks to subagents and MCP servers.

---

## Acknowledgements

Built on [Claude Code](https://claude.com/claude-code) and the [Claude Code plugin system](https://code.claude.com/docs/en/plugins) by Anthropic. The marketplace manifest follows the schema published in [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official).

---

## License

[MIT](./LICENSE) © 2026 Greenfield Labs
