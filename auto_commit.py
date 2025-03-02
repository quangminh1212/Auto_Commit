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
                commit_message = f"Auto commit at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nChanged files: {changed_files_str}"
                
                # Commit các thay đổi
                self.repo.index.commit(commit_message)
                
                # Push lên remote repository
                try:
                    origin = self.repo.remote(name='origin')
                    origin.push()
                    logging.info(f"[SUCCESS] Đã commit và push thành công:\n{commit_message}")
                except Exception as e:
                    logging.error(f"[ERROR] Lỗi khi push lên remote: {str(e)}")
                    logging.info("[INFO] Các thay đổi đã được commit locally và sẽ được push khi có kết nối")
            
        except Exception as e:
            logging.error(f"[ERROR] Lỗi: {str(e)}")

class CommitMessageDialog(simpledialog.Dialog):
    def __init__(self, parent, title, default_message, changed_files):
        self.default_message = default_message
        self.changed_files = changed_files
        self.result_message = None
        super().__init__(parent, title)
        
    def body(self, master):
        ttk.Label(master, text="Các file đã thay đổi:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Hiển thị danh sách file đã thay đổi
        files_frame = ttk.Frame(master)
        files_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        files_text = scrolledtext.ScrolledText(files_frame, wrap=tk.WORD, width=60, height=5)
        files_text.pack(fill=tk.BOTH, expand=True)
        files_text.insert(tk.END, "\n".join(self.changed_files))
        files_text.config(state=tk.DISABLED)
        
        ttk.Label(master, text="Nội dung commit:").grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        # Text area cho commit message
        self.message_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=10)
        self.message_text.grid(row=3, column=0, sticky="ew")
        self.message_text.insert(tk.END, self.default_message)
        
        # Nút Generate với Copilot
        generate_frame = ttk.Frame(master)
        generate_frame.grid(row=4, column=0, sticky="ew", pady=10)
        
        ttk.Button(generate_frame, text="Generate với Copilot", 
                  command=self.generate_with_copilot).pack(side=tk.LEFT, padx=5)
        
        return self.message_text  # initial focus
        
    def generate_with_copilot(self):
        try:
            # Lấy thông tin về các thay đổi
            files_info = "\n".join(self.changed_files)
            
            # Thực hiện lệnh git diff để lấy thông tin chi tiết về thay đổi
            try:
                diff_output = subprocess.check_output(
                    ["git", "diff", "--staged"], 
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
            except subprocess.CalledProcessError:
                diff_output = "Không thể lấy thông tin diff"
            
            # Tạo prompt cho Copilot
            prompt = f"Tạo commit message dựa trên các thay đổi sau:\n\nCác file đã thay đổi:\n{files_info}\n\nDiff:\n{diff_output[:1000]}"
            
            # Hiển thị dialog đang xử lý
            self.message_text.config(state=tk.DISABLED)
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, "Đang tạo commit message với Copilot...")
            self.message_text.config(state=tk.NORMAL)
            
            # Mô phỏng việc gọi Copilot API (thực tế sẽ cần tích hợp với API của Copilot)
            # Trong trường hợp này, chúng ta tạo một commit message mẫu
            import time
            time.sleep(1)  # Giả lập thời gian xử lý
            
            # Tạo commit message dựa trên các file đã thay đổi
            generated_message = f"feat: cập nhật {len(self.changed_files)} file\n\n"
            
            # Phân loại các thay đổi
            if any("fix" in f.lower() for f in self.changed_files):
                generated_message += "- Sửa lỗi trong các module\n"
            if any(".py" in f.lower() for f in self.changed_files):
                generated_message += "- Cập nhật mã nguồn Python\n"
            if any(".md" in f.lower() or "readme" in " ".join(self.changed_files).lower()):
                generated_message += "- Cập nhật tài liệu\n"
            if any("test" in f.lower() for f in self.changed_files):
                generated_message += "- Thêm/cập nhật test cases\n"
                
            generated_message += f"\nCác file đã thay đổi: {', '.join(self.changed_files)}"
            
            # Cập nhật text area
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(tk.END, generated_message)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo commit message: {str(e)}")
            self.message_text.config(state=tk.NORMAL)
    
    def apply(self):
        self.result_message = self.message_text.get(1.0, tk.END).strip()

class AutoCommitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Commit Tool")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        self.create_widgets()
        self.observer = None
        self.event_handler = None
        self.is_running = False
        
        # Bắt đầu thread để cập nhật log
        self.log_update_thread = threading.Thread(target=self.update_log_widget, daemon=True)
        self.log_update_thread.start()
        
        # Tự động bắt đầu theo dõi khi khởi động
        self.start_monitoring()
        
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
        status_label = ttk.Label(control_frame, textvariable=self.status_var, foreground="blue")
        status_label.pack(side=tk.RIGHT, padx=5)
        
        # Frame log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Widget hiển thị log
        self.log_widget = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.log_widget.pack(fill=tk.BOTH, expand=True)
        self.log_widget.config(state=tk.DISABLED)
        
        # Thông tin
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        repo_path = os.path.abspath('.')
        ttk.Label(info_frame, text=f"Repository: {repo_path}", foreground="gray").pack(anchor=tk.W)
        
    def update_log_widget(self):
        """Cập nhật widget log từ queue"""
        while True:
            try:
                record = log_queue.get(block=False)
                self.log_widget.config(state=tk.NORMAL)
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
            self.observer = Observer()
            self.observer.schedule(self.event_handler, repo_path, recursive=True)
            self.observer.start()
            
            self.is_running = True
            self.status_var.set("Đang theo dõi")
            self.toggle_button.config(text="Dừng theo dõi")
            
            logging.info("[START] Bắt đầu theo dõi thay đổi trong repository...")
            logging.info(f"[PATH] Đường dẫn repository: {os.path.abspath(repo_path)}")
            
        except Exception as e:
            logging.error(f"[ERROR] Lỗi khởi động ứng dụng: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể bắt đầu theo dõi: {str(e)}")
    
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
            default_message = f"Auto commit at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nChanged files: {', '.join(all_changed_files)}"
            
            # Hiển thị dialog để chỉnh sửa commit message
            dialog = CommitMessageDialog(
                self.root, 
                "Tạo Commit Message", 
                default_message,
                all_changed_files
            )
            
            if dialog.result_message:
                # Thực hiện commit với message đã chỉnh sửa
                repo.index.commit(dialog.result_message)
                
                # Push lên remote repository
                try:
                    origin = repo.remote(name='origin')
                    origin.push()
                    logging.info(f"[SUCCESS] Đã commit và push thành công (với message tùy chỉnh):\n{dialog.result_message}")
                except Exception as e:
                    logging.error(f"[ERROR] Lỗi khi push lên remote: {str(e)}")
                    logging.info("[INFO] Các thay đổi đã được commit locally và sẽ được push khi có kết nối")
                
        except Exception as e:
            logging.error(f"[ERROR] Lỗi khi tạo commit message: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể tạo commit message: {str(e)}")
    
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
            commit_message = f"Manual commit at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nChanged files: {changed_files_str}"
            
            # Commit các thay đổi
            repo.index.commit(commit_message)
            
            # Push lên remote repository
            try:
                origin = repo.remote(name='origin')
                origin.push()
                logging.info(f"[SUCCESS] Đã commit và push thành công (thủ công):\n{commit_message}")
            except Exception as e:
                logging.error(f"[ERROR] Lỗi khi push lên remote: {str(e)}")
                logging.info("[INFO] Các thay đổi đã được commit locally và sẽ được push khi có kết nối")
                
        except Exception as e:
            logging.error(f"[ERROR] Lỗi khi commit thủ công: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể commit: {str(e)}")
    
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
        root = tk.Tk()
        app = AutoCommitApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
        
    except Exception as e:
        logging.error(f"[ERROR] Lỗi khởi động ứng dụng: {str(e)}")
        sys.exit(1) 