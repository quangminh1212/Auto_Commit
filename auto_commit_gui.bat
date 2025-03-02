@echo off
echo === Auto Commit GUI ===
echo Dang khoi dong ung dung...

REM Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Loi: Python khong duoc cai dat hoac khong co trong PATH.
    echo Vui long cai dat Python tu https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Kiem tra va cai dat cac thu vien can thiet
echo Dang kiem tra cac thu vien can thiet...
pip install -r requirements.txt >nul 2>&1

REM Chay ung dung
python auto_commit_gui.py

if %errorlevel% neq 0 (
    echo Loi khi chay ung dung. Vui long kiem tra log de biet them chi tiet.
    pause
)

exit /b 0 