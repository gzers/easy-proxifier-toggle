"""设置窗口 GUI"""
import tkinter as tk
from tkinter import filedialog, messagebox
from ..config import manager as config_manager


class SettingsWindow:
    """设置窗口类"""
    
    def __init__(self):
        self.window = None
        self.proxifier_path_var = None
        self.service_name_var = None
    
    def show(self):
        """显示设置窗口"""
        # 如果窗口已经存在，则将其置于前台
        if self.window is not None:
            try:
                self.window.lift()
                self.window.focus_force()
                return
            except:
                pass
        
        # 创建新窗口
        self.window = tk.Tk()
        self.window.title("Proxifier Toggler 设置")
        self.window.geometry("600x250")
        self.window.resizable(False, False)
        
        # 设置窗口图标（可选）
        try:
            self.window.iconbitmap(default='')
        except:
            pass
        
        # 加载当前配置
        config = config_manager.load_config()
        
        # 创建界面元素
        self._create_widgets(config)
        
        # 窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # 运行窗口
        self.window.mainloop()
    
    def _create_widgets(self, config):
        """创建界面元素"""
        # 标题
        title_label = tk.Label(
            self.window,
            text="Proxifier Toggler 配置",
            font=("Microsoft YaHei UI", 14, "bold")
        )
        title_label.pack(pady=15)
        
        # Proxifier 可执行文件路径
        path_frame = tk.Frame(self.window)
        path_frame.pack(pady=10, padx=20, fill=tk.X)
        
        path_label = tk.Label(
            path_frame,
            text="Proxifier 可执行文件路径:",
            font=("Microsoft YaHei UI", 10),
            width=20,
            anchor='w'
        )
        path_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.proxifier_path_var = tk.StringVar(value=config["proxifier_exe_path"])
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.proxifier_path_var,
            font=("Consolas", 9),
            width=40
        )
        path_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        browse_button = tk.Button(
            path_frame,
            text="浏览...",
            command=self._browse_file,
            font=("Microsoft YaHei UI", 9),
            width=8
        )
        browse_button.pack(side=tk.LEFT)
        
        # 服务名称
        service_frame = tk.Frame(self.window)
        service_frame.pack(pady=10, padx=20, fill=tk.X)
        
        service_label = tk.Label(
            service_frame,
            text="服务名称:",
            font=("Microsoft YaHei UI", 10),
            width=20,
            anchor='w'
        )
        service_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.service_name_var = tk.StringVar(value=config["service_name"])
        service_entry = tk.Entry(
            service_frame,
            textvariable=self.service_name_var,
            font=("Consolas", 9),
            width=40
        )
        service_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 提示信息
        hint_label = tk.Label(
            self.window,
            text="提示: 服务名称默认为 'proxifierdrv'，一般无需修改",
            font=("Microsoft YaHei UI", 8),
            fg="gray"
        )
        hint_label.pack(pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        save_button = tk.Button(
            button_frame,
            text="保存",
            command=self._save_config,
            font=("Microsoft YaHei UI", 10),
            width=10,
            bg="#0078D4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2"
        )
        save_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="取消",
            command=self._on_close,
            font=("Microsoft YaHei UI", 10),
            width=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
    
    def _browse_file(self):
        """浏览文件对话框"""
        filename = filedialog.askopenfilename(
            title="选择 Proxifier 可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")],
            initialdir="C:\\Program Files"
        )
        
        if filename:
            self.proxifier_path_var.set(filename)
    
    def _save_config(self):
        """保存配置"""
        proxifier_path = self.proxifier_path_var.get().strip()
        service_name = self.service_name_var.get().strip()
        
        # 验证输入
        if not proxifier_path:
            messagebox.showerror("错误", "Proxifier 可执行文件路径不能为空！")
            return
        
        if not service_name:
            messagebox.showerror("错误", "服务名称不能为空！")
            return
        
        # 保存配置
        success = config_manager.update_config(
            proxifier_exe_path=proxifier_path,
            service_name=service_name
        )
        
        if success:
            messagebox.showinfo("成功", "配置已保存！\n\n注意: 配置将在下次操作时生效。")
            self._on_close()
        else:
            messagebox.showerror("错误", "保存配置失败！")
    
    def _on_close(self):
        """关闭窗口"""
        if self.window:
            self.window.destroy()
            self.window = None


def open_settings():
    """打开设置窗口（供外部调用）"""
    settings = SettingsWindow()
    settings.show()


if __name__ == "__main__":
    # 测试设置窗口
    open_settings()
