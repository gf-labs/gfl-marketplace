# Contributing to gfl-marketplace

This repo is a rolling registry — a pure catalog, no plugin code. The walk-through for
adding a plugin (entry shape, house conventions) lives in the README's
[Contributing a plugin](README.md#contributing-a-plugin) section; this file is the formal
rules around it.

## PR rules

- All changes land via **PR to `main`** — no direct pushes (branch protection: PR
  required, the `validate` check, no force-pushes).
- `python3 scripts/validate-marketplace.py` must pass — CI runs it on every change to
  the manifest, the validator, the workflow, or the README.
- The README's `plugins-N` badge must match the catalog count — the validator fails the
  PR otherwise, so update both together.
- Commit style: `type(scope): imperative summary` (≤ 50 chars).

No CHANGELOG and no version tags here — the registry rolls: installs always clone each
plugin's `main` HEAD, so the catalog itself is never "released."

Licensed MIT — contributions land under the same license.
