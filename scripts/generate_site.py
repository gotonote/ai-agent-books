#!/usr/bin/env python3
"""Generate docs/index.html (GitHub Pages site) from README.md.

Parses the category tables in README.md and renders a
responsive static page with client-side search & difficulty filtering.
Intended to run right after update_stars.py in CI so the site always reflects
the latest star counts. Pure stdlib, no deps.
"""

import html as html_mod
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

README = "README.md"
OUT = "docs/index.html"

# 黑板报：docs/blackboard/*.md 为每日出刊存档，主页展示最近一周，其余进归档页
BB_DIR = Path("docs/blackboard")
BB_ARCHIVE = "docs/blackboard.html"
BB_DAYS_ON_HOME = 7

# 本仓库 Star 历史（由 update_stars.py 每日记录）→ 渲染为 README 增长图
STAR_HISTORY = "docs/star-history.json"
STAR_CHART = "docs/star-chart.svg"

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
    ("harness-ecosystem", "🧩 Agent Harness 生态"),
    ("agent-frameworks", "🤖 Agent 框架 / 工具库"),
]
ORDER = [s[0] for s in SECTIONS] + ["roadmap"]

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
.controls { display:flex; gap:10px; align-items:center; justify-content:center; flex-wrap:wrap; margin:26px 0 6px; }
.search { background:var(--card); border:1px solid var(--line); color:var(--text); border-radius:10px; padding:9px 14px; font-size:.9rem; width:280px; max-width:100%; outline:none; }
.search:focus { border-color:var(--accent); }
.filter-btn { background:var(--card); border:1px solid var(--line); color:var(--text); border-radius:20px; padding:6px 15px; font-size:.83rem; cursor:pointer; transition:.15s; }
.filter-btn:hover { border-color:var(--accent); }
.filter-btn.active { background:var(--accent); border-color:var(--accent); color:#fff; }
.count { color:var(--muted); font-size:.82rem; text-align:center; margin:6px 0 0; }
section { margin-top:44px; }
section h2 { font-size:1.3rem; margin-bottom:16px; padding-left:12px; border-left:4px solid var(--accent); }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:14px; }
.card { display:block; background:var(--card); border:1px solid var(--line); border-radius:14px; padding:16px 18px; text-decoration:none; color:var(--text); transition:.15s; }
.card:hover { border-color:var(--accent); transform:translateY(-2px); }
.card.hidden { display:none; }
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
@media (max-width:640px) { .grid { grid-template-columns:1fr; } header h1 { font-size:1.5rem; } .search { width:100%; } }
/* ── 黑板报 ── */
.bb-intro { color:var(--muted); font-size:.9rem; margin-bottom:16px; }
.bb-intro a { color:var(--accent); text-decoration:none; }
.bb-intro a:hover { text-decoration:underline; }
.bb-day { background:var(--card); border:1px solid var(--line); border-radius:14px; margin-bottom:14px; overflow:hidden; }
.bb-day summary { cursor:pointer; padding:14px 18px; font-weight:600; font-size:1rem; list-style:none; user-select:none; display:flex; justify-content:space-between; align-items:center; }
.bb-day summary::-webkit-details-marker { display:none; }
.bb-day summary::after { content:'▸'; color:var(--muted); transition:.15s; }
.bb-day[open] summary::after { transform:rotate(90deg); }
.bb-day summary:hover { background:#0f1526; }
.bb-day[open] summary { border-bottom:1px solid var(--line); background:#0f1526; }
.bb-day .bb-tag { font-size:.72rem; color:var(--muted); font-weight:400; border:1px solid var(--line); border-radius:20px; padding:1px 10px; }
.bb-share { font-size:.72rem; color:var(--accent); border:1px solid var(--line); border-radius:20px; padding:1px 10px; margin-left:6px; text-decoration:none; }
.bb-share:hover { border-color:var(--accent); color:var(--accent); }
.bb-body { padding:6px 22px 18px; font-size:.92rem; }
.bb-body h3, .bb-body h4 { margin:14px 0 6px; color:var(--accent); font-size:1rem; }
.bb-body h3 { font-size:1.05rem; }
.bb-body ol { padding-left:22px; margin:6px 0; }
.bb-body li { margin:5px 0; }
.bb-body a { color:var(--accent); text-decoration:none; }
.bb-body a:hover { text-decoration:underline; }
.bb-body blockquote { border-left:3px solid var(--line); color:var(--muted); padding-left:12px; margin:8px 0; font-size:.85rem; }
.bb-body p { margin:8px 0; }
.bb-body hr { border:none; border-top:1px solid var(--line); margin:14px 0; }
.bb-body code { background:#0f1526; padding:1px 6px; border-radius:6px; font-size:.85em; }
.bb-empty { color:var(--muted); background:var(--card); border:1px dashed var(--line); border-radius:14px; padding:28px; text-align:center; font-size:.9rem; }
.bb-link { text-align:right; margin:2px 0 18px; }
.bb-link a { color:var(--accent); text-decoration:none; font-size:.85rem; }
.bb-link a:hover { text-decoration:underline; }
"""

JS = """
<script>
(function () {
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var search = document.getElementById('search');
  var btns = Array.prototype.slice.call(document.querySelectorAll('.filter-btn'));
  var count = document.getElementById('count');
  var diff = 'all';
  function apply() {
    var q = (search.value || '').trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {
      var okDiff = diff === 'all' || c.getAttribute('data-diff') === diff;
      var okQ = !q || (c.getAttribute('data-search') || '').indexOf(q) !== -1;
      var show = okDiff && okQ;
      c.classList.toggle('hidden', !show);
      if (show) shown++;
    });
    count.textContent = '显示 ' + shown + ' / ' + cards.length + ' 个仓库';
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      btns.forEach(function (x) { x.classList.remove('active'); });
      b.classList.add('active');
      diff = b.getAttribute('data-diff');
      apply();
    });
  });
  search.addEventListener('input', apply);
  apply();
})();
</script>
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
        search = f"{repo} {title} {desc}".lower()
        rows.append(
            {
                "name": md(title),
                "repo": repo,
                "stars": stars,
                "desc": md(desc),
                "diff_cls": diff_cls,
                "diff_label": diff_label,
                "search": html_mod.escape(search, quote=True),
            }
        )
    return rows


