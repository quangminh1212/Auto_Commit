import time
from watchdog.observers import Observer
from core.file_watcher import FileChangeHandler
from core.git_handler import GitHandler
from utils.config import Config
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    
    # Load config
    config = Config()
    settings = config.settings
    
    # Initialize handlers
    git_handler = GitHandler(
        settings.get('repo_path', '.'),
        settings.get('github_token')
    )
    event_handler = FileChangeHandler(git_handler)
    
    # Set up observer
    observer = Observer()
    observer.schedule(
        event_handler,
        settings.get('watch_path', '.'),
        recursive=True
    )
    
    try:
        observer.start()
        logging.info("File watcher started...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("File watcher stopped")
    observer.join()

if __name__ == "__main__":
    main() 