import os
import subprocess
import sys

print("=" * 50)
print("Proxifier 配置检查工具")
print("=" * 50)
print()

# 从主程序导入配置
try:
    from proxifier_toggler import PROXIFIER_EXE_PATH, SERVICE_NAME
    print("✓ 成功加载配置")
except Exception as e:
    print(f"✗ 加载配置失败: {e}")
    sys.exit(1)

print()
print("当前配置:")
print(f"  Proxifier 路径: {PROXIFIER_EXE_PATH}")
print(f"  服务名称: {SERVICE_NAME}")
print()

# 检查 Proxifier 文件是否存在
print("[1/3] 检查 Proxifier 文件...")
if os.path.exists(PROXIFIER_EXE_PATH):
    print(f"  ✓ 文件存在: {PROXIFIER_EXE_PATH}")
else:
    print(f"  ✗ 文件不存在: {PROXIFIER_EXE_PATH}")
    print("  请检查路径是否正确！")
print()

# 检查服务状态
print("[2/3] 检查服务状态...")
try:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    
    output = subprocess.check_output(
        f'sc query "{SERVICE_NAME}"',
        shell=True,
        text=True,
        startupinfo=startupinfo,
        stderr=subprocess.DEVNULL
    )
    
    if "RUNNING" in output:
        print(f"  ✓ 服务正在运行: {SERVICE_NAME}")
    elif "STOPPED" in output:
        print(f"  ✓ 服务已安装但未运行: {SERVICE_NAME}")
    else:
        print(f"  ? 服务状态未知: {SERVICE_NAME}")
        
except subprocess.CalledProcessError:
    print(f"  ✗ 服务未安装: {SERVICE_NAME}")
    print("  请以管理员身份运行一次 Proxifier 来安装驱动服务")
except Exception as e:
    print(f"  ✗ 检查失败: {e}")

print()

# 检查 Python 依赖
print("[3/3] 检查 Python 依赖...")
try:
    import pystray
    print("  ✓ pystray 已安装")
except ImportError:
    print("  ✗ pystray 未安装")
    print("  请运行: pip install -r requirements.txt")

try:
    from PIL import Image
    print("  ✓ Pillow 已安装")
except ImportError:
    print("  ✗ Pillow 未安装")
    print("  请运行: pip install -r requirements.txt")

print()
print("=" * 50)
print("检查完成！")
print("=" * 50)
print()
print("如果所有检查都通过，你可以运行:")
print("  python proxifier_toggler.py")
print()

input("按回车键退出...")
