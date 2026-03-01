# OpenClaw Claude Bridge

> 让 OpenClaw 无缝调用 Claude Code - 修复嵌套调用问题

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/nardwang2026/openclaw-claude-bridge)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## 问题背景

当 OpenClaw 在 Claude Code 内部运行时，直接调用 `claude -p` 会失败：

```
❌ 错误: CLAUDECODE 环境变量已设置，嵌套调用被拒绝
```

**本工具修复了这个问题**，让 OpenClaw 可以无缝调用 Claude Code 协作完成任务。

---

## 一键安装

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/nardwang2026/openclaw-claude-bridge/main/scripts/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/nardwang2026/openclaw-claude-bridge/main/scripts/install.ps1 | iex
```

---

## 快速开始

### 1. 验证安装

```bash
openclaw-verify
```

### 2. 基础使用

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

# 简单调用
result = helper.call("请检查 Git 状态")
print(result)
```

### 3. 常用功能

```python
# GitHub 同步
helper.git_sync("/path/to/your/repo")

# 运行命令
helper.run_command("pytest tests/")

# 协作任务
helper.collaborate(
    task_description="初始化 Node.js 项目",
    task_name="node-init"
)
```

---

## 特性

| 特性 | 说明 |
|------|------|
| ✅ **嵌套调用修复** | 自动处理 CLAUDECODE 环境变量 |
| ✅ **智能回退** | Claude 不可用时自动尝试 Codex |
| ✅ **超时保护** | 默认 120 秒超时，避免长时间等待 |
| ✅ **详细日志** | 可选 verbose 模式，显示调用进度 |
| ✅ **跨平台** | 支持 macOS、Linux、Windows |

---

## 文档

| 文档 | 适合 | 内容 |
|------|------|------|
| [USAGE_GUIDE.md](USAGE_GUIDE.md) ⭐ | AI + 人类 | **安装后阅读** - 完整使用指南 |
| [QUICK_START.md](QUICK_START.md) | 人类 | 5 分钟快速上手 |
| [docs/SELF_STUDY_GUIDE.md](docs/SELF_STUDY_GUIDE.md) | AI (OpenClaw) | 自学文档 |
| [examples/](examples/) | AI + 人类 | 代码示例 |

> 💡 **安装后请务必阅读 [USAGE_GUIDE.md](USAGE_GUIDE.md)** - 包含所有 API 用法和常见场景

---

## 项目结构

```
openclaw-claude-bridge/
├── openclaw_claude_bridge/     # 核心 Python 包
│   ├── __init__.py
│   └── helper.py               # ClaudeCodeHelper 类
├── scripts/                    # 安装和验证脚本
│   ├── install.sh              # macOS/Linux 安装
│   ├── install.ps1             # Windows 安装
│   └── verify.py               # 安装验证
├── examples/                   # 示例代码
├── docs/                       # 文档
├── tests/                      # 测试
├── README.md                   # 本文件
├── QUICK_START.md              # 快速开始
└── LICENSE                     # 许可证
```

---

## 如何工作

### 核心修复

```python
# 复制环境变量并移除 CLAUDECODE，支持嵌套调用
env = os.environ.copy()
env.pop('CLAUDECODE', None)

result = subprocess.run(
    ['claude', '-p', full_prompt],
    capture_output=True,
    text=True,
    timeout=timeout,
    env=env  # 使用清理后的环境
)
```

---

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与。

---

## 许可证

[MIT License](LICENSE)

---

## 相关项目

- [Claude Code](https://github.com/anthropics/claude-code) - Anthropic 官方 CLI 工具
- [Codex CLI](https://github.com/openai/codex) - OpenAI CLI 工具

---

**Made with ❤️ for OpenClaw users**
