@echo off
chcp 65001 >nul
echo ========================================
echo    简单记账 - Python桌面预览版
echo ========================================
echo.
echo 正在启动应用...
echo.

python "c:\Users\Admins\Documents\记账\preview_app.py"

if %errorlevel% neq 0 (
    echo.
    echo 启动失败！请检查：
    echo 1. Python是否已安装
    echo 2. Tkinter模块是否可用
    echo 3. 文件路径是否正确
    echo.
    pause
)

echo.
echo 应用已关闭
echo.
pause
