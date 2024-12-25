import sys
from pathlib import Path

# Thêm thư mục src vào PYTHONPATH
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from auto_commit.core.watcher import FileWatcher
from auto_commit.config.settings import load_config

def main():
    try:
        # Load config
        config_path = Path("config/settings.yaml")
        if not config_path.exists():
            # Tạo config mặc định nếu chưa có
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w") as f:
                f.write("""
# Repository settings
repo_path: "."
watch_path: "."
github_token: ""

# Commit settings
commit_delay: 30
""")
        
        # Khởi tạo và chạy watcher
        config = load_config(config_path)
        watcher = FileWatcher(config)
        watcher.start()
        
    except KeyboardInterrupt:
        print("\nStopping application...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 