from pathlib import Path
from typing import Dict, List, Optional, Set
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

    def _determine_primary_type(self, files: List[Path], types: List[str]) -> str:
        """Xác định loại commit chính dựa trên các thay đổi"""
        content = ' '.join([str(f) for f in files] + types).lower()
        
        # Đếm số lần xuất hiện của mỗi loại
        type_scores = {}
        for commit_type, info in self.change_patterns.items():
            score = sum(1 for pattern in info['patterns'] 
                       if any(re.search(pattern, content)))
            if score > 0:
                type_scores[commit_type] = {
                    'score': score,
                    'importance': info['importance']
                }
        
        if not type_scores:
            return 'chore'
            
        # Ưu tiên theo importance và score
        importance_levels = {
            'critical': 4,
            'major': 3,
            'medium': 2,
            'minor': 1
        }
        
        return max(type_scores.items(),
                  key=lambda x: (importance_levels[x[1]['importance']], 
                               x[1]['score']))[0]

    def _analyze_scope_and_areas(self, files: List[Path]) -> tuple[str, set]:
        """Phân tích scope và areas bị ảnh hưởng"""
        areas = set()
        components = set()
        
        for file in files:
            file_str = str(file).lower()
            
            # Xác định technical areas
            for area, patterns in self.technical_areas.items():
                if any(re.search(pattern, file_str) for pattern in patterns):
                    areas.add(area)
            
            # Xác định components từ cấu trúc thư mục
            if len(file.parts) > 1:
                components.add(file.parts[0])
        
        # Xác định scope
        if len(components) == 1:
            scope = next(iter(components))
        elif len(areas) == 1:
            scope = next(iter(areas))
        else:
            scope = 'multi'
            
        return scope, areas

    def _create_smart_subject(self, commit_type: str, files: List[Path], 
                            types: List[str], analysis: Dict) -> str:
        """Tạo subject line thông minh"""
        if len(files) == 1:
            file = files[0]
            action = 'add' if 'CREATED' in types else \
                    'remove' if 'DELETED' in types else 'update'
            
            if analysis['importance'] == 'critical':
                return f"{action} critical {file.name}"
            return f"{action} {file.name}"
        
        # Nhóm theo loại file
        file_types = set()
        for file in files:
            for area, patterns in self.technical_areas.items():
                if any(re.search(pattern, str(file)) for pattern in patterns):
                    file_types.add(area)
                    break
        
        if len(file_types) == 1:
            area = next(iter(file_types))
            return f"update {len(files)} {area} files"
            
        return f"update {len(files)} files across {len(file_types)} areas"

    def _analyze_detailed_changes(self, files: List[Path], types: List[str], 
                                analysis: Dict) -> List[str]:
        """Phân tích chi tiết từng thay đổi"""
        changes = []
        for file, change_type in zip(files, types):
            action = {
                'CREATED': 'Add',
                'MODIFIED': 'Update',
                'DELETED': 'Remove'
            }[change_type]
            
            # Thêm context
            context = []
            file_str = str(file).lower()
            
            for area, patterns in self.technical_areas.items():
                if any(re.search(pattern, file_str) for pattern in patterns):
                    context.append(area)
            
            if context:
                changes.append(f"{action} {file} ({', '.join(context)})")
            else:
                changes.append(f"{action} {file}")
        
        return changes

    def _analyze_impacts(self, analysis: Dict) -> List[str]:
        """Phân tích impacts của các thay đổi"""
        impacts = []
        
        if analysis['has_breaking_changes']:
            impacts.append("Breaking changes detected - requires attention")
            
        if analysis['security_impact']:
            impacts.append("Security-related changes - review required")
            
        if analysis['database_changes']:
            impacts.append("Database changes - migration may be needed")
            
        if analysis['dependencies_changed']:
            impacts.append("Dependencies modified - update required")
            
        if analysis['performance_impact']:
            impacts.append("Performance impact - testing recommended")
            
        if analysis['api_changes']:
            impacts.append("API changes - update documentation")
            
        return impacts

    def _create_technical_notes(self, analysis: Dict) -> List[str]:
        """Tạo technical notes cho commit"""
        notes = []
        
        if analysis['testing_required']:
            notes.append("Run full test suite")
            
        if analysis['review_priority'] == 'high':
            notes.append("High-priority review required")
            
        if analysis['complexity'] == 'high':
            notes.append("Complex changes - careful review needed")
            
        if analysis['risk_level'] == 'high':
            notes.append("High-risk changes - thorough testing required")
            
        return notes

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
    breaking: bool
    importance: str = 'minor'
    affected_areas: Set[str] = None
    technical_details: Dict = None

    def __post_init__(self):
        if self.affected_areas is None:
            self.affected_areas = set()
        if self.technical_details is None:
            self.technical_details = {}

