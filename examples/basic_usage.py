#!/usr/bin/env python3
"""
基础使用示例

展示 ClaudeCodeHelper 的基本功能
"""

from openclaw_claude_bridge import ClaudeCodeHelper


def main():
    print("=" * 50)
    print("OpenClaw Claude Bridge - 基础使用示例")
    print("=" * 50)

    # 创建助手实例
    helper = ClaudeCodeHelper()

    # 检查状态
    print("\n1. 检查 Claude Code 状态:")
    status = helper.check_status()
    for key, value in status.items():
        print(f"   {key}: {value}")

    if not status['any_available']:
        print("\n❌ Claude Code 和 Codex 都不可用，请先安装")
        return

    # 简单调用示例
    print("\n2. 简单调用示例:")
    result = helper.call("请回复 'Hello from OpenClaw!'")
    print(f"   结果: {result[:100]}...")

    # 带上下文的调用
    print("\n3. 带上下文的调用:")
    context = "当前工作目录是示例项目"
    result = helper.call("请告诉我当前工作目录", context=context)
    print(f"   结果: {result[:100]}...")

    print("\n" + "=" * 50)
    print("示例完成！")


if __name__ == "__main__":
    main()
