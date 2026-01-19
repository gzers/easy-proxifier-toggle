"""系统托盘图标管理"""
import threading
import pystray
from PIL import Image
from ..core import service, process
from ..config import manager as config_manager
from ..utils import startup
from ..core.constants import ServiceStatus, UIStrings
from .. import __version__

class TrayIcon:
    """托盘图标管理类"""
    
    def __init__(self, settings_window=None):
        self.settings_window = settings_window
        self.icon = None
        self.images = {
            "active": None,
            "inactive": None
        }
        
    def _create_image(self, active=True):
        """获取并缓存托盘图标"""
        cache_key = "active" if active else "inactive"
        if self.images[cache_key]:
            return self.images[cache_key]

        icon_filename = "icon.png" if active else "icon_inactive.png"
        icon_path = config_manager.ASSETS_DIR / icon_filename
        
        if icon_path.exists():
            try:
                image = Image.open(icon_path)
                self.images[cache_key] = image
                return image
            except Exception as e:
                print(f"加载图标失败 ({icon_filename}): {e}")
        
        print(f"警告: 找不到图标文件 {icon_path}，请检查 assets 目录。")
        return Image.new('RGBA', (64, 64), (0, 0, 0, 0))

    def update_state(self, service_status=None):
        """同步实际服务状态到托盘图标
        
        Args:
            service_status: 可选的服务状态，如果提供则直接使用，避免重复查询
        """
        if not self.icon:
            return
        
        # 如果没有提供状态，才查询系统
        if service_status is None:
            service_name = config_manager.get_service_name()
            service_status = service.get_service_status(service_name)
        
        is_active = (service_status == "RUNNING")
        
        new_image = self._create_image(active=is_active)
        if self.icon.icon != new_image:
            self.icon.icon = new_image

    def toggle_proxifier(self, icon, item):
        """切换 Proxifier 状态"""
        service_name = config_manager.get_service_name()
        proxifier_exe_path = config_manager.get_proxifier_exe_path()
        current_status = service.get_service_status(service_name)
        
        app_title = UIStrings.get_app_title_with_version()
        
        if current_status == "RUNNING":
            process.kill_proxifier(proxifier_exe_path)
            if service.stop_service(service_name):
                icon.notify("Proxifier " + UIStrings.STATUS_MAP[ServiceStatus.STOPPED], app_title)
            else:
                icon.notify(UIStrings.NOTIFY_ERROR, app_title)
        elif current_status in [ServiceStatus.STOPPED.value, ServiceStatus.NOT_INSTALLED.value]:
            if service.start_service(service_name):
                if process.start_proxifier(proxifier_exe_path):
                    icon.notify("Proxifier " + UIStrings.STATUS_MAP[ServiceStatus.RUNNING], app_title)
                else:
                    icon.notify("启动 Proxifier 失败！", app_title)
            else:
                icon.notify("驱动启动失败！", app_title)
        else:
            icon.notify(f"Proxifier 状态未知 ({current_status})", app_title)
        
        self.update_state()

    def show_status(self, icon, item):
        """显示当前状态通知"""
        service_name = config_manager.get_service_name()
        proxifier_exe_path = config_manager.get_proxifier_exe_path()
        
        status = service.get_service_status(service_name)
        process_running = process.is_proxifier_running(proxifier_exe_path)
        
        status_text = f"{UIStrings.SERVICE_NAME}: {UIStrings.get_status(status)}\n{UIStrings.PROCESS_STATUS}: {'是' if process_running else '否'}"
        icon.notify(status_text, UIStrings.get_app_title_with_version())

    def open_main_ui(self, icon, item):
        """打开主控面板"""
        if self.settings_window:
            self.settings_window.root.after(0, self.settings_window.show)

    def quit_app(self, icon, item):
        """彻底退出程序"""
        icon.stop()
        if self.settings_window and self.settings_window.root:
            self.settings_window.root.after(0, self.settings_window.root.quit)

    def toggle_auto_start(self, icon, item):
        """托盘快捷切换：开机自启动"""
        current_state = config_manager.get_auto_start()
        new_state = not current_state
        if config_manager.update_config(auto_start=new_state):
            if startup.toggle_auto_start(new_state):
                status_text = "已启用" if new_state else "已禁用"
                icon.notify(f"开机自启动{status_text}", UIStrings.get_app_title_with_version())
            else:
                icon.notify("自启动设置失败，请检查权限", UIStrings.get_app_title_with_version())
                config_manager.update_config(auto_start=current_state)

    def toggle_minimize(self, icon, item):
        """托盘快捷切换：最小化启动"""
        current_state = config_manager.get_start_minimized()
        new_state = not current_state
        if config_manager.update_config(start_minimized=new_state):
            status_text = "启用" if new_state else "禁用"
            icon.notify(f"启动时最小化已{status_text}", UIStrings.get_app_title_with_version())

    def _create_menu(self):
        """组装托盘菜单结构"""
        return pystray.Menu(
            pystray.MenuItem(UIStrings.TRAY_TOGGLE, self.toggle_proxifier, default=True),
            pystray.MenuItem(UIStrings.TRAY_STATUS, self.show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(UIStrings.TRAY_MAIN_UI, self.open_main_ui),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(UIStrings.TRAY_AUTO_START, self.toggle_auto_start, 
                             checked=lambda item: config_manager.get_auto_start()),
            pystray.MenuItem(UIStrings.TRAY_MINIMIZED, self.toggle_minimize, 
                             checked=lambda item: config_manager.get_start_minimized()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(UIStrings.TRAY_QUIT, self.quit_app)
        )

    def run(self):
        """主运行方法 (阻塞)"""
        image = self._create_image(active=True)
        menu = self._create_menu()
        
        self.icon = pystray.Icon(
            "Proxifier_Toggler", 
            image, 
            f"{UIStrings.APP_TITLE} v{__version__}", 
            menu
        )
        
        # 初始状态同步
        self.update_state()
        self.icon.run()

# 全局单例/兼容性接口
_tray_instance = None

def setup_tray_async(settings_window):
    """异步启动托盘图标的入口函数"""
    global _tray_instance
    _tray_instance = TrayIcon(settings_window)
    
    thread = threading.Thread(target=_tray_instance.run, daemon=True)
    thread.start()
    return thread

def refresh_tray_icon(service_status=None):
    """刷新托盘状态的外部接口
    
    Args:
        service_status: 可选的服务状态，如果提供则直接使用，避免重复查询
    """
    if _tray_instance:
        _tray_instance.update_state(service_status)

