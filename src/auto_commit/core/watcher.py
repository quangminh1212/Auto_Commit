from typing import Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from rich import print

from auto_commit.core.git import GitHandler
from auto_commit.ui.console import ConsoleUI

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, git_handler: GitHandler, ui: ConsoleUI):
        self.git_handler = git_handler
        self.ui = ui
        
    def on_created(self, event):
        if not event.is_directory:
            self.ui.add_change(event.src_path, "CREATED")
            self.git_handler.handle_change(event.src_path, "created")
            
    def on_modified(self, event):
        if not event.is_directory:
            self.ui.add_change(event.src_path, "MODIFIED")
            self.git_handler.handle_change(event.src_path, "modified")
            
    def on_deleted(self, event):
        if not event.is_directory:
            self.ui.add_change(event.src_path, "DELETED")
            self.git_handler.handle_change(event.src_path, "deleted")

class FileWatcher:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.git_handler = GitHandler(
            config['repo_path'],
            config.get('github_token')
        )
        self.observer = Observer()
        self.ui = ConsoleUI()
        
    def start(self):
        event_handler = ChangeHandler(self.git_handler, self.ui)
        self.observer.schedule(
            event_handler,
            self.config['watch_path'],
            recursive=True
        )
        
        self.observer.start()
        self.ui.start()  # Khởi động giao diện
        
        try:
            while True:
                time.sleep(self.config.get('commit_delay', 30))
        except KeyboardInterrupt:
            self.observer.stop()
            
        self.observer.join() 