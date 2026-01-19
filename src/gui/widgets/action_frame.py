"""操作按钮板块 - CustomTkinter 现代化版本"""
import customtkinter as ctk
from ..ctk_styles import StyledButton, Sizes


class ActionFrame(ctk.CTkFrame):
    """底部操作按钮板块 - 现代化 CustomTkinter 风格"""
    
    def __init__(self, master, on_save, on_reset, on_about, on_theme, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.on_save = on_save
        self.on_reset = on_reset
        self.on_about = on_about
        self.on_theme = on_theme
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置 UI 布局"""
        # 左侧悬浮按钮区域 (关于, 主题)
        secondary_btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        secondary_btn_frame.pack(side="left")
        
        self.about_btn = StyledButton(
            secondary_btn_frame,
            text="ℹ️ 关于软件",
            command=self.on_about,
            style="secondary",
            width=Sizes.BUTTON_WIDTH_SMALL
        )
        self.about_btn.pack(side="left", padx=(0, Sizes.PADDING_SMALL))
        
        self.theme_btn = StyledButton(
            secondary_btn_frame,
            text="🌓 切换主题",
            command=self.on_theme,
            style="secondary",
            width=Sizes.BUTTON_WIDTH_SMALL
        )
        self.theme_btn.pack(side="left")
        
        # 右侧主要操作区域 (保存, 撤销)
        # 保存按钮
        self.save_btn = StyledButton(
            self,
            text="💾 保存修改",
            command=self.on_save,
            style="primary",
            width=Sizes.BUTTON_WIDTH
        )
        self.save_btn.pack(side="right")
        
        # 重置按钮
        self.reset_btn = StyledButton(
            self,
            text="↩️ 撤销更改",
            command=self.on_reset,
            style="secondary",
            width=Sizes.BUTTON_WIDTH_SMALL
        )
        self.reset_btn.pack(side="right", padx=(0, Sizes.PADDING_SMALL))
