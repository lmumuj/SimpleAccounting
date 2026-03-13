import tkinter as tk
from tkinter import messagebox

# 创建一个简单的测试窗口
root = tk.Tk()
root.title("测试窗口")
root.geometry("400x300")

# 添加一个标签
label = tk.Label(root, text="Tkinter工作正常！\n记账应用可以运行。", font=("Arial", 14))
label.pack(pady=50)

# 添加一个按钮
def on_click():
    messagebox.showinfo("成功", "Tkinter测试通过！")

button = tk.Button(root, text="测试", command=on_click, font=("Arial", 12))
button.pack(pady=20)

root.mainloop()
