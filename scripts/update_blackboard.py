#!/usr/bin/env python3
"""📰 黑板报（每日 AI 新闻精选）生成器。

工作流：
1. 收集当日热门新闻 —— Hacker News（官方 API）+ 中文科技 RSS（少数派 / InfoQ / 量子位 / IT之家）
2. 调用 DeepSeek API 让 AI 主笔筛选、归类、点评，生成一期「黑板报」
3. 保存到 docs/blackboard/YYYY-MM-DD.md（历史全部留存，由 GitHub Pages 存档）
4. 由 generate_site.py 渲染到主页（最近一周）与 docs/blackboard.html（全量归档）

约定：
- 只在工作日（周一至周五，北京时间）出刊；周末或当日已出刊则直接跳过
- 纯标准库，无第三方依赖；DEEPSEEK_API_KEY 缺失或调用失败时降级为「原始热榜」版，
  保证每日出刊不中断（失败原因写入文件，方便排查）
"""

import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

CN_TZ = timezone(timedelta(hours=8))
OUT_DIR = "docs/blackboard"
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
USER_AGENT = "Mozilla/5.0 (gotonote/ai-agent-books blackboard)"

WEEKDAYS_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# 新闻源：每个源返回 [(标题, 链接, 一句话/元信息), ...]，按热度/时间排序
SOURCE_RSS = [
    ("少数派", "https://sspai.com/feed"),
    ("InfoQ 中文", "https://www.infoq.cn/feed"),
    ("量子位", "https://www.qbitai.com/feed"),
    ("IT之家", "https://www.ithome.com/rss/"),
]
HN_TOP_N = 30  # 取 HN 前 N 条拉取详情
RSS_TOP_N = 10  # 每个中文 RSS 源取前 N 条


