@echo off
echo Gỡ cài đặt extension Auto Commit với Copilot...
echo.

REM Kiểm tra xem VS Code đã được cài đặt chưa
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo VS Code không được tìm thấy. Vui lòng cài đặt VS Code trước.
    echo Bạn có thể tải VS Code từ: https://code.visualstudio.com/download
    pause
    exit /b 1
)

REM Kiểm tra xem extension đã được cài đặt chưa
code --list-extensions | findstr "undefined_publisher.auto-commit-copilot" >nul
if %ERRORLEVEL% NEQ 0 (
    echo Extension Auto Commit với Copilot chưa được cài đặt.
    pause
    exit /b 0
)

REM Gỡ cài đặt extension
echo Đang gỡ cài đặt extension...
code --uninstall-extension undefined_publisher.auto-commit-copilot
if %ERRORLEVEL% NEQ 0 (
    echo Không thể gỡ cài đặt extension. Vui lòng thử lại sau.
    pause
    exit /b 1
)

echo.
echo Extension đã được gỡ cài đặt thành công!
echo Vui lòng khởi động lại VS Code nếu nó đang chạy.
echo.
pause 