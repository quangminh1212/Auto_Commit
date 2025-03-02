import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import datetime

class GitAutoCommit(FileSystemEventHandler):
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.last_modified = 0
        self.cooldown = 5  # Thời gian chờ giữa các lần commit (giây)

    def on_modified(self, event):
        if event.is_directory:
            return
            
        current_time = time.time()
        if current_time - self.last_modified < self.cooldown:
            return
            
        self.last_modified = current_time
        
        try:
            # Kiểm tra trạng thái của repository
            if self.repo.is_dirty(untracked_files=True):
                # Add tất cả các file đã thay đổi
                self.repo.git.add(all=True)
                
                # Tạo commit message với timestamp
                commit_message = f"Auto commit at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.repo.index.commit(commit_message)
                
                # Push lên remote repository
                origin = self.repo.remote(name='origin')
                origin.push()
                
                print(f"Đã commit và push thay đổi: {commit_message}")
            
        except Exception as e:
            print(f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    repo_path = '.'  # Đường dẫn tới repository
    event_handler = GitAutoCommit(repo_path)
    observer = Observer()
    observer.schedule(event_handler, repo_path, recursive=True)
    observer.start()
    
    print("Bắt đầu theo dõi thay đổi trong repository...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Đã dừng theo dõi repository")
    observer.join() 