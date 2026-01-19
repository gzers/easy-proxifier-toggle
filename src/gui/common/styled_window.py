"""现代化样式窗口基类"""
import customtkinter as ctk
from PIL import Image, ImageTk
from ...config import manager as config_manager
from ..ctk_styles import Sizes

class StyledWindow(ctk.CTkToplevel):
    """支持高分辨率图标和自动居中的现代化窗口基类"""
    
    def __init__(self, master=None, title="Window", width=None, height=None, icon_path=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title(title)
        
        # 记录图标路径
        self.icon_path = icon_path
        
        # 如果提供了宽高，则居中并固定大小
        if width and height:
            self.center_window(width, height)
            self.resizable(False, False)
        
        # 延迟设置图标，确保窗口句柄已创建
        self.after(200, self.setup_window_icon)

    def center_window(self, width, height):
        """将窗口移动到屏幕中央"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_window_icon(self, icon_path=None):
        """设置高分辨率窗口图标"""
        try:
            if not self.winfo_exists():
                return
            
            base_path = icon_path or self.icon_path
            
            if base_path:
                from pathlib import Path
                path_obj = Path(base_path)
                if path_obj.is_absolute() or path_obj.exists():
                    if path_obj.suffix == "":
                        icon_path_ico = path_obj.with_suffix(".ico")
                        icon_path_png = path_obj.with_suffix(".png")
                    else:
                        icon_path_ico = path_obj
                        icon_path_png = path_obj
                else:
                    icon_path_ico = config_manager.ASSETS_DIR / f"{base_path}.ico"
                    icon_path_png = config_manager.ASSETS_DIR / f"{base_path}.png"
            else:
                icon_path_ico = config_manager.ASSETS_DIR / "icon.ico"
                icon_path_png = config_manager.ASSETS_DIR / "icon.png"
            
            if icon_path_ico.exists():
                self.iconbitmap(str(icon_path_ico))
                
            if icon_path_png.exists():
                img = Image.open(icon_path_png)
                img = img.resize((256, 256), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.wm_iconphoto(False, photo)
                self._icon_photo = photo
        except Exception as e:
            print(f"窗口 [{self.title()}] 设置图标失败: {e}")
