@echo off
echo Building Auto Commit with Copilot installer...
echo.

REM Di chuyển đến thư mục extension
cd extension

REM Biên dịch TypeScript
echo Đang biên dịch TypeScript...
call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo Không thể biên dịch TypeScript. Vui lòng kiểm tra lại cài đặt.
    cd ..
    pause
    exit /b 1
)

REM Đóng gói extension
echo Đang đóng gói extension...
call npx @vscode/vsce package
if %ERRORLEVEL% NEQ 0 (
    echo Không thể đóng gói extension. Vui lòng kiểm tra lại cài đặt.
    cd ..
    pause
    exit /b 1
)

REM Trở về thư mục gốc
cd ..

REM Kiểm tra xem Inno Setup đã được cài đặt chưa
where iscc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Inno Setup không được tìm thấy. Vui lòng cài đặt Inno Setup trước.
    echo Bạn có thể tải Inno Setup từ: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

REM Tạo file exe
echo Đang tạo file exe...
iscc create-installer.iss
if %ERRORLEVEL% NEQ 0 (
    echo Không thể tạo file exe. Vui lòng kiểm tra lại cài đặt.
    pause
    exit /b 1
)

echo.
echo File exe đã được tạo thành công!
echo Bạn có thể tìm thấy file exe tại: %CD%\Auto-Commit-Installer.exe
echo.
pause 