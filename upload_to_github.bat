@echo off
chcp 65001 >nul
echo ========================================
echo   上传项目到 GitHub
echo ========================================
echo.

REM 检查是否安装了 Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Git
    echo.
    echo 请先安装 Git：
    echo 下载地址：https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到 Git 环境
echo.

REM 进入项目目录
cd /d "%~dp0"
echo ✅ 当前目录: %CD%
echo.

REM 检查是否已经是 Git 仓库
if exist .git (
    echo ℹ️  此目录已经是 Git 仓库
    echo.
    choice /C YN /M "是否重新初始化（会删除旧的 Git 历史）"
    if %errorlevel%==2 (
        echo.
        echo 继续使用现有仓库...
        goto check_remote
    )
    rmdir /s /q .git
    echo ✅ 已清理旧仓库
)

echo.
echo [1/4] 初始化 Git 仓库...
git init
if %errorlevel% neq 0 (
    echo ❌ Git 初始化失败
    pause
    exit /b 1
)
echo ✅ Git 仓库初始化成功
echo.

echo [2/4] 添加文件到 Git...
git add .
if %errorlevel% neq 0 (
    echo ❌ Git add 失败
    pause
    exit /b 1
)
echo ✅ 文件添加成功
echo.

echo [3/4] 创建初始提交...
git commit -m "Initial commit: Simple Accounting App"
if %errorlevel% neq 0 (
    echo ❌ Git commit 失败
    pause
    exit /b 1
)
echo ✅ 提交成功
echo.

:check_remote
echo [4/4] 关联 GitHub 仓库...

set /p GITHUB_USERNAME=请输入你的 GitHub 用户名:
set /p REPO_NAME=请输入仓库名称（默认: SimpleAccounting）:
if "%REPO_NAME%"=="" set REPO_NAME=SimpleAccounting

echo.
echo 准备连接到：https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
echo.
echo 重要提示：
echo 1. 请先在 GitHub 上创建仓库：%REPO_NAME%
echo 2. 创建仓库时，不要初始化 README、.gitignore、LICENSE
echo 3. 创建空仓库即可
echo.
pause

echo.
set REMOTE_URL=https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
echo 关联远程仓库：%REMOTE_URL%
git remote add origin %REMOTE_URL%
if %errorlevel% neq 0 (
    echo ❌ 关联远程仓库失败
    pause
    exit /b 1
)

echo.
echo 推送代码到 GitHub...
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 可能的原因：
    echo 1. 仓库不存在或地址错误
    echo 2. 未在 GitHub 上创建仓库
    echo 3. 需要身份验证（用户名和密码）
    echo.
    echo 解决方案：
    echo 1. 检查 GitHub 用户名和仓库名称是否正确
    echo 2. 访问以下链接创建仓库：
    echo    https://github.com/new
    echo 3. 或配置 Git 凭据：
    echo    git config --global user.name "你的用户名"
    echo    git config --global user.email "你的邮箱"
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 上传成功！
echo ========================================
echo.
echo 仓库地址：%REMOTE_URL%
echo.
echo 下一步：
echo 1. 访问仓库查看 Actions 标签
echo 2. 等待 GitHub Actions 自动构建（约 5-10 分钟）
echo 3. 构建完成后下载 APK 文件
echo.
echo 详细教程：GITHUB_ACTIONS_指南.md
echo.
pause

REM 询问是否打开仓库页面
set /p OPEN_REPO=是否打开仓库页面？(Y/N):
if /i "%OPEN_REPO%"=="Y" (
    start "" https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
)
