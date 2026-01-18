import tkinter as tk
from ..styles import FONTS, COLORS

class StartupFrame(tk.LabelFrame):
    """启动选项配置板块"""
    def __init__(self, master, config, **kwargs):
        super().__init__(master, text=" 启动及运行 ", font=FONTS["title"], padx=15, pady=10, **kwargs)
        
        self.auto_start_var = tk.BooleanVar(value=config.get("auto_start", False))
        self.minimized_var = tk.BooleanVar(value=config.get("start_minimized", True))
        
        self._setup_ui()

    def _setup_ui(self):
        tk.Checkbutton(
            self, 
            text="随 Windows 登录自动启动程序", 
            variable=self.auto_start_var, 
            font=("Microsoft YaHei UI", 9),
            bg=self["bg"],
            activebackground=self["bg"]
        ).pack(anchor="w", pady=2)
        
        tk.Checkbutton(
            self, 
            text="程序启动时自动最小化到系统托盘", 
            variable=self.minimized_var, 
            font=("Microsoft YaHei UI", 9),
            bg=self["bg"],
            activebackground=self["bg"]
        ).pack(anchor="w", pady=2)

    def get_data(self):
        return {
            "auto_start": self.auto_start_var.get(),
            "start_minimized": self.minimized_var.get()
        }

    def set_data(self, config):
        self.auto_start_var.set(config.get("auto_start", False))
        self.minimized_var.set(config.get("start_minimized", True))
