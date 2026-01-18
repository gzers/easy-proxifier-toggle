"""UI 样式规范与现代组件风格 - 对标 Fluent UI (Windows 11)"""
import tkinter as tk
from tkinter import ttk

# Fluent UI 颜色调色板 (平衡明亮与简洁)
COLORS = {
    # 基础背景
    "bg_window": "#F3F3F3",       # 主窗口背景 (Mica-like)
    "bg_card": "#FFFFFF",         # 卡片背景 (白色)
    "bg_hover": "#E5E5E5",        # 悬停淡灰色
    
    # 品牌色 (Windows 11 蓝)
    "primary": "#005FB8",         # 标准蓝
    "primary_hover": "#0052A1",
    "primary_active": "#004588",
    
    # 功能色
    "success": "#0F7B0F",         # 森林绿
    "danger": "#C42B1C",          # 警示红
    "secondary": "#FFFFFF",       # 标准按钮背景
    "secondary_border": "#CCCCCC",
    "secondary_text": "#000000",
    
    # 文本色
    "text_main": "#1A1A1A",
    "text_secondary": "#5D5D5D",
    "text_white": "#FFFFFF",
    "border": "#E5E5E5"
}

# 现代字体规范
FONTS = {
    "caption": ("Microsoft YaHei UI", 14, "bold"), # 大标题
    "title": ("Microsoft YaHei UI", 10, "bold"),    # 板块标题
    "normal": ("Microsoft YaHei UI", 9),            # 正文
    "small": ("Microsoft YaHei UI", 8),             # 页脚/补充说明
    "code": ("Consolas", 9)                         # 代码/路径
}

class FluentCard(tk.Frame):
    """现代卡片容器，模范 Fluent UI 的独立板块"""
    def __init__(self, master, title=None, **kwargs):
        # 强制设置背景为白色，并添加边框模拟卡片效果
        super().__init__(master, bg=COLORS["bg_card"], highlightthickness=1, 
                         highlightbackground=COLORS["border"], padx=20, pady=15, **kwargs)
        
        if title:
            tk.Label(
                self, text=title, font=FONTS["title"], 
                fg=COLORS["text_main"], bg=COLORS["bg_card"]
            ).pack(anchor="w", pady=(0, 10))

def apply_fluent_button(button, style="standard"):
    """
    为按钮应用 Fluent UI 风格
    style: 'accent' (蓝色主按钮) | 'standard' (白色标准按钮) | 'success' | 'danger'
    """
    # 基础属性配置
    if style == "accent":
        bg, fg, hbg = COLORS["primary"], COLORS["text_white"], COLORS["primary_hover"]
        border_w = 0
    elif style == "success":
        bg, fg, hbg = COLORS["success"], COLORS["text_white"], "#0D6B0D"
        border_w = 0
    elif style == "danger":
        bg, fg, hbg = COLORS["danger"], COLORS["text_white"], "#A22418"
        border_w = 0
    else: # standard
        bg, fg, hbg = COLORS["secondary"], COLORS["secondary_text"], COLORS["bg_hover"]
        border_w = 1

    button.configure(
        bg=bg, fg=fg,
        font=FONTS["normal"],
        relief=tk.FLAT,
        borderwidth=border_w,
        highlightthickness=border_w,
        highlightbackground=COLORS["secondary_border"],
        padx=12, pady=6,
        cursor="hand2",
        activebackground=hbg,
        activeforeground=fg
    )
    
    def on_enter(e): button.config(bg=hbg)
    def on_leave(e): button.config(bg=bg)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def create_styled_button(master, text, command, style="standard", **kwargs):
    """便捷创建 Fluent 风格按钮"""
    btn = tk.Button(master, text=text, command=command, **kwargs)
    apply_fluent_button(btn, style)
    return btn

def apply_fluent_entry(entry):
    """为 Entry 应用 Fluent UI 风格"""
    entry.configure(
        font=FONTS["normal"],
        bg=COLORS["bg_card"],
        fg=COLORS["text_main"],
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground=COLORS["secondary_border"],
        highlightcolor=COLORS["primary"], # 聚焦时颜色
        insertbackground=COLORS["text_main"]
    )

def apply_fluent_checkbutton(cb, bg_color=COLORS["bg_card"]):
    """为 Checkbutton 应用样式"""
    cb.configure(
        font=FONTS["normal"],
        bg=bg_color,
        activebackground=bg_color,
        selectcolor=COLORS["bg_card"], # Win下的勾选框内色
        highlightthickness=0
    )
