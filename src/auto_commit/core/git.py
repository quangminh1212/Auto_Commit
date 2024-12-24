from pathlib import Path
from typing import Optional
import logging
from git import Repo
from github import Github

class GitHandler:
    def __init__(self, repo_path: str, github_token: Optional[str] = None):
        self.repo_path = Path(repo_path)
        self.repo = Repo(self.repo_path)
        self.github = Github(github_token) if github_token else None
        
    def handle_change(self, file_path: str, change_type: str) -> None:
        """Handle file changes and create commits"""
        try:
            relative_path = Path(file_path).relative_to(self.repo_path)
            
            # Skip git and cache files
            if self._should_ignore(relative_path):
                return

            # Add or remove file from git
            if change_type != "deleted":
                self.repo.index.add([str(relative_path)])
            else:
                self.repo.index.remove([str(relative_path)])

            # Create commit
            commit_message = self._generate_commit_message(relative_path, change_type)
            self.repo.index.commit(commit_message)
            
            # Push if GitHub token is provided
            if self.github:
                self._push_changes()
                
        except Exception as e:
            logging.error(f"Git operation failed: {str(e)}")
            raise

    def _should_ignore(self, file_path: Path) -> bool:
        """Check if file should be ignored"""
        ignore_patterns = [".git", "__pycache__", ".pyc", ".swp"]
        return any(pattern in str(file_path) for pattern in ignore_patterns)

    def _generate_commit_message(self, file_path: Path, change_type: str) -> str:
        """Generate standardized commit message"""
        file_ext = file_path.suffix.lower()
        
        # Map file types to commit prefixes
        type_prefix = {
            '.py': 'feat',
            '.md': 'docs',
            '.yml': 'config',
            '.yaml': 'config',
            '.txt': 'chore',
            '.json': 'config',
            '.gitignore': 'chore',
        }.get(file_ext, 'chore')
        
        action_map = {
            "created": "add",
            "modified": "update",
            "deleted": "remove"
        }
        action = action_map.get(change_type, "update")
        
        return f"{type_prefix}: {action} {file_path}"

    def _push_changes(self) -> None:
        """Push changes to remote repository"""
        try:
            origin = self.repo.remote("origin")
            origin.push()
        except Exception as e:
            logging.error(f"Failed to push changes: {str(e)}")
            raise 