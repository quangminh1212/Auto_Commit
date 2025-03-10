import os
import subprocess
import datetime

class GitHandler:
    def __init__(self, repo_path, commit_message_template):
        self.repo_path = repo_path
        self.commit_message_template = commit_message_template
    
    def is_git_repo(self):
        """Check if the directory is a git repository"""
        git_dir = os.path.join(self.repo_path, ".git")
        return os.path.exists(git_dir) and os.path.isdir(git_dir)
    
    def init_repo(self):
        """Initialize a new git repository if needed"""
        if not self.is_git_repo():
            try:
                subprocess.run(["git", "init"], cwd=self.repo_path, check=True)
                return True
            except subprocess.SubprocessError:
                print(f"Error initializing git repository in {self.repo_path}")
                return False
        return True
    
    def has_changes(self):
        """Check if there are any changes to commit"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"], 
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return len(result.stdout.strip()) > 0
        except subprocess.SubprocessError:
            return False
    
    def add_all_changes(self):
        """Add all changes to git staging area"""
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            return True
        except subprocess.SubprocessError:
            print("Error adding changes to git staging area")
            return False
    
    def commit_changes(self):
        """Commit all staged changes"""
        if not self.is_git_repo():
            if not self.init_repo():
                return False
        
        if not self.has_changes():
            print("No changes to commit")
            return False
        
        if not self.add_all_changes():
            return False
        
        # Format commit message
        now = datetime.datetime.now()
        commit_message = self.commit_message_template.format(
            datetime=now.strftime("%Y-%m-%d %H:%M:%S"),
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S")
        )
        
        try:
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            print(f"Committed changes with message: {commit_message}")
            return True
        except subprocess.SubprocessError:
            print("Error committing changes")
            return False
