import tkinter as tk
from tkinter import filedialog
from ..styles import create_styled_button, COLORS, FONTS

class ConfigFrame(tk.LabelFrame):
    """基本参数配置板块"""
    def __init__(self, master, config, **kwargs):
        super().__init__(master, text=" 基本配置 ", font=FONTS["title"], padx=15, pady=10, **kwargs)
        
        self.path_var = tk.StringVar(value=config.get("proxifier_exe_path", ""))
        self.service_var = tk.StringVar(value=config.get("service_name", "proxifierdrv"))
        
        self._setup_ui()

    def _setup_ui(self):
        # Proxifier 路径
        tk.Label(self, text="Proxifier 可执行文件路径:", font=("Microsoft YaHei UI", 9), bg=self["bg"]).pack(anchor="w")
        path_frame = tk.Frame(self, bg=self["bg"])
        path_frame.pack(fill="x", pady=(2, 10))
        
        tk.Entry(path_frame, textvariable=self.path_var, font=("Consolas", 9)).pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))
        create_styled_button(path_frame, text="浏览", command=self._browse_file, width=8, style="secondary").pack(side=tk.RIGHT)
        
        # 服务名称
        tk.Label(self, text="驱动服务名称:", font=("Microsoft YaHei UI", 9), bg=self["bg"]).pack(anchor="w")
        tk.Entry(self, textvariable=self.service_var, font=("Consolas", 9)).pack(fill="x", pady=2)
        tk.Label(self, text="* 通常为 'proxifierdrv'，不熟悉请勿修改", font=("Microsoft YaHei UI", 8), fg="gray", bg=self["bg"]).pack(anchor="w")

    def _browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择 Proxifier 可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if filename:
            self.path_var.set(filename)

    def get_data(self):
        """获取当前输入的数据"""
        return {
            "proxifier_exe_path": self.path_var.get().strip(),
            "service_name": self.service_var.get().strip()
        }

    def set_data(self, config):
        """重置数据"""
        self.path_var.set(config.get("proxifier_exe_path", ""))
        self.service_var.set(config.get("service_name", "proxifierdrv"))
