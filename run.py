"""
Proxifier Toggler 启动脚本
支持以下运行模式：
1. 交互模式（默认）：启动时询问是否需要管理员权限
2. 开发模式：python run.py --dev 或 python run.py -d（跳过管理员权限）
3. 管理员模式：python run.py --admin 或 python run.py -a（直接请求管理员权限）
"""
import sys
import argparse


def ask_for_admin():
    """询问用户是否需要管理员权限"""
    print("=" * 60)
    print("Proxifier Toggler - 启动选项")
    print("=" * 60)
    print()
    print("请选择运行模式：")
    print("  [1] 管理员模式（推荐）- 完整功能，可控制 Proxifier 服务")
    print("  [2] 开发模式 - 无需管理员权限，但服务控制功能不可用")
    print()
    
    while True:
        choice = input("请输入选择 [1/2] (默认: 1): ").strip()
        
        if choice == "" or choice == "1":
            return True
        elif choice == "2":
            return False
        else:
            print("❌ 无效选择，请输入 1 或 2")


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Proxifier Toggler - 系统托盘切换工具"
    )
    parser.add_argument(
        "-d", "--dev",
        action="store_true",
        help="开发模式：跳过管理员权限检查"
    )
    parser.add_argument(
        "-a", "--admin",
        action="store_true",
        help="管理员模式：直接请求管理员权限"
    )
    
    args = parser.parse_args()
    
    # 决定是否需要管理员权限
    need_admin = True  # 默认需要管理员权限
    
    if args.dev:
        # 开发模式：不需要管理员权限
        need_admin = False
        print("=" * 60)
        print("Proxifier Toggler - 开发模式")
        print("=" * 60)
        print("⚠️  注意：开发模式下跳过管理员权限检查")
        print("⚠️  某些功能（如服务控制）可能无法正常工作")
        print("=" * 60)
        print()
    elif args.admin:
        # 管理员模式：需要管理员权限
        need_admin = True
    else:
        # 交互模式：询问用户
        need_admin = ask_for_admin()
    
    # 导入并运行主程序
    from src.main import main as app_main
    app_main(need_admin=need_admin)


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
