"""UI 样式规范与现代组件风格 - 对标 Fluent UI (Windows 11)"""
import tkinter as tk
from tkinter import ttk

# Fluent UI 颜色调色板 (平衡明亮与简洁)
COLORS = {
    # 基础背景
    "bg_window": "#F9F9F9",       # 更浅的背景，增加现代感
    "bg_card": "#FFFFFF",         # 卡片背景
    "bg_hover": "#F0F0F0",        # 悬停淡灰色
    
    # 品牌色 (Windows 11 风格蓝 - 更生动)
    "primary": "#0078D4",         # 标准蓝 (Microsoft Blue)
    "primary_hover": "#106EBE",
    "primary_active": "#005A9E",
    
    # 功能色 (更鲜亮)
    "success": "#107C10",         # 现代绿
    "success_bg": "#DFF6DD",      # 浅绿背景
    "danger": "#D13438",          # 现代红
    "danger_bg": "#FDE7E9",       # 浅红背景
    "warning": "#FFB900",
    
    # 中性色
    "secondary": "#FFFFFF",       # 标准按钮背景
    "secondary_border": "#D2D2D2",
    "secondary_text": "#323130",
    "text_main": "#201F1E",       # 深灰近黑
    "text_secondary": "#605E5C",  # 辅助文本
    "text_white": "#FFFFFF",
    "border": "#EDEBE9"           # 边框色
}

# 现代字体规范 - 优先使用微软雅黑以确保中文兼容性
FONTS = {
    "caption": ("Microsoft YaHei UI", 16, "bold"), # 大标题
    "title": ("Microsoft YaHei UI", 10, "bold"),   # 板块标题
    "normal": ("Microsoft YaHei UI", 9),           # 正文
    "bold": ("Microsoft YaHei UI", 9, "bold"),     # 强调
    "small": ("Microsoft YaHei UI", 8),            # 页脚/补充说明
    "code": ("Consolas", 9)                        # 代码/路径
}

class FluentCard(tk.Frame):
    """现代卡片容器，模范 Fluent UI 的独立板块"""
    def __init__(self, master, title=None, **kwargs):
        # 强制设置背景为白色，并添加边框
        super().__init__(master, bg=COLORS["bg_card"], highlightthickness=1, 
                         highlightbackground=COLORS["border"], padx=20, pady=12, **kwargs)
        
        if title:
            # 显式指定 foreground 参数
            tk.Label(
                self, text=title, font=FONTS["title"], 
                foreground=COLORS["text_main"], bg=COLORS["bg_card"]
            ).pack(anchor="w", pady=(0, 8))

def apply_fluent_button(button, style="standard"):
    """
    为按钮应用现代 Fluent UI 纯平风格
    """
    if style == "accent":
        bg, fg, hbg = COLORS["primary"], COLORS["text_white"], COLORS["primary_hover"]
        border_color = COLORS["primary"]
        font = FONTS["bold"]
    elif style == "success":
        bg, fg, hbg = COLORS["success"], COLORS["text_white"], "#0D6B0D"
        border_color = COLORS["success"]
        font = FONTS["bold"]
    elif style == "danger":
        bg, fg, hbg = COLORS["danger"], COLORS["text_white"], "#A22418"
        border_color = COLORS["danger"]
        font = FONTS["bold"]
    else: # standard
        bg, fg, hbg = COLORS["secondary"], COLORS["secondary_text"], COLORS["bg_hover"]
        border_color = COLORS["secondary_border"]
        font = FONTS["normal"]

    button.configure(
        bg=bg,
        foreground=fg,
        font=font,
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=1,
        highlightbackground=border_color,
        padx=18,
        pady=6,
        cursor="hand2",
        activebackground=hbg,
        activeforeground=fg
    )
    
    def on_enter(e):
        if str(button['state']) == 'normal':
            button.config(bg=hbg)
            if style == "standard":
                button.config(highlightbackground=COLORS["primary"])
            
    def on_leave(e):
        if str(button['state']) == 'normal':
            button.config(bg=bg, highlightbackground=border_color)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def create_styled_button(master, text, command, style="standard", width=None, icon=None, **kwargs):
    """便捷创建样式的 tk.Button，支持简单文字图标"""
    if icon:
        # 使用更稳健的间隔
        full_text = f"{icon}  {text}" 
    else:
        full_text = text
        
    btn = tk.Button(master, text=full_text, command=command, **kwargs)
    if width:
        btn.config(width=width)
    apply_fluent_button(btn, style)
    return btn

def apply_fluent_entry(entry):
    """为 Entry 应用 Fluent UI 风格"""
    entry.configure(
        font=FONTS["normal"],
        bg=COLORS["bg_card"],
        foreground=COLORS["text_main"],
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground=COLORS["secondary_border"],
        highlightcolor=COLORS["primary"], # 聚焦时颜色
        insertbackground=COLORS["text_main"],
        bd=0
    )

def apply_fluent_checkbutton(cb, bg_color=COLORS["bg_card"]):
    """为 Checkbutton 应用样式 - 深度修复兼容性"""
    cb.configure(
        font=FONTS["normal"],
        bg=bg_color,
        fg=COLORS["text_main"],
        activebackground=bg_color,
        activeforeground=COLORS["primary"],
        selectcolor="#FFFFFF",     # 勾选框内部颜色 (必选白色以防背景干扰)
        highlightthickness=0,
        bd=0,
        padx=5,                    # 适当内边距
        pady=5,
        anchor="w",                # 内容靠左
        justify="left"             # 多行文字左对齐
    )
