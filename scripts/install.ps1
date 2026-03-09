# ==========================================
# TestWithAI 一键安装脚本 (PowerShell 版)
# 支持 Windows
# ==========================================

$ErrorActionPreference = "Stop"

Write-Host "==> 正在准备安装 TestWithAI..." -ForegroundColor Blue

# 1. 基础环境检查
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "错误: 请先安装 Git (https://git-scm.com/)"
    exit
}

# 2. 检查并安装 uv
if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "==> 正在安装 uv (高性能 Python 包管理器)..." -ForegroundColor Yellow
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    # 将 uv 路径添加到当前会话
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
}

# 3. 准备工作目录
$PROJECT_DIR = Join-Path $env:USERPROFILE ".testwithai"
if (!(Test-Path $PROJECT_DIR)) { New-Item -ItemType Directory -Path $PROJECT_DIR }
Set-Location $PROJECT_DIR

# 4. 克隆项目 (如果目录不存在)
if (!(Test-Path ".git")) {
    Write-Host "==> 正在从 GitHub 获取 TestWithAI 源码..." -ForegroundColor Blue
    git clone https://github.com/YourUsername/TestWithAI.git .
}

# 5. 使用 uv 进行安装
Write-Host "==> 正在创建虚拟环境并安装依赖..." -ForegroundColor Blue
uv venv --python 3.10
.\.venv\Scripts\Activate.ps1
uv pip install -e .

# 6. 配置用户 Path (以便全局使用 twai 命令)
$BIN_DIR = Join-Path $env:USERPROFILE ".local\bin"
if (!(Test-Path $BIN_DIR)) { New-Item -ItemType Directory -Path $BIN_DIR }

# 创建一个 PowerShell 别名脚本或启动程序
$TWAI_PATH = Join-Path $BIN_DIR "twai.ps1"
@"
& `"$PROJECT_DIR\.venv\Scripts\test_with_ai.exe`" @args
"@ | Set-Content $TWAI_PATH

# 将 BIN_DIR 添加到 User PATH (如果尚未添加)
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$BIN_DIR*") {
    [Environment]::SetEnvironmentVariable("Path", $userPath + ";" + $BIN_DIR, "User")
    Write-Host "==> 已将安装目录添加到 User PATH，请重启终端使命令生效。" -ForegroundColor Cyan
}

# 7. 完成
Write-Host "==> 安装完成！" -ForegroundColor Green
Write-Host "您可以直接运行以下命令启动项目：" -ForegroundColor Blue
Write-Host "twai init --defaults && twai app" -ForegroundColor Yellow
Write-Host "提示: 如果 twai 命令未生效，请重启 PowerShell 窗口。" -ForegroundColor Blue
