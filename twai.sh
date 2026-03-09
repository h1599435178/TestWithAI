#!/bin/bash

# 获取脚本所在目录
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

if [ ! -f ".venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found."
    echo "Please run: bash scripts/install.sh"
    exit 1
fi

source .venv/bin/activate
test_with_ai "$@"
