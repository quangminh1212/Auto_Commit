import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import datetime
import logging
import sys
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, simpledialog
import threading
import queue
import subprocess 
import io

# Cấu hình logging với custom handler để gửi log đến giao diện
log_queue = queue.Queue()
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('auto_commit.log', encoding='utf-8')
    ]
)

# Thêm handler để gửi log đến queue
class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(self.format(record))

queue_handler = QueueHandler(log_queue)
queue_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(queue_handler)

# Định nghĩa các màu cho dark mode
DARK_BG = "#2E2E2E"
DARKER_BG = "#252525"
DARK_TEXT = "#E0E0E0"
ACCENT_COLOR = "#007ACC"
BUTTON_BG = "#3E3E3E"
BUTTON_ACTIVE = "#505050"
HIGHLIGHT_BG = "#3A3D41"

class GitAutoCommit(FileSystemEventHandler):
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.last_modified = 0
        self.cooldown = 5  # Thời gian chờ giữa các lần commit (giây)
        self.is_active = True  # Trạng thái theo dõi
        
        # Các file và thư mục sẽ được bỏ qua
        self.ignored_patterns = [
            '.git',
            '__pycache__',
            '*.pyc',
            '.vscode',
            'auto_commit.log',
            '.gitignore'
        ]

    def should_ignore(self, path):
        """Kiểm tra xem file có nên được bỏ qua hay không"""
        from fnmatch import fnmatch
        
        # Chuyển đổi đường dẫn tương đối
        rel_path = os.path.relpath(path, self.repo_path)
        
        for pattern in self.ignored_patterns:
            if fnmatch(rel_path, pattern) or any(fnmatch(part, pattern) for part in rel_path.split(os.sep)):
                return True
        return False

    def on_modified(self, event):
        if not self.is_active:
            return
            
        if event.is_directory:
            return
            
        if self.should_ignore(event.src_path):
            return
            
        current_time = time.time()
        if current_time - self.last_modified < self.cooldown:
            return
            
        self.last_modified = current_time
        
        try:
            # Kiểm tra trạng thái của repository
            if self.repo.is_dirty(untracked_files=True):
                # Add tất cả các file đã thay đổi
                changed_files = [item.a_path for item in self.repo.index.diff(None)]
                untracked_files = self.repo.untracked_files
                
                self.repo.git.add(all=True)
                
                # Tạo commit message với thông tin chi tiết
                changed_files_str = ", ".join(changed_files + untracked_files)
                commit_message = "Auto commit at {}\n\nChanged files: {}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    changed_files_str
                )
                
                # Commit các thay đổi
                self.repo.index.commit(commit_message)
                
                # Push lên remote repository
                try:
                    origin = self.repo.remote(name='origin')
                    origin.push()
                    logging.info("[SUCCESS] Đã commit và push thành công:\n{}".format(commit_message))
                except Exception as e:
                    logging.error("[ERROR] Lỗi khi push lên remote: {}".format(str(e)))
                    logging.info("[INFO] Các thay đổi đã được commit locally và sẽ được push khi có kết nối")
            
        except Exception as e:
            logging.error("[ERROR] Lỗi: {}".format(str(e)))

