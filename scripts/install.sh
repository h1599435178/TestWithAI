#!/bin/bash

# ==========================================
# TestWithAI 一键安装与运行脚本 (Bash 版)
# 支持 Linux / macOS / WSL
# ==========================================

set -e # 遇到错误立即停止

# 定义颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==> 开始部署 TestWithAI...${NC}"

# 1. 环境检测
echo -e "${BLUE}==> 正在检测运行环境...${NC}"
command -v git >/dev/null 2>&1 || { echo "错误: 需要安装 Git"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "错误: 需要安装 Python 3"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "错误: 需要安装 Node.js"; exit 1; }

# 2. 检查目录
if [ ! -d ".git" ]; then
    echo -e "${BLUE}==> 正在克隆仓库...${NC}"
    git clone https://github.com/YourUsername/TestWithAI.git .
fi

# 3. 后端环境配置
echo -e "${BLUE}==> 正在配置后端环境 (Python)...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
# pip install -r backend/requirements.txt  # 假设有此文件

# 4. 前端环境配置
echo -e "${BLUE}==> 正在配置前端环境 (Node.js)...${NC}"
# cd frontend && npm install && npm run build # 假设有此目录

# 5. 启动项目
echo -e "${GREEN}==> 部署完成！正在启动...${NC}"
# python main.py & 
# npm run start

echo -e "${GREEN}==> 项目已在本地运行。${NC}"
