import os
import time
import hashlib

class FileMonitor:
    def __init__(self, directory):
        self.directory = directory
        self.last_state = self.get_directory_state()
        
    def get_directory_state(self):
        """Get a hash representation of the current directory state"""
        state = {}
        for root, _, files in os.walk(self.directory):
            if ".git" in root:
                continue
                
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(full_path)
                    size = os.path.getsize(full_path)
                    state[full_path] = (mtime, size)
                except (FileNotFoundError, PermissionError):
                    continue
        
        return state
    
    def check_for_changes(self):
        """Check if there are any changes in the directory"""
        current_state = self.get_directory_state()
        
        # Check if anything changed
        if current_state != self.last_state:
            self.last_state = current_state
            return True
        
        return False
