"""
Proxifier Toggler - 主程序入口
一个简单的系统托盘工具，用于快速切换 Proxifier 的开关状态
"""
import sys
import os


def main():
    """主函数入口
    
    负责环境检查、权限请求以及启动主应用程序类。
    """
    # 1. 环境预检查 (开发模式跳过管理员检查)
    skip_admin = os.environ.get('SKIP_ADMIN_CHECK') == '1'
    if not skip_admin:
        from src.utils.admin import run_as_admin
        run_as_admin()
    
    # 2. 启动应用
    from src.gui.app import ProxifierApp
    app = ProxifierApp()
    app.run()


if __name__ == "__main__":
    main()
