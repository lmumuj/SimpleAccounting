@echo off
chcp 65001 >nul
echo ========================================
echo    简单记账 - Python桌面预览版
echo ========================================
echo.
echo 正在启动应用...
echo.

python preview_app.py

if errorlevel 1 (
    echo.
    echo 启动失败！请检查Python是否已安装。
    echo.
    echo 如果没有安装Python，请访问：
    echo https://www.python.org/downloads/
    echo.
    echo 安装后，请确保勾选"Add Python to PATH"选项
    echo.
    pause
) else (
    echo.
    echo 应用已关闭
    echo.
)
