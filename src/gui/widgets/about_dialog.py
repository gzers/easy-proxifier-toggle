import tkinter as tk
import webbrowser
from ..styles import FONTS, COLORS, create_styled_button

class AboutDialog(tk.Toplevel):
    """关于对话框组件"""
    def __init__(self, master, version, author, github_url):
        super().__init__(master)
        self.version = version
        self.author = author
        self.github_url = github_url
        
        self.title("关于")
        self.geometry("350x220")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg_window"])
        
        # 设置为模态窗口
        self.transient(master)
        self.grab_set()
        
        # 居中显示在父窗口
        self.update_idletasks() # 确保尺寸已计算
        main_x = master.winfo_x()
        main_y = master.winfo_y()
        self.geometry(f"+{main_x + 150}+{main_y + 150}")
        
        self._setup_ui()

    def _setup_ui(self):
        # 软件标题
        tk.Label(
            self, 
            text="Easy-Proxifier-Toggler", 
            font=FONTS["title"], 
            bg=COLORS["bg_window"], 
            fg=COLORS["primary"]
        ).pack(pady=(20, 10))
        
        # 版本信息
        tk.Label(
            self, 
            text=f"版本: v{self.version}", 
            font=FONTS["normal"], 
            bg=COLORS["bg_window"]
        ).pack()
        
        # 作者信息
        tk.Label(
            self, 
            text=f"作者: {self.author}", 
            font=FONTS["normal"], 
            bg=COLORS["bg_window"]
        ).pack()
        
        # GitHub 链接
        link_label = tk.Label(
            self, 
            text="项目开源地址 (GitHub)", 
            font=FONTS["normal"], 
            fg=COLORS["primary"], 
            cursor="hand2", 
            bg=COLORS["bg_window"]
        )
        link_label.pack(pady=15)
        link_label.bind("<Button-1>", lambda e: webbrowser.open(self.github_url))

        # 关闭按钮
        create_styled_button(
            self, 
            text="关闭", 
            command=self.destroy, 
            style="secondary", 
            width=10
        ).pack(pady=5)
