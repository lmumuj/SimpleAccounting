#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单记账 - 现代化桌面预览版
使用Tkinter实现，采用现代化设计语言
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional
import random

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

# 类别配置 - 使用现代化emoji图标
class Category:
    EXPENSE_CATEGORIES = [
        {'id': 1, 'name': '餐饮', 'icon': '🍜', 'color': '#FF6B6B'},
        {'id': 2, 'name': '交通', 'icon': '🚇', 'color': '#4ECDC4'},
        {'id': 3, 'name': '购物', 'icon': '🛍️', 'color': '#45B7D1'},
        {'id': 4, 'name': '娱乐', 'icon': '🎮', 'color': '#96CEB4'},
        {'id': 5, 'name': '医疗', 'icon': '💊', 'color': '#FFEAA7'},
        {'id': 6, 'name': '教育', 'icon': '📚', 'color': '#DDA0DD'},
        {'id': 7, 'name': '居住', 'icon': '🏠', 'color': '#98D8C8'},
        {'id': 8, 'name': '其他', 'icon': '📦', 'color': '#F7DC6F'}
    ]

    INCOME_CATEGORIES = [
        {'id': 101, 'name': '工资', 'icon': '💳', 'color': '#52B788'},
        {'id': 102, 'name': '奖金', 'icon': '🎁', 'color': '#F7B731'},
        {'id': 103, 'name': '投资', 'icon': '📈', 'color': '#2ED573'},
        {'id': 104, 'name': '兼职', 'icon': '💼', 'color': '#3742FA'},
        {'id': 105, 'name': '其他', 'icon': '✨', 'color': '#A55EEA'}
    ]

    @staticmethod
    def get_category(category_id: int, type: str) -> Optional[Dict]:
        categories = Category.EXPENSE_CATEGORIES if type == 'expense' else Category.INCOME_CATEGORIES
        for cat in categories:
            if cat['id'] == category_id:
                return cat
        return None

