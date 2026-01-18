"""UI 样式规范与常用组件风格"""
import tkinter as tk

# 颜色调色板 (契合图标蓝色)
COLORS = {
    "primary": "#0078D7",      # 主色调 (蓝色)
    "primary_hover": "#005CBF",
    "success": "#28A745",      # 成功/保存 (绿色)
    "success_hover": "#218838",
    "danger": "#DC3545",       # 危险/删除 (红色)
    "danger_hover": "#C82333",
    "secondary": "#6C757D",    # 次要/重置 (灰色)
    "secondary_hover": "#5A6268",
    "background": "#F3F3F3",   # 轻微灰色背景
    "text_main": "#333333",
    "text_white": "#FFFFFF",
    "border": "#CCCCCC"
}

# 字体规范
FONTS = {
    "title": ("Microsoft YaHei UI", 12, "bold"),
    "normal": ("Microsoft YaHei UI", 9),
    "bold": ("Microsoft YaHei UI", 9, "bold"),
    "code": ("Consolas", 9),
    "small": ("Microsoft YaHei UI", 8)
}

def apply_button_style(button, style="primary"):
    """
    为 tk.Button 应用统一的现代风格
    :param button: tk.Button 实例
    :param style: 风格类型 ("primary", "success", "danger", "secondary")
    """
    bg_color = COLORS.get(style, COLORS["primary"])
    hover_color = COLORS.get(f"{style}_hover", COLORS["primary_hover"])
    fg_color = COLORS["text_white"] if style != "secondary" else COLORS["text_white"]
    
    button.configure(
        bg=bg_color,
        fg=fg_color,
        font=FONTS["bold"] if style in ["primary", "success"] else FONTS["normal"],
        relief=tk.FLAT,
        borderwidth=0,
        padx=15,
        pady=5,
        cursor="hand2",
        activebackground=hover_color,
        activeforeground=COLORS["text_white"]
    )
    
    # 悬停效果
    def on_enter(e):
        button.config(bg=hover_color)
    def on_leave(e):
        button.config(bg=bg_color)
        
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def create_styled_button(master, text, command, style="primary", **kwargs):
    """便捷创建样式按钮"""
    btn = tk.Button(master, text=text, command=command, **kwargs)
    apply_button_style(btn, style)
    return btn
