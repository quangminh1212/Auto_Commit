@echo off
setlocal

echo ===================================================
echo    AUTO COMMIT WITH COPILOT - DEBUG INSTALLATION
echo ===================================================
echo.

echo [DEBUG] Starting debug log > debug_log.txt
echo [DEBUG] %date% %time% >> debug_log.txt

echo [DEBUG] Step 1: Admin check
echo [DEBUG] Step 1: Admin check >> debug_log.txt
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [DEBUG] Admin check failed >> debug_log.txt
    echo Please run this script as Administrator.
    pause
    exit /b 1
)
echo [DEBUG] Admin check passed >> debug_log.txt

echo [DEBUG] Step 2: VS Code check
echo [DEBUG] Step 2: VS Code check >> debug_log.txt
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [DEBUG] VS Code check failed >> debug_log.txt
    echo VS Code not found. Please install VS Code first.
    pause
    exit /b 1
)
echo [DEBUG] VS Code check passed >> debug_log.txt

echo [DEBUG] Step 3: Node.js check
echo [DEBUG] Step 3: Node.js check >> debug_log.txt
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [DEBUG] Node.js check failed >> debug_log.txt
    echo Node.js not found. Please install Node.js first.
    pause
    exit /b 1
)
echo [DEBUG] Node.js check passed >> debug_log.txt

echo [DEBUG] Step 4: npm check
echo [DEBUG] Step 4: npm check >> debug_log.txt
where npm >nul 2>nul
set NPM_STATUS=%ERRORLEVEL%
if %NPM_STATUS% NEQ 0 (
    echo [DEBUG] npm check failed >> debug_log.txt
    echo npm not found. Please install Node.js (including npm) first.
    pause
    exit /b 1
)
echo [DEBUG] npm check passed >> debug_log.txt

echo [DEBUG] Step 5: Extension check
echo [DEBUG] Step 5: Extension check >> debug_log.txt
code --list-extensions | findstr "undefined_publisher.auto-commit-copilot" >nul
set EXT_STATUS=%ERRORLEVEL%
if %EXT_STATUS% EQU 0 (
    echo [DEBUG] Extension already installed >> debug_log.txt
    echo Auto Commit with Copilot extension is already installed.
    echo Do you want to reinstall? (Y/N)
    set /p REINSTALL=
    if /i "%REINSTALL%" NEQ "Y" (
        echo [DEBUG] Installation cancelled by user >> debug_log.txt
        echo Installation cancelled.
        pause
        exit /b 0
    )
    echo [DEBUG] User chose to reinstall >> debug_log.txt
)
echo [DEBUG] Extension check passed >> debug_log.txt

echo [DEBUG] Step 6: Directory check
echo [DEBUG] Step 6: Directory check >> debug_log.txt
if not exist "extension" (
    echo [DEBUG] Extension directory not found >> debug_log.txt
    echo Extension directory not found. Please make sure you are running this script from the correct location.
    pause
    exit /b 1
)
echo [DEBUG] Directory check passed >> debug_log.txt

echo [DEBUG] Step 7: Installing vsce
echo [DEBUG] Step 7: Installing vsce >> debug_log.txt
echo.
echo === Installing vsce ===
echo Installing vsce...
call npm install -g @vscode/vsce
set VSCE_STATUS=%ERRORLEVEL%
if %VSCE_STATUS% NEQ 0 (
    echo [DEBUG] vsce installation failed >> debug_log.txt
    echo Could not install vsce. Please try again later.
    pause
    exit /b 1
)
echo [DEBUG] vsce installation passed >> debug_log.txt

echo [DEBUG] Step 8: Installing dependencies
echo [DEBUG] Step 8: Installing dependencies >> debug_log.txt
echo.
echo === Installing extension dependencies ===
cd extension
echo Installing dependencies...
call npm install
set DEP_STATUS=%ERRORLEVEL%
if %DEP_STATUS% NEQ 0 (
    echo [DEBUG] Dependencies installation failed >> debug_log.txt
    echo Could not install dependencies. Please try again later.
    cd ..
    pause
    exit /b 1
)
echo [DEBUG] Dependencies installation passed >> debug_log.txt

echo [DEBUG] Step 9: Compiling TypeScript
echo [DEBUG] Step 9: Compiling TypeScript >> debug_log.txt
echo.
echo === Compiling TypeScript ===
echo Compiling TypeScript...
call npm run compile
set COMPILE_STATUS=%ERRORLEVEL%
if %COMPILE_STATUS% NEQ 0 (
    echo [DEBUG] TypeScript compilation failed >> debug_log.txt
    echo Could not compile TypeScript. Please check for errors and try again.
    cd ..
    pause
    exit /b 1
)
echo [DEBUG] TypeScript compilation passed >> debug_log.txt

echo [DEBUG] Step 10: Packaging extension
echo [DEBUG] Step 10: Packaging extension >> debug_log.txt
echo.
echo === Packaging extension ===
echo Packaging extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license
set PACKAGE_STATUS=%ERRORLEVEL%
if %PACKAGE_STATUS% NEQ 0 (
    echo [DEBUG] Extension packaging failed >> debug_log.txt
    echo Could not package the extension. Please check for errors and try again.
    cd ..
    pause
    exit /b 1
)
echo [DEBUG] Extension packaging passed >> debug_log.txt

echo [DEBUG] Step 11: Returning to root directory
echo [DEBUG] Step 11: Returning to root directory >> debug_log.txt
cd ..
echo [DEBUG] Now in root directory >> debug_log.txt

echo [DEBUG] Step 12: Installing extension
echo [DEBUG] Step 12: Installing extension >> debug_log.txt
echo.
echo === Installing extension to VS Code ===
echo Installing extension...
code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"
set INSTALL_STATUS=%ERRORLEVEL%
if %INSTALL_STATUS% NEQ 0 (
    echo [DEBUG] Extension installation failed >> debug_log.txt
    echo Could not install extension. Please try again later.
    pause
    exit /b 1
)
echo [DEBUG] Extension installation passed >> debug_log.txt

echo [DEBUG] Step 13: Installation complete
echo [DEBUG] Step 13: Installation complete >> debug_log.txt
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
echo [DEBUG] Script completed successfully >> debug_log.txt
pause 