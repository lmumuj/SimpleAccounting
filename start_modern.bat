@echo off
chcp 65001 >nul
echo ========================================
echo    ✨ 简单记账 - 现代化版
echo ========================================
echo.
echo 🎨 全新设计，现代风格
echo.
echo 正在启动应用...
echo.

python "c:\Users\Admins\Documents\记账\modern_app.py"

if %errorlevel% neq 0 (
    echo.
    echo ❌ 启动失败！
    echo.
    echo 请检查：
    echo 1. ✓ Python 3.6+ 是否已安装
    echo 2. ✓ Tkinter 模块是否可用
    echo 3. ✓ 文件路径是否正确
    echo.
    echo 运行: python --version
    echo.
    pause
)

echo.
echo 📱 应用已关闭
echo.
pause
