#!/usr/bin/env python3
"""Check catalog links concurrently and write a reviewable JSON report."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "awesome-ai-skills-link-check/1.0 (+https://github.com/Zac10ck/awesome-ai-skills)"


def check(item: dict, attempts: int = 3) -> dict:
    last_error = "unknown error"
    for attempt in range(attempts):
        request = urllib.request.Request(item["url"], headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return {"id": item["id"], "url": item["url"], "status": response.status, "final_url": response.url, "ok": response.status < 400}
        except urllib.error.HTTPError as error:
            last_error = f"HTTP {error.code}"
            if error.code in {403, 429}:
                return {"id": item["id"], "url": item["url"], "status": error.code, "final_url": None, "ok": False, "review": True, "error": last_error}
            if error.code not in {429, 500, 502, 503, 504}:
                break
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = str(error.reason if hasattr(error, "reason") else error)
        if attempt + 1 < attempts:
            time.sleep(2 ** attempt)
    return {"id": item["id"], "url": item["url"], "status": None, "final_url": None, "ok": False, "error": last_error}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, help="Optional path for a JSON report")
    args = parser.parse_args()
    resources = json.loads((ROOT / "data/resources.json").read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(check, resources))
    reviews = [result for result in results if result.get("review")]
    failures = [result for result in results if not result["ok"] and not result.get("review")]
    for result in reviews:
        print(f"REVIEW {result['id']}: {result.get('error', result.get('status'))} (access limited or rate limited)")
    for result in failures:
        print(f"FAIL {result['id']}: {result.get('error', result.get('status'))}")
    print(f"Checked {len(results)} links: {sum(result['ok'] for result in results)} passed, {len(reviews)} inconclusive, {len(failures)} failed.")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(results, indent=2) + "\n")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
