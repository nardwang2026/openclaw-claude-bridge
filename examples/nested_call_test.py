#!/usr/bin/env python3
"""
嵌套调用测试

验证在 Claude Code 内部调用 Claude Code 是否正常工作
"""

import os
from openclaw_claude_bridge import ClaudeCodeHelper


def main():
    print("=" * 50)
    print("OpenClaw Claude Bridge - 嵌套调用测试")
    print("=" * 50)

    # 检查是否在 Claude Code 内部
    if 'CLAUDECODE' in os.environ:
        print("\n✅ 检测到在 Claude Code 内部运行")
        print("   正在测试嵌套调用...")
    else:
        print("\n⚠️  不在 Claude Code 内部")
        print("   此测试主要用于验证嵌套调用场景")
        print("   要在嵌套环境中测试，请在 Claude Code 中运行此脚本")

    # 创建助手实例
    helper = ClaudeCodeHelper()

    # 测试嵌套调用
    print("\n1. 测试简单调用:")
    result = helper.call("请回复 'NESTED_CALL_SUCCESS'")

    if 'NESTED_CALL_SUCCESS' in result or 'nested_call_success' in result.lower():
        print("   ✅ 嵌套调用成功！")
        print(f"   响应: {result.strip()}")
    else:
        print("   ❌ 嵌套调用可能失败")
        print(f"   响应: {result[:200]}")

    # 测试多次调用
    print("\n2. 测试多次调用:")
    for i in range(3):
        result = helper.call(f"请回复 'TEST_{i+1}'", verbose=False)
        print(f"   调用 {i+1}: {'✅' if f'TEST_{i+1}' in result else '❌'}")

    print("\n" + "=" * 50)
    print("测试完成！")


if __name__ == "__main__":
    main()
