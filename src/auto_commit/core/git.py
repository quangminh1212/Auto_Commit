from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import re
from dataclasses import dataclass
from enum import Enum

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
        
        # Định nghĩa các pattern
        self.test_patterns = [
            r"test_.*\.py$",
            r".*_test\.py$",
            r"tests/.*\.py$"
        ]
        
        self.config_extensions = {
            ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"
        }
        
        self.doc_extensions = {
            ".md", ".rst", ".txt", ".doc", ".docx", ".pdf"
        }
        
        # Mapping commit types
        self.commit_type_mapping = {
            # Python files
            ".py": {
                "created": "feat",
                "modified": "fix",
                "deleted": "refactor"
            },
            # Config files
            ".yaml": {
                "created": "config",
                "modified": "config",
                "deleted": "config"
            },
            # Doc files
            ".md": {
                "created": "docs",
                "modified": "docs",
                "deleted": "docs"
            }
        }

    def add_change(self, file_path: str, change_type: ChangeType) -> None:
        path = Path(file_path)
        
        change = FileChange(
            path=path,
            type=change_type,
            time=datetime.now(),
            extension=path.suffix.lower(),
            is_test=any(re.match(pattern, str(path)) for pattern in self.test_patterns),
            is_config=path.suffix.lower() in self.config_extensions,
            is_doc=path.suffix.lower() in self.doc_extensions
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

    def generate_commit_messages(self) -> List[str]:
        """Tạo commit messages thông minh"""
        messages = []
        groups = self.analyze_changes()
        
        for group_type, changes in groups.items():
            if not changes:
                continue
                
            # Xác định prefix
            if group_type == "test":
                prefix = "test"
            elif group_type == "config":
                prefix = "config"
            elif group_type == "docs":
                prefix = "docs"
            else:
                # Lấy type phổ biến nhất trong nhóm
                type_counts = {}
                for change in changes:
                    change_type = self.commit_type_mapping.get(
                        change.extension, {}
                    ).get(change.type.value, "chore")
                    type_counts[change_type] = type_counts.get(change_type, 0) + 1
                
                prefix = max(type_counts.items(), key=lambda x: x[1])[0]
            
            # Tạo mô tả chi tiết
            if len(changes) == 1:
                change = changes[0]
                action = "add" if change.type == ChangeType.CREATED else \
                        "update" if change.type == ChangeType.MODIFIED else "remove"
                detail = f"{action} {change.path.name}"
            else:
                # Nhóm các hành động
                actions = {c.type for c in changes}
                if len(actions) == 1:
                    action = next(iter(actions)).value
                    detail = f"bulk {action} {len(changes)} {group_type} files"
                else:
                    detail = f"update multiple {group_type} files"
            
            # Tạo commit message
            message = f"{prefix}: {detail}"
            
            # Thêm scope nếu cần
            if any(c.is_test for c in changes):
                message = f"{prefix}(test): {detail}"
            
            # Thêm breaking change nếu có file bị xóa
            if any(c.type == ChangeType.DELETED for c in changes):
                message += "\n\nBREAKING CHANGE: Some files were deleted"
            
            messages.append(message)
        
        return messages

    def clear(self):
        """Xóa tất cả thay đổi đã phân tích"""
        self.changes.clear() 