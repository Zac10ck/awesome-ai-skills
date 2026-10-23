"""Discover GitHub candidates without changing the approved catalog.

Uses the supported REST API, bounded requests, conditional rate-limit handling,
and one updatable issue for maintainer review. No third-party code is executed.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def api(path, payload=None, method=None):
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'awesome-ai-skills-discovery', 'X-GitHub-Api-Version': '2022-11-28'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    request = urllib.request.Request('https://api.github.com/' + path, headers=headers,
        data=json.dumps(payload).encode() if payload is not None else None, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def discover():
    sources = json.loads((ROOT / 'data/discovery-sources.json').read_text())
    catalog = json.loads((ROOT / 'data/resources.json').read_text())
    known = {r['url'].lower().rstrip('/') for r in catalog}
    candidates = {}
    errors = []
    for query in sources['queries']:
        try:
            result = api('search/repositories?' + urllib.parse.urlencode({'q': query, 'sort': 'updated', 'per_page': 8}))
            for repo in result['items']:
                candidates[repo['full_name'].lower()] = repo
        except urllib.error.HTTPError as error:
            errors.append(f'Search incomplete (HTTP {error.code}): {query}')
            if error.code in (403, 429):
                break
    for name in sources['seed_repositories']:
        try:
            repo = api('repos/' + name)
            candidates[repo['full_name'].lower()] = repo
        except urllib.error.HTTPError as error:
            errors.append(f'Seed lookup incomplete (HTTP {error.code}): {name}')
            if error.code in (403, 429):
                break
    rows = []
    for repo in candidates.values():
        url = repo['html_url']
        if url.lower().rstrip('/') in known or repo.get('archived') or repo.get('fork'):
            continue
        rows.append({'name': repo['full_name'], 'url': url, 'description': repo.get('description') or 'No description supplied.',
            'pushed_at': repo.get('pushed_at'), 'license': (repo.get('license') or {}).get('spdx_id'),
            'topics': repo.get('topics', []), 'review_status': 'unreviewed'})
    return sorted(rows, key=lambda row: row['name'].lower()), errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--issue', action='store_true')
    parser.add_argument('--repo', default='Zac10ck/awesome-ai-skills')
    args = parser.parse_args()
    rows, errors = discover()
    report = ROOT / 'reports'
    report.mkdir(exist_ok=True)
    (report / 'discovery.json').write_text(json.dumps({'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidates': rows, 'errors': errors}, indent=2) + '\n')
    lines = ['<!-- automated-resource-discovery -->', '# Resource discovery review', '',
        'Candidates from bounded GitHub API searches and configured primary-source seeds. No candidate has been added to the catalog.', '',
        'Review project ownership, documentation, actual resource type, compatibility, license, and maintenance before accepting. For financial and medical tools, assess the stated use and limitations.', '']
    for row in rows:
        description = row['description'].replace('\n', ' ')[:240]
        lines.extend([f"- [ ] [{row['name']}]({row['url']})", f"  {description}", f"  Last push: {row['pushed_at']}; license: {row['license'] or 'not stated'}."])
    if not rows:
        lines.append('No new candidates returned by this run.')
    if errors:
        lines.extend(['', '## Incomplete checks', *errors])
    lines.extend(['', 'After approval, edit `data/resources.json`, validate it, and regenerate the README. Merging a catalog change deploys the website automatically.'])
    body = '\n'.join(lines)
    (report / 'discovery.md').write_text(body + '\n')
    if args.issue:
        issues = api(f'repos/{args.repo}/issues?state=open&labels=editorial-review&per_page=100')
        existing = next((i for i in issues if '<!-- automated-resource-discovery -->' in (i.get('body') or '')), None)
        if existing:
            if existing['body'] != body:
                api(f"repos/{args.repo}/issues/{existing['number']}", {'body': body}, 'PATCH')
        elif rows or errors:
            api(f'repos/{args.repo}/issues', {'title': 'Automated resource discovery: candidates for review', 'body': body, 'labels': ['editorial-review', 'automated']})
    print(f'Discovered {len(rows)} unreviewed candidates; {len(errors)} incomplete checks. Catalog unchanged.')
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
