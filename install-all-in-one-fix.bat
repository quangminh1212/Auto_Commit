@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo    AUTO COMMIT WITH COPILOT - INSTALLATION
echo ===================================================
echo.

REM Create log file
echo Setup started at %date% %time% > setup_log.txt

REM Check admin rights
echo Checking admin rights...
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Please run this script as Administrator.
    echo Right-click on the batch file and select "Run as administrator".
    pause
    exit /b 1
)

REM Check VS Code
echo Checking VS Code...
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo VS Code not found. Please install VS Code first.
    echo You can download VS Code from: https://code.visualstudio.com/download
    pause
    exit /b 1
)

REM Check Node.js
echo Checking Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js not found. Please install Node.js first.
    echo You can download Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check npm
echo Checking npm...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo npm not found. Please install Node.js (including npm) first.
    echo You can download Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if extension is already installed
echo Checking current extension...
code --list-extensions | findstr "undefined_publisher.auto-commit-copilot" >nul
if %ERRORLEVEL% EQU 0 (
    echo Auto Commit with Copilot extension is already installed.
    echo Do you want to reinstall? (Y/N)
    set /p reinstall=
    if /i "!reinstall!" NEQ "Y" (
        echo Installation cancelled.
        pause
        exit /b 0
    )
)

REM Check extension directory
echo Checking extension directory...
if not exist "extension" (
    echo Extension directory not found. Please make sure you are running this script from the correct location.
    pause
    exit /b 1
)

REM Install vsce
echo.
echo === Installing vsce ===
echo Installing vsce...
call npm install -g @vscode/vsce
if %ERRORLEVEL% NEQ 0 (
    echo Could not install vsce. Please try again later.
    pause
    exit /b 1
)

REM Install dependencies for extension
echo.
echo === Installing extension dependencies ===
cd extension
echo Installing dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Could not install dependencies. Please try again later.
    cd ..
    pause
    exit /b 1
)

REM Compile TypeScript
echo.
echo === Compiling TypeScript ===
echo Compiling TypeScript...
call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo Could not compile TypeScript. Please check for errors and try again.
    cd ..
    pause
    exit /b 1
)

REM Package extension
echo.
echo === Packaging extension ===
echo Packaging extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license
if %ERRORLEVEL% NEQ 0 (
    echo Could not package the extension. Please check for errors and try again.
    cd ..
    pause
    exit /b 1
)

REM Return to root directory
cd ..

REM Install extension
echo.
echo === Installing extension to VS Code ===
echo Installing extension...
code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"
if %ERRORLEVEL% NEQ 0 (
    echo Could not install extension. Please try again later.
    pause
    exit /b 1
)

echo.
echo === Installation complete ===
echo.
echo Extension has been successfully installed!
echo Please restart VS Code if it is currently running.
echo.
echo To use the extension:
echo 1. Make changes to your project
echo 2. Stage the changes you want to commit
echo 3. Press Ctrl+Space to automatically generate a commit message and perform the commit
echo.
echo Thank you for using Auto Commit with Copilot!
echo.
pause 