class DarkThemeDialog(simpledialog.Dialog):
    def __init__(self, parent, title, default_message, changed_files):
        self.default_message = default_message
        self.changed_files = changed_files
        self.result_message = None
        
        # Thiết lập style cho dialog
        parent.option_add("*Dialog.msg.background", DARK_BG)
        parent.option_add("*Dialog.msg.foreground", DARK_TEXT)
        parent.option_add("*Dialog.background", DARK_BG)
        parent.option_add("*Dialog.foreground", DARK_TEXT)
        
        super().__init__(parent, title)
        
    def body(self, master):
        master.configure(bg=DARK_BG)
        
        ttk.Label(master, text="Các file đã thay đổi:", background=DARK_BG, foreground=DARK_TEXT).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Hiển thị danh sách file đã thay đổi
        files_frame = ttk.Frame(master)
        files_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        files_text = scrolledtext.ScrolledText(files_frame, wrap=tk.WORD, width=60, height=5, 
                                              bg=DARKER_BG, fg=DARK_TEXT, insertbackground=DARK_TEXT)
        files_text.pack(fill=tk.BOTH, expand=True)
        files_text.insert(tk.END, "\n".join(self.changed_files))
        files_text.config(state=tk.DISABLED)
        
        ttk.Label(master, text="Nội dung commit:", background=DARK_BG, foreground=DARK_TEXT).grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        # Text area cho commit message
        self.message_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=10,
                                                     bg=DARKER_BG, fg=DARK_TEXT, insertbackground=DARK_TEXT)
        self.message_text.grid(row=3, column=0, sticky="ew")
        self.message_text.insert(tk.END, self.default_message)
        
        # Nút Generate với Copilot
        generate_frame = ttk.Frame(master)
        generate_frame.grid(row=4, column=0, sticky="ew", pady=10)
        
        generate_button = ttk.Button(generate_frame, text="Generate với Copilot", 
                                    command=self.generate_with_copilot)
        generate_button.pack(side=tk.LEFT, padx=5)
        
        return self.message_text  # initial focus
        
    def generate_with_copilot(self):
        try:
            # Lấy thông tin về các thay đổi
            files_info = "\n".join(self.changed_files)
            
            # Thực hiện lệnh git diff để lấy thông tin chi tiết về thay đổi
            try:
                # Sử dụng encoding utf-8 để xử lý đúng các ký tự Unicode
                process = subprocess.Popen(
                    ["git", "diff", "--staged"], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    encoding='utf-8'
                )
                diff_output, _ = process.communicate()
            except Exception:
                diff_output = "Không thể lấy thông tin diff"
            
            # Tạo prompt cho Copilot
            prompt = "Tạo commit message dựa trên các thay đổi sau:\n\nCác file đã thay đổi:\n{}\n\nDiff:\n{}".format(
                files_info, diff_output[:1000]
            )
            
            # Hiển thị dialog đang xử lý
            self.message_text.config(state=tk.NORMAL)
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, "Đang tạo commit message với Copilot...")
            
            # Mô phỏng việc gọi Copilot API (thực tế sẽ cần tích hợp với API của Copilot)
            # Trong trường hợp này, chúng ta tạo một commit message mẫu
            time.sleep(1)  # Giả lập thời gian xử lý
            
            # Tạo commit message dựa trên các file đã thay đổi
            generated_message = "feat: cập nhật {} file\n\n".format(len(self.changed_files))
            
            # Phân loại các thay đổi
            if any("fix" in f.lower() for f in self.changed_files):
                generated_message += "- Sửa lỗi trong các module\n"
            if any(".py" in f.lower() for f in self.changed_files):
                generated_message += "- Cập nhật mã nguồn Python\n"
            if any(".md" in f.lower() or "readme" in " ".join(self.changed_files).lower()):
                generated_message += "- Cập nhật tài liệu\n"
            if any("test" in f.lower() for f in self.changed_files):
                generated_message += "- Thêm/cập nhật test cases\n"
                
            generated_message += "\nCác file đã thay đổi: {}".format(", ".join(self.changed_files))
            
            # Cập nhật text area
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, generated_message)
            
        except Exception as e:
            messagebox.showerror("Lỗi", "Không thể tạo commit message: {}".format(str(e)))
            self.message_text.config(state=tk.NORMAL)
    
    def buttonbox(self):
        # Tạo frame cho các nút
        box = ttk.Frame(self)
        
        # Tạo nút OK và Cancel
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        
        box.pack(pady=5)
    
    def apply(self):
        self.result_message = self.message_text.get(1.0, tk.END).strip()

class AutoCommitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Commit Tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Thiết lập dark theme
        self.setup_dark_theme()
        
        self.create_widgets()
        self.observer = None
        self.event_handler = None
        self.is_running = False
        
        # Bắt đầu thread để cập nhật log
        self.log_update_thread = threading.Thread(target=self.update_log_widget, daemon=True)
        self.log_update_thread.start()
        
        # Tự động bắt đầu theo dõi khi khởi động
        self.start_monitoring()
    
    def setup_dark_theme(self):
        """Thiết lập giao diện tối giản"""
        self.root.configure(bg=DARK_BG)
        
        # Tạo style cho ttk widgets
        self.style = ttk.Style()
        
        # Cấu hình màu sắc cho các widget
        self.style.configure("TFrame", background=DARK_BG)
        self.style.configure("TLabel", background=DARK_BG, foreground=DARK_TEXT)
        self.style.configure("TLabelframe", background=DARK_BG, foreground=DARK_TEXT)
        self.style.configure("TLabelframe.Label", background=DARK_BG, foreground=DARK_TEXT)
        
        # Cấu hình nút
        self.style.configure("TButton", background=BUTTON_BG, foreground=DARK_TEXT)
        self.style.map("TButton", 
                      background=[("active", BUTTON_ACTIVE), ("pressed", ACCENT_COLOR)],
                      foreground=[("active", DARK_TEXT)])
        
        # Cấu hình spinbox
        self.style.configure("TSpinbox", background=DARKER_BG, foreground=DARK_TEXT, 
                            fieldbackground=DARKER_BG, arrowcolor=DARK_TEXT)
        
    def create_widgets(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame điều khiển
        control_frame = ttk.LabelFrame(main_frame, text="Điều khiển", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Nút Start/Stop
        self.toggle_button = ttk.Button(control_frame, text="Dừng theo dõi", command=self.toggle_monitoring)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        
        # Nút Force Commit
        self.force_commit_button = ttk.Button(control_frame, text="Commit ngay", command=self.force_commit)
        self.force_commit_button.pack(side=tk.LEFT, padx=5)
        
        # Nút Generate Commit Message
        self.gen_commit_button = ttk.Button(control_frame, text="Generate Commit Message", 
                                           command=self.generate_commit_message)
        self.gen_commit_button.pack(side=tk.LEFT, padx=5)
        
        # Nút Clear Log
        self.clear_log_button = ttk.Button(control_frame, text="Xóa log", command=self.clear_log)
        self.clear_log_button.pack(side=tk.LEFT, padx=5)
        
        # Cooldown setting
        ttk.Label(control_frame, text="Thời gian chờ (giây):").pack(side=tk.LEFT, padx=(20, 5))
        self.cooldown_var = tk.StringVar(value="5")
        cooldown_spinbox = ttk.Spinbox(control_frame, from_=1, to=60, textvariable=self.cooldown_var, width=5)
        cooldown_spinbox.pack(side=tk.LEFT)
        
        # Trạng thái
        self.status_var = tk.StringVar(value="Đang khởi động...")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground=ACCENT_COLOR)
        status_label.pack(side=tk.RIGHT, padx=5)
        
        # Frame log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Widget hiển thị log
        self.log_widget = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 10),
                                                  bg=DARKER_BG, fg=DARK_TEXT, insertbackground=DARK_TEXT)
        self.log_widget.pack(fill=tk.BOTH, expand=True)
        self.log_widget.config(state=tk.DISABLED)
        
        # Thông tin
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        repo_path = os.path.abspath('.')
        ttk.Label(info_frame, text="Repository: {}".format(repo_path), foreground=ACCENT_COLOR).pack(anchor=tk.W)
        
    def update_log_widget(self):
        """Cập nhật widget log từ queue"""
        while True:
            try:
                record = log_queue.get(block=False)
                self.log_widget.config(state=tk.NORMAL)
                
                # Thêm màu sắc cho log
                if "[SUCCESS]" in record:
                    self.log_widget.insert(tk.END, record + "\n", "success")
                    self.log_widget.tag_configure("success", foreground="#4EC9B0")
                elif "[ERROR]" in record:
                    self.log_widget.insert(tk.END, record + "\n", "error")
                    self.log_widget.tag_configure("error", foreground="#F48771")
                elif "[INFO]" in record:
                    self.log_widget.insert(tk.END, record + "\n", "info")
                    self.log_widget.tag_configure("info", foreground="#9CDCFE")
                else:
                    self.log_widget.insert(tk.END, record + "\n")
                
                self.log_widget.see(tk.END)
                self.log_widget.config(state=tk.DISABLED)
            except queue.Empty:
                time.sleep(0.1)
                continue
    
    def start_monitoring(self):
        """Bắt đầu theo dõi repository"""
        if self.is_running:
            return
            
        try:
            repo_path = '.'
            self.event_handler = GitAutoCommit(repo_path)
            
            # Cập nhật cooldown từ UI
            try:
                cooldown = int(self.cooldown_var.get())
                self.event_handler.cooldown = cooldown
            except ValueError:
                pass
                
            self.observer = Observer()
            self.observer.schedule(self.event_handler, repo_path, recursive=True)
            self.observer.start()
            
            self.is_running = True
            self.status_var.set("Đang theo dõi")
            self.toggle_button.config(text="Dừng theo dõi")
            
            logging.info("[START] Bắt đầu theo dõi thay đổi trong repository...")
            logging.info("[PATH] Đường dẫn repository: {}".format(os.path.abspath(repo_path)))
            
        except Exception as e:
            logging.error("[ERROR] Lỗi khởi động ứng dụng: {}".format(str(e)))
            messagebox.showerror("Lỗi", "Không thể bắt đầu theo dõi: {}".format(str(e)))
    
    def stop_monitoring(self):
        """Dừng theo dõi repository"""
        if not self.is_running:
            return
            
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            
        self.is_running = False
        self.status_var.set("Đã dừng")
        self.toggle_button.config(text="Bắt đầu theo dõi")
        
        logging.info("[STOP] Đã dừng theo dõi repository")
    
    def toggle_monitoring(self):
        """Bật/tắt theo dõi repository"""
        if self.is_running:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def generate_commit_message(self):
        """Tạo commit message với Copilot"""
        if not self.is_running or not self.event_handler:
            messagebox.showinfo("Thông báo", "Vui lòng bắt đầu theo dõi trước khi tạo commit message")
            return
            
        try:
            repo = self.event_handler.repo
            
            if not repo.is_dirty(untracked_files=True):
                messagebox.showinfo("Thông báo", "Không có thay đổi để commit")
                return
                
            # Add tất cả các file đã thay đổi để có thể lấy thông tin
            repo.git.add(all=True)
            
            # Lấy danh sách file đã thay đổi
            changed_files = [item.a_path for item in repo.index.diff(None)]
            untracked_files = repo.untracked_files
            all_changed_files = changed_files + untracked_files
            
            # Tạo commit message mặc định
            default_message = "Auto commit at {}\n\nChanged files: {}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ", ".join(all_changed_files)
            )
            
            # Hiển thị dialog để chỉnh sửa commit message
            dialog = DarkThemeDialog(
                self.root, 
                "Tạo Commit Message", 
                default_message,
                all_changed_files
            )
            
            # Kiểm tra xem người dùng đã nhấn OK hay Cancel
            if hasattr(dialog, 'result_message') and dialog.result_message:
                # Thực hiện commit với message đã chỉnh sửa
                # Đảm bảo commit message là chuỗi ASCII hoặc UTF-8 hợp lệ
                safe_message = dialog.result_message.encode('utf-8', errors='replace').decode('utf-8')
                repo.index.commit(safe_message)
                
                # Push lên remote repository
                try:
                    origin = repo.remote(name='origin')
                    origin.push()
                    logging.info("[SUCCESS] Đã commit và push thành công (với message tùy chỉnh):\n{}".format(safe_message))
                except Exception as e:
                    logging.error("[ERROR] Lỗi khi push lên remote: {}".format(str(e)))
                    logging.info("[INFO] Các thay đổi đã được commit locally và sẽ được push khi có kết nối")
                
        except Exception as e:
            logging.error("[ERROR] Lỗi khi tạo commit message: {}".format(str(e)))
            messagebox.showerror("Lỗi", "Không thể tạo commit message: {}".format(str(e)))
    
    def force_commit(self):
        """Thực hiện commit ngay lập tức"""
        if not self.is_running or not self.event_handler:
            messagebox.showinfo("Thông báo", "Vui lòng bắt đầu theo dõi trước khi commit")
            return
            
        try:
            repo = self.event_handler.repo
            
            if not repo.is_dirty(untracked_files=True):
                messagebox.showinfo("Thông báo", "Không có thay đổi để commit")
                return
                
            # Add tất cả các file đã thay đổi
            changed_files = [item.a_path for item in repo.index.diff(None)]
            untracked_files = repo.untracked_files
            
            repo.git.add(all=True)
            
            # Tạo commit message
            changed_files_str = ", ".join(changed_files + untracked_files)
            commit_message = "Manual commit at {}\n\nChanged files: {}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                changed_files_str
            )
            
            # Đảm bảo commit message là chuỗi ASCII hoặc UTF-8 hợp lệ
            safe_message = commit_message.encode('utf-8', errors='replace').decode('utf-8')
            
            # Commit các thay đổi
            repo.index.commit(safe_message)
            
            # Push lên remote repository
            try:
                origin = repo.remote(name='origin')
                origin.push()
                logging.info("[SUCCESS] Đã commit và push thành công (thủ công):\n{}".format(safe_message))
            except Exception as e:
                logging.error("[ERROR] Lỗi khi push lên remote: {}".format(str(e)))
                logging.info("[INFO] Các thay đổi đã được commit locally và sẽ được push khi có kết nối")
                
        except Exception as e:
            logging.error("[ERROR] Lỗi khi commit thủ công: {}".format(str(e)))
            messagebox.showerror("Lỗi", "Không thể commit: {}".format(str(e)))
    
    def clear_log(self):
        """Xóa nội dung log widget"""
        self.log_widget.config(state=tk.NORMAL)
        self.log_widget.delete(1.0, tk.END)
        self.log_widget.config(state=tk.DISABLED)
        
    def on_closing(self):
        """Xử lý khi đóng ứng dụng"""
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát ứng dụng?"):
            self.stop_monitoring()
            self.root.destroy()

if __name__ == "__main__":
    try:
        # Đặt mã hóa mặc định cho stdout và stderr
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
            
        root = tk.Tk()
        app = AutoCommitApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
        
    except Exception as e:
        logging.error("[ERROR] Lỗi khởi động ứng dụng: {}".format(str(e)))
        sys.exit(1) 