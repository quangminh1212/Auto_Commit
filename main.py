import os
import argparse
import time
from file_monitor import FileMonitor
from git_handler import GitHandler
from scheduler import Scheduler
import config

def parse_args():
    parser = argparse.ArgumentParser(description='Auto Commit - Automatically commit changes to git repositories')
    parser.add_argument('--watch', '-w', help='Directory to watch for changes', default=config.DEFAULT_WATCH_DIR)
    parser.add_argument('--interval', '-i', type=int, help='Commit interval in minutes', default=config.DEFAULT_INTERVAL)
    parser.add_argument('--message', '-m', help='Commit message template', default=config.DEFAULT_COMMIT_MESSAGE)
    parser.add_argument('--once', action='store_true', help='Commit once and exit')
    return parser.parse_args()

def main():
    args = parse_args()
    
    if not os.path.exists(args.watch):
        print(f"Error: Watch directory {args.watch} does not exist.")
        return
    
    git_handler = GitHandler(args.watch, args.message)
    file_monitor = FileMonitor(args.watch)
    
    if args.once:
        # Run once mode
        if file_monitor.check_for_changes():
            git_handler.commit_changes()
        return
    
    # Run in monitoring mode
    scheduler = Scheduler(args.interval)
    
    print(f"Auto Commit started. Watching: {args.watch}, Interval: {args.interval} minutes")
    try:
        while True:
            if scheduler.should_run() and file_monitor.check_for_changes():
                git_handler.commit_changes()
                scheduler.update_last_run()
            time.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        print("Auto Commit stopped")

if __name__ == "__main__":
    main()
