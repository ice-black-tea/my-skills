---
name: superpower-autopilot
description: Use when a coding request would trigger any superpower command (brainstorming, writing-plans, etc.) — this skill is the gate and MUST run first: it triages, doing small/low-risk changes inline and routing the rest into the full superpower pipeline.
---

# Superpower Autopilot

## Overview
给定编码需求后，**先分诊再执行**：小而确定的就地做完，其余**除 brainstorming 外全程自治到底**。
本 skill 拦截 superpower 命令——任何会触发 Superpowers 重流程的编码任务都由它接管：要么走快速通道，
要么按固定顺序编排既有 Superpowers 技能，并施加"自治契约"（自审替代人审、有界重试、明确停机条件）。
**不复制被编排技能的内容；需要细节时打开对应技能。**

**核心原则：** 自治 ≠ 莽撞；小需求不堆重流程，大需求不打断用户，不可逆后果绝不自作主张，判不准就问。

## 前置依赖
本 skill 只编排、不自带实现，**依赖 Superpowers 技能包**（brainstorming / writing-plans /
using-git-worktrees / subagent-driven-development / test-driven-development /
verification-before-completion / finishing-a-development-branch）。环境未安装则先按官方文档安装：
https://github.com/obra/superpowers ，否则编排阶段无法 invoke。

## 分诊闸门（入口，三选一）
**① 走快速通道** —— 需求同时满足四条：单文件、少量行（约 < 20 行）；无新依赖、无 schema / 架构变更；
可逆且低风险（不碰生产密钥 / 数据 / 破坏性迁移）；措辞明确（含"简单改一下 / 顺手 / quick / typo /
加个日志"等小任务措辞）。→ 就地最小改动、跑能跑的验证并以输出为证据、一两句说明改了什么；
**不开 worktree、不写 spec/plan、不起 subagent、不堆全流程**。做到一半发现超界（蔓延多文件 / 加依赖 /
触架构），立即停手转入下方完整编排，不在快速通道里硬扛。

**② 走完整编排** —— 明显超出上述边界（多文件 / 新依赖 / 架构改动 / 高风险）→ 按"编排顺序"自治跑完。

**③ 停下来问** —— 范围模糊、判不准算大算小时，**不猜、不替用户决定**：问一句"这要走完整流程还是我直接改？"，
由用户拍板。用户显式要求用某流程或每步确认时，以用户为准。

## 编排顺序（完整路径，不可乱序）
1. **brainstorming** — 唯一交互阶段。澄清需求 → 写 spec 到 `docs/superpowers/specs/` → spec 自审。
2. **writing-plans** — 写实现计划到 `docs/superpowers/plans/`。
3. **using-git-worktrees** — 建隔离 worktree；环境受限无法创建则降级当前工作区并**显式说明**。
4. **subagent-driven-development**（默认，不询问执行方式）— 每 task：fresh subagent +
   **test-driven-development**（红→绿→重构）+ spec-compliance & code-quality review；
   Critical/Important 必修复并复审。
5. **verification-before-completion** — 跑真实测试/lint/typecheck，以输出为证据。
6. **finishing-a-development-branch** — 默认 **Keep the branch as-is**；不 merge/push/PR；输出最终总结。

## 自治契约

### 自审替代人审
被编排技能内置的人审门（spec 人审、收尾方式选择等）由**本流程的 self-review 替代**，不停下等人。
唯一保留的人类交互是 brainstorming（及上方分诊的"停下来问"）。

### 有界重试（防"直到达成"退化为空转）
单个 task 的失败修复循环（含 systematic-debugging）**最多 N=3 次**。达上限仍无法转绿，
**停止并如实汇报**：失败现场、已尝试方案、未完成项，交还用户。
**绝不**假装通过、绝不"应该可以"、绝不为完成而弱化或跳过测试。

### Tripwire —— 只在这四类情况停机问用户
1. **数据丢失 / 破坏性迁移**（删库、不可逆 schema 迁移、覆盖用户数据）。
2. **安全风险 / 密钥**（改动生产密钥 / token / 私有配置，或引入安全风险）。
3. **架构方向无法抉择**（需要用户拍板的架构分叉）。
4. **需求与现有代码根本矛盾**（继续会破坏正确性）。

**停机是局部的，不是全局的：** 命中 tripwire 时，只隔离并暂停那一处不安全的改动，
**继续自治交付其余所有不受影响的部分**。最终汇报里点明"哪一处在等你拍板、其余已完成到什么程度"。
其余普通实现歧义（已在完整编排内）：基于仓库风格 + 行业最佳实践合理假设，写进 spec，不停下询问。

### 交付边界（硬禁止）
不删除用户数据；不改生产密钥 / token / 私有配置；不自动 push；不自动建 PR、不自动 merge
（除非用户明确要求）。两条路径同此约束。

## Red Flags — 出现即自检
- "这个小问题先停下来问一下吧" → 完整编排内不是 tripwire 就别停，按合理假设推进。
- "算大算小判不准" → 分诊阶段别猜，问用户，别替他决定要不要上重流程。
- "顺手把周边也重构了吧" → 超出快速通道的最小改动，退出并转完整编排。
- "测试有点烦，先跳过/放宽" → 违反有界重试契约，禁止。
- "应该可以了" → 没跑能跑的验证就不准说完成。
- "顺手 push / 开个 PR 吧" → 交付边界禁止，除非用户明确要求。

## 指令优先级
用户显式指令（CLAUDE.md / AGENTS.md / 直接对话）> 本 skill > 默认系统行为。
若用户要求每步确认或不用 TDD，以用户为准。