class CommitMessageBuilder:
    def __init__(self):
        self.change_patterns = {
            'feat': {
                'patterns': [r'add', r'new', r'create', r'implement'],
                'importance': 'major',
                'description': 'New feature or functionality'
            },
            'fix': {
                'patterns': [r'fix', r'resolve', r'bug', r'issue', r'error', r'crash'],
                'importance': 'critical',
                'description': 'Bug fix or error resolution'
            },
            'refactor': {
                'patterns': [r'refactor', r'restructure', r'optimize', r'improve'],
                'importance': 'medium',
                'description': 'Code refactoring or optimization'
            },
            'style': {
                'patterns': [r'style', r'format', r'ui', r'design', r'css'],
                'importance': 'minor',
                'description': 'UI/UX or code style changes'
            },
            'docs': {
                'patterns': [r'doc', r'comment', r'readme', r'guide'],
                'importance': 'minor',
                'description': 'Documentation updates'
            }
        }

        self.technical_areas = {
            'frontend': [r'\.vue', r'\.jsx?', r'\.tsx?', r'\.css', r'\.scss', r'\.html'],
            'backend': [r'\.py', r'\.go', r'\.java', r'\.php', r'api', r'server'],
            'database': [r'model', r'migration', r'schema', r'\.sql'],
            'testing': [r'test', r'spec', r'mock', r'fixture'],
            'config': [r'\.env', r'\.yml', r'\.json', r'config', r'setting'],
            'security': [r'auth', r'security', r'crypto', r'password', r'token'],
            'ci_cd': [r'github/workflows', r'gitlab-ci', r'jenkins', r'docker'],
            'dependencies': [r'requirements\.txt', r'package\.json', r'go\.mod']
        }

    def analyze_changes(self, changes: List[tuple]) -> CommitDetails:
        """Phân tích sâu về các thay đổi để tạo commit thông minh"""
        files = [Path(f) for f, _ in changes]
        types = [t for _, t in changes]
        
        # Phân tích kỹ thuật
        tech_analysis = self._analyze_technical_aspects(files, types)
        
        # Xác định loại thay đổi chính
        commit_type = self._determine_primary_type(files, types)
        
        # Phân tích scope và affected areas
        scope, areas = self._analyze_scope_and_areas(files)
        
        # Tạo subject line thông minh
        subject = self._create_smart_subject(commit_type, files, types, tech_analysis)
        
        # Phân tích chi tiết changes
        detailed_changes = self._analyze_detailed_changes(files, types, tech_analysis)
        
        # Phân tích impacts
        impacts = self._analyze_impacts(tech_analysis)
        
        # Tạo technical notes
        notes = self._create_technical_notes(tech_analysis)
        
        return CommitDetails(
            type=commit_type,
            scope=scope,
            subject=subject,
            changes=detailed_changes,
            impacts=impacts,
            notes=notes,
            breaking=tech_analysis['has_breaking_changes'],
            importance=tech_analysis['importance'],
            affected_areas=areas,
            technical_details=tech_analysis
        )

    def _analyze_technical_aspects(self, files: List[Path], types: List[str]) -> Dict:
        """Phân tích chi tiết kỹ thuật của các thay đổi"""
        analysis = {
            'areas': set(),
            'has_breaking_changes': False,
            'importance': 'minor',
            'complexity': 'low',
            'risk_level': 'low',
            'testing_required': False,
            'review_priority': 'normal',
            'dependencies_changed': False,
            'security_impact': False,
            'performance_impact': False,
            'database_changes': False,
            'api_changes': False
        }

        for file in files:
            file_str = str(file).lower()
            
            # Phân tích technical areas
            for area, patterns in self.technical_areas.items():
                if any(re.search(pattern, file_str) for pattern in patterns):
                    analysis['areas'].add(area)

            # Phân tích mức độ quan trọng và rủi ro
            if any(term in file_str for term in ['api', 'auth', 'security', 'core']):
                analysis['importance'] = 'critical'
                analysis['risk_level'] = 'high'
                analysis['review_priority'] = 'high'

            # Kiểm tra breaking changes
            if 'DELETED' in types or any(term in file_str for term in ['api', 'interface', 'contract']):
                analysis['has_breaking_changes'] = True

            # Phân tích dependencies
            if any(term in file_str for term in ['requirements.txt', 'package.json', 'go.mod']):
                analysis['dependencies_changed'] = True

            # Phân tích security
            if any(term in file_str for term in ['auth', 'security', 'crypto', 'password']):
                analysis['security_impact'] = True
                analysis['review_priority'] = 'high'

            # Phân tích database
            if any(term in file_str for term in ['model', 'migration', 'schema']):
                analysis['database_changes'] = True
                analysis['testing_required'] = True

        return analysis

    def build_message(self, analysis: CommitDetails) -> str:
        """Tạo commit message chi tiết và có ý nghĩa"""
        # Header
        message = [f"{analysis.type}"]
        if analysis.scope:
            message[0] += f"({analysis.scope})"
        message[0] += f": {analysis.subject}"

        # Changes section
        if analysis.changes:
            message.extend(["", "Changes:"])
            message.extend(f"- {change}" for change in analysis.changes)

        # Impact section
        if analysis.impacts:
            message.extend(["", "Impact:"])
            message.extend(f"- {impact}" for impact in analysis.impacts)

        # Technical notes
        if analysis.notes:
            message.extend(["", "Notes:"])
            message.extend(f"- {note}" for note in analysis.notes)

        # Breaking changes warning
        if analysis.breaking:
            message.extend([
                "",
                "BREAKING CHANGE: This commit includes breaking changes that require attention"
            ])

        return '\n'.join(message) 