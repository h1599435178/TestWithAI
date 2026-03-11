@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Please run scripts\install.ps1 first.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
python -m test_with_ai %*
endlocal
