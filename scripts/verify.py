#!/usr/bin/env python3
"""
OpenClaw Claude Bridge 安装验证脚本
"""

import sys
import shutil
import os


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    return version.major == 3 and version.minor >= 7


def check_claude_code():
    """检查 Claude Code 是否可用"""
    return shutil.which('claude') is not None


def check_codex():
    """检查 Codex 是否可用"""
    return shutil.which('codex') is not None


def check_helper_module():
    """检查 helper 模块是否可以导入"""
    try:
        from openclaw_claude_bridge import ClaudeCodeHelper
        return True
    except ImportError as e:
        print(f"  ❌ 导入失败: {e}")
        return False


def test_nested_call():
    """测试嵌套调用"""
    try:
        from openclaw_claude_bridge import ClaudeCodeHelper
        helper = ClaudeCodeHelper(verbose=False)

        # 简单测试调用
        result = helper.call("请回复 'PONG'")

        if 'PONG' in result or 'pong' in result.lower():
            return True, "嵌套调用测试成功"
        else:
            return False, f"响应不符合预期: {result[:100]}"
    except Exception as e:
        return False, str(e)


def main():
    print("🧪 OpenClaw Claude Bridge 验证")
    print("=" * 40)

    all_passed = True

    # 1. 检查 Python 版本
    print("\n1. 检查 Python 版本...")
    if check_python_version():
        print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(f"  ⚠️  Python 版本过低 (需要 3.7+)")
        all_passed = False

    # 2. 检查 Claude Code
    print("\n2. 检查 Claude Code...")
    if check_claude_code():
        print("  ✅ Claude Code 已安装")
    else:
        print("  ⚠️  Claude Code 未安装 (可选)")

    # 3. 检查 Codex
    print("\n3. 检查 Codex...")
    if check_codex():
        print("  ✅ Codex 已安装")
    else:
        print("  ⚠️  Codex 未安装 (可选)")

    if not check_claude_code() and not check_codex():
        print("\n  ❌ 错误: Claude Code 和 Codex 都未安装")
        print("     请先安装其中之一才能使用")
        all_passed = False

    # 4. 检查模块导入
    print("\n4. 检查模块导入...")
    if check_helper_module():
        print("  ✅ 模块可以正常导入")
    else:
        print("  ❌ 模块导入失败")
        print("     请确保 PYTHONPATH 配置正确:")
        print(f"     export PYTHONPATH=\"$PYTHONPATH:{os.path.expanduser('~/.openclaw-claude-bridge')}\"")
        all_passed = False

    # 5. 测试嵌套调用（如果在 Claude Code 内部）
    print("\n5. 测试嵌套调用...")
    if 'CLAUDECODE' in os.environ:
        print("  ℹ️  检测到在 Claude Code 内部运行")
        if check_claude_code() or check_codex():
            success, msg = test_nested_call()
            if success:
                print(f"  ✅ {msg}")
            else:
                print(f"  ❌ {msg}")
                all_passed = False
        else:
            print("  ⚠️  跳过测试（Claude Code/Codex 未安装）")
    else:
        print("  ℹ️  不在 Claude Code 内部，跳过嵌套测试")
        print("     要在嵌套环境中测试，请在 Claude Code 中运行此脚本")

    # 总结
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ 所有检查通过！")
        print("\n你现在可以使用了:")
        print("  from openclaw_claude_bridge import ClaudeCodeHelper")
        return 0
    else:
        print("❌ 部分检查失败，请查看上方信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
