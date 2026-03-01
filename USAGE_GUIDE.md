# OpenClaw Claude Bridge - 使用指南

> 安装完成后，请阅读本文档了解如何使用

---

## 🎯 本文档适合谁

- **OpenClaw (AI)**: 快速掌握 API 用法
- **人类用户**: 了解功能和使用场景

---

## 📦 安装后检查清单

### 1. 验证安装

```bash
openclaw-verify
```

期望输出：
```
✅ Python 3.x
✅ Claude Code 已安装
✅ Codex 已安装 (可选)
✅ 模块可以正常导入
✅ 嵌套调用测试成功
```

### 2. 重新加载 shell

```bash
source ~/.zshrc  # 或 ~/.bashrc
```

---

## 🚀 3 分钟快速上手

### 基础调用

```python
from openclaw_claude_bridge import ClaudeCodeHelper

# 创建助手
helper = ClaudeCodeHelper()

# 简单调用
result = helper.call("请检查当前目录的 Git 状态")
print(result)
```

### 运行结果示例

```
🤖 Claude Code 助手初始化
   Claude 可用: True
   Codex 可用: False
📤 正在调用 Claude Code (超时: 120秒)...
✅ Claude Code 调用成功

当前目录状态：
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## 📚 API 参考

### ClaudeCodeHelper 类

```python
helper = ClaudeCodeHelper(
    timeout=120,      # 默认超时时间（秒）
    verbose=True      # 是否打印进度信息
)
```

### 方法列表

| 方法 | 用途 | 示例 |
|------|------|------|
| `call(prompt, context, timeout)` | 发送任意指令 | `helper.call("分析代码")` |
| `git_sync(repo_path)` | 同步 GitHub | `helper.git_sync("~/project")` |
| `run_command(cmd, cwd)` | 运行命令 | `helper.run_command("pytest")` |
| `collaborate(task, name)` | 协作任务 | `helper.collaborate("重构代码", "refactor")` |
| `check_status()` | 检查状态 | `helper.check_status()` |

### 便捷函数

```python
from openclaw_claude_bridge import quick_call, git_sync

# 无需创建实例，直接调用
result = quick_call("请回复 Hello")
result = git_sync("~/my-project")
```

---

## 💡 常见使用场景

### 场景 1: GitHub 同步

**适合**: 每天结束时同步代码

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

# 同步当前项目
result = helper.git_sync("/Users/moltnard/Documents/molt/2026-03-02")
print(result)
```

**Claude Code 会执行**:
1. `git status` 查看状态
2. `git add -A` 添加更改
3. `git commit -m "feat: 更新任务 2026-03-02"`
4. `git push origin main`
5. 返回执行结果

---

### 场景 2: 运行测试

**适合**: 让 Claude Code 运行复杂测试

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

# 运行测试（设置更长超时）
result = helper.run_command(
    command="pytest tests/ -v",
    cwd="/Users/moltnard/Documents/molt/2026-02-27",
    timeout=300  # 5分钟
)

print(result)
```

---

### 场景 3: 协作任务

**适合**: OpenClaw 和 Claude Code 分工合作

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

# 让 Claude Code 处理命令行部分
result = helper.collaborate(
    task_description="初始化 Node.js 项目，创建 package.json 并安装 express",
    task_name="node-init"
)

# 返回结果会明确说明：
# "已完成命令行部分，OpenClaw 可以继续处理代码编辑部分"

# OpenClaw 继续：创建代码文件、编辑代码...
```

**分工建议**:
| 任务 | Claude Code | OpenClaw |
|------|-------------|----------|
| 命令行操作 | ✅ 执行 | ❌ |
| 文件创建 | ✅ 可以 | ✅ 更好 |
| 代码编辑 | ✅ 可以 | ✅ 更好 |
| Git 操作 | ✅ 执行 | ❌ |
| 代码重构 | ✅ 擅长 | ❌ |

---

### 场景 4: 复杂指令

**适合**: 需要多步骤的任务

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

