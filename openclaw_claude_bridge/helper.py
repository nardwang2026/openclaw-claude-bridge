#!/usr/bin/env python3
"""
Claude Code Helper - OpenClaw 调用 Claude Code 的工具类

修复了嵌套调用问题，支持在 Claude Code 内部调用 Claude Code。

Usage:
    from openclaw_claude_bridge import ClaudeCodeHelper

    helper = ClaudeCodeHelper()

    # 简单调用
    result = helper.call("请检查 Git 状态")

    # GitHub 同步
    result = helper.git_sync()

    # 运行命令
    result = helper.run_command("pytest tests/")

    # 协作任务
    result = helper.collaborate("创建新任务文件夹", "task-新任务")
"""

import subprocess
import shutil
import os  # 关键：用于环境变量处理
from typing import Optional
from pathlib import Path


class ClaudeCodeHelper:
    """
    Claude Code 调用助手

    帮助 OpenClaw 在必要时调用 Claude Code 协作完成任务。
    自动处理 CLAUDECODE 环境变量，支持嵌套调用。
    """

    def __init__(self, timeout: int = 120, verbose: bool = True):
        """
        初始化助手

        Args:
            timeout: 默认超时时间（秒）
            verbose: 是否打印进度信息
        """
        self.timeout = timeout
        self.verbose = verbose
        self.claude_available = shutil.which('claude') is not None
        self.codex_available = shutil.which('codex') is not None

        if self.verbose:
            print(f"🤖 Claude Code 助手初始化")
            print(f"   Claude 可用: {self.claude_available}")
            print(f"   Codex 可用: {self.codex_available}")

    def call(self, prompt: str, context: Optional[str] = None, timeout: Optional[int] = None) -> str:
        """
        调用 Claude Code

        Args:
            prompt: 提示词
            context: 上下文信息
            timeout: 超时时间（覆盖默认值）

        Returns:
            Claude Code 的回复
        """
        if not self.claude_available and not self.codex_available:
            return "❌ Claude Code 和 Codex 都不可用，请检查安装"

        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        timeout = timeout or self.timeout

        if self.verbose:
            print(f"📤 正在调用 Claude Code (超时: {timeout}秒)...")

        try:
            # 关键修复：复制环境变量并移除 CLAUDECODE，支持嵌套调用
            # 当 OpenClaw 在 Claude Code 内部运行时，需要清理此变量
            env = os.environ.copy()
            env.pop('CLAUDECODE', None)

            # 优先使用 Claude
            if self.claude_available:
                result = subprocess.run(
                    ['claude', '-p', full_prompt],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env  # 使用清理后的环境，支持嵌套调用
                )
                if result.returncode == 0:
                    if self.verbose:
                        print("✅ Claude Code 调用成功")
                    return result.stdout
                else:
                    if self.verbose:
                        print(f"⚠️ Claude 失败: {result.stderr}")

            # 备选 Codex
            if self.codex_available:
                if self.verbose:
                    print("🔄 尝试使用 Codex...")
                result = subprocess.run(
                    ['codex', '-q', full_prompt],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env  # 使用同样的清理环境
                )
                if result.returncode == 0:
                    if self.verbose:
                        print("✅ Codex 调用成功")
                    return result.stdout
                else:
                    return f"❌ Codex 也失败了: {result.stderr}"

            return f"❌ 调用失败"

        except subprocess.TimeoutExpired:
            return f"❌ 调用超时（>{timeout}秒）"
        except Exception as e:
            return f"❌ 异常: {e}"

    def git_sync(self, repo_path: Optional[str] = None) -> str:
        """
        同步到 GitHub

        Args:
            repo_path: 仓库路径（默认当前目录）

        Returns:
            执行结果
        """
        if repo_path is None:
            repo_path = os.getcwd()

        if self.verbose:
            print(f"🔄 正在同步 GitHub: {repo_path}")

        prompt = f"""
请在 {repo_path} 执行 Git 同步：
1. cd {repo_path}
2. git status 查看当前状态
3. 如果有未跟踪或修改的文件：
   - git add -A
   - git commit -m "feat: 更新任务 $(date +%Y-%m-%d)"
4. git push origin main
5. 返回执行结果

注意：如果今天已经提交过，可以只 push。
"""
        return self.call(prompt, timeout=120)

    def run_command(self, command: str, cwd: Optional[str] = None, timeout: Optional[int] = None) -> str:
        """
        让 Claude Code 运行系统命令

        Args:
            command: 要执行的命令
            cwd: 工作目录
            timeout: 超时时间

        Returns:
            执行结果
        """
        if self.verbose:
            print(f"⚡ 执行命令: {command}")

        context = f"cd {cwd}" if cwd else ""
        prompt = f"请执行命令：{command}\n返回执行结果和输出。"

        return self.call(prompt, context=context, timeout=timeout)

    def collaborate(self, task_description: str, task_name: str) -> str:
        """
        与 Claude Code 协作完成任务

        Args:
            task_description: 任务描述
            task_name: 任务名称

        Returns:
            协作结果
        """
        if self.verbose:
            print(f"🤝 开始与 Claude Code 协作: {task_name}")

        prompt = f"""
用户需要完成这个任务：{task_description}
任务名称：{task_name}

请执行以下步骤：
1. 创建必要的目录结构（如果需要）
2. 初始化项目（如果需要）
3. 执行命令行相关的操作
4. 明确告诉我："已完成命令行部分，OpenClaw 可以继续处理代码编辑部分"

工作目录：{os.getcwd()}
"""

        result = self.call(prompt, timeout=180)

        if self.verbose:
            print("=" * 40)
            print("Claude Code 完成部分:")
            print(result)
            print("=" * 40)
            print("📝 现在由 OpenClaw 继续处理代码部分...")

        return result

    def check_status(self) -> dict:
        """
        检查 Claude Code 和 Codex 的可用性

        Returns:
            状态字典
        """
        return {
            'claude_available': self.claude_available,
            'codex_available': self.codex_available,
            'any_available': self.claude_available or self.codex_available,
            'timeout': self.timeout
        }


# 便捷函数
def quick_call(prompt: str, timeout: int = 60) -> str:
    """快速调用 Claude Code"""
    helper = ClaudeCodeHelper(verbose=False)
    return helper.call(prompt, timeout=timeout)


def git_sync(repo_path: Optional[str] = None) -> str:
    """快速同步 GitHub"""
    helper = ClaudeCodeHelper()
    return helper.git_sync(repo_path)


# 测试
if __name__ == "__main__":
    print("=== Claude Code Helper 测试 ===\n")

    helper = ClaudeCodeHelper()

    # 检查状态
    status = helper.check_status()
    print("状态检查:")
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 40 + "\n")

    # 简单调用测试
    if status['any_available']:
        print("测试简单调用:")
        result = helper.call("请说 'Hello from Claude Code!'")
        print(result)
    else:
        print("❌ Claude Code 和 Codex 都不可用，跳过测试")
