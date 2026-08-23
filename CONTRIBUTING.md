# 贡献指南

感谢你愿意为这份书单添砖加瓦！任何 PR 都非常欢迎 🎉

## 如何提交一个新仓库

1. **Fork** 本仓库，并新建一个分支
2. 在 `README.md` 中找到合适的分类表格，按以下格式添加一行：

   ```markdown
   | [owner/repo](https://github.com/owner/repo) | ⭐ 0 | 一句话说明：是什么 + 为什么值得读 |
   ```

3. **Star 数不用手动填写**（填 `0` 即可），GitHub Actions 每天会自动抓取并更新
4. 提交 PR，并在描述里写明新增书/课程的名称和推荐理由

## 提交标准

- 内容必须与 **AI Agent / LLM Agent / Agentic Engineering** 相关
- 必须是**开源仓库**（免费可读、可下载或配套代码公开）
- 有实际内容：书籍正文、完整课程、配套代码或成体系的资源清单
- 说明栏要具体：写清「是什么 + 为什么值得读」，避免「XX 入门书籍」这类空话

## 其他贡献方式

- 修正 Star 数 / 失效链接
- 修正分类归属或描述文案
- 优化 README 排版、翻译、目录
- 在 [Issues](https://github.com/gotonote/ai-agent-books/issues) 里推荐新书（贴链接即可，会有人整理进列表）

## 自动化说明

仓库通过 [GitHub Actions](.github/workflows/update-stars.yml) 每天自动抓取各仓库 Star 数并更新 README（北京时间 0:00），因此**请不要手动修改 Star 数字**，以免被自动任务覆盖。
