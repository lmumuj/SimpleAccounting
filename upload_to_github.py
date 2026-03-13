#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传项目到 GitHub - 自动化脚本
"""

import os
import sys
import subprocess
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

def run_command(cmd, show_output=False):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            timeout=300
        )

        if show_output:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)

        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print_error(f"命令超时: {' '.join(cmd)}")
        return False, "", "Timeout"
    except Exception as e:
        print_error(f"命令执行失败: {e}")
        return False, "", str(e)

def check_git():
    """检查 Git 是否安装"""
    print_info("检查 Git 安装...")
    success, stdout, stderr = run_command('git --version')

    if success:
        version = stdout.strip().split()[-1]
        print_success(f"Git 版本: {version}")
        return True
    else:
        print_error("未安装 Git")
        print("\n请先安装 Git：")
        print("下载地址：https://git-scm.com/downloads")
        return False

def init_git():
    """初始化 Git 仓库"""
    git_dir = Path('.git')

    if git_dir.exists():
        print_warning("已存在 Git 仓库")
        response = input("是否重新初始化？(Y/N): ").strip().upper()
        if response == 'Y':
            success, stdout, stderr = run_command('rmdir /s /q .git')
            if success:
                print_success("已清理旧仓库")
            else:
                print_error("清理失败")
                return False
        else:
            return True

    print_info("初始化 Git 仓库...")
    success, stdout, stderr = run_command('git init')

    if success:
        print_success("Git 仓库初始化成功")
        return True
    else:
        print_error(f"初始化失败: {stderr}")
        return False

def add_files():
    """添加文件到 Git"""
    print_info("添加文件到 Git...")
    success, stdout, stderr = run_command('git add .')

    if success:
        print_success("文件添加成功")
        return True
    else:
        print_error(f"添加失败: {stderr}")
        return False

def commit():
    """创建提交"""
    print_info("创建初始提交...")
    success, stdout, stderr = run_command('git commit -m "Initial commit: Simple Accounting App"')

    if success:
        print_success("提交成功")
        return True
    else:
        print_error(f"提交失败: {stderr}")
        return False

def add_remote(username, repo_name):
    """添加远程仓库"""
    remote_url = f"https://github.com/{username}/{repo_name}.git"

    print_info(f"关联远程仓库: {remote_url}")
    success, stdout, stderr = run_command(f'git remote add origin {remote_url}')

    if success:
        print_success("远程仓库关联成功")
        return True, remote_url
    else:
        print_error(f"关联失败: {stderr}")
        return False, None

def push_code():
    """推送代码到 GitHub"""
    print_info("推送代码到 GitHub...")
    print_info("这可能需要几分钟，请耐心等待...")
    print()

    # 重命名分支为 main
    success, stdout, stderr = run_command('git branch -M main')
    if not success:
        print_error(f"重命名分支失败: {stderr}")
        return False

    # 推送代码
    success, stdout, stderr = run_command('git push -u origin main', show_output=True)

    if success:
        print_success("\n推送成功！")
        return True
    else:
        print_error("\n推送失败！")
        print("\n可能的原因：")
        print("1. 仓库不存在或地址错误")
        print("2. 未在 GitHub 上创建仓库")
        print("3. 需要身份验证")
        return False

def create_repo_instructions(username, repo_name):
    """显示创建仓库的说明"""
    print("\n" + "="*60)
    print("  在 GitHub 上创建仓库")
    print("="*60)
    print("\n步骤：")
    print(f"1. 访问：https://github.com/new")
    print(f"2. Repository name: {repo_name}")
    print(f"3. Description: Simple Accounting App")
    print(f"4. 选择 Public 或 Private")
    print(f"5. ⚠️  重要：不要初始化 README、.gitignore 或 License")
    print(f"6. 点击 Create repository")
    print()

def main():
    """主函数"""
    print_header("上传项目到 GitHub")

    # 切换到脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print_info(f"工作目录: {str(script_dir)}\n")

    # 步骤1：检查 Git
    print_header("[1/5] 检查环境")
    if not check_git():
        return False

    # 步骤2：初始化 Git
    print_header("[2/5] 初始化 Git 仓库")
    if not init_git():
        return False

    # 步骤3：添加文件
    print_header("[3/5] 添加文件")
    if not add_files():
        return False

    # 步骤4：提交
    print_header("[4/5] 创建提交")
    if not commit():
        return False

    # 步骤5：输入 GitHub 信息
    print_header("[5/5] 配置 GitHub")

    username = input("请输入你的 GitHub 用户名: ").strip()
    if not username:
        print_error("用户名不能为空")
        return False

    repo_name = input("请输入仓库名称（默认: SimpleAccounting）: ").strip()
    if not repo_name:
        repo_name = "SimpleAccounting"

    print()
    print("="*60)
    print(f"  仓库信息")
    print("="*60)
    print(f"用户名: {username}")
    print(f"仓库名: {repo_name}")
    print(f"仓库地址: https://github.com/{username}/{repo_name}.git")
    print()

    # 显示创建仓库的说明
    create_repo_instructions(username, repo_name)

    response = input("是否已在 GitHub 上创建仓库？(Y/N): ").strip().upper()
    if response != 'Y':
        print("\n请先在 GitHub 上创建仓库，然后重新运行此脚本")
        return False

    # 添加远程仓库
    print_info("关联远程仓库...")
    success, remote_url = add_remote(username, repo_name)
    if not success:
        return False

    # 推送代码
    print()
    response = input("是否推送代码到 GitHub？(Y/N): ").strip().upper()
    if response != 'Y':
        print_info("用户取消")
        return False

    print()
    print_header("推送代码")

    if push_code():
        print_header("上传成功！")
        print_success("代码已上传到 GitHub")
        print_info(f"仓库地址: {remote_url}")
        print("\n下一步：")
        print("1. 访问仓库查看 Actions 标签")
        print("2. 等待 GitHub Actions 自动构建（约 5-10 分钟）")
        print("3. 构建完成后下载 APK 文件")
        print("\n详细教程：GITHUB_ACTIONS_指南.md")
        print()

        # 询问是否打开仓库
        response = input("是否打开仓库页面？(Y/N): ").strip().upper()
        if response == 'Y':
            print(f"正在打开: https://github.com/{username}/{repo_name}")
            try:
                import webbrowser
                webbrowser.open(f"https://github.com/{username}/{repo_name}")
            except:
                print_info("请在浏览器中访问上面的链接")

        return True
    else:
        print_header("上传失败")
        print("\n故障排除：")
        print("1. 检查 GitHub 用户名和仓库名称是否正确")
        print("2. 确认仓库已在 GitHub 上创建")
        print("3. 检查网络连接")
        print("4. 查看上面的错误信息")
        print("\n详细教程：GITHUB_ACTIONS_指南.md")
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
