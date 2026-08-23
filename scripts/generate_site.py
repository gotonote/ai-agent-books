#!/usr/bin/env python3
"""Generate docs/index.html (GitHub Pages site) from README.md.

Parses the category tables and Top 10 leaderboard in README.md and renders a
responsive static page. Intended to run right after update_stars.py in CI so
the site always reflects the latest star counts. Pure stdlib, no deps.
"""

import re
from pathlib import Path

README = "README.md"
OUT = "docs/index.html"

DIFF = {
    "🟢": ("beginner", "入门"),
    "🟡": ("intermediate", "进阶"),
    "🔴": ("advanced", "深度"),
}
SECTIONS = [
    ("chinese-books", "📖 开源图书（中文）"),
    ("english-books", "🌍 开源图书 / 课程（英文）"),
    ("commercial-code", "📦 商业图书配套代码"),
    ("papers-resources", "📑 论文清单 / 资源汇总"),
    ("agent-rules", "🛠️ Agent 规则书"),
    ("ai-writing", "✍️ AI Agent 写书实验"),
]
ORDER = [s[0] for s in SECTIONS] + ["top-10", "roadmap"]

CSS = """
:root { --bg:#0b0f1a; --card:#141a2b; --line:#232b40; --text:#e6e9f2; --muted:#8b93a7; --accent:#6c8cff; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  background:radial-gradient(1200px 600px at 80% -10%, #1b2a4a 0%, var(--bg) 55%); color:var(--text); line-height:1.6; }
.wrap { max-width:1080px; margin:0 auto; padding:48px 20px 80px; }
header { text-align:center; padding:24px 0 8px; }
header h1 { font-size:2rem; letter-spacing:.5px; }
header p { color:var(--muted); margin-top:8px; font-size:.95rem; }
.stats { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin:22px 0 6px; }
.stat { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:10px 18px; font-size:.9rem; }
.stat b { color:var(--accent); font-size:1.15rem; margin-right:4px; }
.actions { display:flex; gap:12px; justify-content:center; margin:22px 0 10px; flex-wrap:wrap; }
.btn { display:inline-block; padding:9px 18px; border-radius:10px; text-decoration:none; font-size:.92rem; border:1px solid var(--line); color:var(--text); background:var(--card); transition:.15s; }
.btn:hover { border-color:var(--accent); transform:translateY(-1px); }
.btn.primary { background:var(--accent); border-color:var(--accent); color:#fff; }
section { margin-top:44px; }
section h2 { font-size:1.3rem; margin-bottom:16px; padding-left:12px; border-left:4px solid var(--accent); }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:14px; }
.card { display:block; background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px 18px; text-decoration:none; color:var(--text); transition:.15s; }
.card:hover { border-color:var(--accent); transform:translateY(-2px); }
.card-top { display:flex; justify-content:space-between; align-items:center; gap:10px; }
.repo { font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.82rem; color:var(--accent); }
.stars { font-size:.85rem; white-space:nowrap; }
.card-name { font-weight:600; margin-top:8px; font-size:.98rem; }
.card-desc { color:var(--muted); font-size:.86rem; margin-top:6px; }
.badge { display:inline-block; font-size:.72rem; padding:1px 8px; border-radius:20px; margin-right:6px; vertical-align:1px; }
.badge.beginner { background:#12351f; color:#4ade80; }
.badge.intermediate { background:#3a2c10; color:#facc15; }
.badge.advanced { background:#3a1414; color:#f87171; }
table { width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--line); border-radius:14px; overflow:hidden; font-size:.9rem; }
th, td { padding:10px 14px; text-align:left; border-bottom:1px solid var(--line); }
th { background:#10162a; color:var(--muted); font-weight:600; }
tr:last-child td { border-bottom:none; }
td a { color:var(--accent); text-decoration:none; font-family:ui-monospace,Menlo,monospace; font-size:.85rem; }
td.rank { color:var(--muted); width:40px; }
td.stars { white-space:nowrap; text-align:right; }
.roadmap { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px 24px; font-size:.92rem; }
.roadmap li { margin:8px 0; list-style:none; }
.roadmap b { color:var(--accent); }
footer { text-align:center; color:var(--muted); font-size:.82rem; margin-top:56px; }
footer a { color:var(--accent); text-decoration:none; }
@media (max-width:640px) { .grid { grid-template-columns:1fr; } header h1 { font-size:1.5rem; } }
"""


def md(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+?)\*", r"<em>\1</em>", text)
    return text


def parse_rows(lines, start, end):
    rows = []
    for line in lines[start:end]:
        m = re.match(
            r"^\| \[([^]]+)\]\(https://github\.com/([^)]+)\) \| ⭐ ([\d.]+k?) \| (.*) \|$",
            line,
        )
        if not m:
            continue
        name, repo, stars, desc = m.groups()
        diff_cls = diff_label = ""
        dm = re.match(r"([🟢🟡🔴]) (\S+) · (.*)", desc)
        if dm:
            icon, label, desc = dm.groups()
            diff_cls, diff_label = DIFF[icon]
        # lift the bolded book title (if any) into its own field
        title = name
        bm = re.search(r"\*\*(.+?)\*\*", desc)
        if bm:
            title = bm.group(1)
            desc = desc.replace(f"**{title}**", "", 1).strip()
        rows.append(
            {
                "name": md(title),
                "repo": repo,
                "stars": stars,
                "desc": md(desc),
                "diff_cls": diff_cls,
                "diff_label": diff_label,
            }
        )
    return rows


