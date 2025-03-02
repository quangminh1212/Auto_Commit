import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import logging
from typing import Dict, Any, Optional, List, Callable

# Cấu hình logging trước khi import auto_commit
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("auto_commit_gui.log", mode="a", encoding="utf-8")
    ]
)
logger = logging.getLogger('auto_commit_gui')
logger.info("Khởi động ứng dụng Auto Commit GUI")

# Định nghĩa các chuỗi song ngữ
TRANSLATIONS = {
    "vi": {
        "app_title": "Auto Commit",
        "settings": "Cài đặt",
        "repository_path": "Đường dẫn repository:",
        "browse": "Chọn",
        "info_tab": "Thông tin",
        "diff_tab": "Diff",
        "commit_tab": "Commit",
        "log_tab": "Log",
        "system_info": "Thông tin hệ thống:",
        "git_info": "Thông tin Git:",
        "refresh": "Làm mới",
        "commit_message": "Commit message:",
        "generate_message": "Tạo commit message",
        "auto_commit": "Tự động commit",
        "auto_push": "Auto push",
        "auto_generate": "Auto generate",
        "commit": "Commit",
        "exit": "Thoát",
        "ready": "Sẵn sàng",
        "welcome": "Chào mừng đến với Auto Commit! Sẵn sàng để tạo commit.",
        "api_key": "API Key Gemini:",
        "max_diff_size": "Kích thước tối đa của diff:",
        "max_retries": "Số lần thử lại tối đa:",
        "retry_delay": "Thời gian chờ giữa các lần thử lại (giây):",
        "simulation_mode": "Chế độ mô phỏng:",
        "save": "Lưu",
        "cancel": "Hủy",
        "error": "Lỗi",
        "success": "Thành công",
        "notice": "Thông báo",
        "language": "Ngôn ngữ:",
        "theme": "Giao diện:",
        "light_theme": "Sáng",
        "dark_theme": "Tối",
        "tooltip_generate": "Tạo commit message bằng API Gemini",
        "tooltip_auto_commit": "Tự động tạo commit message và commit ngay lập tức",
        "tooltip_auto_push": "Tự động push lên remote repository sau khi commit",
        "tooltip_auto_generate": "Tự động tạo commit message khi chuyển đến tab Commit",
        "tooltip_commit": "Tạo commit với message hiện tại",
        "no_changes": "Không có thay đổi nào để commit.",
        "generating_message": "Đang tạo commit message...",
        "message_generated": "Đã tạo commit message",
        "committing": "Đang commit...",
        "commit_success": "Đã commit thành công",
        "pushing": "Đang push...",
        "push_success": "Đã push thành công",
        "push_error": "Lỗi khi push",
        "no_api_key": "API key chưa được cấu hình. Vui lòng cấu hình API key trong phần Cài đặt.",
        "enter_commit_message": "Vui lòng nhập commit message.",
        "settings_saved": "Đã lưu cài đặt thành công.",
        "settings_saved_memory": "Đã lưu cài đặt vào bộ nhớ (không cập nhật file).",
        "not_git_repo": "Thư mục hiện tại không phải là git repository.",
        "init_git_question": "Thư mục hiện tại không phải là git repository. Bạn có muốn khởi tạo git repository không?",
        "git_init_success": "Đã khởi tạo git repository thành công.",
        "git_not_installed": "Git chưa được cài đặt hoặc không có trong PATH.",
        "git_install_prompt": "Vui lòng cài đặt Git từ https://git-scm.com/downloads",
        "simulation_question": "Git chưa được cài đặt hoặc không có trong PATH. Bạn có muốn chuyển sang chế độ mô phỏng không?",
        "simulation_enabled": "Đã chuyển sang chế độ mô phỏng.",
        "no_staged_files": "Không có file nào được staged.",
        "files_changed": "Files đã thay đổi:",
        "diff_content": "Nội dung diff:",
        "branch_current": "Branch hiện tại:",
        "remote": "Remote:",
        "last_commit": "Commit gần nhất:",
        "no_remote": "Không có remote",
        "remote_error": "Không có remote hoặc lỗi khi lấy thông tin",
        "no_commits": "Chưa có commit nào",
        "commits_error": "Chưa có commit nào hoặc lỗi khi lấy thông tin",
        "branch_unknown": "Không xác định",
        "integer_error": "Các giá trị phải là số nguyên.",
        "positive_integer_error": "Các giá trị phải là số nguyên dương."
    },
    "en": {
        "app_title": "Auto Commit",
        "settings": "Settings",
        "repository_path": "Repository path:",
        "browse": "Browse",
        "info_tab": "Info",
        "diff_tab": "Diff",
        "commit_tab": "Commit",
        "log_tab": "Log",
        "system_info": "System information:",
        "git_info": "Git information:",
        "refresh": "Refresh",
        "commit_message": "Commit message:",
        "generate_message": "Generate message",
        "auto_commit": "Auto commit",
        "auto_push": "Auto push",
        "auto_generate": "Auto generate",
        "commit": "Commit",
        "exit": "Exit",
        "ready": "Ready",
        "welcome": "Welcome to Auto Commit! Ready to create commits.",
        "api_key": "Gemini API Key:",
        "max_diff_size": "Maximum diff size:",
        "max_retries": "Maximum retries:",
        "retry_delay": "Retry delay (seconds):",
        "simulation_mode": "Simulation mode:",
        "save": "Save",
        "cancel": "Cancel",
        "error": "Error",
        "success": "Success",
        "notice": "Notice",
        "language": "Language:",
        "theme": "Theme:",
        "light_theme": "Light",
        "dark_theme": "Dark",
        "tooltip_generate": "Generate commit message using Gemini API",
        "tooltip_auto_commit": "Automatically generate commit message and commit immediately",
        "tooltip_auto_push": "Automatically push to remote repository after commit",
        "tooltip_auto_generate": "Automatically generate commit message when switching to Commit tab",
        "tooltip_commit": "Create commit with current message",
        "no_changes": "No changes to commit.",
        "generating_message": "Generating commit message...",
        "message_generated": "Commit message generated",
        "committing": "Committing...",
        "commit_success": "Commit successful",
        "pushing": "Pushing...",
        "push_success": "Push successful",
        "push_error": "Error while pushing",
        "no_api_key": "API key not configured. Please configure API key in Settings.",
        "enter_commit_message": "Please enter a commit message.",
        "settings_saved": "Settings saved successfully.",
        "settings_saved_memory": "Settings saved to memory (file not updated).",
        "not_git_repo": "Current directory is not a git repository.",
        "init_git_question": "Current directory is not a git repository. Do you want to initialize a git repository?",
        "git_init_success": "Git repository initialized successfully.",
        "git_not_installed": "Git is not installed or not in PATH.",
        "git_install_prompt": "Please install Git from https://git-scm.com/downloads",
        "simulation_question": "Git is not installed or not in PATH. Do you want to switch to simulation mode?",
        "simulation_enabled": "Switched to simulation mode.",
        "no_staged_files": "No staged files.",
        "files_changed": "Changed files:",
        "diff_content": "Diff content:",
        "branch_current": "Current branch:",
        "remote": "Remote:",
        "last_commit": "Last commit:",
        "no_remote": "No remote",
        "remote_error": "No remote or error getting information",
        "no_commits": "No commits yet",
        "commits_error": "No commits yet or error getting information",
        "branch_unknown": "Unknown",
        "integer_error": "Values must be integers.",
        "positive_integer_error": "Values must be positive integers."
    }
}

