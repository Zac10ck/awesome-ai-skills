# Automatic discovery and publication

The website is built from `data/resources.json` and `data/categories.json`.

- Every Tuesday, `discover-resources.yml` searches GitHub's supported API using bounded queries and a primary-source seed list in `data/discovery-sources.json`.
- Results exclude existing canonical URLs, forks, and archived repositories. Candidates retain source links, descriptions, license metadata, and last-push dates.
- Discovery updates one review issue and preserves downloadable JSON and Markdown reports. Partial API failures are reported and fail the workflow instead of silently claiming full coverage.
- Maintainers approve candidates by adding accurate entries to the catalog and regenerating the README. Discovery never merges unreviewed external resources.
- A push to `main` that changes the catalog automatically validates, builds, and deploys GitHub Pages.
- Weekly link checks and monthly editorial reminders provide ongoing maintenance. A single outage never removes an entry automatically.

No personal token is required for scheduled runs; the workflow uses GitHub's scoped job token. Configure new searches and seeds in `data/discovery-sources.json`. Queries do not promise exhaustive coverage of the internet.

To run locally, provide `GH_TOKEN` through your credential environment and execute `python3 scripts/discover_resources.py`. Add `--issue` only when you intend to publish or update the review queue.
