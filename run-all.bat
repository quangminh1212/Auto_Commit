@echo off
echo Chạy tất cả các bước để cài đặt công cụ, đóng gói và cài đặt extension...
echo.

REM Cài đặt công cụ
echo === Bước 1: Cài đặt công cụ ===
call setup-tools.bat
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt công cụ. Vui lòng kiểm tra lỗi và thử lại.
    pause
    exit /b 1
)
echo.

REM Đóng gói extension
echo === Bước 2: Đóng gói extension ===
call package-extension.bat
if %ERRORLEVEL% NEQ 0 (
    echo Không thể đóng gói extension. Vui lòng kiểm tra lỗi và thử lại.
    pause
    exit /b 1
)
echo.

REM Tạo file cài đặt
echo === Bước 3: Tạo file cài đặt ===
call build-installer.bat
if %ERRORLEVEL% NEQ 0 (
    echo Không thể tạo file cài đặt. Vui lòng kiểm tra lỗi và thử lại.
    pause
    exit /b 1
)
echo.

REM Hỏi người dùng có muốn cài đặt extension không
set /p install=Bạn có muốn cài đặt extension không? (y/n): 
if /i "%install%"=="y" (
    echo === Bước 4: Cài đặt extension ===
    call quick-install.bat
    if %ERRORLEVEL% NEQ 0 (
        echo Không thể cài đặt extension. Vui lòng kiểm tra lỗi và thử lại.
        pause
        exit /b 1
    )
)

echo.
echo Tất cả các bước đã hoàn thành!
echo.
echo Các file đã được tạo:
echo - VSIX: extension\auto-commit-copilot-0.0.1.vsix
echo - EXE: Auto-Commit-Installer.exe
echo.
echo Để biết thêm thông tin, vui lòng xem file HƯỚNG_DẪN_SỬ_DỤNG.md
echo.
pause 