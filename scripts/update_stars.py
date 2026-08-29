#!/usr/bin/env python3
"""Fetch latest star counts for all GitHub repos listed in README.md / README.en.md
and update both files in place.

- Reads every `https://github.com/owner/repo` link in each README
- Queries the GitHub API once per unique repo for its stargazers_count
- Rewrites the "⭐ x.xk" cells in every row that links to that repo
- Updates the "books-NN" badge count and the crawl timestamp in each file
- Only writes a file when something actually changed (no-op commits are avoided)

Intended to run inside GitHub Actions (GITHUB_TOKEN gives 5000 req/h); also works
locally with the anonymous limit of 60 req/h, which is plenty for a list this size.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# path -> (regex for its crawl-timestamp line, replacement prefix)
FILES = {
    "README.md": (r"数据抓取时间：\d{4}-\d{2}-\d{2}", "数据抓取时间："),
    "README.en.md": (r"Data fetched: \d{4}-\d{2}-\d{2}", "Data fetched: "),
}
SELF = "gotonote/awesome-agent-boom"  # badge links reference this repo itself; exclude it
API = "https://api.github.com/repos/"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
USER_AGENT = "gotonote/awesome-agent-boom star-updater"

REPO_RE = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")


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


def load_repos(content: str) -> set:
    return {r for r in REPO_RE.findall(content) if r != SELF}


def main() -> int:
    contents = {}
    all_repos: set = set()
    for path in FILES:
        with open(path, encoding="utf-8") as f:
            contents[path] = f.read()
        all_repos |= load_repos(contents[path])
    print(f"Found {len(all_repos)} unique repos across {len(FILES)} files")

    # Fetch each repo's star count exactly once, then apply to every file
    stars = {}
    for repo in sorted(all_repos):
        try:
            stars[repo] = fetch_stars(repo)
            print(f"  {repo}: {stars[repo]}")
        except Exception as exc:
            print(f"  !! {repo}: {exc}", file=sys.stderr)

    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    # 记录本仓库自身的 Star 历史（用于 README 增长图，每天覆盖同一天记录）
    try:
        self_stars = fetch_stars(SELF)
        hist_path = Path("docs/star-history.json")
        hist = (
            json.loads(hist_path.read_text(encoding="utf-8"))
            if hist_path.exists()
            else {}
        )
        hist[now] = self_stars
        hist_path.write_text(
            json.dumps(hist, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"  star history: {now} -> {self_stars}")
    except Exception as exc:
        print(f"  !! star history: {exc}", file=sys.stderr)

    changed = False
    for path, (ts_re, ts_prefix) in FILES.items():
        content = contents[path]
        new = content
        for repo, count in stars.items():
            # Rewrite "⭐ <old>" in every row (category tables + Top 10) linking to this repo
            pattern = re.compile(
                r"(\[" + re.escape(repo) + r"\]\([^)]*\)\s*\|\s*⭐\s*)[\d.]+k?"
            )
            new = pattern.subn(lambda m: m.group(1) + fmt_stars(count), new)[0]
        new = re.sub(r"books-\d+", f"books-{len(all_repos)}", new)
        new = re.sub(ts_re, ts_prefix + now, new)
        if new != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"{path}: updated.")
            changed = True
        else:
            print(f"{path}: no changes.")
    return 0 if changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
