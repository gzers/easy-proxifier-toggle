"""主应用程序类
封装主循环、根窗口管理以及托盘图标交互
"""
import sys
import os
import customtkinter as ctk
from PIL import Image, ImageTk

from ..config import manager as config_manager
from ..gui.settings import SettingsWindow
from ..gui.tray_icon import setup_tray_async
from ..gui.ctk_styles import DEFAULT_APPEARANCE_MODE, DEFAULT_COLOR_THEME
from ..gui.dpi_fix import enable_dpi_awareness
from ..utils.win_utils import setup_app_id

class ProxifierApp:
    def __init__(self):
        """初始化应用状态和主窗口"""
        # 1. 基础系统环境配置
        enable_dpi_awareness()
        setup_app_id()
        
        # 2. CTk 全局主题配置
        ctk.set_appearance_mode(DEFAULT_APPEARANCE_MODE)
        ctk.set_default_color_theme(DEFAULT_COLOR_THEME)
        
        # 3. 创建隐藏的根窗口（用于承载主循环和托盘联动）
        self.root = ctk.CTk()
        self.root.withdraw()
        
        # 4. 配置根窗口图标
        self._setup_root_icons()
        
        # 5. 初始化设置窗口管理器 (持久化)
        self.settings_window = SettingsWindow(self.root)
        
    def _setup_root_icons(self):
        """为根窗口设置图标，确保任务栏和 Alt-Tab 渲染质量"""
        try:
            icon_path_ico = config_manager.ASSETS_DIR / "icon.ico"
            icon_path_png = config_manager.ASSETS_DIR / "icon.png"
            
            # 设置标准 iconbitmap
            if icon_path_ico.exists():
                self.root.iconbitmap(str(icon_path_ico))
                
            # 设置高分辨率 wm_iconphoto
            if icon_path_png.exists():
                img = Image.open(icon_path_png)
                # 保持比例调整到 256x256
                img = img.resize((256, 256), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.root.wm_iconphoto(True, photo)
                # 必须保持引用，防止垃圾回收
                self.root._icon_photo = photo
        except Exception as e:
            print(f"设置主程序图标失败: {e}")

    def run(self):
        """启动应用"""
        # 1. 异步启动托盘图标
        setup_tray_async(self.settings_window)
        
        # 2. 根据配置决定是否初始打开界面
        start_minimized = config_manager.get_start_minimized()
        if not start_minimized:
            # 使用 after 确保其在主循环启动后立即执行
            self.root.after(100, self.settings_window.show)
            
        # 3. 进入主循环
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
