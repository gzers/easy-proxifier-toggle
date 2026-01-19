"""常量与枚举定义模块

统一管理业务状态枚举、UI 文案以及全局常量。
"""
from enum import Enum


class ServiceStatus(Enum):
    """服务状态枚举"""
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    NOT_INSTALLED = "NOT_INSTALLED"
    UNKNOWN = "UNKNOWN"
    ERROR = "ERROR"
    LOADING = "LOADING"


class AppearanceMode(Enum):
    """外观主题模式"""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class UIStrings:
    """UI 文案统一管理 (支持后续可能的 i18n 扩展)"""
    
    # 状态对应的中文描述
    STATUS_MAP = {
        ServiceStatus.RUNNING: "运行中",
        ServiceStatus.STOPPED: "已停止",
        ServiceStatus.NOT_INSTALLED: "未安装",
        ServiceStatus.UNKNOWN: "未知状态",
        ServiceStatus.ERROR: "服务错误",
        ServiceStatus.LOADING: "正在获取"
    }

    # 窗口标题与通用文本
    APP_TITLE = "Proxifier 切换器"
    CURRENT_STATUS = "当前状态"
    SERVICE_NAME = "驱动服务"
    PROCESS_STATUS = "进程状态"
    
    # 按钮文本
    BTN_TOGGLE_STATE = "⚡  切换服务状态"
    BTN_PROCESSING = "⏳  正在处理..."
    
    # 托盘菜单文本
    TRAY_TOGGLE = "切换 Proxifier"
    TRAY_STATUS = "查看状态"
    TRAY_MAIN_UI = "主界面"
    TRAY_AUTO_START = "开机自启动"
    TRAY_MINIMIZED = "最小化启动"
    TRAY_QUIT = "退出"
    
    # 通知文案
    NOTIFY_SWITCHING = "正在切换状态..."
    NOTIFY_COMPLETED = "状态切换完成"
    NOTIFY_ERROR = "操作失败，请检查权限"
    
    # 设置与 Footer
    SETTINGS_TITLE = "应用设置"
    SETTINGS_DESC = "管理服务名称、执行文件路径及显示设置"
    VERSION_PREFIX = "版本"

    @classmethod
    def get_status(cls, status_key) -> str:
        """获取状态对应的中文文案
        
        Args:
            status_key: 可以是 ServiceStatus 枚举，也可以是原始字符串
        """
        if isinstance(status_key, str):
            try:
                status_key = ServiceStatus(status_key)
            except ValueError:
                return status_key
        
        return cls.STATUS_MAP.get(status_key, str(status_key))
