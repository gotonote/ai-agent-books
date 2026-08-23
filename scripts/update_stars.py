#!/usr/bin/env python3
"""Fetch latest star counts for all GitHub repos in README.md and update it in place.

- Reads every `https://github.com/owner/repo` link in README.md
- Queries the GitHub API for each repo's stargazers_count
- Rewrites the "⭐ x.xk" cells in every row that links to that repo
- Updates the "数据抓取时间" line and the "books-NN" badge count
- Only writes the file when something actually changed (no-op commits are avoided)

Intended to run inside GitHub Actions; also works locally (anonymous API limit
is 60 req/h, which is plenty for a list of this size).
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

README = "README.md"
API = "https://api.github.com/repos/"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
USER_AGENT = "gotonote/ai-agent-books star-updater"


def fetch_stars(repo: str) -> int:
    req = urllib.request.Request(API + repo)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return int(data["stargazers_count"])


def fmt_stars(n: int) -> str:
    """40900 -> '40.9k', 2900 -> '2.9k', 116 -> '116' (matches existing style)."""
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def main() -> int:
    with open(README, encoding="utf-8") as f:
        content = f.read()

    SELF = "gotonote/ai-agent-books"
    repos = sorted(
        {
            r
            for r in re.findall(
                r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", content
            )
            if r != SELF  # badge links reference the repo itself; exclude it
        }
    )
    print(f"Found {len(repos)} unique repos")

    new_content = content
    for repo in repos:
        try:
            stars = fetch_stars(repo)
        except Exception as exc:
            print(f"  !! {repo}: {exc}", file=sys.stderr)
            continue
        # Rewrite "⭐ <old>" in every row (category tables + Top 10) linking to this repo
        pattern = re.compile(
            r"(\[" + re.escape(repo) + r"\]\([^)]*\)\s*\|\s*⭐\s*)[\d.]+k?"
        )
        new_content, n = pattern.subn(
            lambda m: m.group(1) + fmt_stars(stars), new_content
        )
        print(f"  {repo}: {stars} (rows updated: {n})")

    # Keep the repo-count badge and the crawl timestamp in sync
    new_content = re.sub(r"books-\d+", f"books-{len(repos)}", new_content)
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    new_content = re.sub(
        r"数据抓取时间：\d{4}-\d{2}-\d{2}", f"数据抓取时间：{now}", new_content
    )

    if new_content != content:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated.")
    else:
        print("No changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
