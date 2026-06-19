#!/usr/bin/env python3
"""Validate .claude-plugin/marketplace.json against this catalog's house conventions.

These conventions are a deliberately strict subset of what the official Claude Code
marketplace schema allows (for example, we require a `$schema` identifier and standardize
on HTTPS `url` sources), and they're documented in README.md ("House conventions") so the
catalog and its docs can't silently drift apart. Standard library only — no third-party
dependencies, so CI needs no install step and it runs anywhere.

Exits non-zero on any violation, so a broken catalog can't merge or ship.

    python3 scripts/validate-marketplace.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
README = ROOT / "README.md"
# House convention: HTTPS github.com `.git` URLs (the official schema is broader).
GITHUB_GIT_URL = re.compile(r"^https://github\.com/[^/]+/[^/]+\.git$")


def fail(errors: list[str]) -> NoReturn:
    print(f"✗ {MANIFEST.name} is INVALID:\n")
    for err in errors:
        print(f"  • {err}")
    sys.exit(1)


def main() -> None:
    if not MANIFEST.exists():
        fail([f"manifest not found at {MANIFEST}"])

    try:
        data = json.loads(MANIFEST.read_text())
    except json.JSONDecodeError as exc:
        fail([f"not valid JSON: {exc}"])

    if not isinstance(data, dict):
        fail(["top level must be a JSON object"])

    errors: list[str] = []

    # Top-level contract.
    if "$schema" not in data:
        errors.append("missing top-level `$schema`")
    if not data.get("name"):
        errors.append("missing top-level `name`")
    if not data.get("description"):
        errors.append("missing top-level `description`")
    owner = data.get("owner")
    if not isinstance(owner, dict) or not owner.get("name"):
        errors.append("`owner` must be an object with a `name`")

    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail(errors + ["`plugins` must be a non-empty array"])

    # Per-plugin contract.
    seen: set[str] = set()
    for i, plugin in enumerate(plugins):
        where = f"plugins[{i}]"
        name = plugin.get("name")
        if not name:
            errors.append(f"{where}: missing `name`")
        else:
            where = f"plugin '{name}'"
            if name in seen:
                errors.append(f"{where}: duplicate plugin name")
            seen.add(name)
        if not plugin.get("description"):
            errors.append(f"{where}: missing `description`")

        # House convention: standardize on HTTPS github.com `.git` `url` sources.
        # The official schema also allows `github`, `git-subdir`, and `npm`.
        source = plugin.get("source")
        if not isinstance(source, dict):
            errors.append(f"{where}: missing `source` object")
            continue
        if source.get("source") != "url":
            errors.append(f'{where}: source.source must be "url"')
        url = source.get("url", "")
        if not GITHUB_GIT_URL.match(url):
            errors.append(f"{where}: source.url must be an HTTPS github.com .git URL (got {url!r})")

    # House convention: the README "plugins" badge must match the catalog count.
    if README.exists():
        match = re.search(r"badge/plugins-(\d+)-", README.read_text())
        if match and int(match.group(1)) != len(plugins):
            errors.append(
                f"README plugins badge says {match.group(1)} but the catalog has "
                f"{len(plugins)} (update the badge in README.md)"
            )

    if errors:
        fail(errors)

    print(f"✓ {MANIFEST.name} is valid — {len(plugins)} plugin(s): {', '.join(sorted(seen))}")


if __name__ == "__main__":
    main()
