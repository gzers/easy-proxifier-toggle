@echo off
REM Proxifier Toggler - 以管理员权限启动
REM 此脚本会自动请求管理员权限并启动程序

echo ========================================
echo Proxifier Toggler - 启动程序
echo ========================================
echo.

REM 检查是否已经是管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [√] 已获得管理员权限
    echo [*] 正在启动程序...
    echo.
    python run.py
) else (
    echo [!] 需要管理员权限
    echo [*] 正在请求管理员权限...
    echo.
    
    REM 请求管理员权限并重新运行此脚本
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d %CD% && python run.py && pause' -Verb RunAs"
)

pause
