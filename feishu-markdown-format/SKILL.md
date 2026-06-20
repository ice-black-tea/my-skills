---
name: feishu-markdown-format
description: Use when formatting or editing Markdown documents intended for pasting into Feishu — blank lines are excessive, heading numbers are missing or mismatched, tables/lists contain bold/italic syntax, or code blocks may cause Feishu rendering errors.
---

# Feishu Markdown 格式化

## 概述

飞书对 Markdown 有特定解析限制，本 skill 定义四条规则使文档在飞书中正确渲染。

## 规则

### 1. 空行

保留以下三种空行，其余全部删除：
- 表格后恰好一行（否则后续段落被解析为表格的一部分）
- 代码块内部的空行（示例内容，不得删除）
- 相邻两段正文之间的空行（删除则合并为一段）

删除的位置：标题前后、段落↔列表、段落↔代码块（前后均删）、段落↔表格前、段落↔引用块、图片↔段落。

### 2. 标题编号

各级标题手动添加编号，层级与格式须一一对应：

| Markdown 层级 | 编号格式 | 示例 |
|---|---|---|
| `##` | N. | `## 1. 背景` |
| `###` | N.N | `### 1.1 方案` |
| `####` | N.N.N | `#### 1.1.1 细节` |

### 3. 表格和列表内禁用内联语法

表格单元格和列表条目内，不得使用 `**加粗**`、`*斜体*` 等内联语法（飞书不兼容）。段落正文内可正常使用。

### 4. 代码块兼容性

- 内容为 Markdown 格式的代码块 → 改用 ` ```text ` 渲染为纯文本
- 代码块内部含三反引号 ` ``` ` → 改用四反引号 ` ```` ` 包装整个代码块

## 执行顺序

1. 修正标题层级与编号
2. 清除表格/列表内的内联语法
3. 处理代码块兼容性
4. 最后删除所有非必要空行（最后处理避免前几步引入新空行）

## 常见错误

| 错误 | 症状 | 修正 |
|---|---|---|
| 层级与编号不符 | `## 1.1` 应为 `### 1.1` | 对齐层级 |
| 表格后无空行 | 后续段落渲染为表格行 | 补一行空行 |
| 列表内有加粗 | 飞书显示 `**文字**` 原文 | 去掉 `**` |
| 代码块含三反引号 | 代码块提前闭合 | 改用四反引号 |
| Markdown 代码块 | 内层语法被飞书解析 | 改用 text 标签 |
