"""
Proxifier Toggler - 主程序入口
一个简单的系统托盘工具，用于快速切换 Proxifier 的开关状态
"""
import sys
from src.utils.admin import run_as_admin
from src.gui.tray_icon import setup_icon


def main(need_admin=True):
    """主函数
    
    Args:
        need_admin: 是否需要管理员权限，默认为 True
    """
    # 根据参数决定是否请求管理员权限
    if need_admin:
        run_as_admin()
    
    # 启动托盘图标
    try:
        setup_icon()
    except KeyboardInterrupt:
        print("程序已退出")
        sys.exit(0)


if __name__ == "__main__":
    main()
