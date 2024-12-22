from pathlib import Path
from typing import Optional
import logging

from git import Repo
from github import Github

from auto_commit.utils.logger import get_logger

logger = get_logger(__name__)

class GitHandler:
    def __init__(
        self,
        repo_path: str,
        github_token: Optional[str] = None
    ):
        self.repo_path = Path(repo_path)
        self.repo = Repo(self.repo_path)
        self.github = Github(github_token) if github_token else None
        logger.info(f"Initialized Git handler for {repo_path}")

    def handle_change(self, file_path: str, change_type: str) -> None:
        """Handle file changes and create commits"""
        try:
            relative_path = Path(file_path).relative_to(self.repo_path)
            
            if self._should_ignore(relative_path):
                return

            if change_type != "deleted":
                self.repo.index.add([str(relative_path)])
            else:
                self.repo.index.remove([str(relative_path)])

            commit_message = self._generate_commit_message(relative_path, change_type)
            self.repo.index.commit(commit_message)
            
            if self.github:
                self._push_changes()
                
            logger.info(f"Successfully handled {change_type} for {relative_path}")
            
        except Exception as e:
            logger.error(f"Git operation failed: {str(e)}")
            raise

    def _should_ignore(self, file_path: Path) -> bool:
        """Check if file should be ignored"""
        ignore_patterns = [".git", "__pycache__", ".pyc", ".swp"]
        return any(pattern in str(file_path) for pattern in ignore_patterns)

    def _generate_commit_message(self, file_path: Path, change_type: str) -> str:
        """Generate standardized commit message"""
        action_map = {
            "created": "add",
            "modified": "update",
            "deleted": "remove"
        }
        action = action_map.get(change_type, "update")
        return f"{action}: {file_path}"

    def _push_changes(self) -> None:
        """Push changes to remote repository"""
        try:
            origin = self.repo.remote("origin")
            origin.push()
            logger.info("Successfully pushed changes to remote")
        except Exception as e:
            logger.error(f"Failed to push changes: {str(e)}")
            raise 