# Định nghĩa các theme
THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "text_bg": "#ffffff",
        "text_fg": "#000000",
        "button_bg": "#e0e0e0",
        "button_fg": "#000000",
        "highlight_bg": "#d0d0d0",
        "highlight_fg": "#000000",
        "tooltip_bg": "#ffffe0",
        "tooltip_fg": "#000000"
    },
    "dark": {
        "bg": "#2d2d2d",
        "fg": "#ffffff",
        "text_bg": "#3d3d3d",
        "text_fg": "#ffffff",
        "button_bg": "#444444",
        "button_fg": "#ffffff",
        "highlight_bg": "#555555",
        "highlight_fg": "#ffffff",
        "tooltip_bg": "#555555",
        "tooltip_fg": "#ffffff"
    }
}

# Import các hàm từ auto_commit.py
try:
    from auto_commit import (
        get_git_diff, generate_commit_message, create_commit, 
        check_git_installed, check_api_key, push_to_remote, 
        get_system_info, logger as auto_commit_logger, API_KEY, SIMULATION_MODE
    )
    logger.info("Đã import thành công từ auto_commit.py")
except ImportError as e:
    error_msg = f"Lỗi khi import từ auto_commit.py: {e}"
    logger.error(error_msg)
    print(error_msg)
    messagebox.showerror("Lỗi", f"Không thể import từ auto_commit.py: {e}. Đảm bảo file này tồn tại trong cùng thư mục.")
    sys.exit(1)

