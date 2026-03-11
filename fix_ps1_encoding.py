
import os

content = r'''# ==========================================
# TestWithAI 一键稳健安装脚本 (PowerShell 版)
# 支持 Windows
# ==========================================

$ErrorActionPreference = "Stop"

Write-Host "==> 正在准备安装 TestWithAI..." -ForegroundColor Blue

# 1. 基础环境检查
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "错误: 请先安装 Git (https://git-scm.com/)"
    exit 1
}

# 2. 准备项目目录
$PROJECT_DIR = Get-Location
Write-Host "==> 项目目录: $PROJECT_DIR" -ForegroundColor Blue

# 3. 创建虚拟环境 (优先使用 uv，失败则回退到 venv)
$USE_UV = $false
if (Get-Command uv -ErrorAction SilentlyContinue) {
    $USE_UV = $true
} else {
    Write-Host "提示: 未找到 uv，正在尝试自动安装以加速部署..." -ForegroundColor Yellow
    try {
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
        if (Get-Command uv -ErrorAction SilentlyContinue) {
            $USE_UV = $true
        }
    } catch {
        Write-Host "警告: uv 自动安装失败，将尝试标准 pip/venv 模式。" -ForegroundColor Yellow
    }
}

if ($USE_UV) {
    Write-Host "==> 使用 uv 创建虚拟环境并安装依赖..." -ForegroundColor Blue
    uv venv --python 3.10
    & ".\.venv\Scripts\Activate.ps1"
    uv pip install -e .
} else {
    Write-Host "==> 使用标准 venv 创建虚拟环境并安装依赖..." -ForegroundColor Blue
    python -m venv .venv
    & ".\.venv\Scripts\Activate.ps1"
    python -m pip install --upgrade pip
    pip install -e .
}

# 4. 创建根目录快捷启动脚本 (Windows 批处理)
Write-Host "==> 正在创建快捷启动脚本 (twai.bat)..." -ForegroundColor Blue
$batLines = @(
    "@echo off",
    "setlocal",
    "cd /d ""%~dp0""",
    "if not exist "".venv\Scripts\activate.bat"" (",
    "    echo [ERROR] Virtual environment not found. Please run scripts\install.ps1 first.",
    "    pause",
    "    exit /b 1",
    ")",
    "call .venv\Scripts\activate.bat",
    "python -m test_with_ai %*",
    "endlocal"
)
$batLines | Set-Content -Path (Join-Path $PROJECT_DIR "twai.bat") -Encoding UTF8

# 5. 完成
Write-Host "==> 安装完成！" -ForegroundColor Green
Write-Host "您可以直接在根目录下运行以下命令（无需配置 PATH）：" -ForegroundColor Blue
Write-Host ".\twai.bat init --defaults && .\twai.bat app" -ForegroundColor Yellow
Write-Host "提示: 以后运行项目，只需执行 .\twai.bat 即可。" -ForegroundColor Blue
'''

file_path = r'd:\TestWithAI\scripts\install.ps1'
with open(file_path, 'wb') as f:
    # Write UTF-8 BOM
    f.write(b'\xef\xbb\xbf')
    # Write content using CRLF for Windows compatibility
    f.write(content.replace('\n', '\r\n').encode('utf-8'))

print(f"Successfully wrote {file_path} with UTF-8 BOM and CRLF.")
