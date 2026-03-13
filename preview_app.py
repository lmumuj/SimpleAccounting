#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单记账 - Python桌面预览版
使用Tkinter实现，模拟Android应用的功能和界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional

# 数据模型
class Transaction:
    def __init__(self, id: int, type: str, amount: float, category_id: int,
                 remark: str, date: str, create_time: str):
        self.id = id
        self.type = type  # 'expense' or 'income'
        self.amount = amount
        self.category_id = category_id
        self.remark = remark
        self.date = date
        self.create_time = create_time

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'amount': self.amount,
            'category_id': self.category_id,
            'remark': self.remark,
            'date': self.date,
            'create_time': self.create_time
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            data['id'], data['type'], data['amount'],
            data['category_id'], data['remark'], data['date'], data['create_time']
        )

# 类别配置
class Category:
    EXPENSE_CATEGORIES = [
        {'id': 1, 'name': '餐饮', 'icon': '🍔'},
        {'id': 2, 'name': '交通', 'icon': '🚗'},
        {'id': 3, 'name': '购物', 'icon': '🛒'},
        {'id': 4, 'name': '娱乐', 'icon': '🎮'},
        {'id': 5, 'name': '医疗', 'icon': '💊'},
        {'id': 6, 'name': '教育', 'icon': '📚'},
        {'id': 7, 'name': '居住', 'icon': '🏠'},
        {'id': 8, 'name': '其他', 'icon': '📦'}
    ]

    INCOME_CATEGORIES = [
        {'id': 101, 'name': '工资', 'icon': '💰'},
        {'id': 102, 'name': '奖金', 'icon': '🎁'},
        {'id': 103, 'name': '投资', 'icon': '📈'},
        {'id': 104, 'name': '兼职', 'icon': '💼'},
        {'id': 105, 'name': '其他', 'icon': '📦'}
    ]

    @staticmethod
    def get_category(category_id: int, type: str) -> Optional[Dict]:
        categories = Category.EXPENSE_CATEGORIES if type == 'expense' else Category.INCOME_CATEGORIES
        for cat in categories:
            if cat['id'] == category_id:
                return cat
        return None

