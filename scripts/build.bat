@echo off
chcp 65001 >nul
echo ====================================
echo Proxifier 切换器 - 打包脚本
echo ====================================
echo.

echo [1/3] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
) else (
    echo PyInstaller 已安装
)
echo.

echo [2/3] 开始打包...
cd ..
pyinstaller --noconfirm --onefile --windowed --icon="assets/icon.ico" --add-data "assets;assets" --name="Easy-Proxifier-Toggler" run.py
echo.

echo [3/3] 打包完成！
echo.
echo 生成的文件位置: dist\Easy-Proxifier-Toggler.exe
echo.
echo 按任意键退出...
pause >nul
