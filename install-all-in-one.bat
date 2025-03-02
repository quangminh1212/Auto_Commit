@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ===================================================
echo    AUTO COMMIT WITH COPILOT - CAI DAT TONG HOP
echo ===================================================
echo.

REM Tao file log
echo Qua trinh cai dat bat dau luc %date% %time% > setup_log.txt

REM Kiem tra quyen admin
echo Dang kiem tra quyen admin...
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Vui long chay script nay voi quyen Administrator de cai dat cac cong cu can thiet.
    echo Nhap chuot phai vao install-all-in-one.bat va chon "Run as administrator".
    pause
    exit /b 1
)

REM Kiem tra VS Code
echo Dang kiem tra VS Code...
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo VS Code khong duoc tim thay. Vui long cai dat VS Code truoc.
    echo Ban co the tai VS Code tu: https://code.visualstudio.com/download
    pause
    exit /b 1
)

REM Kiem tra Node.js
echo Dang kiem tra Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js khong duoc tim thay. Vui long cai dat Node.js truoc.
    echo Ban co the tai Node.js tu: https://nodejs.org/
    pause
    exit /b 1
)

REM Kiem tra npm
echo Dang kiem tra npm...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo npm khong duoc tim thay. Vui long cai dat Node.js (bao gom npm) truoc.
    echo Ban co the tai Node.js tu: https://nodejs.org/
    pause
    exit /b 1
)

REM Kiem tra xem extension da duoc cai dat chua
echo Dang kiem tra extension hien tai...
code --list-extensions | findstr "undefined_publisher.auto-commit-copilot" >nul
if %ERRORLEVEL% EQU 0 (
    echo Extension Auto Commit voi Copilot da duoc cai dat.
    echo Ban co muon cai dat lai khong? (Y/N)
    set /p reinstall=
    if /i "!reinstall!" NEQ "Y" (
        echo Cai dat da bi huy.
        pause
        exit /b 0
    )
)

REM Kiem tra thu muc extension
echo Dang kiem tra thu muc extension...
if not exist "extension" (
    echo Thu muc extension khong tim thay. Vui long dam bao ban dang chay script nay tu dung vi tri.
    pause
    exit /b 1
)

REM Cai dat vsce
echo.
echo === Dang cai dat vsce ===
echo Dang cai dat vsce...
call npm install -g @vscode/vsce
if %ERRORLEVEL% NEQ 0 (
    echo Khong the cai dat vsce. Vui long thu lai sau.
    pause
    exit /b 1
)

REM Cai dat dependencies cho extension
echo.
echo === Dang cai dat dependencies cho extension ===
cd extension
echo Dang cai dat dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Khong the cai dat dependencies. Vui long thu lai sau.
    cd ..
    pause
    exit /b 1
)

REM Bien dich TypeScript
echo.
echo === Dang bien dich TypeScript ===
echo Dang bien dich TypeScript...
call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo Khong the bien dich TypeScript. Vui long kiem tra loi va thu lai.
    cd ..
    pause
    exit /b 1
)

REM Dong goi extension
echo.
echo === Dang dong goi extension ===
echo Dang dong goi extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license
if %ERRORLEVEL% NEQ 0 (
    echo Khong the dong goi extension. Vui long kiem tra loi va thu lai.
    cd ..
    pause
    exit /b 1
)

REM Quay lai thu muc goc
cd ..

REM Cai dat extension
echo.
echo === Dang cai dat extension vao VS Code ===
echo Dang cai dat extension...
code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"
if %ERRORLEVEL% NEQ 0 (
    echo Khong the cai dat extension. Vui long thu lai sau.
    pause
    exit /b 1
)

echo.
echo === Cai dat hoan tat ===
echo.
echo Extension da duoc cai dat thanh cong!
echo Vui long khoi dong lai VS Code neu no dang chay.
echo.
echo De su dung extension:
echo 1. Thuc hien cac thay doi trong du an cua ban
echo 2. Stage cac thay doi ban muon commit
echo 3. Nhan Ctrl+Space de tu dong tao commit message va thuc hien commit
echo.
echo Cam on ban da su dung Auto Commit with Copilot!
echo.
pause 