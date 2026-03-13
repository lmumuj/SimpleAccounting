#!/usr/bin/env python3
import urllib.request
import os

# 下载 gradle-wrapper.jar
url = "https://raw.githubusercontent.com/gradle/gradle/v8.2.0/gradle/wrapper/gradle-wrapper.jar"
target = "gradle/wrapper/gradle-wrapper.jar"

print(f"正在下载: {url}")
print(f"保存到: {target}")

try:
    urllib.request.urlretrieve(url, target)
    print("下载成功！")
    print(f"文件已保存到: {os.path.abspath(target)}")
except Exception as e:
    print(f"下载失败: {e}")
