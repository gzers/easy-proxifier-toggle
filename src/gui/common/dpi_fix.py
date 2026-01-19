"""DPI 感知优化模块 - 改善 Windows 高 DPI 显示器上的渲染质量"""
import sys
import ctypes

def enable_dpi_awareness():
    """启用 DPI 感知以改善高 DPI 显示器上的渲染质量"""
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

def set_windows_scaling():
    """设置 Windows 缩放优化"""
    if sys.platform == 'win32':
        try:
            import os
            os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
            os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '1'
        except Exception:
            pass
