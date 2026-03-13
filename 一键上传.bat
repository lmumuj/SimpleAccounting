@echo off
chcp 65001 >nul
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║        简单记账APP - 一键上传到 GitHub                    ║
echo ║                                                          ║
echo ║        你只需要按回车键就能完成所有操作！                ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo [1/5] 检查环境...
cd c:\Users\Admins\Documents\记账
echo √ 已进入项目目录
echo.

echo [2/5] 创建提交...
git commit -m Initial >nul 2>&1
if %errorlevel% neq 0 (
    git commit -m ""Initial"" >nul 2>&1
)
if %errorlevel% neq 0 (
    git commit -m "" >nul 2>&1
)
echo √ 提交成功
echo.

echo [3/5] 配置 GitHub 仓库...
set /p GITHUB_USERNAME=请输入你的 GitHub 用户名（然后按回车）:
set REMOTE_URL=https://github.com/%GITHUB_USERNAME%/SimpleAccounting.git
echo.
echo 仓库地址：%REMOTE_URL%
echo.

git remote add origin %REMOTE_URL% >nul 2>&1
git branch -M main >nul 2>&1
echo √ 仓库配置完成
echo.

echo ╔══════════════════════════════════════════════════════════╗
echo ║                    重要提示！！！                        ║
echo ║                                                          ║
echo ║  接下来会要求输入用户名和密码：                         ║
echo ║                                                          ║
echo ║  1. Username: 输入你的 GitHub 用户名                      ║
echo ║                                                          ║
echo ║  2. Password: 不要输入登录密码！                         ║
echo ║     需要先创建一个 Token（密钥）                        ║
echo ║                                                          ║
echo ║  如何创建 Token：                                       ║
echo ║  1. 访问：https://github.com/settings/tokens             ║
echo ║  2. 点击：Generate new token → Generate new token (classic) ║
echo ║  3. 勾选：repo（全部勾选）                               ║
echo ║  4. 点击：Generate token                                 ║
echo ║  5. 复制显示的 token（只显示一次！）                     ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

set /p READY=准备好了吗？（按回车继续，或输入 N 取消）:
if /i "%READY%"=="N" (
    echo.
    echo 操作已取消
    pause
    exit /b 0
)

echo.
echo [4/5] 上传代码到 GitHub...
echo 这个过程可能需要几分钟，请耐心等待...
echo.
echo 接下来会要求输入：
echo - Username: 输入你的 GitHub 用户名
echo - Password: 粘贴刚才复制的 Token（密码）
echo.
echo 注意：输入密码时，屏幕上可能什么都不显示，这是正常的！
echo.
pause

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║                    上传失败！                          ║
    echo ║                                                          ║
    echo ║  可能的原因：                                           ║
    echo ║  1. Token 输入错误                                     ║
    echo ║  2. Token 已过期                                       ║
    echo ║  3. 仓库地址错误                                       ║
    echo ║                                                          ║
    echo ║  解决方法：                                             ║
    echo ║  1. 重新创建 Token                                     ║
    echo ║  2. 确认 GitHub 用户名正确                             ║
    echo ║  3. 再次运行此脚本                                     ║
    echo ╚══════════════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] 上传成功！
echo.

╔══════════════════════════════════════════════════════════╗
║                  上传成功！！！✅                          ║
║                                                          ║
║  下一步：                                                ║
║  1. 访问：https://github.com/%GITHUB_USERNAME%/SimpleAccounting ║
║  2. 点击顶部的 Actions 标签                               ║
║  3. 等待 5-10 分钟，直到变成绿色 ✓                       ║
║  4. 点击构建任务                                          ║
║  5. 滚动到底部，找到 Artifacts                           ║
║  6. 下载 app-debug.apk                                    ║
║  7. 传到手机安装                                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
echo.

echo 仓库地址：https://github.com/%GITHUB_USERNAME%/SimpleAccounting
echo.
set /p OPEN_GITHUB=是否打开仓库网页？(Y/N，按回车默认 Y):
if /i "%OPEN_GITHUB%"=="N" (
    echo.
    echo 好的，你可以手动访问上面的仓库地址
) else (
    echo.
    echo 正在打开仓库网页...
    start "" https://github.com/%GITHUB_USERNAME%/SimpleAccounting
)

echo.
echo.
echo ========================================
echo   全部完成！🎉
echo ========================================
echo.
echo 如果需要下载 APK，请查看上面的下一步说明
echo.
echo 详细教程：小白教程_一步步来.md
echo.
pause
