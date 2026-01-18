"""Windows 开机启动管理工具"""
import os
import sys
import winreg


def get_startup_registry_key():
    """获取启动项注册表键"""
    return winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_ALL_ACCESS
    )


def is_auto_start_enabled(app_name="ProxifierToggler"):
    """检查是否已设置开机启动
    
    Args:
        app_name: 应用程序名称，用作注册表键名
        
    Returns:
        bool: 是否已设置开机启动
    """
    try:
        key = get_startup_registry_key()
        try:
            winreg.QueryValueEx(key, app_name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except Exception as e:
        print(f"检查开机启动状态失败: {e}")
        return False


def enable_auto_start(app_name="ProxifierToggler"):
    """启用开机启动
    
    Args:
        app_name: 应用程序名称，用作注册表键名
        
    Returns:
        bool: 是否设置成功
    """
    try:
        # 获取当前脚本的绝对路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的 exe
            exe_path = sys.executable
        else:
            # 如果是 Python 脚本
            script_path = os.path.abspath(sys.argv[0])
            exe_path = f'"{sys.executable}" "{script_path}"'
        
        # 写入注册表
        key = get_startup_registry_key()
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        
        return True
    except Exception as e:
        print(f"设置开机启动失败: {e}")
        return False


def disable_auto_start(app_name="ProxifierToggler"):
    """禁用开机启动
    
    Args:
        app_name: 应用程序名称，用作注册表键名
        
    Returns:
        bool: 是否取消成功
    """
    try:
        key = get_startup_registry_key()
        try:
            winreg.DeleteValue(key, app_name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            # 如果键不存在，也算成功
            winreg.CloseKey(key)
            return True
    except Exception as e:
        print(f"取消开机启动失败: {e}")
        return False


def toggle_auto_start(enable, app_name="ProxifierToggler"):
    """切换开机启动状态
    
    Args:
        enable: True 启用，False 禁用
        app_name: 应用程序名称
        
    Returns:
        bool: 是否操作成功
    """
    if enable:
        return enable_auto_start(app_name)
    else:
        return disable_auto_start(app_name)