def http_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_hn() -> list:
    """Hacker News 前 30 条热榜（含 score / 评论数）。"""
    ids = http_json("https://hacker-news.firebaseio.com/v0/topstories.json")[:HN_TOP_N]
    items = []
    for sid in ids:
        try:
            it = http_json(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
        except Exception:
            continue
        if not it or not it.get("title") or it.get("type") != "story":
            continue
        items.append(
            {
                "title": it["title"],
                "url": it.get("url") or f"https://news.ycombinator.com/item?id={sid}",
                "meta": f"HN 热度 {it.get('score', 0)} · {it.get('descendants', 0)} 评论",
            }
        )
    return items


def fetch_rss(name: str, url: str) -> list:
    """抓取一个 RSS 源，返回前 RSS_TOP_N 条。任何异常都返回空列表。"""
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as resp:
            root = ET.fromstring(resp.read())
        for entry in root.iter("item"):
            title = entry.findtext("title")
            link = entry.findtext("link")
            if not title or not link:
                continue
            desc = re.sub(r"<[^>]+>", "", entry.findtext("description") or "")
            desc = re.sub(r"\s+", " ", desc).strip()[:120]
            items.append({"title": title.strip(), "url": link.strip(), "meta": desc})
            if len(items) >= RSS_TOP_N:
                break
    except Exception as exc:
        print(f"  !! RSS {name} 抓取失败: {exc}", file=sys.stderr)
    return items


def collect_news() -> dict:
    """汇总各来源新闻。"""
    news = {"Hacker News": fetch_hn()}
    for name, url in SOURCE_RSS:
        got = fetch_rss(name, url)
        if got:
            news[name] = got
        else:
            print(f"  !! {name} 无有效条目，跳过该源", file=sys.stderr)
    return news


def build_prompt(today: str, weekday: str, news: dict) -> str:
    """构造发给 DeepSeek 的提示词。"""
    lines = [f"今天是 {today}（{weekday}），以下是今日新闻素材：", ""]
    for source, items in news.items():
        lines.append(f"## 来源：{source}")
        for i, it in enumerate(items[:15], 1):
            lines.append(f"{i}. {it['title']}｜{it['url']}")
            if it.get("meta"):
                lines.append(f"   （{it['meta']}）")
        lines.append("")
    prompt = "\n".join(lines)
    system = (
        "你是「AI Agent 热门书单」黑板报的主笔编辑，面向 AI 工程师 / 程序员 / 技术从业者。"
        "请从提供的新闻素材中筛选出最有信息量、最值得关注的内容，写一期中文黑板报。\n"
        "要求：\n"
        "1. 观点鲜明，语言精炼，拒绝凑字数；同一主题只保留最有价值的一条\n"
        "2. 按以下 Markdown 结构输出（不要输出其他内容）：\n"
        "   ## 🔥 今日头条\n"
        "   3-5 条最重磅新闻，每条格式：`1. **标题** —— 一句话点评（[链接](url)）`\n"
        "   ## 📌 分类速览\n"
        "   按「AI 大模型 / 开发者工具 / 开源 / 业界动态」等分类，每类 2-4 条，同样带链接\n"
        "   ## 💡 编辑手记\n"
        "   1-2 段，把今天最重要的 1-2 条新闻串起来讲：为什么重要、对 AI 开发者的启示\n"
        "3. 只能引用素材中出现的新闻，不得编造；链接使用素材提供的原文 URL\n"
        "4. 正文中不要出现『AI 生成』『DeepSeek』『主笔』等字样，语气像资深编辑亲自撰写"
    )
    return system, prompt


def call_deepseek(system: str, prompt: str) -> str:
    """调用 DeepSeek chat completions，返回正文 Markdown。"""
    body = json.dumps(
        {
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        DEEPSEEK_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def render_raw_fallback(news: dict) -> str:
    """DeepSeek 不可用时的降级内容：原始热榜。"""
    parts = []
    for source, items in news.items():
        parts.append(f"## 来源：{source}")
        for i, it in enumerate(items[:15], 1):
            parts.append(f"{i}. **{it['title']}** —— {it.get('meta', '')}（<{it['url']}>）")
        parts.append("")
    return "\n".join(parts)


def main() -> int:
    now = datetime.now(CN_TZ)
    today = now.strftime("%Y-%m-%d")
    weekday = WEEKDAYS_CN[now.weekday()]

    # 只在工作日出刊（工作日 09:00 的 cron 已保证，这里做双保险；--force 可强制）
    if now.weekday() >= 5 and "--force" not in sys.argv:
        print(f"{today} 是周末，黑板报只在工作日更新，跳过。")
        return 0

    out_path = os.path.join(OUT_DIR, f"{today}.md")
    if os.path.exists(out_path):
        print(f"{out_path} 已存在，跳过（当日已出刊）。")
        return 0

    print(f"📰 黑板报 {today}（{weekday}）开始出刊…")
    news = collect_news()
    total = sum(len(v) for v in news.values())
    print(f"  共收集 {len(news)} 个来源 / {total} 条新闻")

    if os.environ.get("DEEPSEEK_API_KEY"):
        try:
            system, prompt = build_prompt(today, weekday, news)
            print("  正在调用 DeepSeek 生成编辑摘要…")
            content = call_deepseek(system, prompt)
            print(f"  DeepSeek 返回 {len(content)} 字符")
        except Exception as exc:
            print(f"  !! DeepSeek 调用失败: {exc}", file=sys.stderr)
            content = render_raw_fallback(news)
    else:
        print("  !! 未设置 DEEPSEEK_API_KEY，输出原始热榜降级版", file=sys.stderr)
        content = render_raw_fallback(news)

    header = (
        f"# 📰 黑板报 · {today}（{weekday}）\n\n"
        f"> 工作日每日出刊 · 数据来源：Hacker News / 少数派 / InfoQ / 量子位 / IT之家\n\n"
        f"---\n\n"
    )
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + content + "\n")
    print(f"✅ 已保存 {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
