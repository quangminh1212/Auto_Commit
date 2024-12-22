import os
import sys

# Thêm thư mục src vào PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main() 