#!/usr/bin/env python3
"""Structural validator for the superpower-autopilot skill.

Performs STRUCTURAL checks only (frontmatter, orchestration sequencing, required
references) and does NOT verify prose is meaningful or behaviorally correct —
semantic coverage comes from the writing-skills behavioral dry-run.

Pure stdlib. Run `python validate.py`; it validates the SKILL.md sitting
next to it. Exit 0 on success, 1 on any failed check.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE / "SKILL.md"

# Orchestration stages, in required order.
ORCHESTRATION_SEQUENCE = [
    "brainstorming",
    "writing-plans",
    "using-git-worktrees",
    "subagent-driven-development",
    "test-driven-development",
    "verification-before-completion",
    "finishing-a-development-branch",
]

# Each marker: human label -> list of acceptable substrings (any one satisfies).
TRIPWIRES = {
    "data loss / destructive migration": ["数据丢失", "破坏性迁移"],
    "security / secrets": ["密钥", "安全风险"],
    "unresolvable architecture fork": ["架构方向", "架构分叉"],
    "spec contradicts existing code": ["根本矛盾", "根本性矛盾"],
}
BOUNDARIES = {
    "no deleting user data": ["不删除用户数据", "不删用户数据", "删除用户数据"],
    "no production secrets": ["生产密钥", "token / 私有配置", "密钥 / token"],
    "no auto push": ["不自动 push", "不 push", "自动 push"],
    "no auto PR / merge": ["不自动建 PR", "自动建 PR", "自动 merge", "不 merge"],
}

MAX_WORDS = 1500  # thin-orchestrator guard (word-based)
MAX_CHARS = 6000  # thin-orchestrator guard (char-based, for CJK)


def fail(errors, msg):
    print(f"FAIL: {msg}")
    errors.append(msg)


def main() -> int:
    errors: list[str] = []
    if not SKILL.exists():
        print("FAIL: SKILL.md not found next to validate.py")
        return 1
    text = SKILL.read_text(encoding="utf-8")

    fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not fm:
        fail(errors, "missing YAML frontmatter block")
        front, body = "", text
    else:
        front, body = fm.group(1), text[fm.end():]

    name_m = re.search(r"^name:\s*(.+?)\s*$", front, re.MULTILINE)
    if not name_m:
        fail(errors, "frontmatter missing name")
    elif name_m.group(1).strip() != HERE.name:
        fail(errors, f"name '{name_m.group(1).strip()}' != directory '{HERE.name}'")

    desc_m = re.search(r"^description:\s*(.+?)\s*$", front, re.MULTILINE)
    if not desc_m:
        fail(errors, "frontmatter missing description")
    else:
        desc = desc_m.group(1).strip().strip('"').strip("'")
        if not desc:
            fail(errors, "description is empty")
        elif not desc.startswith("Use when"):
            fail(errors, "description must start with 'Use when'")

    last_idx = -1
    for skill in ORCHESTRATION_SEQUENCE:
        idx = body.find(skill)
        if idx == -1:
            fail(errors, f"orchestration stage '{skill}' not referenced in body")
        elif idx < last_idx:
            fail(errors, f"orchestration stage '{skill}' out of order")
        else:
            last_idx = idx

    if not re.search(r"N\s*=\s*3", body) and "重试上限" not in body and "bounded" not in body.lower():
        fail(errors, "bounded-retry limit (e.g. N=3) not documented")

    for label, subs in TRIPWIRES.items():
        if not any(s in body for s in subs):
            fail(errors, f"tripwire not documented: {label}")

    for label, subs in BOUNDARIES.items():
        if not any(s in body for s in subs):
            fail(errors, f"delivery boundary not documented: {label}")

    words = len(body.split())
    if words > MAX_WORDS:
        fail(errors, f"body has {words} words (> {MAX_WORDS}); orchestrate, don't copy sub-skills")

    chars = len(body)
    if chars > MAX_CHARS:
        fail(errors, f"body has {chars} chars (> {MAX_CHARS}); orchestrate, don't copy sub-skills")

    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        return 1
    print(f"OK: all structural checks passed ({words} words).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
