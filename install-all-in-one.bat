@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo    AUTO COMMIT WITH COPILOT - CÀI ĐẶT TỔNG HỢP
echo ===================================================
echo.

REM Tạo file log
echo Quá trình cài đặt bắt đầu lúc %date% %time% > setup_log.txt

REM Kiểm tra quyền admin
echo Đang kiểm tra quyền admin...
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Vui lòng chạy script này với quyền Administrator để cài đặt các công cụ cần thiết.
    echo Nhấp chuột phải vào install-all-in-one.bat và chọn "Run as administrator".
    pause
    exit /b 1
)

REM Kiểm tra VS Code
echo Đang kiểm tra VS Code...
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo VS Code không được tìm thấy. Vui lòng cài đặt VS Code trước.
    echo Bạn có thể tải VS Code từ: https://code.visualstudio.com/download
    pause
    exit /b 1
)

REM Kiểm tra Node.js
echo Đang kiểm tra Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js không được tìm thấy. Vui lòng cài đặt Node.js trước.
    echo Bạn có thể tải Node.js từ: https://nodejs.org/
    pause
    exit /b 1
)

REM Kiểm tra npm
echo Đang kiểm tra npm...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo npm không được tìm thấy. Vui lòng cài đặt Node.js (bao gồm npm) trước.
    echo Bạn có thể tải Node.js từ: https://nodejs.org/
    pause
    exit /b 1
)

REM Kiểm tra xem extension đã được cài đặt chưa
echo Đang kiểm tra extension hiện tại...
code --list-extensions | findstr "undefined_publisher.auto-commit-copilot" >nul
if %ERRORLEVEL% EQU 0 (
    echo Extension Auto Commit với Copilot đã được cài đặt.
    echo Bạn có muốn cài đặt lại không? (Y/N)
    set /p reinstall=
    if /i "!reinstall!" NEQ "Y" (
        echo Cài đặt đã bị hủy.
        pause
        exit /b 0
    )
)

REM Kiểm tra thư mục extension
echo Đang kiểm tra thư mục extension...
if not exist "extension" (
    echo Thư mục extension không tìm thấy. Vui lòng đảm bảo bạn đang chạy script này từ đúng vị trí.
    pause
    exit /b 1
)

REM Cài đặt vsce
echo.
echo === Đang cài đặt vsce ===
echo Đang cài đặt vsce...
call npm install -g @vscode/vsce
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt vsce. Vui lòng thử lại sau.
    pause
    exit /b 1
)

REM Cài đặt dependencies cho extension
echo.
echo === Đang cài đặt dependencies cho extension ===
cd extension
echo Đang cài đặt dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt dependencies. Vui lòng thử lại sau.
    cd ..
    pause
    exit /b 1
)

REM Biên dịch TypeScript
echo.
echo === Đang biên dịch TypeScript ===
echo Đang biên dịch TypeScript...
call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo Không thể biên dịch TypeScript. Vui lòng kiểm tra lỗi và thử lại.
    cd ..
    pause
    exit /b 1
)

REM Đóng gói extension
echo.
echo === Đang đóng gói extension ===
echo Đang đóng gói extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license
if %ERRORLEVEL% NEQ 0 (
    echo Không thể đóng gói extension. Vui lòng kiểm tra lỗi và thử lại.
    cd ..
    pause
    exit /b 1
)

REM Quay lại thư mục gốc
cd ..

REM Cài đặt extension
echo.
echo === Đang cài đặt extension vào VS Code ===
echo Đang cài đặt extension...
code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt extension. Vui lòng thử lại sau.
    pause
    exit /b 1
)

echo.
echo === Cài đặt hoàn tất ===
echo.
echo Extension đã được cài đặt thành công!
echo Vui lòng khởi động lại VS Code nếu nó đang chạy.
echo.
echo Để sử dụng extension:
echo 1. Thực hiện các thay đổi trong dự án của bạn
echo 2. Stage các thay đổi bạn muốn commit
echo 3. Nhấn Ctrl+Space để tự động tạo commit message và thực hiện commit
echo.
echo Cảm ơn bạn đã sử dụng Auto Commit with Copilot!
echo.
pause 