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
        # Mở rộng patterns để nhận diện ý nghĩa thay đổi
        self.semantic_patterns = {
            # Feature patterns
            'feat': {
                'patterns': [r'add', r'new', r'create', r'implement'],
                'contexts': ['component', 'feature', 'function', 'api'],
                'importance': 'major'
            },
            
            # Bug fix patterns  
            'fix': {
                'patterns': [r'fix', r'resolve', r'bug', r'issue', r'error'],
                'contexts': ['crash', 'exception', 'invalid', 'incorrect'],
                'importance': 'critical'
            },
            
            # UI/UX patterns
            'style': {
                'patterns': [r'style', r'ui', r'ux', r'design', r'layout'],
                'contexts': ['visual', 'interface', 'experience', 'responsive'],
                'importance': 'minor'
            },
            
            # Code quality patterns
            'refactor': {
                'patterns': [r'refactor', r'restructure', r'optimize', r'clean'],
                'contexts': ['performance', 'maintainability', 'readability'],
                'importance': 'medium'
            },
            
            # Documentation patterns
            'docs': {
                'patterns': [r'doc', r'comment', r'guide', r'readme'],
                'contexts': ['explanation', 'example', 'usage', 'api'],
                'importance': 'minor'
            }
        }

        # Phân tích impact chi tiết hơn
        self.impact_analysis = {
            'breaking_changes': {
                'patterns': [r'api', r'interface', r'contract', r'schema'],
                'warning_level': 'high',
                'requires_attention': True
            },
            'security': {
                'patterns': [r'auth', r'security', r'crypto', r'password'],
                'warning_level': 'critical',
                'requires_review': True
            },
            'performance': {
                'patterns': [r'optimize', r'performance', r'speed', r'memory'],
                'warning_level': 'medium',
                'needs_testing': True
            },
            'dependencies': {
                'patterns': [r'dependency', r'package', r'version', r'upgrade'],
                'warning_level': 'medium',
                'needs_testing': True
            }
        }

    def analyze_semantic_meaning(self, files: List[Path], changes: List[str]) -> Dict:
        """Phân tích ý nghĩa ngữ nghĩa của thay đổi"""
        content = ' '.join([str(f) for f in files] + changes).lower()
        meanings = []
        
        for type_name, type_info in self.semantic_patterns.items():
            if any(re.search(pattern, content) for pattern in type_info['patterns']):
                if any(context in content for context in type_info['contexts']):
                    meanings.append({
                        'type': type_name,
                        'importance': type_info['importance'],
                        'contexts': [ctx for ctx in type_info['contexts'] if ctx in content]
                    })
        
        return meanings

    def analyze_detailed_impact(self, files: List[Path], changes: List[str]) -> Dict:
        """Phân tích chi tiết tác động của thay đổi"""
        content = ' '.join([str(f) for f in files] + changes).lower()
        impacts = {}
        
        for impact_type, impact_info in self.impact_analysis.items():
            if any(re.search(pattern, content) for pattern in impact_info['patterns']):
                impacts[impact_type] = {
                    'warning_level': impact_info['warning_level'],
                    'requires_attention': impact_info.get('requires_attention', False),
                    'requires_review': impact_info.get('requires_review', False),
                    'needs_testing': impact_info.get('needs_testing', False)
                }
        
        return impacts

    def build_semantic_message(self, meanings: List[Dict], impacts: Dict) -> str:
        """Tạo commit message với ý nghĩa ngữ nghĩa"""
        if not meanings:
            return "chore: routine changes"

        # Lấy meaning quan trọng nhất
        primary_meaning = max(meanings, key=lambda m: {
            'critical': 3,
            'major': 2,
            'medium': 1,
            'minor': 0
        }[m['importance']])

        # Tạo header
        message = [f"{primary_meaning['type']}: "]
        
        # Thêm scope nếu có contexts
        if primary_meaning['contexts']:
            message[0] += f"({','.join(primary_meaning['contexts'])}) "

        # Thêm mô tả ngắn gọn
        message[0] += self._generate_description(primary_meaning, impacts)

        # Thêm chi tiết impacts
        if impacts:
            message.extend(["", "Impact:"])
            for impact_type, impact_info in impacts.items():
                details = []
                if impact_info['requires_attention']:
                    details.append("requires attention")
                if impact_info['requires_review']:
                    details.append("needs security review")
                if impact_info['needs_testing']:
                    details.append("requires testing")
                
                message.append(f"- {impact_type.replace('_', ' ').title()}: "
                             f"{', '.join(details)}")

        return '\n'.join(message)

    def _generate_description(self, meaning: Dict, impacts: Dict) -> str:
        """Tạo mô tả có ý nghĩa dựa trên phân tích"""
        desc = []
        
        # Thêm action từ type
        action_map = {
            'feat': 'add new',
            'fix': 'resolve',
            'style': 'improve',
            'refactor': 'optimize',
            'docs': 'update'
        }
        desc.append(action_map.get(meaning['type'], 'update'))

        # Thêm contexts
        if meaning['contexts']:
            desc.append(' and '.join(meaning['contexts']))

        # Thêm warning nếu có high-impact changes
        if any(i['warning_level'] == 'critical' for i in impacts.values()):
            desc.append("(CRITICAL)")
        elif any(i['warning_level'] == 'high' for i in impacts.values()):
            desc.append("(BREAKING)")

        return ' '.join(desc) 

    def analyze_changes(self, changes: List[tuple]) -> CommitDetails:
        """Phân tích các thay đổi và tạo commit details"""
        # Tách files và types
        files = [Path(f) for f, _ in changes]
        types = [t for _, t in changes]
        
        # Phân tích ngữ nghĩa
        meanings = self.analyze_semantic_meaning(files, types)
        
        # Phân tích impacts
        impacts = self.analyze_detailed_impact(files, types)
        
        # Xác định type và scope chính
        if meanings:
            primary_meaning = max(meanings, key=lambda m: {
                'critical': 3, 'major': 2, 'medium': 1, 'minor': 0
            }[m['importance']])
            commit_type = primary_meaning['type']
            scope = ','.join(primary_meaning['contexts']) if primary_meaning['contexts'] else ''
        else:
            commit_type = 'chore'
            scope = ''

        # Tạo subject
        subject = self._create_subject(files, types)
        
        # Tạo danh sách changes
        detailed_changes = [
            f"{self._get_action_verb(t)} {f}" 
            for f, t in changes
        ]
        
        # Tạo danh sách impacts
        impact_notes = []
        for impact_type, impact_info in impacts.items():
            details = []
            if impact_info['requires_attention']:
                details.append("requires attention")
            if impact_info['requires_review']:
                details.append("needs security review")
            if impact_info['needs_testing']:
                details.append("requires testing")
            
            if details:
                impact_notes.append(
                    f"{impact_type.replace('_', ' ').title()}: {', '.join(details)}"
                )

        # Tạo notes
        notes = self._create_notes(files, types)
        
        # Kiểm tra breaking changes
        breaking = any(
            i['warning_level'] in ['critical', 'high'] 
            for i in impacts.values()
        )
        
        return CommitDetails(
            type=commit_type,
            scope=scope,
            subject=subject,
            changes=detailed_changes,
            impacts=impact_notes,
            notes=notes,
            breaking=breaking
        )

    def _get_action_verb(self, change_type: str) -> str:
        """Trả về động từ mô tả hành động"""
        return {
            'CREATED': 'Add',
            'MODIFIED': 'Update',
            'DELETED': 'Remove'
        }.get(change_type, 'Update')

    def _create_subject(self, files: List[Path], types: List[str]) -> str:
        """Tạo subject line cho commit"""
        if len(files) == 1:
            action = self._get_action_verb(types[0])
            return f"{action.lower()} {files[0].name}"
        
        categories = set(self._get_file_category(f) for f in files)
        if len(categories) == 1:
            category = next(iter(categories))
            return f"update {len(files)} {category} files"
        
        return f"update {len(files)} files across {len(categories)} categories"

    def _get_file_category(self, file: Path) -> str:
        """Xác định category của file"""
        if 'test' in str(file).lower():
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