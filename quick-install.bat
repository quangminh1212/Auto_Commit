@echo off
echo Quick Install Auto Commit with Copilot extension...
echo.

REM Kiểm tra xem VS Code đã được cài đặt chưa
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo VS Code không được tìm thấy. Vui lòng cài đặt VS Code trước.
    echo Bạn có thể tải VS Code từ: https://code.visualstudio.com/download
    pause
    exit /b 1
)

REM Kiểm tra xem file VSIX đã tồn tại chưa
if not exist "extension\auto-commit-copilot-0.0.1.vsix" (
    echo File VSIX không tồn tại. Đang tạo file VSIX...
    call package-extension.bat
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
pause 