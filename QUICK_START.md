# OpenClaw Claude Bridge - 快速开始

## 5 分钟上手

### 1. 一键安装

#### macOS / Linux

打开终端，复制并运行以下命令：

```bash
curl -fsSL https://raw.githubusercontent.com/nardwang2026/openclaw-claude-bridge/main/scripts/install.sh | bash
```

#### Windows

打开 PowerShell，复制并运行以下命令：

```powershell
irm https://raw.githubusercontent.com/nardwang2026/openclaw-claude-bridge/main/scripts/install.ps1 | iex
```

---

### 2. 验证安装

安装完成后，运行验证命令：

```bash
openclaw-verify
```

你应该看到类似输出：

```
🧪 OpenClaw Claude Bridge 验证
========================================

1. 检查 Python 版本...
  ✅ Python 3.11

2. 检查 Claude Code...
  ✅ Claude Code 已安装

3. 检查 Codex...
  ⚠️  Codex 未安装 (可选)

4. 检查模块导入...
  ✅ 模块可以正常导入

5. 测试嵌套调用...
  ℹ️  检测到在 Claude Code 内部运行
  ✅ 嵌套调用测试成功

========================================
✅ 所有检查通过！
```

---

### 3. 开始使用

重新加载你的 shell 配置：

```bash
source ~/.zshrc  # 或 ~/.bashrc
```

然后在 Python 中使用：

```python
from openclaw_claude_bridge import ClaudeCodeHelper

# 创建助手实例
helper = ClaudeCodeHelper()

# 简单调用
result = helper.call("请检查 Git 状态")
print(result)
```

---

## 常用示例

### 示例 1: GitHub 同步

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

# 同步当前目录的仓库
result = helper.git_sync()
print(result)

# 同步指定目录的仓库
result = helper.git_sync("/path/to/your/project")
print(result)
```

### 示例 2: 运行测试

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

# 运行测试套件
result = helper.run_command("pytest tests/", cwd="/path/to/project")
print(result)
```

### 示例 3: 协作任务

```python
from openclaw_claude_bridge import ClaudeCodeHelper

helper = ClaudeCodeHelper()

# 让 Claude Code 处理命令行部分
result = helper.collaborate(
    task_description="初始化一个 Python 项目，创建虚拟环境并安装依赖",
    task_name="python-init"
)

# Claude Code 返回结果后，OpenClaw 可以继续处理代码编辑部分
print(result)
```

### 示例 4: 快速调用

```python
from openclaw_claude_bridge import quick_call

# 不需要创建实例，直接调用
result = quick_call("分析这个错误日志", timeout=60)
print(result)
```

---

## 配置选项

### 禁用详细输出

```python
from openclaw_claude_bridge import ClaudeCodeHelper

# verbose=False 不打印进度信息
helper = ClaudeCodeHelper(verbose=False)
result = helper.call("请检查 Git 状态")
```

### 自定义超时

```python
from openclaw_claude_bridge import ClaudeCodeHelper

# 默认 120 秒，可以修改
helper = ClaudeCodeHelper(timeout=300)  # 5 分钟

# 单次调用覆盖
result = helper.call("运行测试", timeout=600)  # 10 分钟
```

---

## 故障排除

### 问题 1: 模块导入失败

**错误**: `ModuleNotFoundError: No module named 'openclaw_claude_bridge'`

**解决**:
```bash
# 重新加载 shell 配置
source ~/.zshrc  # 或 ~/.bashrc

# 手动添加 PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$HOME/.openclaw-claude-bridge"
```

### 问题 2: Claude Code 未找到

**错误**: `Claude Code 和 Codex 都不可用`

**解决**:
```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 或安装 Codex
npm install -g @anthropic-ai/codex
```

### 问题 3: 嵌套调用失败

**错误**: `CLAUDECODE 环境变量已设置`

**解决**: 确保使用的是最新版本的 openclaw-claude-bridge：
```bash
cd ~/.openclaw-claude-bridge && git pull
```

---

## 下一步

- 阅读 [完整使用指南](docs/SELF_STUDY_GUIDE.md)
- 查看 [API 文档](docs/API.md)
- 浏览 [示例代码](examples/)

---

## 需要帮助？

- 提交 Issue: [GitHub Issues](https://github.com/nardwang2026/openclaw-claude-bridge/issues)
- 查看文档: [完整文档](docs/)
