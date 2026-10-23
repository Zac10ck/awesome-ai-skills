#!/usr/bin/env python3
"""Validate the curated resource catalog without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TYPES = {
    "agent-skill", "skill-collection", "mcp-server", "mcp-registry", "mcp-sdk",
    "ai-tool", "framework", "guide", "tutorial", "awesome-list", "documentation",
    "open-source-app", "library", "platform",
}
ALLOWED_SOURCES = {"official", "community", "standards-body"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    resources = json.loads((ROOT / "data/resources.json").read_text())
    categories = json.loads((ROOT / "data/categories.json").read_text())
    category_ids = {item["id"] for item in categories}
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    errors = 0

    if not isinstance(resources, list):
        fail("resources.json must contain an array")
        return 1

    required = {"id", "name", "type", "category", "description", "url", "source", "compatibility", "tags", "verified_at", "maintenance"}
    for index, item in enumerate(resources):
        label = item.get("id", f"item #{index + 1}")
        missing = required - item.keys()
        if missing:
            fail(f"{label}: missing {', '.join(sorted(missing))}")
            errors += 1
            continue
        if not ID_RE.fullmatch(item["id"]):
            fail(f"{label}: id must be lowercase kebab-case")
            errors += 1
        if item["id"] in seen_ids:
            fail(f"{label}: duplicate id")
            errors += 1
        seen_ids.add(item["id"])
        normalized_url = item["url"].rstrip("/").lower()
        if normalized_url in seen_urls:
            fail(f"{label}: duplicate URL")
            errors += 1
        seen_urls.add(normalized_url)
        parsed = urlparse(item["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"{label}: URL must be an absolute HTTPS URL")
            errors += 1
        if item["category"] not in category_ids:
            fail(f"{label}: unknown category {item['category']}")
            errors += 1
        if item["type"] not in ALLOWED_TYPES:
            fail(f"{label}: unsupported type {item['type']}")
            errors += 1
        if item["source"] not in ALLOWED_SOURCES:
            fail(f"{label}: unsupported source {item['source']}")
            errors += 1
        if not isinstance(item["description"], str) or len(item["description"].strip()) < 25:
            fail(f"{label}: description must contain at least 25 characters")
            errors += 1
        if not isinstance(item["compatibility"], list) or not isinstance(item["tags"], list):
            fail(f"{label}: compatibility and tags must be arrays")
            errors += 1

    if errors:
        print(f"Validation failed with {errors} error(s).", file=sys.stderr)
        return 1
    print(f"Validated {len(resources)} resources across {len(category_ids)} categories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
