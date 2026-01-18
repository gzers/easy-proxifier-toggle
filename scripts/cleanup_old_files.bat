@echo off
echo 正在清理旧文件...
echo.

REM 删除旧的 Python 文件
if exist config_manager.py del config_manager.py
if exist settings_gui.py del settings_gui.py
if exist proxifier_toggler.py del proxifier_toggler.py

REM 删除旧的配置文件（已移动到 config 目录）
if exist config.json del config.json

REM 删除 __pycache__
if exist __pycache__ rmdir /s /q __pycache__

echo 清理完成！
echo.
pause
