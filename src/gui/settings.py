"""主控面板 - 采用模块化组件设计"""
import tkinter as tk
from tkinter import messagebox
from ..config import manager as config_manager
from ..utils import startup
from .widgets.status_frame import StatusFrame
from .widgets.config_frame import ConfigFrame
from .widgets.startup_frame import StartupFrame
from .styles import create_styled_button, COLORS


class SettingsWindow:
    """主控面板类 (聚合组件)"""
    
    def __init__(self):
        self.window = None
        self.status_panel = None
        self.config_panel = None
        self.startup_panel = None
        self.initial_config = None
    
    def show(self):
        """显示主控面板"""
        if self.window is not None:
            try:
                self.window.lift()
                self.window.focus_force()
                return
            except:
                pass
        
        self.window = tk.Tk()
        self.window.title("Easy-Proxifier-Toggler 主控面板")
        
        # 窗口布局与大小
        self._center_window(650, 620)
        self.window.configure(bg=COLORS["background"])
        self.window.resizable(False, False)
        
        # 设置图标
        try:
            icon_path = config_manager.ASSETS_DIR / "icon.ico"
            if icon_path.exists():
                self.window.iconbitmap(str(icon_path))
        except:
            pass
            
        # 加载初始配置
        self.initial_config = config_manager.load_config()
        
        self._create_layout()
        
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self.window.mainloop()

    def _center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def _create_layout(self):
        """组装各个模块化组件"""
        pad_x = 25
        
        # 1. 状态监控板块
        self.status_panel = StatusFrame(self.window, self.initial_config, bg=COLORS["background"])
        self.status_panel.pack(fill="x", padx=pad_x, pady=(20, 10))
        
        # 2. 基本配置板块
        self.config_panel = ConfigFrame(self.window, self.initial_config, bg=COLORS["background"])
        self.config_panel.pack(fill="x", padx=pad_x, pady=10)
        
        # 3. 启动配置板块
        self.startup_panel = StartupFrame(self.window, self.initial_config, bg=COLORS["background"])
        self.startup_panel.pack(fill="x", padx=pad_x, pady=10)
        
        # 4. 底部操作按钮区域
        btn_frame = tk.Frame(self.window, bg=COLORS["background"])
        btn_frame.pack(side=tk.BOTTOM, fill="x", pady=20)
        
        # 保存按钮
        create_styled_button(
            btn_frame, text="保存所有修改", 
            command=self._handle_save, 
            style="success",
            width=15
        ).pack(side=tk.RIGHT, padx=(10, pad_x))
        
        # 重置按钮
        create_styled_button(
            btn_frame, text="恢复初始配置", 
            command=self._handle_reset, 
            style="secondary",
            width=12
        ).pack(side=tk.RIGHT, padx=10)
        
        # 版本标识
        from .. import __version__
        tk.Label(
            self.window, 
            text=f"Easy-Proxifier-Toggler v{__version__} | By EZIO T", 
            font=("Consolas", 8), fg="#aaa", bg=COLORS["background"]
        ).place(x=pad_x, y=585)

    def _handle_save(self):
        """收集各组件数据并保存"""
        # 合并数据
        new_data = {**self.config_panel.get_data(), **self.startup_panel.get_data()}
        
        # 执行保存
        success = config_manager.update_config(**new_data)
        
        if success:
            # 同步自启动状态
            if new_data["auto_start"]:
                startup.enable_auto_start()
            else:
                startup.disable_auto_start()
            
            # 通知状态面板配置已变（防止路径失效）
            self.status_panel.update_config(new_data)
            
            messagebox.showinfo("成功", "配置已保存到本地！\n\n部分设置（如最小化启动）将在下次运行程序时生效。")
        else:
            messagebox.showerror("错误", "保存失败，请检查文件访问权限。")

    def _handle_reset(self):
        """重置各组件的数据"""
        if messagebox.askyesno("确认", "确定要放弃当前所有修改并恢复到软件启动时的状态吗？"):
            self.config_panel.set_data(self.initial_config)
            self.startup_panel.set_data(self.initial_config)
            self.status_panel.update_config(self.initial_config)

    def _on_close(self):
        """关闭逻辑：停止所有异步任务"""
        if self.status_panel:
            self.status_panel.stop_monitoring()
        if self.window:
            self.window.destroy()
            self.window = None


def open_settings():
    """外部调用接口"""
    SettingsWindow().show()


if __name__ == "__main__":
    open_settings()
