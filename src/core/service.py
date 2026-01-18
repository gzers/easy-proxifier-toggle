"""Proxifier 服务管理模块"""
import subprocess
import time


def run_command_admin(command):
    """执行命令（需要管理员权限）"""
    try:
        # 使用 CREATE_NO_WINDOW 标志隐藏窗口
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo
        )
        stdout, stderr = process.communicate()
        return process.returncode
    except Exception as e:
        print(f"执行命令失败: {command}\n错误: {e}")
        return -1


def get_service_status(service_name):
    """获取服务状态"""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        output = subprocess.check_output(
            f'sc query "{service_name}"',
            shell=True,
            text=True,
            startupinfo=startupinfo,
            stderr=subprocess.DEVNULL
        )
        if "RUNNING" in output:
            return "RUNNING"
        elif "STOPPED" in output:
            return "STOPPED"
        else:
            return "UNKNOWN"
    except subprocess.CalledProcessError:
        return "NOT_INSTALLED"
    except Exception as e:
        print(f"获取服务状态失败: {e}")
        return "ERROR"


def start_service(service_name):
    """启动服务"""
    run_command_admin(f"net start {service_name}")
    time.sleep(2)
    return get_service_status(service_name) == "RUNNING"


def stop_service(service_name):
    """停止服务"""
    run_command_admin(f"net stop {service_name}")
    time.sleep(1)
    return get_service_status(service_name) == "STOPPED"
