@echo off
echo ===================================================
echo    THIẾT LẬP AUTO COMMIT VỚI COPILOT
echo ===================================================
echo.

REM Kiểm tra quyền admin
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Vui lòng chạy script với quyền Administrator để cài đặt các công cụ cần thiết.
    echo Nhấn chuột phải vào file auto-commit-setup.bat và chọn "Run as administrator".
    pause
    exit /b 1
)

REM Kiểm tra xem VS Code đã được cài đặt chưa
where code >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo VS Code không được tìm thấy. Vui lòng cài đặt VS Code trước.
    echo Bạn có muốn tải VS Code không? (Y/N)
    set /p download_vscode=
    if /i "%download_vscode%"=="Y" (
        echo Đang mở trang tải VS Code...
        start https://code.visualstudio.com/download
        echo Sau khi cài đặt VS Code, vui lòng chạy lại script này.
        pause
        exit /b 1
    ) else (
        echo Cài đặt đã bị hủy.
        pause
        exit /b 1
    )
)

REM Kiểm tra xem Node.js đã được cài đặt chưa
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js không được tìm thấy. Cần cài đặt Node.js.
    echo Bạn có muốn tải Node.js không? (Y/N)
    set /p download_node=
    if /i "%download_node%"=="Y" (
        echo Đang mở trang tải Node.js...
        start https://nodejs.org/
        echo Sau khi cài đặt Node.js, vui lòng chạy lại script này.
        pause
        exit /b 1
    ) else (
        echo Cài đặt đã bị hủy.
        pause
        exit /b 1
    )
)

REM Kiểm tra xem npm đã được cài đặt chưa
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo npm không được tìm thấy. Cần cài đặt Node.js.
    echo Bạn có muốn tải Node.js không? (Y/N)
    set /p download_npm=
    if /i "%download_npm%"=="Y" (
        echo Đang mở trang tải Node.js...
        start https://nodejs.org/
        echo Sau khi cài đặt Node.js, vui lòng chạy lại script này.
        pause
        exit /b 1
    ) else (
        echo Cài đặt đã bị hủy.
        pause
        exit /b 1
    )
)

REM Kiểm tra xem Inno Setup đã được cài đặt chưa
where iscc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Inno Setup không được tìm thấy. Cần cài đặt Inno Setup để tạo file cài đặt.
    echo Bạn có muốn tải Inno Setup không? (Y/N)
    set /p download_inno=
    if /i "%download_inno%"=="Y" (
        echo Đang mở trang tải Inno Setup...
        start https://jrsoftware.org/isdl.php
        echo Sau khi cài đặt Inno Setup, vui lòng chạy lại script này.
        pause
        exit /b 1
    ) else (
        echo Sẽ bỏ qua bước tạo file cài đặt EXE.
        set skip_exe=1
    )
) else (
    set skip_exe=0
)

REM Cài đặt vsce
echo.
echo === Cài đặt vsce ===
echo Đang cài đặt vsce...
call npm install -g @vscode/vsce
if %ERRORLEVEL% NEQ 0 (
    echo Không thể cài đặt vsce. Vui lòng thử lại sau.
    pause
    exit /b 1
)

REM Cài đặt dependencies cho extension
echo.
echo === Cài đặt dependencies cho extension ===
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
echo === Biên dịch TypeScript ===
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
echo === Đóng gói extension ===
echo Đang đóng gói extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license
if %ERRORLEVEL% NEQ 0 (
    echo Không thể đóng gói extension. Vui lòng kiểm tra lỗi và thử lại.
    cd ..
    pause
    exit /b 1
)

REM Trở về thư mục gốc
cd ..

REM Tạo file cài đặt EXE nếu Inno Setup đã được cài đặt
if %skip_exe% EQU 0 (
    echo.
    echo === Tạo file cài đặt EXE ===
    echo Đang tạo file cài đặt EXE...
    iscc create-installer.iss
    if %ERRORLEVEL% NEQ 0 (
        echo Không thể tạo file cài đặt EXE. Vui lòng kiểm tra lỗi và thử lại.
        pause
    ) else (
        echo File cài đặt EXE đã được tạo thành công tại: %CD%\Auto-Commit-Installer.exe
    )
)

REM Cài đặt extension
echo.
echo === Cài đặt extension ===
echo Bạn có muốn cài đặt extension vào VS Code không? (Y/N)
set /p install_extension=
if /i "%install_extension%"=="Y" (
    echo Đang cài đặt extension...
    code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"
    if %ERRORLEVEL% NEQ 0 (
        echo Không thể cài đặt extension. Vui lòng thử lại sau.
        pause
    ) else (
        echo Extension đã được cài đặt thành công!
        echo Vui lòng khởi động lại VS Code nếu nó đang chạy.
    )
)

echo.
echo === Thiết lập hoàn tất ===
echo.
echo Các file đã được tạo:
echo - VSIX: extension\auto-commit-copilot-0.0.1.vsix
if %skip_exe% EQU 0 echo - EXE: Auto-Commit-Installer.exe
echo.
echo Để sử dụng extension:
echo 1. Thực hiện các thay đổi trong dự án của bạn
echo 2. Stage các thay đổi bạn muốn commit
echo 3. Nhấn Ctrl+Space để tự động tạo commit message và thực hiện commit
echo.
echo Bạn có muốn mở VS Code ngay bây giờ không? (Y/N)
set /p open_vscode=
if /i "%open_vscode%"=="Y" (
    echo Đang mở VS Code...
    start code
)

echo.
echo Cảm ơn bạn đã sử dụng Auto Commit với Copilot!
echo.
pause 