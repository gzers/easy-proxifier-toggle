# Proxifier 切换器

一个简单的系统托盘工具，用于快速切换 Proxifier 的开关状态。

## 功能特性

- 🎯 系统托盘图标，常驻后台
- 🔄 一键切换 Proxifier 服务和进程
- 📊 查看当前 Proxifier 运行状态
- ⚙️ GUI 配置窗口，可视化设置
- 💾 配置持久化存储（config.json）
- 🔐 自动请求管理员权限
- 💡 Windows 通知提示

## 使用前准备

### 1. 安装 Python

从 [python.org](https://www.python.org/downloads/) 下载并安装 Python 3.8 或更高版本。

### 2. 安装依赖

在项目目录下打开命令提示符或 PowerShell，运行：

```bash
pip install -r requirements.txt
```

### 3. 配置路径

**方式一：通过 GUI 设置（推荐）**

1. 运行程序后，右键点击系统托盘图标
2. 选择"设置"菜单项
3. 在弹出的设置窗口中配置 Proxifier 路径和服务名称
4. 点击"保存"

**方式二：手动编辑配置文件**

编辑 `config.json` 文件（首次运行会自动创建）：

```json
{
    "proxifier_exe_path": "D:\\Software\\Common\\Proxifier\\Proxifier.exe",
    "service_name": "proxifierdrv"
}
```

详细配置说明请参考 [CONFIG.md](CONFIG.md)。

## 使用方法

### 启动程序

项目提供了统一的启动脚本 `run.py`，支持三种运行模式：

#### 1️⃣ **交互模式（推荐）**

直接运行，程序会询问你是否需要管理员权限：

```bash
python run.py
```

程序会显示选项让你选择：
- **[1] 管理员模式** - 完整功能，可控制 Proxifier 服务
- **[2] 开发模式** - 无需管理员权限，但服务控制功能不可用

#### 2️⃣ **开发模式（快速调试）**

跳过询问，直接以开发模式运行（不需要管理员权限）：

```bash
python run.py --dev
# 或简写
python run.py -d
```

**特点**：
- ✅ 不需要管理员权限
- ✅ 不会弹出 UAC 对话框
- ✅ 命令行窗口保持打开，可以看到输出
- ✅ 显示详细的错误信息
- ⚠️ 服务控制功能不可用（需要管理员权限）

#### 3️⃣ **管理员模式（完整功能）**

跳过询问，直接请求管理员权限：

```bash
python run.py --admin
# 或简写
python run.py -a
```

**特点**：
- ✅ 自动请求管理员权限
- ✅ 所有功能完整可用
- ⚠️ 会弹出 UAC 对话框
- ⚠️ 程序会重启，命令行窗口会关闭

程序会自动请求管理员权限，然后在系统托盘显示图标。

**注意**：程序启动后会在系统托盘运行，不会显示主窗口。请在任务栏右下角查找托盘图标。

### 托盘菜单功能

- **切换 Proxifier**（默认操作）：点击切换 Proxifier 的开关状态
- **查看状态**：显示当前服务和进程状态
- **设置**：打开配置窗口，修改 Proxifier 路径和服务名称
- **退出**：关闭托盘程序

## 打包为 EXE（可选）

如果你想将程序打包成独立的 `.exe` 文件，方便在其他电脑上使用：

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 打包程序

```bash
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico --name="ProxifierToggler" proxifier_toggler.py
```

参数说明：
- `--noconfirm`: 不提示确认，直接覆盖
- `--onefile`: 打包成单个 exe 文件
- `--windowed`: 不显示控制台窗口
- `--icon=icon.ico`: 指定图标文件（可选）
- `--name`: 指定输出的 exe 文件名

### 3. 查找生成的文件

打包完成后，在 `dist` 文件夹中可以找到 `ProxifierToggler.exe`。

## 工作原理

1. **开启 Proxifier**：
   - 启动 Proxifier 驱动服务（`net start proxifierdrv`）
   - 启动 Proxifier 主程序

2. **关闭 Proxifier**：
   - 终止 Proxifier 进程（`taskkill /f /im Proxifier.exe`）
   - 停止 Proxifier 驱动服务（`net stop proxifierdrv`）

## 注意事项

- ⚠️ 本程序需要管理员权限才能控制系统服务
- ⚠️ 首次运行会弹出 UAC 提示，请点击"是"
- ⚠️ 请确保 Proxifier 已正确安装在系统中
- ⚠️ 修改配置文件中的路径时，请使用原始字符串（`r"路径"`）或双反斜杠（`\\`）

## 故障排除

### 问题：提示"服务未安装"

**解决方法**：
- 确认 Proxifier 已正确安装
- 以管理员身份运行一次 Proxifier，让它安装驱动服务

### 问题：切换后状态未改变

**解决方法**：
- 使用"查看状态"菜单检查当前状态
- 检查是否有其他程序占用了 Proxifier 服务
- 尝试手动重启计算机

### 问题：打包后的 exe 无法运行

**解决方法**：
- 确保使用 `--windowed` 参数打包
- 检查杀毒软件是否拦截了程序
- 尝试使用 `--onedir` 代替 `--onefile` 打包

## 项目结构

```
easy-proxifier-toggle/
├── src/                      # 源代码目录
│   ├── __init__.py
│   ├── main.py              # 主程序入口
│   ├── core/                # 核心功能模块
│   │   ├── __init__.py
│   │   ├── service.py       # 服务管理
│   │   └── process.py       # 进程管理
│   ├── gui/                 # GUI 相关
│   │   ├── __init__.py
│   │   ├── tray_icon.py     # 托盘图标
│   │   └── settings.py      # 设置窗口
│   ├── config/              # 配置管理
│   │   ├── __init__.py
│   │   └── manager.py       # 配置管理器
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── admin.py         # 管理员权限相关
├── config/                  # 配置文件目录
│   ├── config.json          # 用户配置（自动生成）
│   └── config.example.json  # 配置示例
├── docs/                    # 文档目录
│   ├── CONFIG.md            # 配置说明
│   ├── QUICKSTART.md        # 快速开始
│   └── CHANGELOG.md         # 更新日志
├── scripts/                 # 脚本目录
│   ├── build.bat            # 打包脚本
│   └── check_config.py      # 配置检查工具
├── run.py                   # 启动脚本
├── .gitignore
├── README.md
└── requirements.txt
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
