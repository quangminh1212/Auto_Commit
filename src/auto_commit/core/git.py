from pathlib import Path

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