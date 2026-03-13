@echo off
chcp 65001 >nul
echo ========================================
echo   简单记账应用 - 快速打包工具
echo ========================================
echo.

echo [1/5] 检查Java版本...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到Java
    echo.
    echo 请按以下步骤操作：
    echo 1. 下载并安装 Android Studio: https://developer.android.com/studio
    echo 2. 使用 Android Studio 打开项目：c:\Users\Admins\Documents\记账
    echo 3. 等待Gradle同步完成后，点击 Build -^> Build APK(s)
    echo.
    pause
    exit /b 1
)

for /f "tokens=3" %%i in ('java -version 2^>^&1 ^| findstr /i "version"') do set JAVA_VERSION=%%i
set JAVA_VERSION=%JAVA_VERSION:"=%
echo ✅ 检测到Java版本: %JAVA_VERSION%

REM 检查Java版本是否为17+
for /f "tokens=1,2 delims=." %%a in ("%JAVA_VERSION%") do (
    if %%a lss 17 (
        echo ❌ 错误：Java版本过低（当前：%%a.%%b，需要：17+）
        echo.
        echo 解决方案：
        echo 1. 下载 OpenJDK 17: https://adoptium.net/
        echo 2. 安装后配置 JAVA_HOME 环境变量
        echo 3. 或者直接安装 Android Studio（推荐）
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [2/5] 检查Gradle Wrapper...
if not exist "gradle\wrapper\gradle-wrapper.jar" (
    echo ❌ 错误：缺少 gradle-wrapper.jar
    echo.
    echo 解决方案：
    echo 使用 Android Studio 打开项目，它会自动下载所需的Gradle文件
    echo.
    pause
    exit /b 1
)
echo ✅ Gradle Wrapper 已就绪

echo.
echo [3/5] 进入项目目录...
cd /d "%~dp0"
if %errorlevel% neq 0 (
    echo ❌ 错误：无法进入项目目录
    pause
    exit /b 1
)
echo ✅ 已进入项目目录

echo.
echo [4/5] 开始构建Debug APK...
echo 这可能需要几分钟，请耐心等待...
echo.

call gradlew.bat assembleDebug

if %errorlevel% neq 0 (
    echo.
    echo ❌ 构建失败！
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题（无法下载依赖）
    echo 2. Android SDK未安装或配置错误
    echo 3. 磁盘空间不足
    echo.
    echo 建议：使用 Android Studio 打开项目，它会更友好地处理这些问题
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] 查找APK文件...
if exist "app\build\outputs\apk\debug\app-debug.apk" (
    echo.
    echo ========================================
    echo   ✅ 构建成功！
    echo ========================================
    echo.
    echo APK文件位置：
    echo %CD%\app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo 后续操作：
    echo 1. 使用 USB 连接 Android 设备
    echo 2. 在设备上启用"USB调试"（开发者选项）
    echo 3. 运行：adb install app\build\outputs\apk\debug\app-debug.apk
    echo.
    
    REM 询问是否打开文件夹
    set /p OPEN_FOLDER="是否打开APK所在文件夹？(Y/N): "
    if /i "%OPEN_FOLDER%"=="Y" (
        explorer "app\build\outputs\apk\debug"
    )
) else (
    echo ❌ 错误：未找到生成的APK文件
    echo 请检查构建日志
)

echo.
pause
