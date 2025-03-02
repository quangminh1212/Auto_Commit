@echo off
echo Setting up tools for Auto Commit with Copilot...
echo.

REM Kiểm tra xem Node.js đã được cài đặt chưa
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js không được tìm thấy. Vui lòng cài đặt Node.js trước.
    echo Bạn có thể tải Node.js từ: https://nodejs.org/
    pause
    exit /b 1
)

REM Kiểm tra xem npm đã được cài đặt chưa
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo npm không được tìm thấy. Vui lòng cài đặt Node.js trước.
    echo Bạn có thể tải Node.js từ: https://nodejs.org/
    pause
    exit /b 1
)

REM Cài đặt vsce
echo Đang cài đặt vsce...
call npm install -g @vscode/vsce
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt vsce. Vui lòng thử lại sau.
    pause
    exit /b 1
)

REM Kiểm tra xem Inno Setup đã được cài đặt chưa
where iscc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Inno Setup không được tìm thấy.
    echo Bạn có muốn tải Inno Setup không? (Y/N)
    set /p download=
    if /i "%download%" EQU "Y" (
        echo Vui lòng tải và cài đặt Inno Setup từ: https://jrsoftware.org/isdl.php
        start https://jrsoftware.org/isdl.php
    )
)

REM Cài đặt dependencies cho extension
echo Đang cài đặt dependencies cho extension...
cd extension
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt dependencies cho extension. Vui lòng thử lại sau.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo Các công cụ đã được cài đặt thành công!
echo Bây giờ bạn có thể chạy build-installer.bat để tạo file exe.
echo.
pause 