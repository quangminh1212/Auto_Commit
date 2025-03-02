import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import datetime
import logging
import sys

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('auto_commit.log', encoding='utf-8')
    ]
)

class GitAutoCommit(FileSystemEventHandler):
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.last_modified = 0
        self.cooldown = 5  # Thời gian chờ giữa các lần commit (giây)
        
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

if __name__ == "__main__":
    try:
        repo_path = '.'  # Đường dẫn tới repository
        event_handler = GitAutoCommit(repo_path)
        observer = Observer()
        observer.schedule(event_handler, repo_path, recursive=True)
        observer.start()
        
        logging.info("[START] Bắt đầu theo dõi thay đổi trong repository...")
        logging.info(f"[PATH] Đường dẫn repository: {os.path.abspath(repo_path)}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logging.info("[STOP] Đã dừng theo dõi repository")
        observer.join()
        
    except Exception as e:
        logging.error(f"[ERROR] Lỗi khởi động ứng dụng: {str(e)}")
        sys.exit(1) 