# 数据管理
class DataManager:
    def __init__(self, data_file: str = 'transactions.json'):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.transactions = [Transaction.from_dict(t) for t in data]
            except Exception as e:
                print(f"加载数据失败: {e}")
                self.transactions = []

    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([t.to_dict() for t in self.transactions], f,
                         ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False

    def add_transaction(self, transaction: Transaction):
        self.transactions.insert(0, transaction)
        return self.save_data()

    def update_transaction(self, transaction: Transaction):
        for i, t in enumerate(self.transactions):
            if t.id == transaction.id:
                self.transactions[i] = transaction
                return self.save_data()
        return False

    def delete_transaction(self, transaction_id: int):
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        return self.save_data()

    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        for t in self.transactions:
            if t.id == transaction_id:
                return t
        return None

    def get_all_transactions(self) -> List[Transaction]:
        return self.transactions

    def get_filtered_transactions(self, filter_type: str = 'all') -> List[Transaction]:
        if filter_type == 'all':
            return self.transactions
        elif filter_type == 'expense':
            return [t for t in self.transactions if t.type == 'expense']
        elif filter_type == 'income':
            return [t for t in self.transactions if t.type == 'income']
        return self.transactions

    def get_monthly_totals(self):
        now = datetime.now()
        current_month = now.strftime('%Y-%m')

        expense_total = sum(
            t.amount for t in self.transactions
            if t.type == 'expense' and t.date.startswith(current_month)
        )
        income_total = sum(
            t.amount for t in self.transactions
            if t.type == 'income' and t.date.startswith(current_month)
        )

        return expense_total, income_total

    def get_period_totals(self, period: str):
        now = datetime.now()

        if period == 'week':
            # 本周（周一）
            week_start = now - timedelta(days=now.weekday())
            filtered = [t for t in self.transactions
                       if datetime.strptime(t.date, '%Y-%m-%d') >= week_start]
        elif period == 'month':
            # 本月
            month_start = now.replace(day=1)
            filtered = [t for t in self.transactions
                       if datetime.strptime(t.date, '%Y-%m-%d') >= month_start]
        else:  # year
            # 本年
            year_start = now.replace(month=1, day=1)
            filtered = [t for t in self.transactions
                       if datetime.strptime(t.date, '%Y-%m-%d') >= year_start]

        expense_total = sum(t.amount for t in filtered if t.type == 'expense')
        income_total = sum(t.amount for t in filtered if t.type == 'income')

        return expense_total, income_total, filtered

    def get_category_stats(self, transactions: List[Transaction]):
        stats = {}
        for t in transactions:
            category = Category.get_category(t.category_id, t.type)
            if not category:
                continue

            key = f"{t.type}_{t.category_id}"
            if key not in stats:
                stats[key] = {
                    'name': category['name'],
                    'icon': category['icon'],
                    'amount': 0,
                    'type': t.type
                }
            stats[key]['amount'] += t.amount

        return sorted(stats.values(), key=lambda x: x['amount'], reverse=True)

    def clear_all(self):
        self.transactions = []
        return self.save_data()

    def get_stats(self):
        total_records = len(self.transactions)
        unique_dates = len(set(t.date for t in self.transactions))
        used_categories = len(set(t.category_id for t in self.transactions))
        return total_records, unique_dates, used_categories

# 主应用界面
class AccountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("简单记账 - Python预览版")
        self.root.geometry("400x700")
        self.root.resizable(False, False)

        self.data_manager = DataManager()
        self.current_filter = 'all'
        self.editing_transaction = None

        # 样式配置
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # 配色方案
        self.colors = {
            'primary': '#4A90E2',
            'expense': '#FF5252',
            'income': '#52C41A',
            'bg': '#F5F5F5',
            'card_bg': '#FFFFFF',
            'text': '#333333',
            'text_secondary': '#999999'
        }

        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('Card.TFrame', background=self.colors['card_bg'])
        self.style.configure('TLabel', background=self.colors['card_bg'],
                            foreground=self.colors['text'])
        self.style.configure('TButton', background=self.colors['primary'],
                            foreground='white', borderwidth=0)
        self.style.map('TButton', background=[('active', '#357ABD')])

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # 主容器
        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 顶部总览卡片
        self.create_overview_card(main_container)

        # 筛选按钮
        self.create_filter_buttons(main_container)

        # 交易列表
        self.create_transaction_list(main_container)

        # 底部导航
        self.create_bottom_nav(main_container)

    def create_overview_card(self, parent):
        card = tk.Frame(parent, bg=self.colors['primary'],
                      padx=20, pady=20, relief=tk.RAISED, bd=0)
        card.pack(fill=tk.X, pady=(0, 15))

        # 获取本月数据
        expense, income = self.data_manager.get_monthly_totals()

        # 支出
        expense_frame = tk.Frame(card, bg=self.colors['primary'])
        expense_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(expense_frame, text="本月支出",
                bg=self.colors['primary'], fg='white',
                font=('Arial', 10)).pack()
        tk.Label(expense_frame, text=f"¥{expense:.2f}",
                bg=self.colors['primary'], fg='white',
                font=('Arial', 20, 'bold')).pack(pady=5)

        # 分隔线
        tk.Frame(card, bg='white', width=2).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # 收入
        income_frame = tk.Frame(card, bg=self.colors['primary'])
        income_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(income_frame, text="本月收入",
                bg=self.colors['primary'], fg='white',
                font=('Arial', 10)).pack()
        tk.Label(income_frame, text=f"¥{income:.2f}",
                bg=self.colors['primary'], fg='white',
                font=('Arial', 20, 'bold')).pack(pady=5)

        self.overview_card = card

    def create_filter_buttons(self, parent):
        filter_frame = tk.Frame(parent, bg=self.colors['bg'])
        filter_frame.pack(fill=tk.X, pady=(0, 15))

        self.filter_buttons = {}

        for i, (filter_type, text) in enumerate([('all', '全部'),
                                                  ('expense', '支出'),
                                                  ('income', '收入')]):
            btn = tk.Button(filter_frame, text=text,
                          font=('Arial', 10),
                          bg='white', fg='#666666',
                          relief=tk.FLAT, padx=15, pady=8,
                          command=lambda ft=filter_type: self.set_filter(ft))
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0 if i == 0 else 5, 0))
            self.filter_buttons[filter_type] = btn

        self.update_filter_buttons()

    def update_filter_buttons(self):
        for filter_type, btn in self.filter_buttons.items():
            if filter_type == self.current_filter:
                btn.config(bg=self.colors['primary'], fg='white')
            else:
                btn.config(bg='white', fg='#666666')

    def set_filter(self, filter_type):
        self.current_filter = filter_type
        self.update_filter_buttons()
        self.update_transaction_list()

    def create_transaction_list(self, parent):
        # 列表容器
        list_container = tk.Frame(parent, bg=self.colors['card_bg'],
                                relief=tk.RAISED, bd=0)
        list_container.pack(fill=tk.BOTH, expand=True)

        # 使用Text组件和滚动条
        self.list_text = tk.Text(list_container, bg=self.colors['card_bg'],
                               wrap=tk.WORD, font=('Arial', 11),
                               height=15, relief=tk.FLAT,
                               padx=10, pady=10)
        self.list_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 绑定点击事件
        self.list_text.bind('<Button-1>', self.on_transaction_click)

        scrollbar = ttk.Scrollbar(list_container, command=self.list_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_text.config(yscrollcommand=scrollbar.set)
        self.list_text.config(state=tk.DISABLED)

    def on_transaction_click(self, event):
        # 获取点击位置的行号
        index = self.list_text.index(f"@{event.x},{event.y}")
        line_num = int(float(index.split('.')[0]))

        transactions = self.data_manager.get_filtered_transactions(self.current_filter)

        # 计算对应的交易（每笔交易占2行）
        transaction_index = (line_num - 1) // 2

        if 0 <= transaction_index < len(transactions):
            transaction = transactions[transaction_index]
            self.open_edit_dialog(transaction)

    def update_transaction_list(self):
        transactions = self.data_manager.get_filtered_transactions(self.current_filter)

        self.list_text.config(state=tk.NORMAL)
        self.list_text.delete(1.0, tk.END)

        if not transactions:
            self.list_text.insert(tk.END, "还没有记账记录\n\n点击右下角按钮开始记账")
            self.list_text.tag_add('center', '1.0', 'end')
            self.list_text.tag_config('center', justify='center',
                                    foreground=self.colors['text_secondary'])
        else:
            for t in transactions:
                category = Category.get_category(t.category_id, t.type)

                # 格式化日期
                date_obj = datetime.strptime(t.date, '%Y-%m-%d')
                date_str = date_obj.strftime('%m月%d日')
                time_str = date_obj.strftime('%H:%M')

                # 格式化金额
                amount_prefix = '-' if t.type == 'expense' else '+'
                amount_color = self.colors['expense'] if t.type == 'expense' else self.colors['income']

                # 插入交易记录
                self.list_text.insert(tk.END,
                    f"{category['icon']}  {category['name']}\n",
                    'info'
                )
                self.list_text.insert(tk.END,
                    f"{date_str} {time_str}    {amount_prefix}¥{t.amount:.2f}\n",
                    'amount'
                )

                # 配置标签
                self.list_text.tag_config('amount', foreground=amount_color,
                                        font=('Arial', 11, 'bold'))

        self.list_text.config(state=tk.DISABLED)

        # 更新总览
        self.update_overview()

    def update_overview(self):
        self.overview_card.destroy()
        self.create_overview_card(self.root.winfo_children()[0])

    def create_bottom_nav(self, parent):
        nav_frame = tk.Frame(parent, bg='white', height=60)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # 添加按钮
        add_btn = tk.Button(nav_frame, text="+ 记账",
                           font=('Arial', 14, 'bold'),
                           bg=self.colors['primary'], fg='white',
                           relief=tk.FLAT, padx=30, pady=10,
                           command=self.open_add_dialog)
        add_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        # 统计按钮
        stats_btn = tk.Button(nav_frame, text="📊 统计",
                            font=('Arial', 11),
                            bg='white', fg='#666666',
                            relief=tk.FLAT, padx=20, pady=10,
                            command=self.open_statistics)
        stats_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # 我的按钮
        mine_btn = tk.Button(nav_frame, text="👤 我的",
                           font=('Arial', 11),
                           bg='white', fg='#666666',
                           relief=tk.FLAT, padx=20, pady=10,
                           command=self.open_mine)
        mine_btn.pack(side=tk.LEFT, padx=10, pady=10)

    def update_display(self):
        self.update_transaction_list()

    def open_add_dialog(self):
        self.open_add_edit_dialog(None)

    def open_edit_dialog(self, transaction):
        self.open_add_edit_dialog(transaction)

    def open_add_edit_dialog(self, transaction):
        dialog = tk.Toplevel(self.root)
        dialog.title("记账" if transaction is None else "编辑")
        dialog.geometry("380x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (380 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"380x500+{x}+{y}")

        # 类型选择
        type_frame = tk.Frame(dialog, padx=20, pady=10)
        type_frame.pack(fill=tk.X)

        tk.Label(type_frame, text="类型：").pack(side=tk.LEFT)

        type_var = tk.StringVar(value=transaction.type if transaction else 'expense')
        type_rbtn1 = tk.Radiobutton(type_frame, text="支出",
                                    variable=type_var, value='expense')
        type_rbtn1.pack(side=tk.LEFT, padx=10)

        type_rbtn2 = tk.Radiobutton(type_frame, text="收入",
                                    variable=type_var, value='income')
        type_rbtn2.pack(side=tk.LEFT, padx=10)

        # 金额输入
        amount_frame = tk.Frame(dialog, padx=20, pady=10)
        amount_frame.pack(fill=tk.X)

        tk.Label(amount_frame, text="金额：").pack(side=tk.LEFT)

        amount_var = tk.StringVar(value=str(transaction.amount) if transaction else '')
        amount_entry = tk.Entry(amount_frame, textvariable=amount_var,
                              font=('Arial', 14), width=15)
        amount_entry.pack(side=tk.LEFT, padx=10)

        # 类别选择
        category_frame = tk.Frame(dialog, padx=20, pady=10)
        category_frame.pack(fill=tk.X)

        tk.Label(category_frame, text="类别：").pack(side=tk.LEFT)

        category_var = tk.IntVar(value=transaction.category_id if transaction else 1)
        category_combo = ttk.Combobox(category_frame, textvariable=category_var,
                                    width=15, state='readonly')
        category_combo.pack(side=tk.LEFT, padx=10)

        def update_categories():
            type_val = type_var.get()
            categories = Category.EXPENSE_CATEGORIES if type_val == 'expense' else Category.INCOME_CATEGORIES
            category_combo['values'] = [f"{cat['icon']} {cat['name']}" for cat in categories]
            category_combo.current(0)
            category_var.set(categories[0]['id'])

        update_categories()
        type_rbtn1.config(command=update_categories)
        type_rbtn2.config(command=update_categories)

        if transaction:
            # 恢复选中的类别
            cat = Category.get_category(transaction.category_id, transaction.type)
            if cat:
                for i, c in enumerate(Category.EXPENSE_CATEGORIES if transaction.type == 'expense' else Category.INCOME_CATEGORIES):
                    if c['id'] == cat['id']:
                        category_combo.current(i)
                        break

        # 备注输入
        remark_frame = tk.Frame(dialog, padx=20, pady=10)
        remark_frame.pack(fill=tk.X)

        tk.Label(remark_frame, text="备注：").pack(side=tk.LEFT)

        remark_var = tk.StringVar(value=transaction.remark if transaction else '')
        remark_entry = tk.Entry(remark_frame, textvariable=remark_var,
                              width=20)
        remark_entry.pack(side=tk.LEFT, padx=10)

        # 日期选择
        date_frame = tk.Frame(dialog, padx=20, pady=10)
        date_frame.pack(fill=tk.X)

        tk.Label(date_frame, text="日期：").pack(side=tk.LEFT)

        date_var = tk.StringVar(value=transaction.date if transaction else datetime.now().strftime('%Y-%m-%d'))
        date_entry = tk.Entry(date_frame, textvariable=date_var, width=15)
        date_entry.pack(side=tk.LEFT, padx=10)

        # 按钮区域
        button_frame = tk.Frame(dialog, padx=20, pady=20)
        button_frame.pack(fill=tk.X)

        def save():
            amount = amount_var.get().strip()
            if not amount or not amount.replace('.', '').isdigit() or float(amount) <= 0:
                messagebox.showerror("错误", "请输入有效金额")
                return

            type_val = type_var.get()
            category_id = category_var.get()
            remark = remark_var.get().strip()
            date_str = date_var.get().strip()

            if not date_str:
                messagebox.showerror("错误", "请输入日期")
                return

            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("错误", "日期格式不正确，应为 YYYY-MM-DD")
                return

            new_transaction = Transaction(
                id=transaction.id if transaction else int(datetime.now().timestamp()),
                type=type_val,
                amount=float(amount),
                category_id=category_id,
                remark=remark,
                date=date_str,
                create_time=transaction.create_time if transaction else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

            if transaction:
                self.data_manager.update_transaction(new_transaction)
                messagebox.showinfo("成功", "更新成功")
            else:
                self.data_manager.add_transaction(new_transaction)
                messagebox.showinfo("成功", "添加成功")

            self.update_display()
            dialog.destroy()

        tk.Button(button_frame, text="保存", command=save,
                 bg=self.colors['primary'], fg='white',
                 font=('Arial', 12), width=10).pack(side=tk.LEFT, padx=5)

        if transaction:
            def delete():
                if messagebox.askyesno("确认", "确定要删除这条记录吗？"):
                    self.data_manager.delete_transaction(transaction.id)
                    self.update_display()
                    dialog.destroy()

            tk.Button(button_frame, text="删除", command=delete,
                     bg=self.colors['expense'], fg='white',
                     font=('Arial', 12), width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="取消", command=dialog.destroy,
                 bg='#999999', fg='white',
                 font=('Arial', 12), width=10).pack(side=tk.LEFT, padx=5)

    def open_statistics(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("统计")
        dialog.geometry("380x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (380 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"380x500+{x}+{y}")

        # 创建容器
        container = tk.Frame(dialog, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 时间选择
        time_frame = tk.Frame(container, bg=self.colors['bg'])
        time_frame.pack(fill=tk.X, pady=(0, 15))

        period_var = tk.StringVar(value='month')

        for i, (value, text) in enumerate([('week', '本周'), ('month', '本月'), ('year', '本年')]):
            rb = tk.Radiobutton(time_frame, text=text, variable=period_var,
                               value=value, bg=self.colors['bg'],
                               command=lambda: self.update_statistics_display(dialog, period_var))
            rb.pack(side=tk.LEFT, expand=True)

        # 统计显示区域
        stats_text = tk.Text(container, bg=self.colors['card_bg'],
                           wrap=tk.WORD, font=('Arial', 11),
                           height=20, relief=tk.FLAT,
                           padx=10, pady=10)
        stats_text.pack(fill=tk.BOTH, expand=True)
        stats_text.config(state=tk.DISABLED)

        def update_stats():
            period = period_var.get()
            expense, income, transactions = self.data_manager.get_period_totals(period)
            balance = income - expense

            stats_text.config(state=tk.NORMAL)
            stats_text.delete(1.0, tk.END)

            # 总览
            stats_text.insert(tk.END, f"总支出：¥{expense:.2f}\n")
            stats_text.insert(tk.END, f"总收入：¥{income:.2f}\n")
            stats_text.insert(tk.END, f"结余：¥{balance:.2f}\n\n")
            stats_text.tag_add('balance', '3.0', '3.end')

            balance_color = self.colors['income'] if balance >= 0 else self.colors['expense']
            stats_text.tag_config('balance', foreground=balance_color,
                                 font=('Arial', 12, 'bold'))

            # 分类统计
            category_stats = self.data_manager.get_category_stats(transactions)

            if category_stats:
                stats_text.insert(tk.END, "支出分类：\n")
                for stat in category_stats:
                    if stat['type'] == 'expense':
                        percent = (stat['amount'] / expense * 100) if expense > 0 else 0
                        stats_text.insert(tk.END,
                            f"{stat['icon']} {stat['name']}：¥{stat['amount']:.2f} ({percent:.1f}%)\n")

                stats_text.insert(tk.END, "\n收入分类：\n")
                for stat in category_stats:
                    if stat['type'] == 'income':
                        percent = (stat['amount'] / income * 100) if income > 0 else 0
                        stats_text.insert(tk.END,
                            f"{stat['icon']} {stat['name']}：¥{stat['amount']:.2f} ({percent:.1f}%)\n")
            else:
                stats_text.insert(tk.END, "\n暂无数据\n")

            stats_text.config(state=tk.DISABLED)

        dialog.update_stats = update_stats
        update_stats()

    def update_statistics_display(self, dialog, period_var):
        dialog.update_stats()

    def open_mine(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("我的")
        dialog.geometry("380x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (380 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"380x400+{x}+{y}")

        # 创建容器
        container = tk.Frame(dialog, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 统计信息
        total_records, unique_dates, used_categories = self.data_manager.get_stats()

        stats_frame = tk.Frame(container, bg=self.colors['card_bg'],
                             padx=15, pady=15)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        for i, (label, value) in enumerate([("记账笔数", total_records),
                                            ("记账天数", unique_dates),
                                            ("使用类别", used_categories)]):
            tk.Label(stats_frame, text=label,
                    font=('Arial', 10)).grid(row=i, column=0, sticky='w', pady=5)
            tk.Label(stats_frame, text=str(value),
                    font=('Arial', 14, 'bold'),
                    fg=self.colors['primary']).grid(row=i, column=1, sticky='e', pady=5)

        stats_frame.columnconfigure(1, weight=1)

        # 功能按钮
        button_frame = tk.Frame(container, bg=self.colors['card_bg'],
                              padx=15, pady=10)
        button_frame.pack(fill=tk.X)

        def export_data():
            transactions = self.data_manager.get_all_transactions()
            if not transactions:
                messagebox.showinfo("提示", "暂无数据可导出")
                return

            csv_content = "日期,类型,类别,金额,备注\n"
            for t in transactions:
                category = Category.get_category(t.category_id, t.type)
                type_text = "支出" if t.type == 'expense' else "收入"
                csv_content += f"{t.date},{type_text},{category['name']},{t.amount},{t.remark}\n"

            dialog.root.clipboard_clear()
            dialog.root.clipboard_append(csv_content)
            messagebox.showinfo("成功", "数据已复制到剪贴板")

        tk.Button(button_frame, text="📤 导出数据",
                 command=export_data,
                 bg='white', fg=self.colors['text'],
                 font=('Arial', 11), relief=tk.FLAT,
                 width=25, pady=10).pack(pady=5)

        def clear_data():
            if messagebox.askyesno("确认清空", "确定要清空所有记账数据吗？此操作不可恢复！"):
                self.data_manager.clear_all()
                self.update_display()
                messagebox.showinfo("成功", "清空成功")
                dialog.destroy()

        tk.Button(button_frame, text="🗑️ 清空数据",
                 command=clear_data,
                 bg='white', fg=self.colors['expense'],
                 font=('Arial', 11), relief=tk.FLAT,
                 width=25, pady=10).pack(pady=5)

        tk.Button(button_frame, text="ℹ️ 关于我们",
                 command=lambda: messagebox.showinfo("关于简单记账",
                                                   "简单记账 v1.0.0\n\n这是一款轻量级的个人记账工具，\n界面简洁，操作便捷，\n帮助您轻松管理个人财务。"),
                 bg='white', fg=self.colors['text'],
                 font=('Arial', 11), relief=tk.FLAT,
                 width=25, pady=10).pack(pady=5)

        tk.Button(button_frame, text="关闭", command=dialog.destroy,
                 bg='#999999', fg='white',
                 font=('Arial', 11), relief=tk.FLAT,
                 width=25, pady=10).pack(pady=10)

# 主程序入口
def main():
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
