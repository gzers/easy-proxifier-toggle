"""测试导入和基本功能"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 50)
print("测试项目结构和导入")
print("=" * 50)
print()

# 测试导入
try:
    print("[1/7] 测试导入 src...")
    import src
    print(f"    ✓ src 版本: {src.__version__}")
    
    print("[2/7] 测试导入 utils.admin...")
    from src.utils import admin
    print(f"    ✓ is_admin 函数: {hasattr(admin, 'is_admin')}")
    
    print("[3/7] 测试导入 core.service...")
    from src.core import service
    print(f"    ✓ get_service_status 函数: {hasattr(service, 'get_service_status')}")
    
    print("[4/7] 测试导入 core.process...")
    from src.core import process
    print(f"    ✓ is_proxifier_running 函数: {hasattr(process, 'is_proxifier_running')}")
    
    print("[5/7] 测试导入 config.manager...")
    from src.config import manager
    print(f"    ✓ load_config 函数: {hasattr(manager, 'load_config')}")
    
    print("[6/7] 测试导入 gui.settings...")
    from src.gui import settings
    print(f"    ✓ SettingsWindow 类: {hasattr(settings, 'SettingsWindow')}")
    
    print("[7/7] 测试导入 gui.tray_icon...")
    from src.gui import tray_icon
    print(f"    ✓ setup_icon 函数: {hasattr(tray_icon, 'setup_icon')}")
    
    print()
    print("=" * 50)
    print("✓ 所有导入测试通过！")
    print("=" * 50)
    print()
    
    # 测试配置管理
    print("测试配置管理...")
    config = manager.load_config()
    print(f"  配置文件路径: {manager.CONFIG_FILE}")
    print(f"  Proxifier 路径: {config.get('proxifier_exe_path')}")
    print(f"  服务名称: {config.get('service_name')}")
    print()
    
    print("✓ 项目结构测试完成！")
    
except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
