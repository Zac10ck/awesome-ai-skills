#!/usr/bin/env python3
"""Generate catalog sections in README.md from data/resources.json."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- CATALOG:START -->"
END = "<!-- CATALOG:END -->"


def main() -> None:
    resources = json.loads((ROOT / "data/resources.json").read_text())
    categories = json.loads((ROOT / "data/categories.json").read_text())
    grouped: dict[str, list[dict]] = defaultdict(list)
    for resource in resources:
        grouped[resource["category"]].append(resource)

    lines = [START, "", "## Explore the directory", ""]
    visible = [category for category in categories if grouped[category["id"]]]
    lines.extend(["| Category | Resources |", "|---|---:|"])
    lines.extend(f"| [{category['name']}](#{category['id']}) | {len(grouped[category['id']])} |" for category in visible)
    lines.append("")
    for category in visible:
        lines.extend([f"<a id=\"{category['id']}\"></a>", "", f"### {category['name']}", "", category["description"], "", "| Name | Type | Description | Compatibility | Link |", "|---|---|---|---|---|"])
        for item in sorted(grouped[category["id"]], key=lambda value: value["name"].lower()):
            compatibility = ", ".join(item["compatibility"]) if item["compatibility"] else "—"
            lines.append(f"| {item['name']} | {item['type']} | {item['description']} | {compatibility} | [Visit]({item['url']}) |")
        lines.extend(["", "[Back to directory ↑](#explore-the-directory)", ""])
    lines.append(END)

    readme_path = ROOT / "README.md"
    text = readme_path.read_text()
    before, remainder = text.split(START, 1)
    _, after = remainder.split(END, 1)
    readme_path.write_text(before + "\n".join(lines) + after)
    print(f"Generated README with {len(resources)} resources.")


if __name__ == "__main__":
    main()
