"""操作按钮板块 - CustomTkinter 现代化版本"""
import customtkinter as ctk
from ..ctk_styles import StyledButton, Sizes, Fonts, Colors


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
        # 左侧区域 (关于, 主题)
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
        
        # 主题切换下拉框
        theme_map = {
            "Light": "浅色模式",
            "Dark": "深色模式",
            "System": "跟随系统"
        }
        self.theme_menu = ctk.CTkOptionMenu(
            secondary_btn_frame,
            values=list(theme_map.values()),
            command=self._on_theme_change,
            width=Sizes.BUTTON_WIDTH_SMALL, # 严格对齐左侧按钮宽度
            height=Sizes.BUTTON_HEIGHT,
            corner_radius=Sizes.CORNER_RADIUS, # 主控件圆角
            font=Fonts.BODY_SMALL,
            fg_color=(Colors.CARD_LIGHT, Colors.CARD_DARK),
            button_color=(Colors.BORDER_LIGHT, Colors.BORDER_DARK),
            button_hover_color=Colors.PRIMARY,
            text_color=(Colors.TEXT_LIGHT, Colors.TEXT_DARK),
            dropdown_fg_color=(Colors.CARD_LIGHT, Colors.CARD_DARK),
            dropdown_hover_color=Colors.PRIMARY,
            dropdown_text_color=(Colors.TEXT_LIGHT, Colors.TEXT_DARK),
            dropdown_font=Fonts.BODY_SMALL,
            anchor="center",
            dynamic_resizing=False
        )
        # 设置当前值
        from ..ctk_styles import get_current_mode
        current = get_current_mode()
        self.theme_menu.set(theme_map.get(current, "跟随系统"))
        self.theme_menu.pack(side="left")
        
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
            text="🔄 重置配置",
            command=self.on_reset,
            style="secondary",
            width=Sizes.BUTTON_WIDTH_SMALL
        )
        self.reset_btn.pack(side="right", padx=(0, Sizes.PADDING_SMALL))
    
    def _on_theme_change(self, choice):
        """处理主题选择变更"""
        reverse_map = {
            "浅色模式": "light",
            "深色模式": "dark",
            "跟随系统": "system"
        }
        self.on_theme(reverse_map.get(choice, "system"))
