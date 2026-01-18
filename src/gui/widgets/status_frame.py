import tkinter as tk
import threading
import time
from ...core import service, process
from ..styles import create_styled_button, COLORS, FONTS, FluentCard

class StatusFrame(FluentCard):
    """状态监控与切换控制板块 - Fluent UI 风格"""
    def __init__(self, master, config, **kwargs):
        super().__init__(master, title="当前状态", **kwargs)
        self.config = config
        self.is_monitoring = True
        
        self.service_status_var = tk.StringVar(value="获取中...")
        self.process_status_var = tk.StringVar(value="获取中...")
        
        self._setup_ui()
        self._start_monitor()

    def _setup_ui(self):
        # 整体采用两栏布局
        container = tk.Frame(self, bg=COLORS["bg_card"])
        container.pack(fill="both", expand=True)

        info_frame = tk.Frame(container, bg=COLORS["bg_card"])
        info_frame.grid(row=0, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        
        # 驱动服务状态 (使用 Badge 风格)
        tk.Label(info_frame, text="驱动服务:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).grid(row=0, column=0, sticky="w", pady=5)
        
        self.service_badge = tk.Frame(info_frame, bg=COLORS["bg_hover"], padx=8, pady=2)
        self.service_badge.grid(row=0, column=1, sticky="w", padx=15)
        self.service_label = tk.Label(self.service_badge, textvariable=self.service_status_var, font=FONTS["bold"], bg=COLORS["bg_hover"])
        self.service_label.pack()
        
        # 进程状态
        tk.Label(info_frame, text="进程状态:", font=FONTS["normal"], fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).grid(row=1, column=0, sticky="w", pady=5)
        
        self.process_badge = tk.Frame(info_frame, bg=COLORS["bg_hover"], padx=8, pady=2)
        self.process_badge.grid(row=1, column=1, sticky="w", padx=15)
        self.process_label = tk.Label(self.process_badge, textvariable=self.process_status_var, font=FONTS["bold"], bg=COLORS["bg_hover"])
        self.process_label.pack()
        
        # 切换按钮
        self.toggle_btn = create_styled_button(
            container, 
            text="切换服务状态", 
            command=self._handle_toggle,
            width=14,
            style="accent",
            icon="⚡"
        )
        self.toggle_btn.grid(row=0, column=1, sticky="e", padx=(10, 0))

    def _handle_toggle(self):
        """处理切换逻辑"""
        curr_s = self.service_status_var.get()
        s_name = self.config.get("service_name", "proxifierdrv")
        p_path = self.config.get("proxifier_exe_path", "")
        
        real_btn = self.toggle_btn
        real_btn.config(state=tk.DISABLED, text=" 正在处理...")
        
        def run_toggle():
            if "RUNNING" in curr_s:
                process.kill_proxifier(p_path)
                time.sleep(0.5)
                service.stop_service(s_name)
            else:
                if service.start_service(s_name):
                    process.start_proxifier(p_path)
            
            # 操作完成后恢复按钮状态
            self.after(500, lambda: real_btn.config(state=tk.NORMAL, text="⚡ 切换服务状态"))
            
        threading.Thread(target=run_toggle, daemon=True).start()

    def _start_monitor(self):
        """开启异步监控"""
        def monitor_loop():
            while self.is_monitoring:
                try:
                    s_name = self.config.get("service_name", "proxifierdrv")
                    p_path = self.config.get("proxifier_exe_path", "")
                    
                    s_status = service.get_service_status(s_name)
                    p_running = process.is_proxifier_running(p_path)
                    
                    # 更新文字
                    self.service_status_var.set(f"● {s_status}")
                    self.process_status_var.set("● 运行中" if p_running else "● 已停止")
                    
                    # 动态颜色 (Badge 效果)
                    if s_status == "RUNNING":
                        s_bg, s_fg = COLORS["success_bg"], COLORS["success"]
                    elif s_status == "STOPPED":
                        s_bg, s_fg = COLORS["danger_bg"], COLORS["danger"]
                    else:
                        s_bg, s_fg = COLORS["bg_hover"], COLORS["text_secondary"]
                    
                    if p_running:
                        p_bg, p_fg = COLORS["success_bg"], COLORS["success"]
                    else:
                        p_bg, p_fg = COLORS["danger_bg"], COLORS["danger"]

                    self.service_badge.config(bg=s_bg)
                    self.service_label.config(bg=s_bg, fg=s_fg)
                    self.process_badge.config(bg=p_bg)
                    self.process_label.config(bg=p_bg, fg=p_fg)
                except:
                    pass
                time.sleep(2)
        
        threading.Thread(target=monitor_loop, daemon=True).start()

    def stop_monitoring(self):
        """停止刷新"""
        self.is_monitoring = False

    def update_config(self, new_config):
        """当外部路径修改时，更新该组件引用的配置"""
        self.config = new_config
