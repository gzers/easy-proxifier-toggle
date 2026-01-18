import tkinter as tk
from ..styles import FONTS, COLORS

class FooterFrame(tk.Frame):
    """页脚组件 - 显示版本和作者信息"""
    def __init__(self, master, version, author, **kwargs):
        super().__init__(master, **kwargs)
        self.version = version
        self.author = author
        self._setup_ui()

    def _setup_ui(self):
        # 分割线 (更淡的颜色)
        separator = tk.Frame(self, height=1, bg="#E5E5E5")
        separator.pack(fill="x", pady=(0, 10))
        
        # 容器用于居中显示
        content_frame = tk.Frame(self, bg=self["bg"])
        content_frame.pack(expand=True)
        
        # 使用小字体分行显示
        tk.Label(
            content_frame, 
            text=f"版本: v{self.version}", 
            font=FONTS["small"], 
            fg=COLORS["text_secondary"], 
            bg=self["bg"]
        ).pack(side=tk.LEFT, padx=12)
        
        tk.Label(
            content_frame, 
            text=f"作者: {self.author}", 
            font=FONTS["small"], 
            fg=COLORS["text_secondary"], 
            bg=self["bg"]
        ).pack(side=tk.LEFT, padx=12)
