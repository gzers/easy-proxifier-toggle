# 项目结构重构说明

## 重构日期
2026-01-18

## 重构目标
将项目从单文件结构重构为标准的 Python 工程化项目结构，提高代码的可维护性、可扩展性和专业性。

## 新项目结构

```
easy-proxifier-toggle/
├── src/                      # 源代码目录
│   ├── __init__.py          # 包初始化文件
│   ├── main.py              # 主程序入口
│   ├── core/                # 核心功能模块
│   │   ├── __init__.py
│   │   ├── service.py       # Windows 服务管理
│   │   └── process.py       # 进程管理
│   ├── gui/                 # GUI 相关模块
│   │   ├── __init__.py
│   │   ├── tray_icon.py     # 系统托盘图标
│   │   └── settings.py      # 设置窗口
│   ├── config/              # 配置管理模块
│   │   ├── __init__.py
│   │   └── manager.py       # 配置文件管理器
│   └── utils/               # 工具函数模块
│       ├── __init__.py
│       └── admin.py         # 管理员权限工具
├── config/                  # 配置文件目录
│   ├── config.json          # 用户配置（自动生成，不提交）
│   └── config.example.json  # 配置文件示例
├── docs/                    # 文档目录
│   ├── CONFIG.md            # 配置说明文档
│   ├── QUICKSTART.md        # 快速开始指南
│   └── CHANGELOG.md         # 更新日志
├── scripts/                 # 脚本目录
│   ├── build.bat            # 打包脚本
│   ├── check_config.py      # 配置检查工具
│   └── cleanup_old_files.bat # 清理旧文件脚本
├── run.py                   # 启动脚本（项目入口）
├── test_structure.py        # 结构测试脚本
├── .gitignore               # Git 忽略文件
├── README.md                # 项目说明文档
└── requirements.txt         # 依赖列表
```

## 模块职责划分

### 1. `src/core/` - 核心功能模块
- **service.py**: Windows 服务管理
  - `get_service_status()`: 获取服务状态
  - `start_service()`: 启动服务
  - `stop_service()`: 停止服务
  - `run_command_admin()`: 执行管理员命令

- **process.py**: 进程管理
  - `is_proxifier_running()`: 检查进程是否运行
  - `start_proxifier()`: 启动 Proxifier 进程
  - `kill_proxifier()`: 终止 Proxifier 进程

### 2. `src/gui/` - GUI 模块
- **tray_icon.py**: 系统托盘图标
  - `create_image()`: 创建托盘图标
  - `toggle_proxifier_state()`: 切换 Proxifier 状态
  - `show_status()`: 显示当前状态
  - `setup_icon()`: 设置托盘图标和菜单

- **settings.py**: 设置窗口
  - `SettingsWindow`: 设置窗口类
  - `open_settings()`: 打开设置窗口

### 3. `src/config/` - 配置管理模块
- **manager.py**: 配置文件管理
  - `load_config()`: 加载配置
  - `save_config()`: 保存配置
  - `get_proxifier_exe_path()`: 获取 Proxifier 路径
  - `get_service_name()`: 获取服务名称
  - `update_config()`: 更新配置

### 4. `src/utils/` - 工具模块
- **admin.py**: 管理员权限工具
  - `is_admin()`: 检查是否为管理员
  - `run_as_admin()`: 请求管理员权限

### 5. `src/main.py` - 主程序
- 程序入口点
- 协调各模块工作

## 重构优势

### 1. **模块化设计**
- 每个模块职责单一，易于理解和维护
- 模块间低耦合，高内聚
- 便于单元测试

### 2. **可扩展性**
- 新功能可以轻松添加到相应模块
- 不会影响其他模块的功能
- 支持插件式扩展

### 3. **代码复用**
- 工具函数集中管理
- 避免代码重复
- 提高开发效率

### 4. **专业性**
- 符合 Python 项目最佳实践
- 清晰的目录结构
- 便于团队协作

### 5. **可维护性**
- 代码组织清晰
- 易于定位问题
- 便于代码审查

## 迁移指南

### 从旧版本迁移

1. **配置文件迁移**
   - 旧版本的 `config.json` 会自动移动到 `config/config.json`
   - 配置内容保持不变

2. **运行方式变更**
   ```bash
   # 旧版本
   python proxifier_toggler.py
   
   # 新版本
   python run.py
   # 或
   python -m src.main
   ```

3. **打包方式变更**
   ```bash
   # 旧版本
   pyinstaller --onefile --windowed proxifier_toggler.py
   
   # 新版本
   cd scripts
   build.bat
   # 或
   pyinstaller --onefile --windowed run.py
   ```

## 开发指南

### 添加新功能

1. **确定模块位置**
   - 核心功能 → `src/core/`
   - GUI 相关 → `src/gui/`
   - 配置相关 → `src/config/`
   - 工具函数 → `src/utils/`

2. **创建新文件**
   ```python
   # src/core/new_feature.py
   """新功能模块"""
   
   def new_function():
       """新功能函数"""
       pass
   ```

3. **更新导入**
   ```python
   # src/main.py
   from src.core import new_feature
   ```

### 运行测试

```bash
# 测试项目结构
python test_structure.py

# 运行程序
python run.py
```

## 向后兼容性

- ✓ 配置文件格式不变
- ✓ 功能完全兼容
- ✓ 用户体验一致
- ✓ 自动迁移配置

## 未来计划

1. **添加单元测试**
   - 为每个模块编写测试
   - 使用 pytest 框架

2. **添加日志系统**
   - 记录操作日志
   - 便于问题排查

3. **支持多语言**
   - 国际化支持
   - 语言配置

4. **添加更多功能**
   - 自动启动选项
   - 快捷键支持
   - 状态指示器

## 总结

本次重构将项目从单文件结构升级为标准的 Python 工程化项目，大大提高了代码的可维护性和可扩展性。新的结构更加清晰、专业，便于后续开发和维护。
