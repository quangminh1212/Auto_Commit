@echo off
echo === Auto Commit Tool - Test and Optimize ===
echo.

REM Kiểm tra xem Python đã được cài đặt chưa
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Lỗi: Python chưa được cài đặt. Vui lòng cài đặt Python trước khi chạy script này.
    exit /b 1
)

REM Kiểm tra xem Git đã được cài đặt chưa
git --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Lỗi: Git chưa được cài đặt. Vui lòng cài đặt Git trước khi chạy script này.
    exit /b 1
)

REM Cài đặt các thư viện cần thiết
echo Đang cài đặt các thư viện cần thiết...
pip install -r requirements.txt

REM Chạy test và tối ưu
echo.
echo Đang chạy test và tối ưu...
python test_auto_commit.py

REM Kiểm tra xem API key đã được cấu hình chưa
findstr /C:"YOUR_GEMINI_API_KEY" auto_commit.py > nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Cảnh báo: API key chưa được cấu hình.
    set /p API_KEY=Nhập API key của Gemini (để trống để bỏ qua): 
    
    if not "%API_KEY%"=="" (
        echo Đang cập nhật API key...
        powershell -Command "(Get-Content auto_commit.py) -replace 'YOUR_GEMINI_API_KEY', '%API_KEY%' | Set-Content auto_commit.py"
        echo API key đã được cập nhật.
    )
)

echo.
echo === Hoàn tất test và tối ưu ===
echo Bạn có thể chạy auto_commit.bat để sử dụng công cụ.
echo. 