#!/bin/bash

echo "=== Auto Commit GUI ==="
echo "Dang khoi dong ung dung..."

# Kiem tra Python
if ! command -v python3 &> /dev/null; then
    echo "Loi: Python khong duoc cai dat hoac khong co trong PATH."
    echo "Vui long cai dat Python tu https://www.python.org/downloads/"
    exit 1
fi

# Kiem tra va cai dat cac thu vien can thiet
echo "Dang kiem tra cac thu vien can thiet..."
python3 -m pip install -r requirements.txt

# Chay ung dung
python3 auto_commit_gui.py

if [ $? -ne 0 ]; then
    echo "Loi khi chay ung dung. Vui long kiem tra log de biet them chi tiet."
fi

exit 0 