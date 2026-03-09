#!/bin/bash

# ==========================================
# TestWithAI 一键稳健安装脚本 (Bash 版)
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
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}错误: 需要 Python 3.10+${NC}"; exit 1; }

# 2. 准备工作目录
PROJECT_DIR="$(pwd)" # 假设用户就在项目根目录下运行
echo -e "${BLUE}==> 项目目录: $PROJECT_DIR${NC}"

# 3. 创建虚拟环境 (优先使用 uv，失败则回退到 venv)
USE_UV=false
if command -v uv >/dev/null 2>&1; then
    USE_UV=true
else
    echo -e "${YELLOW}提示: 未找到 uv，正在尝试安装以加速部署...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1 && {
        source $HOME/.local/bin/env 2>/dev/null || true
        export PATH="$HOME/.local/bin:$PATH"
        USE_UV=true
    } || echo -e "${YELLOW}警告: uv 安装失败，将回退到标准 pip/venv 模式。${NC}"
fi

if [ "$USE_UV" = true ]; then
    echo -e "${BLUE}==> 使用 uv 创建虚拟环境并安装依赖...${NC}"
    uv venv --python 3.10
    source .venv/bin/activate
    uv pip install -e .
else
    echo -e "${BLUE}==> 使用标准 venv 创建虚拟环境并安装依赖...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -e .
fi

# 4. 创建快捷启动脚本 (根目录下，免 PATH 配置)
echo -e "${BLUE}==> 正在创建快捷启动脚本...${NC}"
cat <<EOF > twai.sh
#!/bin/bash
source "$PROJECT_DIR/.venv/bin/activate"
test_with_ai "\$@"
EOF
chmod +x twai.sh

# 5. 完成
echo -e "${GREEN}==> 安装完成！${NC}"
echo -e "${BLUE}您可以直接运行以下命令启动项目（无需配置环境变量）：${NC}"
echo -e "${YELLOW}./twai.sh init --defaults && ./twai.sh app${NC}"
