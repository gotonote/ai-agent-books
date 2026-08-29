# 📚 AI Agent 热门书单（GitHub 开源仓库整理）

> [🇬🇧 English Version](README.en.md)
>
> 整理自 GitHub 上与 **AI Agent / LLM Agent / Agentic Engineering** 相关的热门开源书籍、教程与配套代码仓库。
> 数据抓取时间：2026-08-29 · Star 数由 GitHub Actions 每日自动更新，按热门度排序。

<p align="center">
  <a href="https://github.com/gotonote/awesome-agent-boom/stargazers">
    <img src="https://img.shields.io/badge/⭐-觉得这份书单有用？点个 Star 支持一下-6c8cff?style=for-the-badge" alt="Star us">
  </a>
</p>

[![GitHub stars](https://img.shields.io/github/stars/gotonote/awesome-agent-boom?style=flat-square)](https://github.com/gotonote/awesome-agent-boom/stargazers)
[![在线书单](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E4%B9%A6%E5%8D%95-gotonote.github.io-blue?style=flat-square)](https://gotonote.github.io/awesome-agent-boom/)
[![收录仓库](https://img.shields.io/badge/books-62-blue?style=flat-square)]()
[![Last commit](https://img.shields.io/github/last-commit/gotonote/awesome-agent-boom?style=flat-square)]()
[![Stars 自动更新](https://img.shields.io/github/actions/workflow/status/gotonote/awesome-agent-boom/update-stars.yml?style=flat-square&label=stars%20update)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

## ✨ 为什么收藏这份书单

- **数据是活的**：Star 数由 GitHub Actions 每日自动抓取更新，榜单永不落伍
- **精选不注水**：62 个仓库按七大主题整理，每个标注难度（🟢 入门 / 🟡 进阶 / 🔴 深度）
- **双端可读**：中英双语 README + 响应式[在线书单](https://gotonote.github.io/awesome-agent-boom/)网页版
- **每日黑板报**：工作日自动精选全球 AI / 科技要闻（[在线黑板报](docs/blackboard.html)）

📈 Star 增长趋势：

[![Star History Chart](https://api.star-history.com/svg?repos=gotonote/awesome-agent-boom&type=Date)](https://star-history.com/#gotonote/awesome-agent-boom&Date)

> 💡 想推荐新书 / 发现错误？[提 Issue](https://github.com/gotonote/awesome-agent-boom/issues/new) 或直接 [提交 PR](https://github.com/gotonote/awesome-agent-boom/compare)，1 分钟即可完成，欢迎共建！

---

## 📑 目录

- [📰 黑板报（每日 AI 科技要闻）](#blackboard)
- [📖 一、开源图书（中文）](#chinese-books)
- [🌍 二、开源图书 / 课程（英文）](#english-books)
- [📦 三、商业图书配套代码仓库](#commercial-code)
- [📑 四、论文清单 / 资源汇总](#papers-resources)
- [🛠️ 五、Agent 规则书 / 编码 Agent 技能集](#agent-rules)
- [✍️ 六、AI Agent 写书实验](#ai-writing)
- [🧩 七、Agent Harness 生态](#harness-ecosystem)
- [🔍 推荐阅读路线](#roadmap)

---

## <a id="blackboard"></a>📰 黑板报 · 每日 AI 科技要闻

工作日每天 09:00（北京时间）自动出刊一期「黑板报」，从 Hacker News、少数派、InfoQ、量子位、IT之家 的热门内容中精选全球 AI / 科技要闻：[在线黑板报](docs/blackboard.html)。

- 🏠 主页展示**最近一周**，往期全部**存档留存**（[docs/blackboard/](docs/blackboard/) 每日一篇）
- ✍️ 每期含今日头条、分类速览与编辑手记

---

## <a id="chinese-books"></a>📖 一、开源图书（中文）

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) | ⭐ 43.0k | 🟢 入门 · **《深入理解 AI Agent：设计原理与工程实践》**（李博杰 著）开源主仓库：全书正文、编译版 PDF 与按章配套代码。目前最热的中文 Agent 书籍 |
| [alchaincyf/hermes-agent-orange-book](https://github.com/alchaincyf/hermes-agent-orange-book) | ⭐ 4.9k | 🟢 入门 · **Hermes Agent 从入门到精通 · 橙皮书系列**：Nous Research 开源 AI Agent 框架实战指南 |
| [lintsinghua/claude-code-book](https://github.com/lintsinghua/claude-code-book) | ⭐ 4.2k | 🟡 进阶 · **《御舆：解码 Agent Harness》**：42 万字拆解 AI Agent 的 Harness 骨架，15 章从对话循环到构建你自己的 Agent Harness |
| [datagallery-lab/enterprise_agent_platform](https://github.com/datagallery-lab/enterprise_agent_platform) | ⭐ 256 | 🔴 深度 · **《企业级 Agent 平台工程》**：首本专注企业级 Agent 平台工程的开源书——框架选型、治理与可观测性 |
| [yeasy/harness_engineering_guide](https://github.com/yeasy/harness_engineering_guide) | ⭐ 117 | 🟡 进阶 · **Harness 工程指南**：智能体 = 大模型 + Harness，深入剖析 Harness 工程原理、设计、实现与实践 |
| [alchaincyf/harness-engineering-orange-book](https://github.com/alchaincyf/harness-engineering-orange-book) | ⭐ 95 | 🟡 进阶 · **Harness Engineering · 橙皮书系列**：AI Agent 缰绳工程学实战指南 |
| [dawei008/openbook](https://github.com/dawei008/openbook) | ⭐ 34 | 🟡 进阶 · **OpenBook: AI Agent Harness Engineering**：构建生产级 Agent Harness 的开源图书（26 章） |

## <a id="english-books"></a>🌍 二、开源图书 / 课程（英文）

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [huggingface/agents-course](https://github.com/huggingface/agents-course) | ⭐ 31.7k | 🟢 入门 · **Hugging Face Agents Course**：最流行的 Agent 入门课程（教材免费开源） |
| [ed-donner/agents](https://github.com/ed-donner/agents) | ⭐ 6.1k | 🟡 进阶 · **Complete Agentic AI Engineering**：Ed Donner 完整 Agentic AI 工程课程配套仓库 |
| [decodingai-magazine/second-brain-ai-assistant-course](https://github.com/decodingai-magazine/second-brain-ai-assistant-course) | ⭐ 3.1k | 🟢 入门 · **Second Brain AI 助手课程**：用 LLM + Agents 构建自己的第二大脑 AI 助手 |
| [wquguru/harness-books](https://github.com/wquguru/harness-books) | ⭐ 2.9k | 🟡 进阶 · **Harness Engineering 两卷本**：Claude Code 与 Codex 背后的设计哲学（约束、查询循环等） |
| [emarco177/langchain-course](https://github.com/emarco177/langchain-course) | ⭐ 1.6k | 🟢 入门 · **LangChain 课程**：项目驱动的 AI Agent 开发实战（LangChain 讲师出品） |
| [neural-maze/realtime-phone-agents-course](https://github.com/neural-maze/realtime-phone-agents-course) | ⭐ 1.1k | 🟡 进阶 · **实时语音 Agent 课程**：用 FastRTC 构建低延迟实时 AI 语音 Agent |
| [https-deeplearning-ai/agentic-ai-public](https://github.com/https-deeplearning-ai/agentic-ai-public) | ⭐ 664 | 🟢 入门 · **Agentic Workflow 课程**（DeepLearning.AI）：Agentic AI 研究助手实战 |
| [bryanyzhu/agentic-ai-system-course](https://github.com/bryanyzhu/agentic-ai-system-course) | ⭐ 590 | 🟡 进阶 · **Agentic AI 系统课程**：以 Agent 教 Agent——从设计到部署的骨架课程 |
| [gerred/building-an-agentic-system](https://github.com/gerred/building-an-agentic-system) | ⭐ 324 | 🟡 进阶 · **Building an Agentic System**：深入构建类 Claude Code 式 Agentic 系统的书籍与参考 |
| [jayminwest/agentic-engineering-book](https://github.com/jayminwest/agentic-engineering-book) | ⭐ 197 | 🟢 入门 · **Agentic Engineering**：构建 Agentic 系统的综合渐进式指南 |
| [Siddhant-K-code/agentic-engineering-guide](https://github.com/Siddhant-K-code/agentic-engineering-guide) | ⭐ 157 | 🟢 入门 · **Agentic Engineering Guide**（MDX 格式，交互式阅读） |
| [AkmmusAI/LLM-Prompt-Engineering-Simplified-Book](https://github.com/AkmmusAI/LLM-Prompt-Engineering-Simplified-Book) | ⭐ 130 | 🟢 入门 · **LLM Prompt 工程简化指南**：从零开始的提示工程开源书 |
| [Drobiazkin/ai-agent-architecture](https://github.com/Drobiazkin/ai-agent-architecture) | ⭐ 46 | 🟡 进阶 · **Build LLM systems you actually control**：免费开源工程书 + 课程，从 tokenization 讲起 |
| [caozhiyi/ai-programming-book](https://github.com/caozhiyi/ai-programming-book) | ⭐ 41 | 🟡 进阶 · **The First Principles of AI Programming**：从底层物理约束出发讲 AI 编程 |
| [awsm-research/agentic-swe-book](https://github.com/awsm-research/agentic-swe-book) | ⭐ 10 | 🟡 进阶 · **Agentic Software Engineering: A Practical Guide for the AI-Native Engineer** |

## <a id="commercial-code"></a>📦 三、商业图书配套代码仓库

| 仓库 | Star | 对应图书 |
| --- | --- | --- |
| [benman1/generative_ai_with_langchain](https://github.com/benman1/generative_ai_with_langchain) | ⭐ 1.4k | 🟢 入门 · *Generative AI with LangChain*（O'Reilly）：用 Python、LangChain、LangGraph 构建生产级 LLM 应用与高级 Agent |
| [towardsai/ragbook-notebooks](https://github.com/towardsai/ragbook-notebooks) | ⭐ 558 | 🟡 进阶 · *Building LLMs for Production*（Towards AI）配套 Notebook |
| [treygrainger/ai-powered-search](https://github.com/treygrainger/ai-powered-search) | ⭐ 404 | 🟡 进阶 · *AI-Powered Search*（Manning, 2025）代码库 |
| [PacktPublishing/Hands-On-Intelligent-Agents-with-OpenAI-Gym](https://github.com/PacktPublishing/Hands-On-Intelligent-Agents-with-OpenAI-Gym) | ⭐ 400 | 🟢 入门 · *Hands-On Intelligent Agents with OpenAI Gym*：深度强化学习 Agent 入门 |
| [Nipi64310/RAG-Book](https://github.com/Nipi64310/RAG-Book) | ⭐ 288 | 🟢 入门 · 《大模型 RAG 实战》配套代码与资料（中文） |
| [abhinav-kimothi/A-Simple-Guide-to-RAG](https://github.com/abhinav-kimothi/A-Simple-Guide-to-RAG) | ⭐ 274 | 🟡 进阶 · *A Simple Guide to RAG* 配套代码：RAG 图解实战 |
| [tomasonjo/kg-rag](https://github.com/tomasonjo/kg-rag) | ⭐ 177 | 🔴 深度 · *Essential GraphRAG* 配套仓库（Manning）：知识图谱 + RAG |

## <a id="papers-resources"></a>📑 四、论文清单 / 资源汇总

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | ⭐ 13.4k | 🟡 进阶 · **DeepSeek Harness 插件精选清单**：dsh 生态插件大全（类 awesome 列表） |
| [WangRongsheng/awesome-LLM-resources](https://github.com/WangRongsheng/awesome-LLM-resources) | ⭐ 8.9k | 🟢 入门 · LLM 资料大全：多模态、Agent、MCP、模型训练/推理等 |
| [WooooDyy/LLM-Agent-Paper-List](https://github.com/WooooDyy/LLM-Agent-Paper-List) | ⭐ 8.2k | 🔴 深度 · SCIS 封面论文 *The Rise and Potential of LLM-based Agents* 配套论文清单 |
| [WeThinkIn/AIGC-Interview-Book](https://github.com/WeThinkIn/AIGC-Interview-Book) | ⭐ 4.5k | 🟡 进阶 · AIGC/LLM/AI Agent 算法工程师面试资源平台（三年面试五年模拟） |
| [luo-junyu/Awesome-Agent-Papers](https://github.com/luo-junyu/Awesome-Agent-Papers) | ⭐ 2.8k | 🔴 深度 · LLM Agent 综述：方法论、应用与挑战（持续更新） |
| [Picrew/awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness) | ⭐ 1.7k | 🟡 进阶 · **awesome-agent-harness**：Agent Harness 工程资源精选 |
| [weitianxin/Awesome-Agentic-Reasoning](https://github.com/weitianxin/Awesome-Agentic-Reasoning) | ⭐ 1.4k | 🔴 深度 · 基于 *Agentic Reasoning for LLMs* 综述整理的资源清单 |
| [RyanAlberts/best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses) | ⭐ 734 | 🟡 进阶 · **best-of-Agent-Harnesses**：100+ 个 Agent Harness 精选排行（含 MCP 生态） |
| [YennNing/Awesome-Code-as-Agent-Harness-Papers](https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers) | ⭐ 661 | 🔴 深度 · **Code-as-Agent-Harness 论文清单**：基于同名综述整理的论文与资源 |
| [Gloriaameng/Awesome-Agent-Harness](https://github.com/Gloriaameng/Awesome-Agent-Harness) | ⭐ 342 | 🔴 深度 · **Awesome Agent Harness**：LLM Agent Harness 综述配套资源清单 |
| [mahonzhan/awesome-agent-harness](https://github.com/mahonzhan/awesome-agent-harness) | ⭐ 269 | 🟡 进阶 · **awesome-agent-harness**：Agent Harness / 框架 / 工作流精选清单 |

## <a id="agent-rules"></a>🛠️ 五、Agent 规则书 / 编码 Agent 技能集

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books) | ⭐ 2.6k | 🟡 进阶 · **AGENTS.md rules / skills for AI coding agents**：Codex、Cursor & Claude Code 的规则与技能书，灵感来自 Clean Code |
| [deusyu/translate-book](https://github.com/deusyu/translate-book) | ⭐ 1.2k | 🟢 入门 · **translate-book**：面向 Codex / Claude Code / OpenClaw 的图书翻译 Agent 技能 |
| [Belkins/ai-dive-deep](https://github.com/Belkins/ai-dive-deep) | ⭐ 369 | 🟡 进阶 · **AI Dive Deep（Vlad's Playbook）**：48 章 Operator 实战手册，拆解 AI 操作员技能 |
| [keli-wen/agentic-harness-patterns-skill](https://github.com/keli-wen/agentic-harness-patterns-skill) | ⭐ 303 | 🟡 进阶 · **Agentic Harness Patterns Skill**：内存 / 权限 / 上下文管理的 Harness 工程技能 |
| [davisjam/model-based-agentic-software-engineering](https://github.com/davisjam/model-based-agentic-software-engineering) | ⭐ 18 | 🔴 深度 · **MAGE**：Model-Based Agentic Software Engineering 书籍 / 网站 / 技能集 |

## <a id="ai-writing"></a>✍️ 六、AI Agent 写书实验

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [mind-protocol/terminal-velocity](https://github.com/mind-protocol/terminal-velocity) | ⭐ 1.1k | 🟢 入门 · 由 10 个 AI Agent 组成的团队自主创作的长篇小说（可作 Agent 协作案例研究） |
| [adamwlarson/ai-book-writer](https://github.com/adamwlarson/ai-book-writer) | ⭐ 393 | 🟢 入门 · 用 AutoGen 实验：验证 AI Agent 能否独立写完一本书 |
| [vkorost/weekend-diy-book](https://github.com/vkorost/weekend-diy-book) | ⭐ 24 | 🟢 入门 · *Claude Code: The Definitive Guide to Agentic Development* —— 一个周末用 Agent 写成的技术书 |

## <a id="harness-ecosystem"></a>🧩 七、Agent Harness 生态

| 仓库 | Star | 说明 |
| --- | --- | --- |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | ⭐ 244.0k | 🟡 进阶 · **ECC: Agent Harness 性能优化系统**：Skills / Instincts / Memory / Security，服务 Claude Code、Codex、OpenCode 等 |
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | ⭐ 202.3k | 🟡 进阶 · **DeepSeek Harness**：「万物皆插件」的官方开源 Agent Harness，上线两周即破 20 万 Star |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | ⭐ 81.1k | 🟡 进阶 · **Deer Flow（字节跳动）**：开源长周期 SuperAgent Harness，研究 / 编码 / 创作一体，沙箱 + 记忆 + 工具 + 子 Agent |
| [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | ⭐ 75.6k | 🟢 入门 · **learn-claude-code**：从 0 到 1 手写一个 nano Claude Code 式 Agent Harness（Bash is all you need） |
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | ⭐ 68.5k | 🟡 进阶 · **omo/lazycodex**：面向复杂代码库的编码 Agent Harness，专为 Codex / OpenCode 打造 |
| [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | ⭐ 46.7k | 🟢 入门 · **CowAgent**：开源超级 AI 助手 + Agent Harness，自主规划任务、调用工具与技能、记忆自进化（原 chatgpt-on-wechat） |
| [wshobson/agents](https://github.com/wshobson/agents) | ⭐ 39.2k | 🟡 进阶 · **Multi-harness 插件市场**：Claude Code / Codex / Cursor / OpenCode 通用插件市场 |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | ⭐ 28.7k | 🟡 进阶 · **Deep Agents**：LangChain 官方「全家桶」Agent Harness（batteries-included） |
| [anywhere-labs/dsh-desktop](https://github.com/anywhere-labs/dsh-desktop) | ⭐ 21.6k | 🟢 入门 · **DSH Desktop**：DeepSeek Harness 插件生态的现代化桌面端，「桌面本身也是插件」 |
| [visa/visa-vulnerability-agentic-harness](https://github.com/visa/visa-vulnerability-agentic-harness) | ⭐ 2.6k | 🟡 进阶 · **Visa Vulnerability Agentic Harness**：Visa 开源漏洞挖掘 Agent Harness |
| [china-qijizhifeng/agentic-harness-engineering](https://github.com/china-qijizhifeng/agentic-harness-engineering) | ⭐ 855 | 🟡 进阶 · **Agentic Harness Engineering（AHE）**：可观测性驱动的 Harness 工程官方代码 |
| [Darwin-Agent/HarnessX](https://github.com/Darwin-Agent/HarnessX) | ⭐ 452 | 🟡 进阶 · **HarnessX**：Harness 锻造厂——一键锻造任意 Agent Harness 组合 |
| [ApodexAI/AgentHarness](https://github.com/ApodexAI/AgentHarness) | ⭐ 424 | 🔴 深度 · **AgentHarness**：Apodex-1.0 深度研究基准评估 Harness |
| [CodelyTV/agent-harness](https://github.com/CodelyTV/agent-harness) | ⭐ 231 | 🟡 进阶 · **agent-harness（CodelyTV）**：Skills / 插件 / Hooks 一体的团队 Agent Harness |

---

## <a id="roadmap"></a>🔍 推荐阅读路线

- **入门**：Hugging Face Agents Course → 《深入理解 AI Agent》→ Hermes Agent 橙皮书
- **进阶（Harness 工程）**：《御舆：解码 Agent Harness》→ harness-books → Harness Engineering 橙皮书
- **面试 / 求职**：AIGC-Interview-Book + Awesome-Agent-Papers
- **动手实践**：Generative AI with LangChain → Hands-On Intelligent Agents with OpenAI Gym
