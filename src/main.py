"""
Proxifier Toggler - 主程序入口
一个简单的系统托盘工具，用于快速切换 Proxifier 的开关状态
"""
import sys
import os
from src.utils.admin import run_as_admin
from src.gui.tray_icon import setup_icon


def main():
    """主函数
    
    程序启动时会自动检查管理员权限，
    如果没有权限会弹出 UAC 对话框请求权限。
    开发模式（SKIP_ADMIN_CHECK=1）可以跳过权限检查。
    """
    # 检查是否跳过管理员权限检查（开发模式）
    skip_admin = os.environ.get('SKIP_ADMIN_CHECK') == '1'
    
    if not skip_admin:
        # 自动请求管理员权限（会弹出 UAC 对话框）
        run_as_admin()
    
    # 检查启动时是否最小化
    from src.config import manager as config_manager
    start_minimized = config_manager.get_start_minimized()
    
    if not start_minimized:
        # 不最小化，打开设置界面
        from src.gui.settings import open_settings
        import threading
        
        # 在新线程中打开设置界面，避免阻塞托盘图标
        settings_thread = threading.Thread(target=open_settings, daemon=True)
        settings_thread.start()
    
    # 启动托盘图标
    try:
        setup_icon()
    except KeyboardInterrupt:
        print("程序已退出")
        sys.exit(0)


if __name__ == "__main__":
    main()