def stars_num(s: str) -> int:
    s = s.lower()
    return int(float(s.rstrip("k")) * 1000) if s.endswith("k") else int(s)


def md_inline(s: str) -> str:
    """黑板报正文行内 Markdown → HTML（加粗 / 链接 / 自动链接 / 行内代码）。"""
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        s,
    )
    s = re.sub(
        r"<((?:https?://)[^>]+)>",
        r'<a href="\1" target="_blank" rel="noopener">\1</a>',
        s,
    )
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def render_md(text: str) -> str:
    """黑板报每日 Markdown 文件 → HTML（标题 / 列表 / 引用 / 分隔线 / 段落）。"""
    lines = text.splitlines()
    # 去掉文件开头的 H1 大标题（日期标题已在 <summary> 中展示）
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    out, list_buf = [], []

    def flush_list():
        if list_buf:
            out.append("<ol>" + "".join(list_buf) + "</ol>")
            list_buf.clear()

    for raw in lines:
        s = raw.strip()
        if not s:
            flush_list()
            continue
        if re.match(r"^#{1,6}\s", s):
            flush_list()
            level = len(s) - len(s.lstrip("#"))
            out.append(f"<h{min(level + 1, 6)}>{md_inline(s.lstrip('#').strip())}</h{min(level + 1, 6)}>")
        elif s == "---":
            flush_list()
            out.append("<hr>")
        elif s.startswith(">"):
            flush_list()
            out.append(f"<blockquote>{md_inline(s.lstrip('>').strip())}</blockquote>")
        elif re.match(r"^\d+\.\s", s):
            list_buf.append(f"<li>{md_inline(re.sub(r'^\d+\.\s', '', s))}</li>")
        else:
            flush_list()
            out.append(f"<p>{md_inline(s)}</p>")
    flush_list()
    return "\n".join(out)


def load_blackboard() -> list:
    """读取 docs/blackboard/ 下所有往期，按日期倒序。"""
    days = []
    if BB_DIR.is_dir():
        for p in sorted(BB_DIR.glob("*.md"), reverse=True):
            m = re.match(r"(\d{4}-\d{2}-\d{2})\.md$", p.name)
            if not m:
                continue
            d = m.group(1)
            try:
                dt = datetime.strptime(d, "%Y-%m-%d")
            except ValueError:
                continue
            days.append(
                {
                    "date": d,
                    "weekday": "周" + "一二三四五六日"[dt.weekday()],
                    "html": render_md(p.read_text(encoding="utf-8")),
                }
            )
    return days


