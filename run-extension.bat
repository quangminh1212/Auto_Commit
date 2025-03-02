@echo off
echo Chuẩn bị chạy extension Auto Commit với Copilot...
echo.

REM Kiểm tra xem VS Code đã được cài đặt chưa
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo VS Code không được tìm thấy. Vui lòng cài đặt VS Code trước.
    echo Bạn có thể tải VS Code từ: https://code.visualstudio.com/download
    pause
    exit /b 1
)

REM Kiểm tra xem VSIX file đã tồn tại chưa
if not exist "extension\auto-commit-copilot-0.0.1.vsix" (
    echo VSIX file không tồn tại. Đang tạo VSIX file...
    call package-extension.bat
    if %ERRORLEVEL% NEQ 0 (
        echo Không thể tạo VSIX file. Vui lòng thử lại sau.
        pause
        exit /b 1
    )
)

REM Cài đặt extension
echo Đang cài đặt extension...
code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt extension. Vui lòng thử lại sau.
    pause
    exit /b 1
)

echo.
echo Extension đã được cài đặt thành công!
echo Vui lòng khởi động lại VS Code nếu nó đang chạy.
echo.
echo Để sử dụng extension:
echo 1. Thực hiện các thay đổi trong dự án của bạn
echo 2. Stage các thay đổi bạn muốn commit
echo 3. Nhấn Ctrl+Space để tự động tạo commit message và thực hiện commit
echo.

REM Hỏi người dùng có muốn mở VS Code không
set /p openVSCode=Bạn có muốn mở VS Code không? (y/n): 
if /i "%openVSCode%"=="y" (
    echo Đang mở VS Code...
    code
)

pause 