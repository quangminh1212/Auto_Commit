@echo off
echo Packaging Auto Commit with Copilot extension...
echo.

REM Di chuyển đến thư mục extension
cd extension

REM Biên dịch TypeScript
echo Dang bien dich TypeScript...
call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo Khong the bien dich TypeScript. Vui long kiem tra lai cai dat.
    cd ..
    pause
    exit /b 1
)

REM Đóng gói extension với tham số bổ sung để bỏ qua cảnh báo
echo Dang dong goi extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license
if %ERRORLEVEL% NEQ 0 (
    echo Khong the dong goi extension. Vui long kiem tra lai cai dat.
    cd ..
    pause
    exit /b 1
)

REM Trở về thư mục gốc
cd ..

echo.
echo Extension da duoc dong goi thanh cong!
echo Ban co the tim thay file VSIX tai: extension\auto-commit-copilot-0.0.1.vsix
echo.
pause 