#!/usr/bin/env python3
"""Validate .claude-plugin/marketplace.json against the manifest rules.

The rules enforced here are the ones documented in README.md ("Manifest rules"),
so the catalog and its docs can never silently drift apart. Standard library only —
no third-party dependencies, so CI needs no install step and it runs anywhere.

Exits non-zero on any violation, so a broken catalog can't merge or ship.

    python3 scripts/validate-marketplace.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
HTTPS_GIT_URL = re.compile(r"^https://.+\.git$")


def fail(errors: list[str]) -> None:
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

    errors: list[str] = []

    # Top-level contract.
    if "$schema" not in data:
        errors.append("missing required top-level `$schema`")
    if not data.get("name"):
        errors.append("missing top-level `name`")
    if not data.get("description"):
        errors.append("missing top-level `description` (top level, not nested under metadata)")
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

        source = plugin.get("source")
        if not isinstance(source, dict):
            errors.append(f"{where}: missing `source` object")
            continue
        if source.get("source") != "url":
            errors.append(f'{where}: source.source must be "url"')
        url = source.get("url", "")
        if not HTTPS_GIT_URL.match(url):
            errors.append(f"{where}: source.url must be an HTTPS .git URL (got {url!r})")

    if errors:
        fail(errors)

    print(f"✓ {MANIFEST.name} is valid — {len(plugins)} plugin(s): {', '.join(sorted(seen))}")


if __name__ == "__main__":
    main()