def stars_num(s: str) -> int:
    s = s.lower()
    return int(float(s.rstrip("k")) * 1000) if s.endswith("k") else int(s)


def card(row):
    badge = (
        f'<span class="badge {row["diff_cls"]}">{row["diff_label"]}</span>'
        if row["diff_cls"]
        else ""
    )
    return (
        f'      <a class="card" href="https://github.com/{row["repo"]}" '
        f'target="_blank" rel="noopener">\n'
        f'        <div class="card-top">\n'
        f'          <span class="repo">{row["repo"]}</span>\n'
        f'          <span class="stars">⭐ {row["stars"]}</span>\n'
        f"        </div>\n"
        f'        <div class="card-name">{row["name"]}</div>\n'
        f'        <div class="card-desc">{badge} {row["desc"]}</div>\n'
        f"      </a>"
    )


def main():
    lines = Path(README).read_text(encoding="utf-8").splitlines()

    anchors = {}
    for i, line in enumerate(lines):
        m = re.match(r'## <a id="([^"]+)"></a>', line)
        if m:
            anchors[m.group(1)] = i

    sections_html, total_stars, repo_count = [], 0, 0
    for idx, (aid, title) in enumerate(SECTIONS):
        rows = parse_rows(lines, anchors[aid], anchors[ORDER[idx + 1]])
        repo_count += len(rows)
        total_stars += sum(stars_num(r["stars"]) for r in rows)
        cards = "\n".join(card(r) for r in rows)
        sections_html.append(
            f'  <section id="{aid}">\n    <h2>{title}</h2>\n'
            f'    <div class="grid">\n{cards}\n    </div>\n  </section>'
        )

    top10_rows = []
    for line in lines[anchors["top-10"] : anchors["roadmap"]]:
        m = re.match(
            r"^\| (\d+) \| \[([^]]+)\]\(https://github\.com/([^)]+)\) \| ⭐ ([\d.]+k?) \| (.*) \|$",
            line,
        )
        if m:
            rank, _, repo, stars, one = m.groups()
            top10_rows.append(
                f'<tr><td class="rank">{rank}</td>'
                f'<td><a href="https://github.com/{repo}">{repo}</a></td>'
                f"<td>{md(one)}</td>"
                f'<td class="stars">⭐ {stars}</td></tr>'
            )

    m_date = re.search(r"数据抓取时间：(\d{4}-\d{2}-\d{2})", "\n".join(lines))
    fetched = m_date.group(1) if m_date else "-"

    stats = (
        f'<div class="stat">📚 收录 <b>{repo_count}</b> 个仓库</div>\n'
        f'<div class="stat">⭐ 合计 <b>{total_stars:,}</b> stars</div>\n'
        f'<div class="stat">🔄 数据 <b>{fetched}</b> 自动更新</div>'
    )

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Agent 热门书单 | Open-source AI Agent Books</title>
<meta name="description" content="GitHub 上最热的 AI Agent / LLM Agent 开源书籍、课程与配套代码仓库精选书单，Star 数每日自动更新。">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>📚 AI Agent 热门书单</h1>
    <p>GitHub 上最热的开源书籍、课程与配套代码仓库 · 按热门度排序 · Star 数每日自动更新</p>
    <div class="stats">
{stats}
    </div>
    <div class="actions">
      <a class="btn primary" href="https://github.com/gotonote/ai-agent-books" target="_blank" rel="noopener">⭐ Star 仓库</a>
      <a class="btn" href="https://github.com/gotonote/ai-agent-books/blob/main/README.md" target="_blank" rel="noopener">🇨🇳 中文版</a>
      <a class="btn" href="https://github.com/gotonote/ai-agent-books/blob/main/README.en.md" target="_blank" rel="noopener">🇬🇧 English</a>
    </div>
  </header>

{chr(10).join(sections_html)}

  <section id="top-10">
    <h2>🏆 Top 10 总榜</h2>
    <table>
      <thead><tr><th>#</th><th>仓库</th><th>一句话</th><th>Star</th></tr></thead>
      <tbody>
{chr(10).join(top10_rows)}
      </tbody>
    </table>
  </section>

  <section id="roadmap">
    <h2>🔍 推荐阅读路线</h2>
    <div class="roadmap">
      <ul>
        <li><b>入门</b>：Hugging Face Agents Course → 《深入理解 AI Agent》→ Hermes Agent 橙皮书</li>
        <li><b>进阶（Harness 工程）</b>：《御舆：解码 Agent Harness》→ harness-books → Harness Engineering 橙皮书</li>
        <li><b>面试 / 求职</b>：AIGC-Interview-Book + Awesome-Agent-Papers</li>
        <li><b>动手实践</b>：Generative AI with LangChain → Hands-On Intelligent Agents with OpenAI Gym</li>
      </ul>
    </div>
  </section>

  <footer>
    数据来自 <a href="https://github.com/gotonote/ai-agent-books" target="_blank" rel="noopener">gotonote/ai-agent-books</a> · 由 GitHub Actions 每日自动更新 · 欢迎 PR 推荐新书
  </footer>
</div>
</body>
</html>
"""
    Path(OUT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT).write_text(page, encoding="utf-8")
    print(f"Generated {OUT}: {repo_count} repos, {total_stars:,} total stars")


if __name__ == "__main__":
    main()
