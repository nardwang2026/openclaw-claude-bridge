#!/bin/bash
# OpenClaw Claude Bridge 一键安装脚本
# 支持 macOS/Linux

set -e

echo "🚀 OpenClaw Claude Bridge 安装程序"
echo "===================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 检查前置依赖
echo "📋 检查前置依赖..."

MISSING_DEPS=()

if ! command -v python3 &> /dev/null; then
    MISSING_DEPS+=("python3")
fi

if ! command -v git &> /dev/null; then
    MISSING_DEPS+=("git")
fi

if ! command -v claude &> /dev/null && ! command -v codex &> /dev/null; then
    echo -e "${YELLOW}⚠️  警告: 未检测到 Claude Code 或 Codex${NC}"
    echo "请先安装其中之一:"
    echo "  - Claude Code: npm install -g @anthropic-ai/claude-code"
    echo "  - Codex: npm install -g @anthropic-ai/codex"
    echo ""
    echo -e "${YELLOW}安装将继续，但工具无法使用，直到你安装 Claude Code 或 Codex${NC}"
    echo ""
else
    if command -v claude &> /dev/null; then
        echo -e "${GREEN}  ✅ Claude Code 已安装${NC}"
    fi
    if command -v codex &> /dev/null; then
        echo -e "${GREEN}  ✅ Codex 已安装${NC}"
    fi
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo -e "${RED}❌ 错误: 缺少必要依赖: ${MISSING_DEPS[*]}${NC}"
    exit 1
fi

echo -e "${GREEN}  ✅ 所有必要依赖已安装${NC}"

# 2. 选择安装路径
echo ""
echo "📁 选择安装路径..."
DEFAULT_INSTALL_DIR="$HOME/.openclaw-claude-bridge"
read -p "安装路径 [$DEFAULT_INSTALL_DIR]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}

# 3. 克隆仓库
echo ""
echo "⬇️  下载 OpenClaw Claude Bridge..."
REPO_URL="https://github.com/nardwang2026/openclaw-claude-bridge.git"

if [ -d "$INSTALL_DIR" ]; then
    echo "  目录已存在，更新中..."
    cd "$INSTALL_DIR" && git pull origin main
else
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi

echo -e "${GREEN}  ✅ 下载完成${NC}"

# 4. 添加到 Python 路径
echo ""
echo "🔧 配置环境..."

# 检测 shell
SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    SHELL_CONFIG="$HOME/.profile"
fi

# 添加到 PYTHONPATH
PYTHONPATH_LINE="export PYTHONPATH=\"\$PYTHONPATH:$INSTALL_DIR\""

if [ -f "$SHELL_CONFIG" ]; then
    if grep -q "openclaw-claude-bridge" "$SHELL_CONFIG" 2>/dev/null; then
        echo "  环境变量已配置"
    else
        echo "" >> "$SHELL_CONFIG"
        echo "# OpenClaw Claude Bridge" >> "$SHELL_CONFIG"
        echo "$PYTHONPATH_LINE" >> "$SHELL_CONFIG"
        echo -e "${GREEN}  ✅ 已添加到 $SHELL_CONFIG${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠️  未找到 shell 配置文件，请手动添加以下行到你的 shell 配置:${NC}"
    echo "     $PYTHONPATH_LINE"
fi

# 5. 创建快捷命令
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/openclaw-verify" << EOF
#!/bin/bash
# OpenClaw Claude Bridge 验证脚本
python3 "$INSTALL_DIR/scripts/verify.py" "\$@"
EOF
chmod +x "$BIN_DIR/openclaw-verify"

# 添加到 PATH
PATH_LINE="export PATH=\"\$PATH:$BIN_DIR\""
if [ -f "$SHELL_CONFIG" ]; then
    if ! grep -q "$BIN_DIR" "$SHELL_CONFIG" 2>/dev/null; then
        echo "$PATH_LINE" >> "$SHELL_CONFIG"
    fi
fi

echo -e "${GREEN}  ✅ 快捷命令已创建: openclaw-verify${NC}"

# 6. 验证安装
echo ""
echo "🧪 验证安装..."
export PYTHONPATH="$PYTHONPATH:$INSTALL_DIR"
if python3 "$INSTALL_DIR/scripts/verify.py"; then
    echo ""
    echo -e "${GREEN}✅ 安装完成！${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  安装完成，但验证未完全通过${NC}"
fi

echo ""
echo "使用说明:"
echo "  1. 重新加载 shell: source $SHELL_CONFIG"
echo "  2. 在 Python 中使用:"
echo ""
echo "     from openclaw_claude_bridge import ClaudeCodeHelper"
echo "     helper = ClaudeCodeHelper()"
echo "     result = helper.call('请检查 Git 状态')"
echo ""
echo "  3. 验证安装: openclaw-verify"
echo ""
echo "文档: https://github.com/nardwang2026/openclaw-claude-bridge"
echo ""
