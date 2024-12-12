from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, git_handler):
        self.git_handler = git_handler
        
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            self.git_handler.handle_change(event.src_path, "modified")
            
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            self.git_handler.handle_change(event.src_path, "created")
            
    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")
            self.git_handler.handle_change(event.src_path, "deleted") 