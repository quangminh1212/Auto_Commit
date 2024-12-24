from typing import Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from PyQt6.QtWidgets import QApplication
from auto_commit.ui.main_window import MainWindow
from auto_commit.core.git import GitHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, git_handler: GitHandler, window: MainWindow):
        self.git_handler = git_handler
        self.window = window
        
    def on_created(self, event):
        if not event.is_directory:
            self.window.add_change(event.src_path, "CREATED")
            self.git_handler.handle_change(event.src_path, "created")
            
    def on_modified(self, event):
        if not event.is_directory:
            self.window.add_change(event.src_path, "MODIFIED")
            self.git_handler.handle_change(event.src_path, "modified")
            
    def on_deleted(self, event):
        if not event.is_directory:
            self.window.add_change(event.src_path, "DELETED")
            self.git_handler.handle_change(event.src_path, "deleted")

class FileWatcher:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.git_handler = GitHandler(
            config['repo_path'],
            config.get('github_token')
        )
        self.observer = Observer()
        
        # Create Qt application and window
        self.app = QApplication([])
        self.window = MainWindow(self.app)
        self.window.show()
        
    def start(self):
        event_handler = ChangeHandler(self.git_handler, self.window)
        self.observer.schedule(
            event_handler,
            self.config['watch_path'],
            recursive=True
        )
        
        self.observer.start()
        self.window.start_watching()
        
        # Start Qt event loop
        return self.app.exec() 