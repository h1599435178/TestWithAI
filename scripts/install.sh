#!/bin/bash

# ==========================================
# TestWithAI 一键安装脚本 (Bash 版)
# 支持 Linux / macOS / WSL
# ==========================================

set -e

# 定义颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}==> 正在准备安装 TestWithAI...${NC}"

# 1. 基础环境检查
command -v git >/dev/null 2>&1 || { echo -e "${RED}错误: 请先安装 Git${NC}"; exit 1; }

# 2. 检查并安装 uv (超快速包管理器)
if ! command -v uv >/dev/null 2>&1; then
    echo -e "${YELLOW}==> 正在安装 uv (高性能 Python 包管理器)...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env 2>/dev/null || true
    export PATH="$HOME/.local/bin:$PATH"
fi

# 3. 准备工作目录
PROJECT_DIR="$HOME/.testwithai"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 4. 克隆项目 (如果目录不存在)
if [ ! -d ".git" ]; then
    echo -e "${BLUE}==> 正在从 GitHub 获取 TestWithAI 源码...${NC}"
    git clone https://github.com/h1599435178/TestWithAI.git .
fi

# 5. 使用 uv 进行安装
echo -e "${BLUE}==> 正在创建虚拟环境并安装依赖...${NC}"
uv venv --python 3.10
source .venv/bin/activate
uv pip install -e .

# 6. 配置环境变量与别名 (可选，帮助用户更方便启动)
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
cat <<EOF > "$BIN_DIR/twai"
#!/bin/bash
source "$PROJECT_DIR/.venv/bin/activate"
test_with_ai "\$@"
EOF
chmod +x "$BIN_DIR/twai"

# 7. 完成
echo -e "${GREEN}==> 安装完成！${NC}"
echo -e "${BLUE}您可以直接运行以下命令启动项目：${NC}"
echo -e "${YELLOW}twai init --defaults && twai app${NC}"
echo -e "${BLUE}提示: 如果 twai 命令未生效，请执行 source ~/.bashrc 或重启终端。${NC}"