# 现代化记账应用
class ModernAccountingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("✨ 简单记账")
        self.root.geometry("420x800")
        self.root.minsize(380, 700)
        
        # 现代化配色方案 - 采用流行的设计系统
        self.colors = {
            'primary': '#667EEA',           # 现代紫色渐变
            'primary_dark': '#764BA2',
            'secondary': '#F093FB',
            'expense': '#FF5252',          # 现代红色
            'income': '#00C853',            # 鲜艳绿色
            'bg': '#F8F9FA',                # 浅灰背景
            'surface': '#FFFFFF',           # 纯白表面
            'text_primary': '#2D3436',      # 深色文字
            'text_secondary': '#636E72',    # 灰色文字
            'divider': '#DFE6E9',           # 分隔线
            'shadow': 'rgba(0,0,0,0.1)',    # 阴影
            'card_shadow': '#E0E0E0',
            'success': '#00B894',
            'warning': '#FDCB6E',
            'error': '#FF7675'
        }
        
        # 设置背景色
        self.root.configure(bg=self.colors['bg'])
        
        # 数据存储
        self.transactions: List[Transaction] = []
        self.current_filter = 'all'  # all, expense, income
        self.current_edit_transaction = None
        
        # 加载数据
        self.load_data()
        
        # 创建界面
        self.create_ui()
        
    def load_data(self):
        """加载数据"""
        try:
            with open('transactions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.transactions = [Transaction.from_dict(item) for item in data]
        except FileNotFoundError:
            self.transactions = []
        except Exception as e:
            print(f"加载数据失败: {e}")
            self.transactions = []
    
    def save_data(self):
        """保存数据"""
        try:
            data = [t.to_dict() for t in self.transactions]
            with open('transactions.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存数据失败: {e}")
    
    def create_ui(self):
        """创建用户界面"""
        # 主容器
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 顶部标题栏
        self.create_header(main_frame)
        
        # 总览卡片
        self.create_summary_card(main_frame)
        
        # 筛选按钮
        self.create_filter_buttons(main_frame)
        
        # 交易列表容器
        self.create_transaction_list(main_frame)
        
        # 底部导航栏
        self.create_bottom_nav(main_frame)
    
    def create_header(self, parent):
        """创建现代化头部"""
        header = tk.Frame(parent, bg=self.colors['bg'])
        header.pack(fill='x', pady=(0, 20))
        
        # 标题
        title_label = tk.Label(
            header,
            text="✨ 简单记账",
            font=("Microsoft YaHei UI", 28, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        )
        title_label.pack(side='left')
        
        # 日期
        today = datetime.now().strftime("%Y年%m月%d日")
        date_label = tk.Label(
            header,
            text=today,
            font=("Microsoft YaHei UI", 12),
            bg=self.colors['bg'],
            fg=self.colors['text_secondary']
        )
        date_label.pack(side='right')
    
    def create_summary_card(self, parent):
        """创建总览卡片"""
        # 卡片容器（带圆角效果）
        card = tk.Frame(parent, bg=self.colors['surface'], height=180)
        card.pack(fill='x', pady=(0, 20))
        
        # 添加边框和阴影效果
        self.style_card(card)
        
        # 收支标题
        summary_frame = tk.Frame(card, bg=self.colors['surface'])
        summary_frame.pack(fill='x', padx=25, pady=20)
        
        # 支出部分
        expense_frame = tk.Frame(summary_frame, bg=self.colors['surface'])
        expense_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            expense_frame,
            text="💸 支出",
            font=("Microsoft YaHei UI", 14),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w')
        
        self.expense_label = tk.Label(
            expense_frame,
            text="¥0.00",
            font=("Microsoft YaHei UI", 24, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['expense']
        )
        self.expense_label.pack(anchor='w', pady=(5, 0))
        
        # 收入部分
        income_frame = tk.Frame(summary_frame, bg=self.colors['surface'])
        income_frame.pack(side='right', fill='x', expand=True)
        
        tk.Label(
            income_frame,
            text="💰 收入",
            font=("Microsoft YaHei UI", 14),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(anchor='e')
        
        self.income_label = tk.Label(
            income_frame,
            text="¥0.00",
            font=("Microsoft YaHei UI", 24, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['income']
        )
        self.income_label.pack(anchor='e', pady=(5, 0))
        
        # 分隔线
        ttk.Separator(card, orient='horizontal').pack(fill='x', padx=20)
        
        # 结余
        balance_frame = tk.Frame(card, bg=self.colors['surface'])
        balance_frame.pack(fill='x', padx=25, pady=20)
        
        tk.Label(
            balance_frame,
            text="📊 结余",
            font=("Microsoft YaHei UI", 14),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(side='left')
        
        self.balance_label = tk.Label(
            balance_frame,
            text="¥0.00",
            font=("Microsoft YaHei UI", 28, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        self.balance_label.pack(side='right')
        
        # 更新数据
        self.update_summary()
    
    def style_card(self, card):
        """为卡片添加现代化样式"""
        # 在Windows上模拟圆角和阴影
        if card.master.winfo_screenwidth() > 0:  # 检查窗口是否已创建
            # 创建阴影效果的背景
            shadow = tk.Frame(card, bg=self.colors['card_shadow'], height=4)
            shadow.pack(side='bottom', fill='x', padx=10, pady=(0, 10))
    
    def create_filter_buttons(self, parent):
        """创建筛选按钮"""
        filter_frame = tk.Frame(parent, bg=self.colors['bg'])
        filter_frame.pack(fill='x', pady=(0, 15))
        
        # 创建按钮容器
        btn_container = tk.Frame(filter_frame, bg=self.colors['bg'])
        btn_container.pack(fill='x')
        
        # 全部按钮
        self.btn_all = tk.Button(
            btn_container,
            text="📋 全部",
            font=("Microsoft YaHei UI", 13),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_dark'],
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=lambda: self.set_filter('all')
        )
        self.btn_all.pack(side='left', fill='x', expand=True, padx=2)
        
        # 支出按钮
        self.btn_expense = tk.Button(
            btn_container,
            text="💸 支出",
            font=("Microsoft YaHei UI", 13),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            activebackground=self.colors['primary'],
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=lambda: self.set_filter('expense')
        )
        self.btn_expense.pack(side='left', fill='x', expand=True, padx=2)
        
        # 收入按钮
        self.btn_income = tk.Button(
            btn_container,
            text="💰 收入",
            font=("Microsoft YaHei UI", 13),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            activebackground=self.colors['primary'],
            activeforeground='white',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            command=lambda: self.set_filter('income')
        )
        self.btn_income.pack(side='left', fill='x', expand=True, padx=2)
    
    def set_filter(self, filter_type):
        """设置筛选类型"""
        self.current_filter = filter_type
        
        # 更新按钮样式
        buttons = {
            'all': self.btn_all,
            'expense': self.btn_expense,
            'income': self.btn_income
        }
        
        for btn_type, btn in buttons.items():
            if btn_type == filter_type:
                btn.configure(bg=self.colors['primary'], fg='white')
            else:
                btn.configure(bg=self.colors['surface'], fg=self.colors['text_secondary'])
        
        # 更新列表
        self.update_transaction_list()
    
    def create_transaction_list(self, parent):
        """创建交易列表"""
        # 列表容器
        list_frame = tk.Frame(parent, bg=self.colors['bg'])
        list_frame.pack(fill='both', expand=True)
        
        # 创建标题
        list_header = tk.Frame(list_frame, bg=self.colors['bg'])
        list_header.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            list_header,
            text="📝 记账明细",
            font=("Microsoft YaHei UI", 18, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        ).pack(side='left')
        
        # 创建Canvas和Scrollbar用于滚动
        canvas_frame = tk.Frame(list_frame, bg=self.colors['bg'])
        canvas_frame.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=360)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 更新列表
        self.update_transaction_list()
    
    def update_transaction_list(self):
        """更新交易列表"""
        # 清空现有列表
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 筛选数据
        filtered_transactions = self.transactions
        if self.current_filter != 'all':
            filtered_transactions = [t for t in self.transactions if t.type == self.current_filter]
        
        # 按日期排序（最新的在前）
        filtered_transactions.sort(key=lambda x: x.date, reverse=True)
        
        # 显示列表
        if not filtered_transactions:
            empty_label = tk.Label(
                self.scrollable_frame,
                text="📭 暂无记录\n点击下方按钮开始记账",
                font=("Microsoft YaHei UI", 14),
                bg=self.colors['bg'],
                fg=self.colors['text_secondary'],
                justify='center',
                pady=40
            )
            empty_label.pack()
        else:
            for transaction in filtered_transactions:
                self.create_transaction_card(transaction)
    
    def create_transaction_card(self, transaction):
        """创建单个交易卡片"""
        # 卡片容器
        card = tk.Frame(self.scrollable_frame, bg=self.colors['surface'], height=80)
        card.pack(fill='x', pady=(0, 10), padx=0)
        card.pack_propagate(False)
        
        # 获取类别信息
        category = Category.get_category(transaction.category_id, transaction.type)
        icon = category['icon'] if category else '📦'
        name = category['name'] if category else '未知'
        color = category['color'] if category else self.colors['text_secondary']
        
        # 左侧：图标和金额
        left_frame = tk.Frame(card, bg=self.colors['surface'])
        left_frame.pack(side='left', padx=20, pady=15)
        
        # 图标圆圈
        icon_frame = tk.Frame(left_frame, bg=color, width=50, height=50)
        icon_frame.pack(anchor='w')
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=("Segoe UI Emoji", 24),
            bg=color,
            fg='white'
        )
        icon_label.pack(expand=True)
        
        # 右侧：详细信息
        right_frame = tk.Frame(card, bg=self.colors['surface'])
        right_frame.pack(side='right', fill='both', expand=True, padx=(0, 20))
        
        # 名称和日期
        top_info = tk.Frame(right_frame, bg=self.colors['surface'])
        top_info.pack(fill='x', pady=(10, 5))
        
        tk.Label(
            top_info,
            text=name,
            font=("Microsoft YaHei UI", 15, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text_primary']
        ).pack(side='left')
        
        tk.Label(
            top_info,
            text=transaction.date,
            font=("Microsoft YaHei UI", 11),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(side='right')
        
        # 备注和金额
        bottom_info = tk.Frame(right_frame, bg=self.colors['surface'])
        bottom_info.pack(fill='x', pady=(0, 10))
        
        remark = transaction.remark if transaction.remark else '无备注'
        tk.Label(
            bottom_info,
            text=remark,
            font=("Microsoft YaHei UI", 11),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(side='left')
        
        amount_text = f"+¥{transaction.amount:.2f}" if transaction.type == 'income' else f"-¥{transaction.amount:.2f}"
        amount_color = self.colors['income'] if transaction.type == 'income' else self.colors['expense']
        
        tk.Label(
            bottom_info,
            text=amount_text,
            font=("Microsoft YaHei UI", 16, "bold"),
            bg=self.colors['surface'],
            fg=amount_color
        ).pack(side='right')
        
        # 点击事件
        card.bind('<Button-1>', lambda e: self.on_transaction_click(transaction))
        for child in card.winfo_children():
            child.bind('<Button-1>', lambda e: self.on_transaction_click(transaction))
    
    def on_transaction_click(self, transaction):
        """点击交易卡片"""
        self.open_add_edit_dialog(transaction)
    
    def create_bottom_nav(self, parent):
        """创建底部导航栏"""
        nav_frame = tk.Frame(parent, bg=self.colors['surface'], height=80)
        nav_frame.pack(fill='x', pady=(20, 0), padx=0)
        
        # 添加按钮（大圆形按钮）
        add_btn = tk.Button(
            nav_frame,
            text="➕\n记账",
            font=("Microsoft YaHei UI", 16, "bold"),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_dark'],
            activeforeground='white',
            relief='flat',
            bd=0,
            width=12,
            height=3,
            cursor='hand2',
            command=lambda: self.open_add_edit_dialog()
        )
        add_btn.pack(pady=15)
        
        # 添加按钮样式
        self.style_button(add_btn)
    
    def style_button(self, button):
        """为按钮添加现代化样式"""
        if button.winfo_screenwidth() > 0:
            pass  # 可以在这里添加更多样式效果
    
    def update_summary(self):
        """更新总览数据"""
        current_month = datetime.now().strftime("%Y-%m")
        
        # 计算本月收支
        expense = sum(t.amount for t in self.transactions 
                     if t.type == 'expense' and t.date.startswith(current_month))
        income = sum(t.amount for t in self.transactions 
                    if t.type == 'income' and t.date.startswith(current_month))
        balance = income - expense
        
        # 更新标签
        self.expense_label.config(text=f"¥{expense:.2f}")
        self.income_label.config(text=f"¥{income:.2f}")
        self.balance_label.config(text=f"¥{balance:.2f}")
        
        # 根据结余设置颜色
        if balance > 0:
            self.balance_label.config(fg=self.colors['income'])
        elif balance < 0:
            self.balance_label.config(fg=self.colors['expense'])
        else:
            self.balance_label.config(fg=self.colors['text_secondary'])
    
    def open_add_edit_dialog(self, transaction=None):
        """打开添加/编辑对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("记账" if not transaction else "编辑")
        dialog.geometry("380x600")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        self.current_edit_transaction = transaction
        
        # 标题
        header = tk.Frame(dialog, bg=self.colors['bg'])
        header.pack(fill='x', padx=20, pady=(20, 30))
        
        tk.Label(
            header,
            text="✏️ 记一笔" if not transaction else "✏️ 编辑记录",
            font=("Microsoft YaHei UI", 22, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        ).pack()
        
        # 类型选择
        type_frame = tk.Frame(dialog, bg=self.colors['bg'])
        type_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        type_var = tk.StringVar(value=transaction.type if transaction else 'expense')
        
        def on_type_change(value):
            type_var.set(value)
            update_category_combobox(value)
        
        type_container = tk.Frame(type_frame, bg=self.colors['bg'])
        type_container.pack(fill='x')
        
        for btn_type, text, emoji in [('expense', '支出', '💸'), ('income', '收入', '💰')]:
            btn = tk.Button(
                type_container,
                text=f"{emoji} {text}",
                font=("Microsoft YaHei UI", 14),
                bg=self.colors['expense'] if btn_type == 'expense' else self.colors['income'],
                fg='white',
                activebackground=self.colors['primary'],
                activeforeground='white',
                relief='flat',
                bd=0,
                padx=20,
                pady=12,
                cursor='hand2'
            )
            btn.pack(side='left', fill='x', expand=True, padx=2)
        
        # 金额输入
        amount_frame = tk.Frame(dialog, bg=self.colors['bg'])
        amount_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            amount_frame,
            text="💵 金额",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        ).pack(anchor='w')
        
        amount_entry = tk.Entry(
            amount_frame,
            font=("Microsoft YaHei UI", 20),
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0,
            insertbackground=self.colors['primary']
        )
        amount_entry.pack(fill='x', pady=(10, 0), ipady=15)
        
        if transaction:
            amount_entry.insert(0, str(transaction.amount))
        
        # 类别选择
        category_frame = tk.Frame(dialog, bg=self.colors['bg'])
        category_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            category_frame,
            text="📦 类别",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        ).pack(anchor='w')
        
        category_var = tk.StringVar(value='')
        
        def update_category_combobox(type):
            categories = Category.EXPENSE_CATEGORIES if type == 'expense' else Category.INCOME_CATEGORIES
            cat_names = [f"{cat['icon']} {cat['name']}" for cat in categories]
            combobox['values'] = cat_names
            if transaction:
                cat = Category.get_category(transaction.category_id, type)
                if cat:
                    category_var.set(f"{cat['icon']} {cat['name']}")
        
        combobox = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            font=("Microsoft YaHei UI", 14),
            state='readonly'
        )
        combobox.pack(fill='x', pady=(10, 0), ipady=10)
        update_category_combobox(type_var.get())
        
        # 备注输入
        remark_frame = tk.Frame(dialog, bg=self.colors['bg'])
        remark_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            remark_frame,
            text="📝 备注",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        ).pack(anchor='w')
        
        remark_entry = tk.Entry(
            remark_frame,
            font=("Microsoft YaHei UI", 14),
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0,
            insertbackground=self.colors['primary']
        )
        remark_entry.pack(fill='x', pady=(10, 0), ipady=10)
        
        if transaction:
            remark_entry.insert(0, transaction.remark)
        
        # 日期选择
        date_frame = tk.Frame(dialog, bg=self.colors['bg'])
        date_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            date_frame,
            text="📅 日期",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text_primary']
        ).pack(anchor='w')
        
        date_var = tk.StringVar(value=transaction.date if transaction else datetime.now().strftime("%Y-%m-%d"))
        date_entry = tk.Entry(
            date_frame,
            textvariable=date_var,
            font=("Microsoft YaHei UI", 14),
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            relief='flat',
            bd=0
        )
        date_entry.pack(fill='x', pady=(10, 0), ipady=10)
        
        # 按钮容器
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(fill='x', padx=20, pady=20)
        
        def save_transaction():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showwarning("提示", "金额必须大于0")
                    return
                
                category_text = category_var.get()
                if not category_text:
                    messagebox.showwarning("提示", "请选择类别")
                    return
                
                # 解析类别
                category_icon = category_text.split()[0]
                categories = Category.EXPENSE_CATEGORIES if type_var.get() == 'expense' else Category.INCOME_CATEGORIES
                category = next((c for c in categories if c['icon'] == category_icon), None)
                
                if not category:
                    messagebox.showwarning("提示", "无效的类别")
                    return
                
                remark = remark_entry.get().strip()
                date = date_entry.get().strip()
                
                if not date:
                    messagebox.showwarning("提示", "请输入日期")
                    return
                
                # 创建或更新交易
                if self.current_edit_transaction:
                    # 更新现有交易
                    self.current_edit_transaction.type = type_var.get()
                    self.current_edit_transaction.amount = amount
                    self.current_edit_transaction.category_id = category['id']
                    self.current_edit_transaction.remark = remark
                    self.current_edit_transaction.date = date
                    messagebox.showinfo("成功", "✅ 记录已更新")
                else:
                    # 创建新交易
                    new_transaction = Transaction(
                        id=int(datetime.now().timestamp()),
                        type=type_var.get(),
                        amount=amount,
                        category_id=category['id'],
                        remark=remark,
                        date=date,
                        create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    self.transactions.append(new_transaction)
                    messagebox.showinfo("成功", "✅ 记录已添加")
                
                self.save_data()
                self.update_summary()
                self.update_transaction_list()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("错误", "请输入有效的金额")
        
        def delete_transaction():
            if self.current_edit_transaction:
                if messagebox.askyesno("确认", "确定要删除这条记录吗？"):
                    self.transactions.remove(self.current_edit_transaction)
                    self.save_data()
                    self.update_summary()
                    self.update_transaction_list()
                    dialog.destroy()
        
        # 保存按钮
        save_btn = tk.Button(
            button_frame,
            text="💾 保存",
            font=("Microsoft YaHei UI", 14, "bold"),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_dark'],
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=save_transaction
        )
        save_btn.pack(fill='x', pady=(0, 10))
        
        # 删除按钮（仅在编辑模式显示）
        if transaction:
            delete_btn = tk.Button(
                button_frame,
                text="🗑️ 删除",
                font=("Microsoft YaHei UI", 14),
                bg=self.colors['error'],
                fg='white',
                activebackground='#D63031',
                activeforeground='white',
                relief='flat',
                bd=0,
                cursor='hand2',
                command=delete_transaction
            )
            delete_btn.pack(fill='x', pady=(0, 10))
        
        # 取消按钮
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            font=("Microsoft YaHei UI", 14),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            activebackground=self.colors['divider'],
            activeforeground=self.colors['text_secondary'],
            relief='flat',
            bd=0,
            cursor='hand2',
            command=dialog.destroy
        )
        cancel_btn.pack(fill='x')
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == '__main__':
    app = ModernAccountingApp()
    app.run()