class RedirectText:
    """Lớp để chuyển hướng output từ stdout và logger vào Text widget"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""
        
    def write(self, string):
        self.buffer += string
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state="disabled")
        
    def flush(self):
        pass

class SettingsDialog(tk.Toplevel):
    """Dialog cài đặt cho ứng dụng"""
    def __init__(self, parent, settings, save_callback):
        super().__init__(parent)
        self.title("Cài đặt")
        self.geometry("500x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.settings = settings
        self.save_callback = save_callback
        
        # Lấy ngôn ngữ hiện tại
        self.current_lang = self.settings.get("language", "vi")
        self.texts = TRANSLATIONS[self.current_lang]
        
        self.create_widgets()
        self.center_window()
        
    def create_widgets(self):
        """Tạo các widget cho dialog cài đặt"""
        # Frame chính
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # API Key
        ttk.Label(main_frame, text=self.texts["api_key"]).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar(value=self.settings.get("api_key", ""))
        ttk.Entry(main_frame, textvariable=self.api_key_var, width=50).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Kích thước tối đa của diff
        ttk.Label(main_frame, text=self.texts["max_diff_size"]).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_diff_size_var = tk.StringVar(value=str(self.settings.get("max_diff_size", 3000)))
        ttk.Entry(main_frame, textvariable=self.max_diff_size_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Số lần thử lại tối đa
        ttk.Label(main_frame, text=self.texts["max_retries"]).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_retries_var = tk.StringVar(value=str(self.settings.get("max_retries", 3)))
        ttk.Entry(main_frame, textvariable=self.max_retries_var, width=5).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Thời gian chờ giữa các lần thử lại
        ttk.Label(main_frame, text=self.texts["retry_delay"]).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.retry_delay_var = tk.StringVar(value=str(self.settings.get("retry_delay", 2)))
        ttk.Entry(main_frame, textvariable=self.retry_delay_var, width=5).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Chế độ mô phỏng
        ttk.Label(main_frame, text=self.texts["simulation_mode"]).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.simulation_mode_var = tk.BooleanVar(value=self.settings.get("simulation_mode", False))
        ttk.Checkbutton(main_frame, variable=self.simulation_mode_var).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Ngôn ngữ
        ttk.Label(main_frame, text=self.texts["language"]).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.language_var = tk.StringVar(value=self.settings.get("language", "vi"))
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var, width=10, state="readonly")
        language_combo["values"] = ["vi", "en"]
        language_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Giao diện
        ttk.Label(main_frame, text=self.texts["theme"]).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        theme_combo = ttk.Combobox(main_frame, textvariable=self.theme_var, width=10, state="readonly")
        theme_combo["values"] = ["light", "dark"]
        theme_combo.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Nút lưu và hủy
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text=self.texts["save"], command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.texts["cancel"], command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_settings(self):
        """Lưu cài đặt và đóng dialog"""
        try:
            max_diff_size = int(self.max_diff_size_var.get())
            max_retries = int(self.max_retries_var.get())
            retry_delay = int(self.retry_delay_var.get())
            
            if max_diff_size <= 0 or max_retries <= 0 or retry_delay <= 0:
                messagebox.showerror(self.texts["error"], self.texts["positive_integer_error"])
                return
            
            # Lấy giá trị mới
            new_settings = {
                "api_key": self.api_key_var.get(),
                "max_diff_size": max_diff_size,
                "max_retries": max_retries,
                "retry_delay": retry_delay,
                "simulation_mode": self.simulation_mode_var.get(),
                "language": self.language_var.get(),
                "theme": self.theme_var.get()
            }
            
            # Gọi callback để lưu cài đặt
            self.save_callback(new_settings)
            
            # Đóng dialog
            self.destroy()
            
            # Cập nhật lại giao diện của cửa sổ chính
            self.master.update_idletasks()
            
        except ValueError:
            messagebox.showerror(self.texts["error"], self.texts["integer_error"])
    
    def center_window(self):
        """Căn giữa cửa sổ dialog"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

