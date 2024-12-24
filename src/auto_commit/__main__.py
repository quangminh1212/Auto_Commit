#!/usr/bin/env python3
import sys
from pathlib import Path

# Thêm thư mục src vào PYTHONPATH
src_path = str(Path(__file__).parent.parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from auto_commit.cli import app

def main():
    app()

if __name__ == "__main__":
    main() 