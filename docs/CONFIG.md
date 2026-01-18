# 配置说明

## 配置文件

配置文件 `config/config.json` 用于存储 Proxifier Toggler 的配置信息，包括：

- **proxifier_exe_path**: Proxifier 可执行文件的完整路径
- **service_name**: Proxifier 驱动服务的名称（默认为 `proxifierdrv`）
- **auto_start**: 是否在 Windows 登录时自动启动程序（`true`/`false`）
- **start_minimized**: 程序启动时是否最小化到系统托盘。如果设置为 `false`，程序启动时会同时打开设置窗口。

## 配置方式

### 方式一：通过 GUI 设置（推荐）

1. 运行程序（双击 `run.py` 或 `start_admin.bat`）
2. 右键点击系统托盘中的 Proxifier Toggler 图标
3. 选择"设置"菜单项
4. 在弹出的设置窗口中：
   - 设置 Proxifier 可执行文件路径（可点击"浏览..."按钮选择）
   - 设置服务名称（一般保持默认值 `proxifierdrv` 即可）
5. 点击"保存"按钮

### 方式二：手动编辑配置文件

1. 打开 `config/config.json` 文件（如果不存在，程序首次运行时会自动创建）
2. 编辑配置项：

```json
{
    "proxifier_exe_path": "D:\\Software\\Common\\Proxifier\\Proxifier.exe",
    "service_name": "proxifierdrv",
    "auto_start": false,
    "start_minimized": true
}
```

3. 保存文件

**注意**: 
- Windows 路径中的反斜杠需要使用双反斜杠 `\\` 或单正斜杠 `/`
- 配置文件使用 UTF-8 编码

## 默认配置

如果配置文件不存在或配置项缺失，程序会使用以下默认值：

- **proxifier_exe_path**: `D:\Software\Common\Proxifier\Proxifier.exe`
- **service_name**: `proxifierdrv`
- **auto_start**: `false`
- **start_minimized**: `true`

## 配置文件位置

配置文件 `config/config.json` 位于项目根目录下的 `config` 文件夹内。

## 示例配置

参考 `config.example.json` 文件查看配置示例。

## 常见问题

### Q: 修改配置后需要重启程序吗？
A: 不需要。配置会在下次执行切换操作时自动加载。

### Q: 如何重置为默认配置？
A: 删除 `config/config.json` 文件，程序会在下次运行时自动创建默认配置。

### Q: 服务名称应该填什么？
A: 默认值 `proxifierdrv` 适用于大多数情况。除非你修改过 Proxifier 的驱动服务名称，否则无需更改。

### Q: 配置文件会被提交到 Git 吗？
A: 不会。`config.json` 已添加到 `.gitignore`，不会被版本控制追踪。
