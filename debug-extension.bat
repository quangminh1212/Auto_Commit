@echo off
echo Chuẩn bị chạy extension trong chế độ debug...
echo.

REM Kiểm tra xem VS Code đã được cài đặt chưa
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo VS Code không được tìm thấy. Vui lòng cài đặt VS Code trước.
    echo Bạn có thể tải VS Code từ: https://code.visualstudio.com/download
    pause
    exit /b 1
)

REM Kiểm tra xem Node.js đã được cài đặt chưa
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js không được tìm thấy. Vui lòng cài đặt Node.js trước.
    echo Bạn có thể tải Node.js từ: https://nodejs.org/
    pause
    exit /b 1
)

REM Chuyển đến thư mục extension
cd extension

REM Cài đặt dependencies nếu cần
if not exist "node_modules" (
    echo Cài đặt dependencies...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo Không thể cài đặt dependencies. Vui lòng thử lại sau.
        cd ..
        pause
        exit /b 1
    )
)

REM Biên dịch TypeScript
echo Biên dịch TypeScript...
call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo Không thể biên dịch TypeScript. Vui lòng kiểm tra lỗi và thử lại.
    cd ..
    pause
    exit /b 1
)

REM Mở VS Code với extension trong chế độ debug
echo Mở VS Code với extension trong chế độ debug...
cd ..
code --disable-extensions --extensionDevelopmentPath="%CD%\extension"

echo.
echo VS Code đã được mở với extension trong chế độ debug.
echo Nhấn F5 trong VS Code để bắt đầu debug extension.
echo.
pause 