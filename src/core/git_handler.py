from git import Repo
from github import Github
import logging

class GitHandler:
    def __init__(self, repo_path, github_token=None):
        self.repo = Repo(repo_path)
        self.github = Github(github_token) if github_token else None
        
    def handle_change(self, file_path, change_type):
        try:
            if change_type != "deleted":
                self.repo.index.add([file_path])
            else:
                self.repo.index.remove([file_path])
                
            commit_message = self.generate_commit_message(file_path, change_type)
            self.repo.index.commit(commit_message)
            
            if self.github:
                self.push_changes()
                
        except Exception as e:
            logging.error(f"Git operation failed: {str(e)}")
            
    def generate_commit_message(self, file_path, change_type):
        file_type = self.get_file_type(file_path)
        return f"{file_type}: {change_type} {file_path}"
        
    def get_file_type(self, file_path):
        if file_path.endswith(('.md', '.txt')):
            return 'docs'
        elif file_path.endswith(('.py', '.js', '.java')):
            return 'feat'
        elif file_path.endswith(('test.py', 'spec.js')):
            return 'test'
        return 'chore'
        
    def push_changes(self):
        origin = self.repo.remote('origin')
        origin.push() 