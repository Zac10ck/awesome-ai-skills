# Contributing

Thank you for helping make Awesome AI Skills more useful. We value accurate descriptions, direct links, clear categorization, and evidence-backed compatibility over list size.

## What belongs here

We accept agent skills, skill collections, MCP servers and registries, AI tools, frameworks, guides, tutorials, awesome lists, and substantial open-source AI applications. A submission should be useful, publicly accessible, relevant, and documented well enough for someone to assess it safely.

We do not accept affiliate links, scraped directories, undisclosed self-promotion, duplicate resources, malicious or deceptive software, thin model wrappers, or claims that cannot be verified.

## Method 1: submit an issue

Use the [Add a resource form](https://github.com/Zac10ck/awesome-ai-skills/issues/new?template=add-resource.yml). Include the canonical URL, type, category, concise description, supported clients only when documented, and your reason for inclusion.

## Method 2: open a pull request

1. Fork the repository and create a focused branch.
2. Add one object to `data/resources.json`; do not edit generated catalog tables by hand.
3. Use an existing category and type. Add a category only when several strong entries justify it.
4. Run `python3 scripts/validate_resources.py`.
5. Run `python3 scripts/generate_readme.py` and include the updated README.
6. Open a pull request explaining your evidence and relationship to the project.

Descriptions should be factual, 25–180 characters where practical, and end with a period. Use the project's canonical HTTPS URL. Set `verified_at` to `null` unless you personally checked the resource and can state the UTC date as `YYYY-MM-DD`.

## Review criteria

Maintainers check schema validity, duplicate URLs, link health, source attribution, category fit, description accuracy, maintenance signals, compatibility evidence, license clarity, suspicious instructions, and spam. Automated checks support review but never constitute editorial approval. External submissions are not merged automatically.

By contributing, you agree that your original list contribution may be distributed under CC0 1.0. Linked projects remain under their respective licenses.
