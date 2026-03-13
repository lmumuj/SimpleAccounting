#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单记账应用 - 自动打包工具
自动检查环境并尝试构建 APK
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path

class Colors:
    """控制台输出颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.YELLOW}[WARNING] {text}{Colors.RESET}")

def print_info(text):
    """打印信息"""
    print(f"[INFO] {text}")

def check_java_version():
    """检查 Java 版本"""
    print_info("检查 Java 版本...")
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        version_output = result.stderr if result.stderr else result.stdout

        # 解析版本号
        for line in version_output.split('\n'):
            if 'version' in line.lower():
                # 提取版本号，格式如：1.8.0_481 或 17.0.1
                version_str = line.split('"')[1] if '"' in line else line.split()[1]
                major_version = version_str.split('.')[0]

                if major_version == '1':
                    # Java 8 的版本号是 1.8.x
                    major_version = version_str.split('.')[1]

                print_info(f"检测到 Java 版本: {version_str}")

                if int(major_version) >= 17:
                    print_success("Java 版本满足要求 (17+)")
                    return True
                else:
                    print_warning(f"Java 版本过低 ({major_version}，需要 17+)")
                    return False
    except Exception as e:
        print_error(f"无法检测 Java 版本: {e}")
        return False

def check_gradle_wrapper():
    """检查 Gradle Wrapper"""
    print_info("检查 Gradle Wrapper...")

    wrapper_jar = Path("gradle/wrapper/gradle-wrapper.jar")
    wrapper_props = Path("gradle/wrapper/gradle-wrapper.properties")

    if not wrapper_props.exists():
        print_error("缺少 gradle-wrapper.properties")
        return False

    if not wrapper_jar.exists():
        print_warning("缺少 gradle-wrapper.jar")
        return False

    print_success("Gradle Wrapper 已就绪")
    return True

def download_gradle_wrapper():
    """下载 Gradle Wrapper JAR 文件"""
    print_info("尝试下载 gradle-wrapper.jar...")

    wrapper_jar = Path("gradle/wrapper/gradle-wrapper.jar")

    # GitHub 官方链接
    urls = [
        "https://raw.githubusercontent.com/gradle/gradle/v8.2.0/gradle/wrapper/gradle-wrapper.jar",
        "https://services.gradle.org/distributions/gradle-8.2-wrapper.jar",
    ]

    for url in urls:
        try:
            print_info(f"从 {url} 下载...")
            urllib.request.urlretrieve(url, wrapper_jar)
            print_success("下载成功！")
            return True
        except Exception as e:
            print_warning(f"从 {url} 下载失败: {e}")
            continue

    print_error("所有下载链接都失败")
    return False

def run_gradle_build():
    """运行 Gradle 构建"""
    print_info("开始构建 APK...")
    print_info("这可能需要几分钟，请耐心等待...")
    print()

    gradlew = Path("gradlew.bat") if os.name == 'nt' else Path("gradlew")

    if not gradlew.exists():
        print_error(f"未找到 {gradlew}")
        return False

    try:
        result = subprocess.run(
            [str(gradlew), 'assembleDebug'],
            capture_output=True,
            text=True,
            timeout=600  # 10分钟超时
        )

        print(result.stdout)

        if result.returncode == 0:
            print_success("\n构建成功！")

            # 查找 APK 文件
            apk_path = Path("app/build/outputs/apk/debug/app-debug.apk")
            if apk_path.exists():
                print_success(f"APK 文件位置: {str(apk_path.absolute())}")
                return True
            else:
                print_error("未找到生成的 APK 文件")
                return False
        else:
            print_error(f"\n构建失败，返回码: {result.returncode}")
            print_error("错误输出:")
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print_error("构建超时（超过10分钟）")
        return False
    except Exception as e:
        print_error(f"构建过程出错: {e}")
        return False

def main():
    """主函数"""
    print_header("简单记账应用 - 自动打包工具")

    # 切换到脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print_info(f"工作目录: {str(script_dir)}\n")

    # 步骤1：检查 Java 版本
    print_header("[1/4] 检查环境")
    if not check_java_version():
        print_error("Java 版本不满足要求")
        print("\n解决方案：")
        print("1. 安装 Android Studio（推荐）")
        print("   下载地址：https://developer.android.com/studio")
        print("   它会自动安装 Java 17+ 和所有必需工具\n")
        print("2. 或手动安装 JDK 17+")
        print("   下载地址：https://adoptium.net/\n")
        return False

    # 步骤2：检查 Gradle Wrapper
    print_header("[2/4] 检查 Gradle Wrapper")
    if not check_gradle_wrapper():
        print("\n尝试下载缺失的文件...")
        if not download_gradle_wrapper():
            print_error("无法修复 Gradle Wrapper")
            print("\n解决方案：")
            print("1. 使用 Android Studio 打开项目")
            print("2. Android Studio 会自动修复所有问题\n")
            return False

    # 步骤3：确认构建
    print_header("[3/4] 确认构建")
    print("即将构建 Debug 版本 APK...")
    response = input("是否继续？(Y/N): ").strip().upper()
    if response != 'Y':
        print_info("用户取消")
        return False

    # 步骤4：执行构建
    print_header("[4/4] 构建应用")
    if run_gradle_build():
        print_header("构建成功！")
        print_success("APK 文件已生成")
        print_info(f"文件位置: {str(Path('app/build/outputs/apk/debug/app-debug.apk').absolute())}")
        print()
        print("后续步骤：")
        print("1. 使用 USB 连接 Android 设备")
        print("2. 启用手机的 USB 调试（开发者选项）")
        print("3. 运行: adb install app/build/outputs/apk/debug/app-debug.apk")
        print()
        print("或者直接将 APK 文件传输到手机安装")
        return True
    else:
        print_header("构建失败")
        print("\n可能的原因：")
        print("1. 网络连接问题（无法下载依赖）")
        print("2. Android SDK 未安装或配置错误")
        print("3. 磁盘空间不足")
        print("4. 其他环境问题\n")
        print("推荐解决方案：")
        print("使用 Android Studio 打开项目，它会更友好地处理这些问题\n")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_warning("\n\n用户中断")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