def bb_day_html(day: dict, open_: bool) -> str:
    bb_url = "https://gotonote.github.io/awesome-agent-boom/blackboard.html"
    share_text = f"📰 黑板报 {day['date']}：AI Agent / 科技每日要闻精选（Star 数每日自动更新）"
    share_href = (
        "https://twitter.com/intent/tweet?text="
        + quote_plus(share_text)
        + "&url=" + quote_plus(bb_url)
    )
    return (
        f'  <details class="bb-day"{" open" if open_ else ""}>\n'
        f'    <summary>📅 {day["date"]}（{day["weekday"]}）<span class="bb-tag">黑板报</span>'
        f'<a class="bb-share" href="{share_href}" target="_blank" rel="noopener" '
        f'title="分享到 X / Twitter" onclick="event.stopPropagation()">分享</a></summary>\n'
        f'    <div class="bb-body">\n{day["html"]}\n    </div>\n'
        "  </details>"
    )


def blackboard_section_html() -> str:
    """主页「最近一周」板块。"""
    days = load_blackboard()
    if not days:
        return (
            '  <section id="blackboard">\n'
            "    <h2>📰 黑板报</h2>\n"
            '    <p class="bb-intro">工作日每日精选全球 AI / 科技要闻，自动出刊并长期归档。</p>\n'
            '    <div class="bb-empty">🎨 黑板报正在筹备中，第一个工作日上午 9 点出刊（北京时间）</div>\n'
            "  </section>"
        )
    week = [bb_day_html(d, True) for d in days[:BB_DAYS_ON_HOME]]
    total = len(days)
    return (
        '  <section id="blackboard">\n'
        "    <h2>📰 黑板报 · 最近一周</h2>\n"
        '    <p class="bb-intro">工作日每日精选全球 AI / 科技要闻，以下为最近一周全部内容；往期可折叠，全部留存。</p>\n'
        + "\n".join(week)
        + f'\n    <p class="bb-link"><a href="blackboard.html">📚 查看全部 {total} 期 →</a></p>\n'
        "  </section>"
    )


def blackboard_archive_html() -> str:
    """独立归档页 docs/blackboard.html：展示全部往期。"""
    days = load_blackboard()
    if not days:
        body = '<div class="bb-empty">🎨 黑板报正在筹备中，第一个工作日上午 9 点出刊（北京时间）</div>'
    else:
        body = "\n".join(bb_day_html(d, i == 0) for i, d in enumerate(days))
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>黑板报 · 全部往期 | AI Agent 热门书单</title>
<meta name="description" content="AI Agent 热门书单 · 黑板报每日 AI 科技新闻精选，全部往期归档。">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>📰 黑板报 · 全部往期</h1>
    <p>工作日每日精选全球 AI / 科技要闻 · 共 {len(days)} 期 · 往期全部留存</p>
    <div class="actions">
      <a class="btn primary" href="./">← 返回书单主页</a>
    </div>
  </header>

{body}

  <footer>
    工作日每日出刊 · 往期全部留存 · <a href="https://github.com/gotonote/awesome-agent-boom" target="_blank" rel="noopener">gotonote/awesome-agent-boom</a>
  </footer>
