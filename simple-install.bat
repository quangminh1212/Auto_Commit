@echo off
echo ===================================================
echo    AUTO COMMIT WITH COPILOT - SIMPLE INSTALLATION
echo ===================================================
echo.

REM Check if extension directory exists
if not exist "extension" (
    echo Extension directory not found. Please make sure you are running this script from the correct location.
    pause
    exit /b 1
)

REM Go to extension directory
cd extension

REM Install dependencies
echo Installing dependencies...
call npm install

REM Compile TypeScript
echo Compiling TypeScript...
call npm run compile

REM Package extension
echo Packaging extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license

REM Return to root directory
cd ..

REM Install extension
echo Installing extension...
call code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"

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