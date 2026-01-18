# 🚀 快速启动指南

## 第一次使用（必读）

### 步骤 1：修改配置 ⚙️

1. 打开 `proxifier_toggler.py` 文件
2. 找到文件开头的配置区：
   ```python
   # --- 配置区 ---
   PROXIFIER_EXE_PATH = r"D:\Software\Common\Proxifier\Proxifier.exe"
   SERVICE_NAME = "proxifierdrv"
   # --- 配置区结束 ---
   ```
3. 修改 `PROXIFIER_EXE_PATH` 为你的 Proxifier 实际安装路径
   - 右键点击 Proxifier 快捷方式 → 属性 → 复制"目标"路径
   - 记得在路径前加 `r`，例如：`r"C:\Program Files\Proxifier\Proxifier.exe"`

### 步骤 2：检查配置 ✅

运行配置检查工具：
```bash
python check_config.py
```

这会检查：
- ✓ Proxifier 文件是否存在
- ✓ 服务是否已安装
- ✓ Python 依赖是否完整

### 步骤 3：运行程序 🎯

```bash
python proxifier_toggler.py
```

- 程序会请求管理员权限（点击"是"）
- 系统托盘会出现蓝色圆形图标
- 右键点击图标即可使用

---

## 日常使用

### 方式 1：Python 脚本（推荐用于开发）

```bash
python proxifier_toggler.py
```

### 方式 2：打包成 EXE（推荐用于日常使用）

1. 运行打包脚本：
   ```bash
   build.bat
   ```

2. 在 `dist` 文件夹找到 `ProxifierToggler.exe`

3. 双击运行即可（无需 Python 环境）

---

## 功能说明

### 托盘菜单

右键点击托盘图标，会显示以下菜单：

- **切换 Proxifier**（默认操作）
  - 如果 Proxifier 正在运行 → 关闭它
  - 如果 Proxifier 已关闭 → 启动它
  
- **查看状态**
  - 显示服务状态（RUNNING/STOPPED）
  - 显示进程是否在运行

- **退出**
  - 关闭托盘程序（不影响 Proxifier）

### 切换逻辑

**开启 Proxifier：**
1. 启动 Proxifier 驱动服务
2. 启动 Proxifier 主程序
3. 显示通知："Proxifier 已开启"

**关闭 Proxifier：**
1. 终止 Proxifier 进程
2. 停止 Proxifier 驱动服务
3. 显示通知："Proxifier 已关闭"

---

## 常见问题

### ❓ 程序没有反应

**检查：**
- 是否点击了 UAC 提示中的"是"
- 查看任务管理器中是否有 `python.exe` 或 `ProxifierToggler.exe` 进程

### ❓ 提示"文件不存在"

**解决：**
- 运行 `python check_config.py` 检查配置
- 确认 Proxifier 路径是否正确

### ❓ 提示"服务未安装"

**解决：**
1. 以管理员身份运行一次 Proxifier
2. 让它安装驱动服务
3. 重启计算机

### ❓ 切换后状态没变化

**解决：**
- 使用"查看状态"菜单检查当前状态
- 等待几秒后再次尝试
- 检查是否有其他程序占用了服务

---

## 开机自启动（可选）

如果你想让程序开机自动运行：

### 方法 1：使用任务计划程序（推荐）

1. 按 `Win + R`，输入 `taskschd.msc`
2. 创建基本任务
3. 触发器：登录时
4. 操作：启动程序
5. 程序路径：选择 `ProxifierToggler.exe`
6. 勾选"使用最高权限运行"

### 方法 2：启动文件夹

1. 按 `Win + R`，输入 `shell:startup`
2. 创建快捷方式指向 `ProxifierToggler.exe`
3. 右键快捷方式 → 属性 → 高级 → 勾选"用管理员身份运行"

---

## 更多帮助

- 📖 详细说明：查看 `README.md`
- ⚙️ 配置帮助：查看 `CONFIG.md`
- 🐛 问题反馈：提交 Issue

---

**祝使用愉快！** 🎉
