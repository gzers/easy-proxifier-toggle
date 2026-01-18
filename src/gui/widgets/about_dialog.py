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
            font=FONTS["caption"], 
            bg=COLORS["bg_window"], 
            fg=COLORS["primary"]
        ).pack(pady=(25, 5))
        
        # 版本信息
        version_frame = tk.Frame(self, bg=COLORS["bg_window"])
        version_frame.pack(pady=5)

        tk.Label(
            version_frame, 
            text=f"Version {self.version}", 
            font=FONTS["bold"], 
            bg=COLORS["bg_window"],
            fg=COLORS["text_main"]
        ).pack(side=tk.LEFT)
        
        # 作者信息
        tk.Label(
            self, 
            text=f"By {self.author}", 
            font=FONTS["normal"], 
            bg=COLORS["bg_window"],
            fg=COLORS["text_secondary"]
        ).pack()
        
        # GitHub 链接
        link_label = tk.Label(
            self, 
            text="Visit Web Site 🌐", 
            font=FONTS["normal"], 
            fg=COLORS["primary"], 
            cursor="hand2", 
            bg=COLORS["bg_window"],
            padx=10,
            pady=10
        )
        link_label.pack(pady=(10, 10))
        link_label.bind("<Button-1>", lambda e: webbrowser.open(self.github_url))

        # 关闭按钮
        create_styled_button(
            self, 
            text="确定", 
            command=self.destroy, 
            style="standard", 
            width=10
        ).pack(pady=(5, 15))