prompt = """
请在 ~/Documents/molt/2026-03-02 执行以下操作：
1. 查找所有包含 "TODO" 的 Python 文件
2. 列出这些文件的路径和 TODO 内容
3. 统计每个文件的 TODO 数量
4. 生成一份报告
"""

result = helper.call(prompt, timeout=180)
print(result)
```

---

## 🔧 高级用法

### 禁用详细输出

```python
# 静默模式，不打印进度
helper = ClaudeCodeHelper(verbose=False)
result = helper.call("请分析代码")
```

### 自定义超时

```python
# 全局超时 5 分钟
helper = ClaudeCodeHelper(timeout=300)

# 单次调用覆盖
result = helper.call("耗时任务", timeout=600)
```

### 带上下文调用

```python
error_log = """
Error: ModuleNotFoundError: No module named 'openai'
File: /Users/moltnard/project/main.py, line 5
"""

result = helper.call(
    prompt="请分析这个错误并提供解决方案",
    context=error_log
)
```

---

## 🐛 故障排除

### 问题 1: 模块未找到

**症状**:
```
ModuleNotFoundError: No module named 'openclaw_claude_bridge'
```

**解决**:
```bash
# 重新加载 shell
source ~/.zshrc  # 或 ~/.bashrc

# 或手动添加 PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$HOME/.openclaw-claude-bridge"
```

---

### 问题 2: Claude Code 未找到

**症状**:
```
❌ Claude Code 和 Codex 都不可用
```

**解决**:
```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 或安装 Codex
npm install -g @anthropic-ai/codex

# 验证安装
which claude
which codex
```

---

### 问题 3: 嵌套调用失败

**症状**:
```
❌ 错误: CLAUDECODE 环境变量已设置
```

**解决**:
```bash
# 更新到最新版本
cd ~/.openclaw-claude-bridge && git pull

# 重新验证
openclaw-verify
```

---

### 问题 4: 调用超时

**症状**:
```
❌ 调用超时（>120秒）
```

**解决**:
```python
# 增加超时时间
helper = ClaudeCodeHelper(timeout=300)  # 5 分钟

# 或单次调用设置
result = helper.call("复杂任务", timeout=600)
```

---

## 📊 性能提示

| 操作 | 建议超时 | 说明 |
|------|----------|------|
| 简单查询 | 60 秒 | 检查状态、简单分析 |
| Git 操作 | 120 秒 | add/commit/push |
| 运行测试 | 300 秒 | 测试套件可能需要时间 |
| 复杂任务 | 600 秒 | 代码重构、分析 |

---

## 🎓 最佳实践

### 1. 明确指令

❌ 不好的指令：
```python
helper.call("帮我处理 Git")
```

✅ 好的指令：
```python
helper.call("""
请在 /Users/moltnard/project 执行：
1. git status 查看状态
2. 如果有更改，执行 git add -A && git commit -m "update"
3. git push origin main
4. 返回执行结果
""")
```

### 2. 告知用户

```python
print("🤖 正在调用 Claude Code 处理命令行部分...")
result = helper.call("...")
print("✅ Claude Code 已完成")
print("📝 现在由我 (OpenClaw) 继续...")
```

### 3. 错误处理

```python
result = helper.call("请执行任务")

if "❌" in result or "错误" in result:
    print("调用失败，尝试备选方案...")
    # 备选处理
else:
    print("调用成功，继续下一步")
```

---

## 📖 更多资源

- [完整使用指南](docs/SELF_STUDY_GUIDE.md) - OpenClaw 自学文档
- [API 文档](docs/API.md) - 详细 API 说明
- [示例代码](examples/) - 常见使用场景
- [GitHub 仓库](https://github.com/nardwang2026/openclaw-claude-bridge)

---

## 💬 需要帮助？

- 提交 Issue: https://github.com/nardwang2026/openclaw-claude-bridge/issues
- 查看文档: https://github.com/nardwang2026/openclaw-claude-bridge/tree/main/docs

---

**现在你可以开始使用 OpenClaw Claude Bridge 了！** 🚀

快速测试：
```python
from openclaw_claude_bridge import ClaudeCodeHelper
helper = ClaudeCodeHelper()
print(helper.call("请回复 'Hello World!'"))
```
