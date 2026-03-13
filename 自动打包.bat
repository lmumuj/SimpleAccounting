@echo off
chcp 65001 >nul
echo ========================================
echo   简单记账应用 - 自动打包工具
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Python
    echo.
    echo 请先安装 Python 3.7+
    echo 下载地址：https://www.python.org/downloads/
    echo.
    echo 或者，更简单的方法：
    echo 1. 下载并安装 Android Studio
    echo 2. 用它打开项目：c:\Users\Admins\Documents\记账
    echo 3. 点击 Build -^> Build APK(s)
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到 Python 环境
echo.

REM 运行 Python 脚本
python auto_build.py

REM 保持窗口打开
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   构建遇到问题
    echo ========================================
    echo.
    echo 推荐解决方案：
    echo 1. 安装 Android Studio（最简单）
    echo    下载：https://developer.android.com/studio
    echo.
    echo 2. 查看详细文档：打包说明_README.md
    echo.
    pause
    exit /b 1
)

pause
