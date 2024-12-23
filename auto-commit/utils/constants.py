from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "settings.yaml"

# Git related
IGNORE_PATTERNS = [
    ".git",
    "__pycache__",
    ".pyc",
    ".swp",
    ".venv",
    "venv",
    ".env",
    ".idea",
    ".vscode"
]

# Commit related
DEFAULT_COMMIT_DELAY = 30