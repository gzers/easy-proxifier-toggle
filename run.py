"""
Proxifier Toggler 启动脚本
程序启动时会自动弹出 UAC 对话框请求管理员权限
支持以下运行模式：
1. 正常模式（默认）：python run.py - 自动请求管理员权限
2. 开发模式：python run.py --dev 或 python run.py -d（跳过权限检查，用于开发调试）
"""
import sys
import os
import argparse


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Proxifier Toggler - 系统托盘切换工具"
    )
    parser.add_argument(
        "-d", "--dev",
        action="store_true",
        help="开发模式：跳过管理员权限检查（用于开发调试）"
    )
    
    args = parser.parse_args()
    
    # 开发模式：跳过权限检查
    if args.dev:
        print("=" * 60)
        print("Proxifier Toggler - 开发模式")
        print("=" * 60)
        print("⚠️  注意：开发模式下跳过管理员权限检查")
        print("⚠️  某些功能（如服务控制）可能无法正常工作")
        print("=" * 60)
        print()
        
        # 设置环境变量，告诉主程序跳过权限检查
        os.environ['SKIP_ADMIN_CHECK'] = '1'
    
    # 导入并运行主程序
    from src.main import main as app_main
    app_main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        sys.exit(1)
