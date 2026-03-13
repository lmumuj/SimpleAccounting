import subprocess
import sys
import os

# 设置编码
if sys.platform == 'win32':
    import locale
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 启动记账应用
script_path = os.path.join(os.path.dirname(__file__), 'preview_app.py')

try:
    subprocess.run([sys.executable, script_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"启动失败: {e}")
    print("请确保:")
    print("1. Python 3.6+ 已安装")
    print("2. Tkinter 模块可用")
    print("3. preview_app.py 文件存在")
    input("\n按回车键退出...")
except KeyboardInterrupt:
    print("\n\n应用已关闭")
except Exception as e:
    print(f"发生错误: {e}")
    input("\n按回车键退出...")
