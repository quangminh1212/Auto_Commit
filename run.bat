@echo off
echo Starting Auto Commit...

REM Kiểm tra môi trường ảo
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate môi trường ảo
call venv\Scripts\activate.bat 

REM Kiểm tra và cài đặt dependencies
pip install -e . 2>nul

REM Chạy chương trình
echo Starting application...
python run.py

REM Deactivate môi trường ảo khi đóng chương trình
call venv\Scripts\deactivate.bat

pause 