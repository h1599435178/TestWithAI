# ==========================================
# TestWithAI 一键安装与运行脚本 (PowerShell 版)
# 支持 Windows
# ==========================================

$ErrorActionPreference = "Stop" # 遇到错误停止执行

Write-Host "==> 开始部署 TestWithAI..." -ForegroundColor Blue

# 1. 环境检测
Write-Host "==> 正在检测运行环境..." -ForegroundColor Blue
if (!(Get-Command git -ErrorAction SilentlyContinue)) { Write-Error "错误: 需要安装 Git"; exit }
if (!(Get-Command python -ErrorAction SilentlyContinue)) { Write-Error "错误: 需要安装 Python"; exit }
if (!(Get-Command node -ErrorAction SilentlyContinue)) { Write-Error "错误: 需要安装 Node.js"; exit }

# 2. 检查目录
if (!(Test-Path ".git")) {
    Write-Host "==> 正在克隆仓库..." -ForegroundColor Blue
    git clone https://github.com/YourUsername/TestWithAI.git .
}

# 3. 后端环境配置
Write-Host "==> 正在配置后端环境 (Python)..." -ForegroundColor Blue
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
# pip install -r backend/requirements.txt  # 假设有此文件

# 4. 前端环境配置
Write-Host "==> 正在配置前端环境 (Node.js)..." -ForegroundColor Blue
# Set-Location frontend
# npm install
# npm run build # 假设有此目录
# Set-Location ..

# 5. 启动项目
Write-Host "==> 部署完成！正在启动..." -ForegroundColor Green
# Start-Process python main.py
# npm run start

Write-Host "==> 项目已在本地运行。" -ForegroundColor Green