class AutoCommitGUI:
    """Giao diện chính cho ứng dụng Auto Commit"""
    def __init__(self, root):
        self.root = root
        
        # Cài đặt mặc định
        self.settings = {
            "api_key": API_KEY if API_KEY != "YOUR_GEMINI_API_KEY" else "",
            "max_diff_size": 3000,
            "max_retries": 3,
            "retry_delay": 2,
            "simulation_mode": SIMULATION_MODE,
            "language": "vi",
            "theme": "light"
        }
        
        # Lấy ngôn ngữ và theme
        self.current_lang = self.settings["language"]
        self.current_theme = self.settings["theme"]
        self.texts = TRANSLATIONS[self.current_lang]
        self.theme = THEMES[self.current_theme]
        
        # Thiết lập cửa sổ chính
        self.root.title(self.texts["app_title"])
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Thiết lập style
        self.style = ttk.Style()
        self.apply_theme()
        
        # Thiết lập icon
        try:
            self.root.iconbitmap("git.ico")
        except:
            pass  # Bỏ qua nếu không tìm thấy file icon
        
        # Biến lưu trữ
        self.repo_path = tk.StringVar(value=os.getcwd())
        self.commit_message = tk.StringVar()
        self.auto_push = tk.BooleanVar(value=False)
        self.auto_generate = tk.BooleanVar(value=True)
        
        # Tạo giao diện
        self.create_widgets()
        self.center_window()
        
        # Hiển thị dialog cài đặt khi khởi động nếu API key chưa được cấu hình
        if self.settings["api_key"] == "" or self.settings["api_key"] == "YOUR_GEMINI_API_KEY":
            self.root.after(500, self.open_settings)
        
        # Kiểm tra Git
        self.check_git()
        
        # Hiển thị thông báo chào mừng
        self.status_var.set(self.texts["welcome"])
    
    def apply_theme(self):
        """Áp dụng theme cho giao diện"""
        self.style.configure(".", 
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TFrame",
            background=self.theme["bg"])
        
        self.style.configure("TLabel",
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TButton",
            background=self.theme["button_bg"],
            foreground=self.theme["button_fg"])
        
        self.style.configure("TCheckbutton",
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TNotebook",
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TNotebook.Tab",
            background=self.theme["button_bg"],
            foreground=self.theme["button_fg"])
        
        self.root.configure(bg=self.theme["bg"])
    
    def update_language(self):
        """Cập nhật ngôn ngữ cho giao diện"""
        self.texts = TRANSLATIONS[self.current_lang]
        
        # Cập nhật tiêu đề cửa sổ
        self.root.title(self.texts["app_title"])
        
        # Cập nhật các label
        self.repo_path_label.configure(text=self.texts["repository_path"])
        self.browse_button.configure(text=self.texts["browse"])
        self.settings_button.configure(text=self.texts["settings"])
        
        # Cập nhật các tab
        self.notebook.tab(0, text=self.texts["info_tab"])
        self.notebook.tab(1, text=self.texts["diff_tab"])
        self.notebook.tab(2, text=self.texts["commit_tab"])
        self.notebook.tab(3, text=self.texts["log_tab"])
        
        # Cập nhật các label trong tab Info
        self.system_info_label.configure(text=self.texts["system_info"])
        self.git_info_label.configure(text=self.texts["git_info"])
        
        # Cập nhật các button trong tab Diff
        self.refresh_button.configure(text=self.texts["refresh"])
        
        # Cập nhật các widget trong tab Commit
        self.commit_message_label.configure(text=self.texts["commit_message"])
        self.generate_button.configure(text=self.texts["generate_message"])
        self.auto_commit_button.configure(text=self.texts["auto_commit"])
        self.auto_push_check.configure(text=self.texts["auto_push"])
        self.auto_generate_check.configure(text=self.texts["auto_generate"])
        self.commit_button.configure(text=self.texts["commit"])
        
        # Cập nhật nút thoát
        self.exit_button.configure(text=self.texts["exit"])
        
        # Cập nhật tooltip
        self.create_tooltip(self.generate_button, self.texts["tooltip_generate"])
        self.create_tooltip(self.auto_commit_button, self.texts["tooltip_auto_commit"])
        self.create_tooltip(self.auto_push_check, self.texts["tooltip_auto_push"])
        self.create_tooltip(self.auto_generate_check, self.texts["tooltip_auto_generate"])
        self.create_tooltip(self.commit_button, self.texts["tooltip_commit"])
    
    def create_widgets(self):
        """Tạo các widget cho giao diện chính"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame trên cùng
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        # Đường dẫn repository
        self.repo_path_label = ttk.Label(top_frame, text=self.texts["repository_path"])
        self.repo_path_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Entry(top_frame, textvariable=self.repo_path, width=50).pack(side=tk.LEFT, padx=5)
        
        self.browse_button = ttk.Button(top_frame, text=self.texts["browse"], command=self.browse_repo)
        self.browse_button.pack(side=tk.LEFT, padx=5)
        
        self.settings_button = ttk.Button(top_frame, text=self.texts["settings"], command=self.open_settings)
        self.settings_button.pack(side=tk.RIGHT, padx=5)
        
        # Frame giữa
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Notebook (tab)
        self.notebook = ttk.Notebook(middle_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Tab 1: Thông tin
        info_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(info_frame, text=self.texts["info_tab"])
        
        # Thông tin hệ thống
        self.system_info_label = ttk.Label(info_frame, text=self.texts["system_info"])
        self.system_info_label.pack(anchor=tk.W)
        
        self.system_info_text = scrolledtext.ScrolledText(info_frame, height=5, width=80, wrap=tk.WORD,
            bg=self.theme["text_bg"], fg=self.theme["text_fg"])
        self.system_info_text.pack(fill=tk.X, pady=5)
        self.system_info_text.insert(tk.END, json.dumps(get_system_info(), indent=2, ensure_ascii=False))
        self.system_info_text.configure(state="disabled")
        
        # Thông tin Git
        self.git_info_label = ttk.Label(info_frame, text=self.texts["git_info"])
        self.git_info_label.pack(anchor=tk.W, pady=(10, 0))
        
        self.git_info_text = scrolledtext.ScrolledText(info_frame, height=5, width=80, wrap=tk.WORD,
            bg=self.theme["text_bg"], fg=self.theme["text_fg"])
        self.git_info_text.pack(fill=tk.X, pady=5)
        self.git_info_text.configure(state="disabled")
        
        # Tab 2: Diff
        diff_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(diff_frame, text=self.texts["diff_tab"])
        
        self.refresh_button = ttk.Button(diff_frame, text=self.texts["refresh"], command=self.refresh_diff)
        self.refresh_button.pack(anchor=tk.W, pady=5)
        
        self.diff_text = scrolledtext.ScrolledText(diff_frame, height=20, width=80, wrap=tk.WORD,
            bg=self.theme["text_bg"], fg=self.theme["text_fg"])
        self.diff_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.diff_text.configure(state="disabled")
        
        # Tab 3: Commit
        commit_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(commit_frame, text=self.texts["commit_tab"])
        
        self.commit_message_label = ttk.Label(commit_frame, text=self.texts["commit_message"])
        self.commit_message_label.pack(anchor=tk.W)
        
        # Frame cho commit message
        message_frame = ttk.Frame(commit_frame)
        message_frame.pack(fill=tk.X, pady=5)
        
        self.commit_message_text = scrolledtext.ScrolledText(message_frame, height=10, width=80, wrap=tk.WORD,
            bg=self.theme["text_bg"], fg=self.theme["text_fg"])
        self.commit_message_text.pack(fill=tk.BOTH, expand=True)
        self.commit_message_text.bind("<Control-Return>", self.on_ctrl_enter)
        
        # Frame cho các nút
        button_frame = ttk.Frame(commit_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.generate_button = ttk.Button(button_frame, text=self.texts["generate_message"], command=self.generate_message)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        self.auto_commit_button = ttk.Button(button_frame, text=self.texts["auto_commit"], command=self.auto_commit)
        self.auto_commit_button.pack(side=tk.LEFT, padx=5)
        
        self.auto_push_check = ttk.Checkbutton(button_frame, text=self.texts["auto_push"], variable=self.auto_push)
        self.auto_push_check.pack(side=tk.LEFT, padx=5)
        
        self.auto_generate_check = ttk.Checkbutton(button_frame, text=self.texts["auto_generate"], variable=self.auto_generate)
        self.auto_generate_check.pack(side=tk.LEFT, padx=5)
        
        self.commit_button = ttk.Button(button_frame, text=self.texts["commit"], command=self.do_commit)
        self.commit_button.pack(side=tk.RIGHT, padx=5)
        
        # Thêm tooltip
        self.create_tooltip(self.generate_button, self.texts["tooltip_generate"])
        self.create_tooltip(self.auto_commit_button, self.texts["tooltip_auto_commit"])
        self.create_tooltip(self.auto_push_check, self.texts["tooltip_auto_push"])
        self.create_tooltip(self.auto_generate_check, self.texts["tooltip_auto_generate"])
        self.create_tooltip(self.commit_button, self.texts["tooltip_commit"])
        
        # Tab 4: Log
        log_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(log_frame, text=self.texts["log_tab"])
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=80, wrap=tk.WORD,
            bg=self.theme["text_bg"], fg=self.theme["text_fg"])
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state="disabled")
        
        # Chuyển hướng stdout và logger vào log_text
        self.redirect = RedirectText(self.log_text)
        sys.stdout = self.redirect
        
        # Thêm handler cho logger
        log_handler = logging.StreamHandler(self.redirect)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        auto_commit_logger.addHandler(log_handler)
        
        # Frame dưới cùng
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # Thanh trạng thái
        self.status_var = tk.StringVar(value=self.texts["ready"])
        ttk.Label(bottom_frame, textvariable=self.status_var).pack(side=tk.LEFT)
        
        # Nút thoát
        self.exit_button = ttk.Button(bottom_frame, text=self.texts["exit"], command=self.root.destroy)
        self.exit_button.pack(side=tk.RIGHT)
    
    def center_window(self):
        """Căn giữa cửa sổ chính"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def browse_repo(self):
        """Mở dialog chọn thư mục repository"""
        repo_path = filedialog.askdirectory(initialdir=self.repo_path.get())
        if repo_path:
            self.repo_path.set(repo_path)
            # Chuyển đến thư mục repository
            os.chdir(repo_path)
            # Cập nhật thông tin
            self.check_git()
            self.refresh_diff()
    
    def check_git(self):
        """Kiểm tra Git trong thư mục hiện tại"""
        self.git_info_text.configure(state="normal")
        self.git_info_text.delete(1.0, tk.END)
        
        try:
            # Kiểm tra xem có phải là git repository không
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                # Lấy thông tin branch
                try:
                    branch = subprocess.check_output(
                        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        text=True,
                        encoding='utf-8'
                    ).strip()
                except Exception:
                    branch = self.texts["branch_unknown"]
                
                # Lấy thông tin remote
                try:
                    remote = subprocess.check_output(
                        ["git", "remote", "-v"],
                        text=True,
                        encoding='utf-8'
                    ).strip()
                    if not remote:
                        remote = self.texts["no_remote"]
                except Exception:
                    remote = self.texts["remote_error"]
                
                # Lấy thông tin commit gần nhất
                try:
                    last_commit = subprocess.check_output(
                        ["git", "log", "-1", "--oneline"],
                        text=True,
                        encoding='utf-8'
                    ).strip()
                    if not last_commit:
                        last_commit = self.texts["no_commits"]
                except Exception:
                    last_commit = self.texts["commits_error"]
                
                self.git_info_text.insert(tk.END, f"{self.texts['branch_current']} {branch}\n\n")
                self.git_info_text.insert(tk.END, f"{self.texts['remote']}\n{remote}\n\n")
                self.git_info_text.insert(tk.END, f"{self.texts['last_commit']} {last_commit}")
                
                self.status_var.set(f"Repository: {os.path.basename(self.repo_path.get())} | Branch: {branch}")
            else:
                self.git_info_text.insert(tk.END, self.texts["not_git_repo"])
                self.status_var.set(self.texts["not_git_repo"])
                
                # Hỏi người dùng có muốn khởi tạo git repository không
                if messagebox.askyesno(self.texts["notice"], self.texts["init_git_question"]):
                    try:
                        subprocess.run(["git", "init"], check=True)
                        self.git_info_text.delete(1.0, tk.END)
                        self.git_info_text.insert(tk.END, self.texts["git_init_success"])
                        self.status_var.set(self.texts["git_init_success"])
                        self.check_git()  # Kiểm tra lại sau khi khởi tạo
                    except Exception as e:
                        self.git_info_text.insert(tk.END, f"\n{self.texts['error']}: {str(e)}")
        except Exception as e:
            self.git_info_text.insert(tk.END, f"{self.texts['error']}: {str(e)}")
            self.status_var.set(self.texts["error"])
            
            # Kiểm tra xem Git đã được cài đặt chưa
            if not check_git_installed():
                self.git_info_text.insert(tk.END, f"\n\n{self.texts['git_not_installed']}")
                self.git_info_text.insert(tk.END, f"\n{self.texts['git_install_prompt']}")
                
                # Hỏi người dùng có muốn chuyển sang chế độ mô phỏng không
                if messagebox.askyesno(self.texts["notice"], self.texts["simulation_question"]):
                    self.settings["simulation_mode"] = True
                    self.save_settings(self.settings)
                    self.git_info_text.insert(tk.END, f"\n\n{self.texts['simulation_enabled']}")
                    self.status_var.set(self.texts["simulation_enabled"])
        
        self.git_info_text.configure(state="disabled")
    
    def refresh_diff(self):
        """Cập nhật thông tin diff"""
        self.diff_text.configure(state="normal")
        self.diff_text.delete(1.0, tk.END)
        
        try:
            # Kiểm tra xem có phải là git repository không
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                self.diff_text.insert(tk.END, self.texts["not_git_repo"])
                self.notebook.tab(1, text=f"{self.texts['diff_tab']} (Error)")
                self.diff_text.configure(state="disabled")
                return
            
            # Lấy danh sách các file đã thay đổi
            try:
                staged_files = subprocess.check_output(
                    ["git", "diff", "--cached", "--name-only"],
                    text=True,
                    encoding='utf-8'
                ).strip()
                
                if not staged_files:
                    self.diff_text.insert(tk.END, self.texts["no_staged_files"])
                    self.notebook.tab(1, text=f"{self.texts['diff_tab']} (0)")
                else:
                    # Lấy nội dung diff
                    diff_content = subprocess.check_output(
                        ["git", "diff", "--cached"],
                        text=True,
                        encoding='utf-8'
                    ).strip()
                    
                    self.diff_text.insert(tk.END, f"{self.texts['files_changed']}\n{staged_files}\n\n")
                    self.diff_text.insert(tk.END, f"{self.texts['diff_content']}\n{diff_content}")
                    
                    # Cập nhật tiêu đề tab
                    file_count = len(staged_files.split("\n"))
                    self.notebook.tab(1, text=f"{self.texts['diff_tab']} ({file_count})")
            except Exception as e:
                self.diff_text.insert(tk.END, f"{self.texts['error']}: {str(e)}")
                self.notebook.tab(1, text=f"{self.texts['diff_tab']} (Error)")
        except Exception as e:
            self.diff_text.insert(tk.END, f"{self.texts['error']}: {str(e)}")
            self.notebook.tab(1, text=f"{self.texts['diff_tab']} (Error)")
        
        self.diff_text.configure(state="disabled")
    
    def generate_message(self):
        """Tạo commit message bằng API Gemini"""
        # Kiểm tra API key
        if not self.settings["api_key"] or self.settings["api_key"] == "YOUR_GEMINI_API_KEY":
            messagebox.showerror(self.texts["error"], self.texts["no_api_key"])
            self.open_settings()
            return
        
        # Kiểm tra xem có file nào được staged không
        try:
            diff_info = get_git_diff()
            if not diff_info:
                messagebox.showinfo(self.texts["notice"], self.texts["no_changes"])
                return
        except Exception as e:
            auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
            messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
            return
        
        # Cập nhật trạng thái
        self.status_var.set(self.texts["generating_message"])
        
        # Tạo thread để không block giao diện
        def generate_thread():
            try:
                # Tạo commit message
                commit_message = generate_commit_message(diff_info)
                if not commit_message:
                    messagebox.showerror(self.texts["error"], self.texts["error"])
                    self.status_var.set(self.texts["error"])
                    return
                
                # Cập nhật text widget
                self.commit_message_text.delete(1.0, tk.END)
                self.commit_message_text.insert(tk.END, commit_message)
                
                # Cập nhật trạng thái
                self.status_var.set(self.texts["message_generated"])
            except Exception as e:
                auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
                messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
                self.status_var.set(self.texts["error"])
        
        threading.Thread(target=generate_thread).start()
    
    def auto_commit(self):
        """Tự động tạo commit message và commit ngay lập tức"""
        # Kiểm tra API key
        if not self.settings["api_key"] or self.settings["api_key"] == "YOUR_GEMINI_API_KEY":
            messagebox.showerror(self.texts["error"], self.texts["no_api_key"])
            self.open_settings()
            return
        
        # Kiểm tra xem có file nào được staged không
        try:
            diff_info = get_git_diff()
            if not diff_info:
                messagebox.showinfo(self.texts["notice"], self.texts["no_changes"])
                return
        except Exception as e:
            auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
            messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
            return
        
        # Cập nhật trạng thái
        self.status_var.set(self.texts["committing"])
        
        # Tạo thread để không block giao diện
        def auto_commit_thread():
            try:
                # Tạo commit message
                commit_message = generate_commit_message(diff_info)
                if not commit_message:
                    messagebox.showerror(self.texts["error"], self.texts["error"])
                    self.status_var.set(self.texts["error"])
                    return
                
                # Cập nhật text widget
                self.commit_message_text.delete(1.0, tk.END)
                self.commit_message_text.insert(tk.END, commit_message)
                
                # Tạo commit
                success = create_commit(commit_message)
                if not success:
                    messagebox.showerror(self.texts["error"], self.texts["error"])
                    self.status_var.set(self.texts["error"])
                    return
                
                # Cập nhật trạng thái
                self.status_var.set(self.texts["commit_success"])
                
                # Cập nhật thông tin
                self.check_git()
                self.refresh_diff()
                
                # Push nếu được chọn
                if self.auto_push.get():
                    self.status_var.set(self.texts["pushing"])
                    try:
                        success = push_to_remote()
                        if success:
                            self.status_var.set(self.texts["push_success"])
                        else:
                            messagebox.showerror(self.texts["error"], self.texts["push_error"])
                            self.status_var.set(self.texts["push_error"])
                    except Exception as e:
                        auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
                        messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
                        self.status_var.set(self.texts["push_error"])
            except Exception as e:
                auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
                messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
                self.status_var.set(self.texts["error"])
        
        threading.Thread(target=auto_commit_thread).start()
    
    def do_commit(self):
        """Thực hiện commit"""
        # Lấy commit message từ text widget
        commit_message = self.commit_message_text.get(1.0, tk.END).strip()
        if not commit_message:
            messagebox.showinfo(self.texts["notice"], self.texts["enter_commit_message"])
            return
        
        # Kiểm tra xem có file nào được staged không
        try:
            diff_info = get_git_diff()
            if not diff_info and not self.settings["simulation_mode"]:
                messagebox.showinfo(self.texts["notice"], self.texts["no_changes"])
                return
        except Exception as e:
            if not self.settings["simulation_mode"]:
                auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
                messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
                return
        
        # Cập nhật trạng thái
        self.status_var.set(self.texts["committing"])
        
        # Tạo thread để không block giao diện
        def commit_thread():
            try:
                # Tạo commit
                success = create_commit(commit_message)
                if not success:
                    messagebox.showerror(self.texts["error"], self.texts["error"])
                    self.status_var.set(self.texts["error"])
                    return
                
                # Cập nhật trạng thái
                self.status_var.set(self.texts["commit_success"])
                
                # Cập nhật thông tin
                self.check_git()
                self.refresh_diff()
                
                # Xóa commit message
                self.commit_message_text.delete(1.0, tk.END)
                
                # Push nếu được chọn
                if self.auto_push.get():
                    self.status_var.set(self.texts["pushing"])
                    try:
                        success = push_to_remote()
                        if success:
                            self.status_var.set(self.texts["push_success"])
                        else:
                            messagebox.showerror(self.texts["error"], self.texts["push_error"])
                            self.status_var.set(self.texts["push_error"])
                    except Exception as e:
                        auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
                        messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
                        self.status_var.set(self.texts["push_error"])
            except Exception as e:
                auto_commit_logger.error(f"{self.texts['error']}: {str(e)}")
                messagebox.showerror(self.texts["error"], f"{self.texts['error']}: {str(e)}")
                self.status_var.set(self.texts["error"])
        
        threading.Thread(target=commit_thread).start()
    
    def open_settings(self):
        """Mở dialog cài đặt"""
        SettingsDialog(self.root, self.settings, self.save_settings)
    
    def save_settings(self, settings):
        """Lưu cài đặt"""
        old_lang = self.settings.get("language", "vi")
        old_theme = self.settings.get("theme", "light")
        
        # Cập nhật settings
        self.settings.update(settings)
        
        # Cập nhật biến toàn cục trong auto_commit.py
        try:
            import auto_commit
            auto_commit.API_KEY = self.settings["api_key"]
            auto_commit.MAX_DIFF_SIZE = self.settings["max_diff_size"]
            auto_commit.MAX_RETRIES = self.settings["max_retries"]
            auto_commit.RETRY_DELAY = self.settings["retry_delay"]
            auto_commit.SIMULATION_MODE = self.settings["simulation_mode"]
            
            # Cập nhật file auto_commit.py
            try:
                with open("auto_commit.py", 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Cập nhật API_KEY
                content = self.update_variable(content, "API_KEY", f'"{self.settings["api_key"]}"')
                
                # Cập nhật MAX_DIFF_SIZE
                content = self.update_variable(content, "MAX_DIFF_SIZE", str(self.settings["max_diff_size"]))
                
                # Cập nhật MAX_RETRIES
                content = self.update_variable(content, "MAX_RETRIES", str(self.settings["max_retries"]))
                
                # Cập nhật RETRY_DELAY
                content = self.update_variable(content, "RETRY_DELAY", str(self.settings["retry_delay"]))
                
                # Cập nhật SIMULATION_MODE
                content = self.update_variable(content, "SIMULATION_MODE", str(self.settings["simulation_mode"]))
                
                with open("auto_commit.py", 'w', encoding='utf-8') as file:
                    file.write(content)
                
                messagebox.showinfo(self.texts["notice"], self.texts["settings_saved"])
            except Exception as e:
                auto_commit_logger.error(f"Lỗi khi cập nhật file auto_commit.py: {str(e)}")
                messagebox.showerror(self.texts["error"], f"Lỗi khi cập nhật file auto_commit.py: {str(e)}")
                messagebox.showinfo(self.texts["notice"], self.texts["settings_saved_memory"])
        except Exception as e:
            auto_commit_logger.error(f"Lỗi khi cập nhật cài đặt: {str(e)}")
            messagebox.showerror(self.texts["error"], f"Lỗi khi cập nhật cài đặt: {str(e)}")
        
        # Cập nhật ngôn ngữ và theme nếu có thay đổi
        if self.settings["language"] != old_lang:
            self.current_lang = self.settings["language"]
        
        if self.settings["theme"] != old_theme:
            self.current_theme = self.settings["theme"]
        
        # Cập nhật lại toàn bộ giao diện
        self.refresh_ui()
    
    def update_variable(self, content, var_name, new_value):
        """Cập nhật giá trị biến trong nội dung file"""
        import re
        pattern = rf"{var_name}\s*=\s*.*"
        replacement = f"{var_name} = {new_value}"
        return re.sub(pattern, replacement, content)
    
    def on_tab_changed(self, event):
        """Xử lý sự kiện khi chuyển tab"""
        selected_tab = self.notebook.index(self.notebook.select())
        
        # Nếu chuyển đến tab Commit (index 2)
        if selected_tab == 2:
            # Kiểm tra xem có thay đổi nào được staged không và có bật tự động tạo không
            if self.auto_generate.get():
                try:
                    diff_info = get_git_diff()
                    if diff_info and not self.commit_message_text.get(1.0, tk.END).strip():
                        # Tự động tạo commit message nếu chưa có
                        self.generate_message()
                except Exception:
                    # Bỏ qua lỗi nếu có
                    pass
    
    def on_ctrl_enter(self, event):
        """Xử lý sự kiện khi nhấn Ctrl+Enter trong ô commit message"""
        self.do_commit()
        return "break"  # Ngăn không cho sự kiện tiếp tục lan truyền

    def create_tooltip(self, widget, text):
        """Tạo tooltip cho widget"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Tạo cửa sổ tooltip
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(self.tooltip, text=text, justify=tk.LEFT,
                             background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                             font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)
        
        def leave(event):
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()
        
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def refresh_ui(self):
        """Cập nhật lại toàn bộ giao diện"""
        # Cập nhật ngôn ngữ
        self.texts = TRANSLATIONS[self.current_lang]
        self.update_language()
        
        # Cập nhật theme
        self.theme = THEMES[self.current_theme]
        self.apply_theme()
        
        # Cập nhật màu nền cho các text widget
        for widget in [self.system_info_text, self.git_info_text, self.diff_text, 
                     self.commit_message_text, self.log_text]:
            widget.configure(bg=self.theme["text_bg"], fg=self.theme["text_fg"])
        
        # Cập nhật màu nền cho cửa sổ chính
        self.root.configure(bg=self.theme["bg"])
        
        # Cập nhật style cho các widget ttk
        self.style.configure(".", 
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TFrame",
            background=self.theme["bg"])
        
        self.style.configure("TLabel",
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TButton",
            background=self.theme["button_bg"],
            foreground=self.theme["button_fg"])
        
        self.style.configure("TCheckbutton",
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TNotebook",
            background=self.theme["bg"],
            foreground=self.theme["fg"])
        
        self.style.configure("TNotebook.Tab",
            background=self.theme["button_bg"],
            foreground=self.theme["button_fg"])
        
        # Force cập nhật giao diện
        self.root.update_idletasks()

def main():
    """Hàm chính của ứng dụng"""
    try:
        logger.info("Bắt đầu khởi tạo ứng dụng")
        root = tk.Tk()
        app = AutoCommitGUI(root)
        logger.info("Đã khởi tạo ứng dụng thành công, bắt đầu vòng lặp chính")
        root.mainloop()
        logger.info("Ứng dụng đã đóng")
    except Exception as e:
        logger.critical(f"Lỗi không xử lý được: {str(e)}", exc_info=True)
        messagebox.showerror("Lỗi nghiêm trọng", f"Ứng dụng gặp lỗi không xử lý được: {str(e)}")

if __name__ == "__main__":
    main() 