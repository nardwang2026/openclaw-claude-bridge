#!/usr/bin/env python3
"""
GitHub 同步示例

展示如何使用 git_sync 方法同步代码到 GitHub
"""

import os
from openclaw_claude_bridge import ClaudeCodeHelper


def main():
    print("=" * 50)
    print("OpenClaw Claude Bridge - GitHub 同步示例")
    print("=" * 50)

    helper = ClaudeCodeHelper()

    # 示例 1: 同步当前目录
    print("\n1. 同步当前目录:")
    current_dir = os.getcwd()
    print(f"   目录: {current_dir}")
    result = helper.git_sync(current_dir)
    print(f"   结果:\n{result}")

    # 示例 2: 同步指定目录（如果存在）
    print("\n2. 同步指定目录:")
    home_dir = os.path.expanduser("~")
    test_dir = os.path.join(home_dir, "Documents")

    if os.path.exists(test_dir):
        print(f"   目录: {test_dir}")
        result = helper.git_sync(test_dir)
        print(f"   结果:\n{result}")
    else:
        print(f"   目录不存在: {test_dir}")

    print("\n" + "=" * 50)
    print("示例完成！")


if __name__ == "__main__":
    main()
