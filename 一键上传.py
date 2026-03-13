#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单记账APP - 一键上传到 GitHub
只需要按几次回车就能完成所有操作！
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """打印标题"""
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)
    print()

def print_step(step, total, text):
    """打印步骤"""
    print(f"[{step}/{total}] {text}")

def print_success(text):
    """打印成功信息"""
    print(f"✓ {text}")

def print_error(text):
    """打印错误信息"""
    print(f"✗ {text}")

def print_info(text):
    """打印信息"""
    print(f"  {text}")

def run_command(cmd, show_output=False):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=300
        )

        if show_output and result.stdout:
            print(result.stdout)

        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print_error("命令超时")
        return False, "", "Timeout"
    except Exception as e:
        print_error(f"命令执行失败: {e}")
        return False, "", str(e)

def main():
    """主函数"""
    clear_screen()

    print_header("简单记账APP - 一键上传到 GitHub")
    print("你只需要按几次回车就能完成所有操作！")
    print()

    # 切换到项目目录
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    # 步骤1：检查环境
    print_step(1, 5, "检查环境...")
    print_success(f"已进入项目目录: {script_dir}")
    print()

    # 步骤2：创建提交
    print_step(2, 5, "创建提交...")
    # 尝试不同的提交消息
    messages = ["Initial", "Initial commit", ""]
    success = False
    for msg in messages:
        cmd = f'git commit -m "{msg}"' if msg else 'git commit -m ""'
        success, stdout, stderr = run_command(cmd)
        if success:
            break

    if success:
        print_success("提交成功")
    else:
        print_error("提交失败，可能已经是最新状态")

    print()

    # 步骤3：配置GitHub仓库
    print_step(3, 5, "配置 GitHub 仓库...")
    print()

    username = input("请输入你的 GitHub 用户名（然后按回车）: ").strip()
    if not username:
        print_error("用户名不能为空")
        input("按回车退出...")
        return False

    remote_url = f"https://github.com/{username}/SimpleAccounting.git"
    print_info(f"仓库地址: {remote_url}")
    print()

    # 添加远程仓库
    success, stdout, stderr = run_command(f'git remote add origin {remote_url}')
    if not success and "already exists" in stderr:
        # 如果已存在，先删除再添加
        run_command('git remote remove origin')
        success, stdout, stderr = run_command(f'git remote add origin {remote_url}')

    if not success:
        print_error("配置仓库失败")
        input("按回车退出...")
        return False

    # 设置分支
    run_command('git branch -M main')

    print_success("仓库配置完成")
    print()

    # 重要提示
    print("=" * 60)
    print("                    重要提示！！！")
    print("=" * 60)
    print()
    print("接下来会要求输入用户名和密码：")
    print()
    print("1. Username: 输入你的 GitHub 用户名")
    print()
    print("2. Password: 不要输入登录密码！")
    print("   需要先创建一个 Token（密钥）")
    print()
    print("如何创建 Token：")
    print("1. 访问：https://github.com/settings/tokens")
    print("2. 点击：Generate new token → Generate new token (classic)")
    print("3. 勾选：repo（全部勾选）")
    print("4. 点击：Generate token")
    print("5. 复制显示的 token（只显示一次！）")
    print()
    print("=" * 60)
    print()

    ready = input("准备好了吗？（按回车继续，或输入 N 取消）: ").strip().upper()
    if ready == 'N':
        print()
        print("操作已取消")
        input("按回车退出...")
        return False

    print()
    print_step(4, 5, "上传代码到 GitHub...")
    print_info("这个过程可能需要几分钟，请耐心等待...")
    print()
    print_info("接下来会要求输入：")
    print_info("- Username: 输入你的 GitHub 用户名")
    print_info("- Password: 粘贴刚才复制的 Token（密码）")
    print()
    print_info("注意：输入密码时，屏幕上可能什么都不显示，这是正常的！")
    print()

    input("按回车继续...")

    # 推送代码
    success, stdout, stderr = run_command('git push -u origin main', show_output=True)

    if not success:
        print()
        print("=" * 60)
        print("                    上传失败！")
        print("=" * 60)
        print()
        print("可能的原因：")
        print("1. Token 输入错误")
        print("2. Token 已过期")
        print("3. 仓库地址错误")
        print()
        print("解决方法：")
        print("1. 重新创建 Token")
        print("2. 确认 GitHub 用户名正确")
        print("3. 再次运行此脚本")
        print()
        print("=" * 60)
        print()
        input("按回车退出...")
        return False

    print()
    print_step(5, 5, "上传成功！")
    print()

    # 成功信息
    print("=" * 60)
    print("                  上传成功！！！✅")
    print("=" * 60)
    print()
    print("下一步：")
    print(f"1. 访问：https://github.com/{username}/SimpleAccounting")
    print("2. 点击顶部的 Actions 标签")
    print("3. 等待 5-10 分钟，直到变成绿色 ✓")
    print("4. 点击构建任务")
    print("5. 滚动到底部，找到 Artifacts")
    print("6. 下载 app-debug.apk")
    print("7. 传到手机安装")
    print()
    print("=" * 60)
    print()

    print(f"仓库地址：https://github.com/{username}/SimpleAccounting")
    print()

    open_github = input("是否打开仓库网页？(Y/N，按回车默认 Y): ").strip().upper()
    if open_github != 'N':
        print()
        print("正在打开仓库网页...")
        webbrowser.open(f"https://github.com/{username}/SimpleAccounting")

    print()
    print()
    print("=" * 60)
    print("  全部完成！🎉")
    print("=" * 60)
    print()
    print("如果需要下载 APK，请查看上面的下一步说明")
    print()
    print("详细教程：小白教程_一步步来.md")
    print()
    input("按回车退出...")
    return True

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        print()
        print()
        print("操作已取消")
        input("按回车退出...")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"发生错误: {e}")
        input("按回车退出...")
        sys.exit(1)
