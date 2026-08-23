# 📚 AI Agent 热门书单（GitHub 开源仓库整理）

> [🇬🇧 English Version](README.en.md)
>
> 整理自 GitHub 上与 **AI Agent / LLM Agent / Agentic Engineering** 相关的热门开源书籍、教程与配套代码仓库。
> 数据抓取时间：2026-08-23 · Star 数由 GitHub Actions 每日自动更新，按热门度排序。

[![GitHub stars](https://img.shields.io/github/stars/gotonote/ai-agent-books?style=flat-square)](https://github.com/gotonote/ai-agent-books/stargazers)
[![收录仓库](https://img.shields.io/badge/books-26-blue?style=flat-square)]()
[![Last commit](https://img.shields.io/github/last-commit/gotonote/ai-agent-books?style=flat-square)]()
[![Stars 自动更新](https://img.shields.io/github/actions/workflow/status/gotonote/ai-agent-books/update-stars.yml?style=flat-square&label=stars%20update)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

---

## 📑 目录

- [📖 一、开源图书（中文）](#chinese-books)
- [🌍 二、开源图书 / 课程（英文）](#english-books)
- [📦 三、商业图书配套代码仓库](#commercial-code)
- [📑 四、论文清单 / 资源汇总](#papers-resources)
- [🛠️ 五、Agent 规则书 / 编码 Agent 技能集](#agent-rules)
- [✍️ 六、AI Agent 写书实验](#ai-writing)
- [🏆 Top 10 总榜](#top-10)
- [🔍 推荐阅读路线](#roadmap)

---

## <a id="chinese-books"></a>📖 一、开源图书（中文）

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) | ⭐ 41.1k | 🟢 入门 · **《深入理解 AI Agent：设计原理与工程实践》**（李博杰 著）开源主仓库：全书正文、编译版 PDF 与按章配套代码。目前最热的中文 Agent 书籍 |
| [alchaincyf/hermes-agent-orange-book](https://github.com/alchaincyf/hermes-agent-orange-book) | ⭐ 4.9k | 🟢 入门 · **Hermes Agent 从入门到精通 · 橙皮书系列**：Nous Research 开源 AI Agent 框架实战指南 |
| [lintsinghua/claude-code-book](https://github.com/lintsinghua/claude-code-book) | ⭐ 4.1k | 🟡 进阶 · **《御舆：解码 Agent Harness》**：42 万字拆解 AI Agent 的 Harness 骨架，15 章从对话循环到构建你自己的 Agent Harness |
| [yeasy/harness_engineering_guide](https://github.com/yeasy/harness_engineering_guide) | ⭐ 117 | 🟡 进阶 · **Harness 工程指南**：智能体 = 大模型 + Harness，深入剖析 Harness 工程原理、设计、实现与实践 |
| [alchaincyf/harness-engineering-orange-book](https://github.com/alchaincyf/harness-engineering-orange-book) | ⭐ 91 | 🟡 进阶 · **Harness Engineering · 橙皮书系列**：AI Agent 缰绳工程学实战指南 |
| [dawei008/openbook](https://github.com/dawei008/openbook) | ⭐ 34 | 🟡 进阶 · **OpenBook: AI Agent Harness Engineering**：构建生产级 Agent Harness 的开源图书（26 章） |

## <a id="english-books"></a>🌍 二、开源图书 / 课程（英文）

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [huggingface/agents-course](https://github.com/huggingface/agents-course) | ⭐ 31.3k | 🟢 入门 · **Hugging Face Agents Course**：最流行的 Agent 入门课程（教材免费开源） |
| [wquguru/harness-books](https://github.com/wquguru/harness-books) | ⭐ 2.9k | 🟡 进阶 · **Harness Engineering 两卷本**：Claude Code 与 Codex 背后的设计哲学（约束、查询循环等） |
| [jayminwest/agentic-engineering-book](https://github.com/jayminwest/agentic-engineering-book) | ⭐ 197 | 🟢 入门 · **Agentic Engineering**：构建 Agentic 系统的综合渐进式指南 |
| [Siddhant-K-code/agentic-engineering-guide](https://github.com/Siddhant-K-code/agentic-engineering-guide) | ⭐ 157 | 🟢 入门 · **Agentic Engineering Guide**（MDX 格式，交互式阅读） |
| [Drobiazkin/ai-agent-architecture](https://github.com/Drobiazkin/ai-agent-architecture) | ⭐ 46 | 🟡 进阶 · **Build LLM systems you actually control**：免费开源工程书 + 课程，从 tokenization 讲起 |
| [caozhiyi/ai-programming-book](https://github.com/caozhiyi/ai-programming-book) | ⭐ 39 | 🟡 进阶 · **The First Principles of AI Programming**：从底层物理约束出发讲 AI 编程 |
| [awsm-research/agentic-swe-book](https://github.com/awsm-research/agentic-swe-book) | ⭐ 10 | 🟡 进阶 · **Agentic Software Engineering: A Practical Guide for the AI-Native Engineer** |

## <a id="commercial-code"></a>📦 三、商业图书配套代码仓库

| 仓库 | Star | 对应图书 |
| --- | --- | --- |
| [benman1/generative_ai_with_langchain](https://github.com/benman1/generative_ai_with_langchain) | ⭐ 1.4k | 🟢 入门 · *Generative AI with LangChain*（O'Reilly）：用 Python、LangChain、LangGraph 构建生产级 LLM 应用与高级 Agent |
| [towardsai/ragbook-notebooks](https://github.com/towardsai/ragbook-notebooks) | ⭐ 557 | 🟡 进阶 · *Building LLMs for Production*（Towards AI）配套 Notebook |
| [treygrainger/ai-powered-search](https://github.com/treygrainger/ai-powered-search) | ⭐ 404 | 🟡 进阶 · *AI-Powered Search*（Manning, 2025）代码库 |
| [PacktPublishing/Hands-On-Intelligent-Agents-with-OpenAI-Gym](https://github.com/PacktPublishing/Hands-On-Intelligent-Agents-with-OpenAI-Gym) | ⭐ 400 | 🟢 入门 · *Hands-On Intelligent Agents with OpenAI Gym*：深度强化学习 Agent 入门 |

## <a id="papers-resources"></a>📑 四、论文清单 / 资源汇总

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [WooooDyy/LLM-Agent-Paper-List](https://github.com/WooooDyy/LLM-Agent-Paper-List) | ⭐ 8.2k | 🔴 深度 · SCIS 封面论文 *The Rise and Potential of LLM-based Agents* 配套论文清单 |
| [WangRongsheng/awesome-LLM-resources](https://github.com/WangRongsheng/awesome-LLM-resources) | ⭐ 8.9k | 🟢 入门 · LLM 资料大全：多模态、Agent、MCP、模型训练/推理等 |
| [WeThinkIn/AIGC-Interview-Book](https://github.com/WeThinkIn/AIGC-Interview-Book) | ⭐ 4.4k | 🟡 进阶 · AIGC/LLM/AI Agent 算法工程师面试资源平台（三年面试五年模拟） |
| [luo-junyu/Awesome-Agent-Papers](https://github.com/luo-junyu/Awesome-Agent-Papers) | ⭐ 2.8k | 🔴 深度 · LLM Agent 综述：方法论、应用与挑战（持续更新） |
| [weitianxin/Awesome-Agentic-Reasoning](https://github.com/weitianxin/Awesome-Agentic-Reasoning) | ⭐ 1.3k | 🔴 深度 · 基于 *Agentic Reasoning for LLMs* 综述整理的资源清单 |

## <a id="agent-rules"></a>🛠️ 五、Agent 规则书 / 编码 Agent 技能集

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books) | ⭐ 2.6k | 🟡 进阶 · **AGENTS.md rules / skills for AI coding agents**：Codex、Cursor & Claude Code 的规则与技能书，灵感来自 Clean Code |

## <a id="ai-writing"></a>✍️ 六、AI Agent 写书实验

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [mind-protocol/terminal-velocity](https://github.com/mind-protocol/terminal-velocity) | ⭐ 1.1k | 🟢 入门 · 由 10 个 AI Agent 组成的团队自主创作的长篇小说（可作 Agent 协作案例研究） |
| [adamwlarson/ai-book-writer](https://github.com/adamwlarson/ai-book-writer) | ⭐ 392 | 🟢 入门 · 用 AutoGen 实验：验证 AI Agent 能否独立写完一本书 |
| [vkorost/weekend-diy-book](https://github.com/vkorost/weekend-diy-book) | ⭐ 24 | 🟢 入门 · *Claude Code: The Definitive Guide to Agentic Development* —— 一个周末用 Agent 写成的技术书 |

---

## <a id="top-10"></a>🏆 Top 10 总榜

| # | 仓库 | Star | 一句话 |
| --- | --- | --- | --- |
| 1 | [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) | ⭐ 41.1k | 深入理解 AI Agent（李博杰） |
| 2 | [huggingface/agents-course](https://github.com/huggingface/agents-course) | ⭐ 31.3k | Hugging Face Agent 课程 |
| 3 | [WangRongsheng/awesome-LLM-resources](https://github.com/WangRongsheng/awesome-LLM-resources) | ⭐ 8.9k | LLM 资料大全 |
| 4 | [WooooDyy/LLM-Agent-Paper-List](https://github.com/WooooDyy/LLM-Agent-Paper-List) | ⭐ 8.2k | LLM Agent 论文清单 |
| 5 | [alchaincyf/hermes-agent-orange-book](https://github.com/alchaincyf/hermes-agent-orange-book) | ⭐ 4.9k | Hermes Agent 橙皮书 |
| 6 | [WeThinkIn/AIGC-Interview-Book](https://github.com/WeThinkIn/AIGC-Interview-Book) | ⭐ 4.4k | Agent 面试题集 |
| 7 | [lintsinghua/claude-code-book](https://github.com/lintsinghua/claude-code-book) | ⭐ 4.1k | 解码 Agent Harness |
| 8 | [wquguru/harness-books](https://github.com/wquguru/harness-books) | ⭐ 2.9k | Harness 工程两卷本 |
| 9 | [luo-junyu/Awesome-Agent-Papers](https://github.com/luo-junyu/Awesome-Agent-Papers) | ⭐ 2.8k | LLM Agent 综述清单 |
| 10 | [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books) | ⭐ 2.6k | Agent 规则书 |

---

## <a id="roadmap"></a>🔍 推荐阅读路线

- **入门**：Hugging Face Agents Course → 《深入理解 AI Agent》→ Hermes Agent 橙皮书
- **进阶（Harness 工程）**：《御舆：解码 Agent Harness》→ harness-books → Harness Engineering 橙皮书
- **面试 / 求职**：AIGC-Interview-Book + Awesome-Agent-Papers
- **动手实践**：Generative AI with LangChain → Hands-On Intelligent Agents with OpenAI Gym