</div>
</body>
</html>
"""


def card(row):
    badge = (
        f'<span class="badge {row["diff_cls"]}">{row["diff_label"]}</span>'
        if row["diff_cls"]
        else ""
    )
    return (
        f'      <a class="card" href="https://github.com/{row["repo"]}" '
        f'target="_blank" rel="noopener" data-diff="{row["diff_cls"] or "none"}" '
        f'data-search="{row["search"]}">\n'
        f'        <div class="card-top">\n'
        f'          <span class="repo">{row["repo"]}</span>\n'
        f'          <span class="stars">⭐ {row["stars"]}</span>\n'
        f"        </div>\n"
        f'        <div class="card-name">{row["name"]}</div>\n'
        f'        <div class="card-desc">{badge} {row["desc"]}</div>\n'
        f"      </a>"
    )


def render_star_chart() -> str:
    """根据 docs/star-history.json 生成 SVG 折线图（README 展示，托管在 GitHub Pages）。"""
    hist_path = Path(STAR_HISTORY)
    hist = (
        json.loads(hist_path.read_text(encoding="utf-8"))
        if hist_path.exists()
        else {}
    )
    dates = sorted(hist)
    W, H, pad_l, pad_r, pad_t, pad_b = 800, 260, 70, 20, 30, 40
    if len(dates) < 2:
        msg = "📈 增长曲线数据积累中，每日自动更新…" if dates else "📈 Star 增长曲线（每日自动更新）"
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'style="font-family:Segoe UI,PingFang SC,sans-serif">'
            f'<rect width="{W}" height="{H}" rx="12" fill="#141a2b"/>'
            f'<text x="{W/2}" y="{H/2}" fill="#8b93a7" font-size="16" text-anchor="middle">{msg}</text>'
            f"</svg>"
        )
    vals = [hist[d] for d in dates]
    vmin, vmax = min(vals), max(vals)
    if vmax == vmin:
        vmax = vmin + 1
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b

    def px(d: str, v: int) -> tuple:
        x = pad_l + (dates.index(d) / (len(dates) - 1)) * plot_w
        y = pad_t + (1 - (v - vmin) / (vmax - vmin)) * plot_h
        return x, y

    pts = " ".join(f"{px(d, v)[0]:.1f},{px(d, v)[1]:.1f}" for d, v in zip(dates, vals))
    # 网格与 Y 轴刻度（3 档）
    grid = []
    for i in range(4):
        v = vmin + (vmax - vmin) * i / 3
        y = pad_t + plot_h * (1 - i / 3)
        grid.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{W - pad_r}" y2="{y:.1f}" stroke="#232b40"/>')
        grid.append(f'<text x="{pad_l - 8}" y="{y + 4:.1f}" fill="#8b93a7" font-size="11" text-anchor="end">{int(round(v))}</text>')
    # X 轴日期标签（首 / 中 / 尾）
    xl = []
    for i in (0, len(dates) // 2, len(dates) - 1):
        d = dates[i]
        xl.append(f'<text x="{px(d, vals[i])[0]:.1f}" y="{H - 14}" fill="#8b93a7" font-size="11" text-anchor="middle">{d}</text>')
    latest = vals[-1]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'style="font-family:Segoe UI,PingFang SC,sans-serif">'
        f'<rect width="{W}" height="{H}" rx="12" fill="#141a2b"/>'
        f'<text x="{pad_l}" y="18" fill="#e6e9f2" font-size="14" font-weight="bold">⭐ Star 增长趋势 · 当前 {latest}</text>'
        + "".join(grid)
        + f'<polyline points="{pts}" fill="none" stroke="#6c8cff" stroke-width="2.5"/>'
        + "".join(
            f'<circle cx="{px(d, v)[0]:.1f}" cy="{px(d, v)[1]:.1f}" r="3.5" fill="#6c8cff"/>'
            for d, v in zip(dates, vals)
        )
        + "".join(xl)
        + f'<text x="{W - pad_r}" y="{H - 14}" fill="#8b93a7" font-size="11" text-anchor="end">由 GitHub Actions 每日自动更新</text>'
        + "</svg>"
    )


def main():
    lines = Path(README).read_text(encoding="utf-8").splitlines()

    anchors = {}
    for i, line in enumerate(lines):
        m = re.match(r'## <a id="([^"]+)"></a>', line)
        if m:
            anchors[m.group(1)] = i

    sections_html, total_stars, repo_count, listed_repos = [], 0, 0, []
    for idx, (aid, title) in enumerate(SECTIONS):
        rows = parse_rows(lines, anchors[aid], anchors[ORDER[idx + 1]])
        repo_count += len(rows)
        listed_repos += [r["repo"] for r in rows]
        total_stars += sum(stars_num(r["stars"]) for r in rows)
        cards = "\n".join(card(r) for r in rows)
        sections_html.append(
            f'  <section id="{aid}">\n    <h2>{title}</h2>\n'
            f'    <div class="grid">\n{cards}\n    </div>\n  </section>'
        )

    m_date = re.search(r"数据抓取时间：(\d{4}-\d{2}-\d{2})", "\n".join(lines))
    fetched = m_date.group(1) if m_date else "-"

    stats = (
        f'<div class="stat">📚 收录 <b>{repo_count}</b> 个仓库</div>\n'
        f'<div class="stat">⭐ 合计 <b>{total_stars:,}</b> stars</div>\n'
        f'<div class="stat">🔄 数据 <b>{fetched}</b> 自动更新</div>'
    )

    bb_section = blackboard_section_html()

    controls = (
        '<div class="controls">\n'
        '  <input class="search" id="search" type="search" '
        'placeholder="🔍 搜索书名 / 仓库 / 关键词…" autocomplete="off">\n'
        '  <button class="filter-btn active" data-diff="all">全部</button>\n'
        '  <button class="filter-btn" data-diff="beginner">🟢 入门</button>\n'
        '  <button class="filter-btn" data-diff="intermediate">🟡 进阶</button>\n'
        '  <button class="filter-btn" data-diff="advanced">🔴 深度</button>\n'
        "</div>\n"
        '<p class="count" id="count"></p>'
    )

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Agent 热门书单 | Open-source AI Agent Books</title>
<meta name="description" content="GitHub 上最热的 AI Agent / LLM Agent 开源书籍、课程与配套代码仓库精选书单，支持难度筛选与搜索，Star 数每日自动更新。">
<meta property="og:type" content="website">
<meta property="og:title" content="AI Agent 热门书单 | Open-source AI Agent Books">
<meta property="og:description" content="GitHub 上最热的 AI Agent / LLM Agent 开源书籍、课程与配套代码仓库精选书单（{repo_count} 个仓库，每日自动更新 Star 数）。">
<meta property="og:url" content="https://gotonote.github.io/awesome-agent-boom/">
<meta property="og:site_name" content="AI Agent 热门书单">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="AI Agent 热门书单 | Open-source AI Agent Books">
<meta name="twitter:description" content="GitHub 上最热的 AI Agent 开源书籍、课程与配套代码仓库精选书单（{repo_count} 个仓库）。">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ItemList","name":"AI Agent 热门书单","description":"GitHub 上最热的 AI Agent / LLM Agent 开源书籍、课程与配套代码仓库精选书单","numberOfItems":{repo_count},"itemListElement":[
{','.join('  {{"@type":"ListItem","position":{i},"url":"https://github.com/{r}"}}'.format(i=i, r=r) for i, r in enumerate(listed_repos, 1))}
]}}
</script>
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
      <a class="btn primary" href="https://github.com/gotonote/awesome-agent-boom" target="_blank" rel="noopener">⭐ Star 仓库</a>
      <a class="btn" href="https://github.com/gotonote/awesome-agent-boom/blob/main/README.md" target="_blank" rel="noopener">🇨🇳 中文版</a>
      <a class="btn" href="https://github.com/gotonote/awesome-agent-boom/blob/main/README.en.md" target="_blank" rel="noopener">🇬🇧 English</a>
    </div>
    {controls}
  </header>

{bb_section}

{chr(10).join(sections_html)}

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
    数据来自 <a href="https://github.com/gotonote/awesome-agent-boom" target="_blank" rel="noopener">gotonote/awesome-agent-boom</a> · 由 GitHub Actions 每日自动更新 · 欢迎 PR 推荐新书
  </footer>
</div>
{JS}
</body>
</html>
"""
    Path(OUT).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT).write_text(page, encoding="utf-8")
    print(f"Generated {OUT}: {repo_count} repos, {total_stars:,} total stars")

    # sitemap.xml：帮助搜索引擎发现主页与黑板报归档页
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://gotonote.github.io/awesome-agent-boom/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>
  <url><loc>https://gotonote.github.io/awesome-agent-boom/blackboard.html</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
</urlset>
"""
    Path("docs/sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("Generated docs/sitemap.xml")

    Path(STAR_CHART).write_text(render_star_chart(), encoding="utf-8")
    print(f"Generated {STAR_CHART}")

    Path(BB_ARCHIVE).write_text(blackboard_archive_html(), encoding="utf-8")
    bb_days = len(load_blackboard())
    print(f"Generated {BB_ARCHIVE}: {bb_days} blackboard issues archived")


if __name__ == "__main__":
    main()
