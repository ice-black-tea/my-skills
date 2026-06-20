---
name: document-polish
description: Polishes reports and other documents by removing AI-generated writing tells and, for Markdown, fixing rendering compatibility issues. Use when editing or polishing report-style documents before sharing.
---

# Document Polish

## Overview

两层独立打磨，互不依赖：

1. **内容层** — 去除 AI 写作痕迹，让文字更有人味。规则详情见 [humanize-patterns.md](humanize-patterns.md)。
2. **格式层** — 仅当文档是 Markdown 时执行，修正渲染兼容问题。规则详情见 [markdown-format.md](markdown-format.md)。

**先内容、后格式**：反过来的话，内容改写会打乱已处理好的标题编号和空行。只需要一层时可以只做对应阶段。

## 阶段一：去除 AI 写作痕迹

对照 [humanize-patterns.md](humanize-patterns.md) 的 22 条模式逐句改写，保留原意和语气。光删痕迹不够，还要注入个性：有观点、变化句子节奏、适当用"我"、承认复杂感受——避免读起来像维基百科或新闻稿。

**检查清单：**
- 连续三句长度雷同？打断一句
- 段落结尾都很工整？变化收尾方式
- 揭示前用了破折号？删掉
- 解释了隐喻/比喻？相信读者能懂，删掉解释
- 出现"此外""然而"等连接词？考虑删除
- 三段式列举？改成两项或四项
- 出现填充短语、过度限定、讨好语气？直接删

**模式索引**（完整规则+例子见 [humanize-patterns.md](humanize-patterns.md)）：
内容模式（1-6：意义遗产/知名度/状语堆砌/宣传语言/模糊归因/挑战展望套路）、
语言语法模式（7-12：AI 词汇/系动词回避/否定式排比/三段式/同义词循环/虚假范围）、
风格模式（13-16：破折号/粗体/内联标题列表/表情符号，含仅英文适用提示）、
交流模式（17-19：协作痕迹/知识截止声明/谄媚语气）、
填充与回避（20-22：填充短语/过度限定/通用积极结论）。

完成后按 5 维度打分（直接性/节奏/信任度/真实性/精炼度，各 1-10 分，共 50）：45+ 优秀，35-44 良好，低于 35 需重写。

## 阶段二：Markdown 渲染兼容

仅 Markdown 文档执行；完整规则与常见错误见 [markdown-format.md](markdown-format.md)。摘要：

1. **标题编号** — `##`→`N.`，`###`→`N.N`，`####`→`N.N.N`
2. **表格/列表内禁用内联语法** — 不得用 `**加粗**`、`*斜体*`
3. **代码块兼容性** — Markdown 代码块改 ` ```text `；内含三反引号改四反引号
4. **空行** — 只保留表格后一行、代码块内部、段落间，其余全删

执行顺序：标题编号 → 表格/列表语法 → 代码块 → 最后删空行（避免前几步引入新空行）。

## 处理流程

1. 读输入
2. **阶段一：** 对照 humanize-patterns.md 识别并重写 AI 痕迹
3. **阶段二：** 若文本是 Markdown，套用渲染兼容修正
4. 输出最终版本，可附简要说明

## 参考

- 阶段一基于 [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（WikiProject AI Cleanup），整理自 op7418/Humanizer-zh，参考 blader/humanizer、hardikpandya/stop-slop。
- 阶段二为原创规则，源于飞书解析限制，适用于有类似限制的任何 Markdown 渲染器。
