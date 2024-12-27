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

@dataclass
class CommitDetails:
    type: str
    scope: str
    subject: str
    changes: List[str]
    impacts: List[str]
    notes: List[str]
    breaking: bool = False

class CommitMessageBuilder:
    def __init__(self):
        self.type_patterns = {
            'feat': [r'add', r'new', r'implement', r'create'],
            'fix': [r'fix', r'resolve', r'bug', r'issue', r'error'],
            'refactor': [r'refactor', r'restructure', r'optimize', r'clean'],
            'style': [r'style', r'format', r'ui', r'css', r'design'],
            'docs': [r'doc', r'comment', r'readme', r'guide'],
            'test': [r'test', r'spec', r'coverage'],
            'chore': [r'chore', r'maintenance', r'config', r'build']
        }
        
        self.impact_patterns = {
            'security': [r'auth', r'password', r'crypto', r'secret', r'secure'],
            'database': [r'database', r'migration', r'schema', r'model', r'db'],
            'api': [r'api', r'endpoint', r'route', r'controller', r'service'],
            'ui': [r'component', r'view', r'template', r'style', r'layout'],
            'performance': [r'performance', r'optimize', r'speed', r'cache'],
            'dependencies': [r'dependency', r'package', r'requirement', r'module']
        }

    def analyze_changes(self, changes: List[tuple]) -> CommitDetails:
        """Phân tích chi tiết các thay đổi và tạo commit message"""
        # Phân tích các files
        files = [Path(f) for f, _ in changes]
        types = [t for _, t in changes]
        
        # Xác định commit type và scope
        commit_type = self._determine_commit_type(files, types)
        scope = self._determine_scope(files)
        
        # Tạo subject
        subject = self._create_subject(files, types)
        
        # Phân tích chi tiết changes
        detailed_changes = self._analyze_detailed_changes(files, types)
        
        # Phân tích impacts
        impacts = self._analyze_impacts(files, types)
        
        # Tạo notes
        notes = self._create_notes(files, types)
        
        # Kiểm tra breaking changes
        breaking = self._has_breaking_changes(files, types)
        
        return CommitDetails(
            type=commit_type,
            scope=scope,
            subject=subject,
            changes=detailed_changes,
            impacts=impacts,
            notes=notes,
            breaking=breaking
        )

    def _determine_commit_type(self, files: List[Path], types: List[str]) -> str:
        """Xác định loại commit dựa trên các thay đổi"""
        content = ' '.join([str(f) for f in files] + types).lower()
        
        for commit_type, patterns in self.type_patterns.items():
            if any(re.search(pattern, content) for pattern in patterns):
                return commit_type
        
        return 'chore'

    def _determine_scope(self, files: List[Path]) -> str:
        """Xác định scope của commit"""
        components = set()
        for file in files:
            parts = file.parts
            if len(parts) > 1:
                components.add(parts[0])
        
        if len(components) == 1:
            return next(iter(components))
        elif len(components) > 1:
            return 'multi'
        return ''

    def _create_subject(self, files: List[Path], types: List[str]) -> str:
        """Tạo subject line cho commit"""
        if len(files) == 1:
            action = 'add' if 'CREATED' in types else \
                    'remove' if 'DELETED' in types else 'update'
            return f"{action} {files[0].name}"
        
        return f"update {len(files)} files"

    def _analyze_detailed_changes(self, files: List[Path], types: List[str]) -> List[str]:
        """Phân tích chi tiết từng thay đổi"""
        changes = []
        for file, change_type in zip(files, types):
            action = {
                'CREATED': 'Add',
                'MODIFIED': 'Update',
                'DELETED': 'Remove'
            }[change_type]
            
            # Thêm context cho mỗi thay đổi
            context = self._get_file_context(file)
            changes.append(f"{action} {file} ({context})")
        
        return changes

    def _analyze_impacts(self, files: List[Path], types: List[str]) -> List[str]:
        """Phân tích ảnh hưởng của các thay đổi"""
        impacts = set()
        content = ' '.join([str(f) for f in files]).lower()
        
        for impact_type, patterns in self.impact_patterns.items():
            if any(re.search(pattern, content) for pattern in patterns):
                impacts.add(f"{impact_type.title()} changes detected")
        
        if 'DELETED' in types:
            impacts.add("Breaking changes: files were deleted")
            
        return sorted(list(impacts))

    def _create_notes(self, files: List[Path], types: List[str]) -> List[str]:
        """Tạo các ghi chú bổ sung"""
        notes = []
        
        # Kiểm tra dependencies
        if any(f.name in ['requirements.txt', 'package.json', 'go.mod'] for f in files):
            notes.append("Remember to update dependencies")
            
        # Kiểm tra database
        if any('migration' in str(f) for f in files):
            notes.append("Database migration required")
            
        # Kiểm tra tests
        if any('test' in str(f) for f in files):
            notes.append("Run tests before deploying")
            
        return notes

    def _has_breaking_changes(self, files: List[Path], types: List[str]) -> bool:
        """Kiểm tra có breaking changes không"""
        return 'DELETED' in types or \
               any(f.name in ['api.py', 'schema.py', 'models.py'] for f in files)

    def _get_file_context(self, file: Path) -> str:
        """Lấy context của file"""
        if 'test' in str(file):
            return 'test'
        elif file.suffix in ['.py', '.js', '.ts']:
            return 'source'
        elif file.suffix in ['.css', '.scss', '.html']:
            return 'ui'
        elif file.suffix in ['.md', '.rst']:
            return 'docs'
        elif file.suffix in ['.json', '.yaml', '.yml']:
            return 'config'
        return 'other'

    def build_message(self, details: CommitDetails) -> str:
        """Tạo commit message hoàn chỉnh"""
        # Header
        message = [f"{details.type}"]
        if details.scope:
            message[0] += f"({details.scope})"
        message[0] += f": {details.subject}"
        
        # Body
        if details.changes:
            message.extend(["", "Changes:"])
            message.extend(f"- {change}" for change in details.changes)
            
        # Impacts
        if details.impacts:
            message.extend(["", "Impact:"])
            message.extend(f"- {impact}" for impact in details.impacts)
            
        # Notes
        if details.notes:
            message.extend(["", "Notes:"])
            message.extend(f"- {note}" for note in details.notes)
            
        # Breaking changes
        if details.breaking:
            message.extend(["", "BREAKING CHANGE: This commit includes breaking changes"])
            
        return '\n'.join(message) 