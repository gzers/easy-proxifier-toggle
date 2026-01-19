"""主控面板 - CustomTkinter 现代化版本"""
import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from ..config import manager as config_manager
from ..utils import startup
from .widgets.status_frame import StatusFrame
from .widgets.config_frame import ConfigFrame
from .widgets.startup_frame import StartupFrame
from .widgets.footer_frame import FooterFrame
from .widgets.header_frame import HeaderFrame
from .widgets.action_frame import ActionFrame
from .widgets.about_dialog import AboutDialog
from .common.styled_window import StyledWindow
from .ctk_styles import ButtonStyles, Fonts, Sizes, Colors, toggle_appearance_mode, StyledButton


class SettingsWindow:
    """主控面板类 - 现代化 CustomTkinter 风格"""
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SettingsWindow, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, root=None):
        # 确保只初始化一次
        if not hasattr(self, 'initialized'):
            self.root = root  # 外部传入的持久化 root
            self.window = None
            self.status_panel = None
            self.config_panel = None
            self.startup_panel = None
            self.initial_config = None
            self.initialized = True
    
    def show(self):
        """显示主控面板"""
        # 如果窗口已存在，直接唤醒
        if self.window is not None:
            try:
                if self.window.winfo_exists():
                    self.window.deiconify()
                    self.window.lift()
                    self.window.focus_force()
                    return
            except:
                self.window = None
        
        # 如果没有传入 root，自行创建
        if self.root is None:
            self.root = ctk.CTk()
            self.root.withdraw()
        
        # 使用 StyledWindow 创建窗口
        self.window = StyledWindow(
            self.root, 
            title="Easy-Proxifier-Toggler 主控面板",
            width=640,
            height=850
        )
        
        # 加载初始配置
        self.initial_config = config_manager.load_config()
        
        self._create_layout()
        
        # 拦截关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    # 原本的 _set_window_icon 和 _center_window 已由 StyledWindow 基类处理
    
    def _create_layout(self):
        """组装各个模块化组件 - 保持代码可读性与布局稳定性"""
        pad_x = Sizes.WINDOW_PAD_X
        
        # 1. 顶部标题区域
        logo_path = config_manager.ASSETS_DIR / "gzgg-logo.gif"
        self.header = HeaderFrame(
            self.window,
            title="Easy-Proxifier-Toggler",
            logo_path=logo_path
        )
        self.header.pack(side="top", fill="x", padx=pad_x, pady=(Sizes.WINDOW_PAD_Y, Sizes.PADDING))
        
        # 2. 中间可滚动卡片容器 (自动填充剩余空间)
        scroll_container = ctk.CTkScrollableFrame(
            self.window, 
            fg_color="transparent",
            scrollbar_button_color=(Colors.BORDER_LIGHT, Colors.BORDER_DARK),
            scrollbar_button_hover_color=Colors.PRIMARY
        )
        scroll_container.pack(side="top", fill="both", expand=True, padx=pad_x - 5, pady=0)
        
        # 内部卡片
        card_pad_x = 5
        self.status_panel = StatusFrame(scroll_container, self.initial_config)
        self.status_panel.pack(fill="x", padx=card_pad_x, pady=Sizes.PADDING_TINY)
        
        self.config_panel = ConfigFrame(scroll_container, self.initial_config)
        self.config_panel.pack(fill="x", padx=card_pad_x, pady=Sizes.PADDING_SMALL)
        
        self.startup_panel = StartupFrame(scroll_container, self.initial_config)
        self.startup_panel.pack(fill="x", padx=card_pad_x, pady=Sizes.PADDING_SMALL)
        
        # 3. 底部操作按钮区域
        self.action_panel = ActionFrame(
            self.window,
            on_save=self._handle_save,
            on_reset=self._handle_reset,
            on_about=self._handle_about,
            on_theme=self._toggle_theme
        )
        self.action_panel.pack(side="top", fill="x", padx=pad_x, pady=(Sizes.PADDING_SMALL, Sizes.PADDING))
        
        # 4. 页脚组件
        from .. import __version__, __author__
        self.footer = FooterFrame(self.window, __version__, __author__)
        self.footer.pack(side="top", fill="x", padx=pad_x, pady=(Sizes.PADDING_SMALL, Sizes.WINDOW_PAD_Y))

    
    def _toggle_theme(self, mode=None):
        """切换或设置深色/浅色模式"""
        new_mode = toggle_appearance_mode(mode)
        mode_text = {
            "light": "浅色",
            "dark": "深色",
            "system": "跟随系统"
        }.get(new_mode, new_mode)
        print(f"已切换到 {mode_text} 模式")
    
    def _handle_about(self):
        """显示关于弹窗"""
        from .. import __version__, __author__, __github_url__
        AboutDialog(self.window, __version__, __author__, __github_url__)
    
    def _handle_save(self):
        """收集各组件数据并保存"""
        new_data = {**self.config_panel.get_data(), **self.startup_panel.get_data()}
        success = config_manager.update_config(**new_data)
        
        if success:
            if new_data["auto_start"]:
                startup.enable_auto_start()
            else:
                startup.disable_auto_start()
            self.status_panel.update_config(new_data)
            messagebox.showinfo("成功", "配置已保存到本地！")
        else:
            messagebox.showerror("错误", "保存失败。")
    
    def _handle_reset(self):
        """重置各组件的数据为出厂默认值"""
        from ..config.manager import DEFAULT_CONFIG
        if messagebox.askyesno("确认", "确定要恢复出厂默认配置吗？\n(这将会清除您保存的所有自定义设置)"):
            self.config_panel.set_data(DEFAULT_CONFIG)
            self.startup_panel.set_data(DEFAULT_CONFIG)
            self.status_panel.update_config(DEFAULT_CONFIG)
            # 同时更新主题下拉框（如果主题也需要重置）
            if hasattr(self, 'action_panel'):
                theme_map = {"light": "浅色模式", "dark": "深色模式", "system": "跟随系统"}
                default_mode = DEFAULT_CONFIG.get("appearance_mode", "system")
                self.action_panel.theme_menu.set(theme_map.get(default_mode, "跟随系统"))
                self._toggle_theme(default_mode)
    
    def _on_close(self):
        """关闭逻辑：停止任务并销毁窗口"""
        try:
            if self.status_panel:
                self.status_panel.stop_monitoring()
                self.status_panel = None
            if self.window:
                self.window.destroy()
        except:
            pass
        finally:
            self.window = None


def open_settings(root=None):
    """外部调用接口"""
    SettingsWindow(root).show()


if __name__ == "__main__":
    open_settings()
