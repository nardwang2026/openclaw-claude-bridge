"""
OpenClaw Claude Bridge - 让 OpenClaw 无缝调用 Claude Code

修复了嵌套调用问题，支持在 Claude Code 内部调用 Claude Code。

示例:
    >>> from openclaw_claude_bridge import ClaudeCodeHelper
    >>> helper = ClaudeCodeHelper()
    >>> result = helper.call("请检查 Git 状态")
    >>> print(result)

特性:
    - 自动处理 CLAUDECODE 环境变量（支持嵌套调用）
    - 智能回退（Claude → Codex）
    - 超时保护
    - 详细日志
"""

from .helper import ClaudeCodeHelper

__version__ = "1.0.0"
__author__ = "nardwang2026"
__all__ = ["ClaudeCodeHelper"]
