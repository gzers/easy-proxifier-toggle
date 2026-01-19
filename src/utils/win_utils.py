"""Windows 平台特定工具"""
import sys
import ctypes

def setup_app_id():
    """启用 Windows 任务栏图标分组支持
    
    通过设置 AppUserModelID，确保 Windows 能够正确地将程序窗口和快捷方式归类，
    并显示正确的任务栏图标。
    """
    if sys.platform == 'win32':
        try:
            from .. import __version__
            # 这里的 ID 格式通常为：Company.Product.SubProduct.Version
            app_id = f"gzers.easy-proxifier-toggler.v{__version__}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception as e:
            print(f"设置 AppUserModelID 失败: {e}")

def is_windows():
    """检查当前是否为 Windows 系统"""
    return sys.platform == 'win32'
