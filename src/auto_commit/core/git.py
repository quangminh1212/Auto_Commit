from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import re
from dataclasses import dataclass
from enum import Enum
from git import Repo
from github import Github

class ChangeType(Enum):
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"

@dataclass
class FileChange:
    path: Path
    type: ChangeType
    time: datetime
    extension: str
    is_test: bool = False
    is_config: bool = False
    is_doc: bool = False

class CommitAnalyzer:
    def __init__(self):
        self.changes: List[FileChange] = []
        
        # Chi tiết hơn về loại file
        self.file_categories = {
            # Frontend
            'frontend': {
                'extensions': {'.js', '.ts', '.jsx', '.tsx', '.vue', '.css', '.scss', '.html'},
                'patterns': [r'src/frontend/.*', r'public/.*', r'static/.*']
            },
            # Backend
            'backend': {
                'extensions': {'.py', '.go', '.java', '.rb'},
                'patterns': [r'src/backend/.*', r'api/.*'] 
            },
            # Database
            'database': {
                'extensions': {'.sql', '.prisma', '.mongodb'},
                'patterns': [r'migrations/.*', r'db/.*']
            },
            # Tests
            'test': {
                'extensions': {'.spec.js', '.test.py'},
                'patterns': [r'test[s]?/.*', r'.*_test\..*', r'.*\.test\..*']
            },
            # Config
            'config': {
                'extensions': {'.json', '.yaml', '.yml', '.toml', '.ini', '.env'},
                'patterns': [r'config/.*', r'settings/.*']
            },
            # Docs
            'docs': {
                'extensions': {'.md', '.rst', '.txt', '.pdf'},
                'patterns': [r'docs/.*', r'README.*', r'CHANGELOG.*']
            },
            # CI/CD
            'ci': {
                'extensions': {'.yml', '.yaml'},
                'patterns': [r'\.github/.*', r'\.gitlab-ci\..*', r'Jenkinsfile']
            }
        }
        
        # Commit type mapping chi tiết hơn
        self.commit_types = {
            'feat': ['new feature', 'add functionality', 'implement'],
            'fix': ['bug fix', 'resolve issue', 'fix error'],
            'refactor': ['reorganize', 'restructure', 'optimize'],
            'style': ['formatting', 'white-space', 'styling'],
            'docs': ['documentation', 'comments', 'explanation'],
            'test': ['testing', 'coverage', 'unit test'],
            'chore': ['maintenance', 'dependencies', 'config']
        }

    def add_change(self, file_path: str, change_type: ChangeType) -> None:

        """Thêm một thay đổi mới để phân tích"""
        path = Path(file_path)
        category = self._get_file_category(str(path))
        
        change = FileChange(
            path=path,  
            type=change_type,
            time=datetime.now(),
            extension=path.suffix.lower(),
            is_test=(category == 'test'),
            is_config=(category == 'config'),
            is_doc=(category == 'docs')
        )
        
        self.changes.append(change)

    def analyze_changes(self) -> Dict[str, List[FileChange]]:
        """Phân tích và nhóm các thay đổi"""
        groups = {}
        
        # Nhóm theo loại file
        for change in self.changes:
            if change.is_test:
                key = "test"
            elif change.is_config:
                key = "config"
            elif change.is_doc:
                key = "docs"
            else:
                key = change.extension.lstrip(".") or "other"
                
            if key not in groups:
                groups[key] = []
            groups[key].append(change)
            
        return groups

    def _get_file_category(self, file_path: str) -> str:
        """Xác định category của file dựa trên extension và pattern"""
        path = str(file_path)
        
        for category, rules in self.file_categories.items():
            # Kiểm tra extension
            if any(path.endswith(ext) for ext in rules['extensions']):
                return category
            
            # Kiểm tra patterns
            if any(re.match(pattern, path) for pattern in rules['patterns']):
                return category
                
        return 'other'

    def _analyze_change_impact(self, changes: List[FileChange]) -> Dict:
        """Phân tích mức độ ảnh hưởng của thay đổi"""
        impact = {
            'breaking': False,
            'scope': set(),
            'components': set(),
            'dependencies_changed': False
        }
        
        for change in changes:
            # Kiểm tra breaking changes
            if change.type == ChangeType.DELETED:
                impact['breaking'] = True
            
            # Xác định scope
            category = self._get_file_category(str(change.path))
            impact['scope'].add(category)
            
            # Xác định components bị ảnh hưởng
            components = re.findall(r'src/([^/]+)/', str(change.path))
            impact['components'].update(components)
            
            # Kiểm tra dependencies
            if any(dep in str(change.path) for dep in ['package.json', 'requirements.txt', 'go.mod']):
                impact['dependencies_changed'] = True
                
        return impact

    def generate_commit_messages(self) -> List[str]:
        """Tạo commit messages chi tiết"""
        if not self.changes:
            return []
            
        # Nhóm changes theo category
        changes_by_category = {}
        for change in self.changes:
            category = self._get_file_category(str(change.path))
            if category not in changes_by_category:
                changes_by_category[category] = []
            changes_by_category[category].append(change)
        
        messages = []
        for category, changes in changes_by_category.items():
            # Phân tích impact
            impact = self._analyze_change_impact(changes)
            
            # Xác định commit type
            if category == 'test':
                commit_type = 'test'
            elif category == 'docs':
                commit_type = 'docs'
            elif category == 'config':
                commit_type = 'chore'
            else:
                commit_type = self._determine_commit_type(changes)
            
            # Tạo scope
            scope = None
            if len(impact['scope']) == 1:
                scope = next(iter(impact['scope']))
            elif impact['components']:
                scope = ','.join(sorted(impact['components']))
            
            # Tạo message chính
            if len(changes) == 1:
                change = changes[0]
                action = self._get_action_verb(change.type)
                subject = f"{action} {change.path.name}"
            else:
                subject = f"update {len(changes)} {category} files"
            
            # Tạo commit message đầy đủ
            message = f"{commit_type}"
            if scope:
                message += f"({scope})"
            message += f": {subject}"
            
            # Thêm body nếu cần
            body = []
            if len(changes) > 1:
                body.append("\nChanges:")
                for change in changes:
                    action = self._get_action_verb(change.type)
                    body.append(f"- {action} {change.path}")
            
            # Thêm breaking change
            if impact['breaking']:
                body.append("\nBREAKING CHANGE: This commit includes file deletions")
            
            # Thêm dependencies notice
            if impact['dependencies_changed']:
                body.append("\nNote: Dependencies were modified")
            
            if body:
                message += '\n' + '\n'.join(body)
            
            messages.append(message)
            
        return messages

    def _determine_commit_type(self, changes: List[FileChange]) -> str:
        """Xác định loại commit dựa trên các thay đổi"""
        if any(c.type == ChangeType.CREATED for c in changes):
            return 'feat'
        elif any(c.type == ChangeType.DELETED for c in changes):
            return 'refactor'
        return 'fix'

    def _get_action_verb(self, change_type: ChangeType) -> str:
        """Trả về động từ mô tả hành động"""
        return {
            ChangeType.CREATED: "add",
            ChangeType.MODIFIED: "update",
            ChangeType.DELETED: "remove"
        }[change_type]

    def clear(self):
        """Xóa tất cả thay đổi đã phân tích"""
        self.changes.clear() 

