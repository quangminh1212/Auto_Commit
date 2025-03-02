@echo off
echo ===================================================
echo    AUTO COMMIT WITH COPILOT SETUP (ABSOLUTE PATH)
echo ===================================================
echo.

REM Set the absolute path to the project directory
set PROJECT_DIR=C:\VF\Auto_Commit

REM Check admin rights
echo Checking admin rights...
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Please run this script as Administrator to install the required tools.
    echo Right-click on auto-commit-absolute.bat and select "Run as administrator".
    pause
    exit /b 1
)

REM Check if extension directory exists
echo Checking if extension directory exists...
if not exist "%PROJECT_DIR%\extension" (
    echo Extension directory not found. Please make sure the directory C:\VF\Auto_Commit\extension exists.
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

REM Install dependencies for the extension
echo.
echo === Installing extension dependencies ===
cd /d "%PROJECT_DIR%\extension"
echo Installing dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo Could not install dependencies. Please try again later.
    cd /d "%PROJECT_DIR%"
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
    cd /d "%PROJECT_DIR%"
    pause
    exit /b 1
)

REM Package the extension
echo.
echo === Packaging extension ===
echo Packaging extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license
if %ERRORLEVEL% NEQ 0 (
    echo Could not package the extension. Please check for errors and try again.
    cd /d "%PROJECT_DIR%"
    pause
    exit /b 1
)

REM Return to the root directory
cd /d "%PROJECT_DIR%"

echo.
echo === Setup completed ===
echo.
echo Files created:
echo - VSIX: %PROJECT_DIR%\extension\auto-commit-copilot-0.0.1.vsix
echo.
echo To install the extension, run:
echo code --install-extension "%PROJECT_DIR%\extension\auto-commit-copilot-0.0.1.vsix"
echo.
echo To use the extension:
echo 1. Make changes to your project
echo 2. Stage the changes you want to commit
echo 3. Press Ctrl+Space to automatically generate a commit message and perform the commit
echo.
echo Thank you for using Auto Commit with Copilot!
echo.
pause 