class GitHandler:
    def __init__(self, repo_path: str, github_token: Optional[str] = None):
        self.repo_path = Path(repo_path)
        self.repo = Repo(self.repo_path)
        self.github = Github(github_token) if github_token else None
        self.analyzer = CommitAnalyzer()
        
    def handle_change(self, file_path: str, change_type: str) -> None:
        """Xử lý thay đổi file và tạo commits"""
        try:
            relative_path = Path(file_path).relative_to(self.repo_path)
            
            # Skip git và cache files
            if self._should_ignore(relative_path):
                return

            # Thêm vào analyzer
            self.analyzer.add_change(str(relative_path), ChangeType(change_type))

            # Add hoặc remove file từ git
            if change_type != "deleted":
                self.repo.index.add([str(relative_path)])
            else:
                self.repo.index.remove([str(relative_path)])

            # Tạo commit messages thông minh
            commit_messages = self.analyzer.generate_commit_messages()
            
            # Tạo commits
            for message in commit_messages:
                self.repo.index.commit(message)
            
            # Push nếu có GitHub token
            if self.github:
                self._push_changes()
                
            # Clear analyzer
            self.analyzer.clear()
                
        except Exception as e:
            print(f"Git operation failed: {str(e)}")
            raise

    def _should_ignore(self, file_path: Path) -> bool:
        """Kiểm tra file có nên bỏ qua không"""
        ignore_patterns = [
            ".git",
            "__pycache__",
            ".pyc",
            ".swp",
            ".vscode",
            ".idea"
        ]
        return any(pattern in str(file_path) for pattern in ignore_patterns)

    def _push_changes(self) -> None:
        """Push changes lên remote repository"""
        try:
            origin = self.repo.remote("origin")
            origin.push()
        except Exception as e:
            print(f"Failed to push changes: {str(e)}")
            raise 