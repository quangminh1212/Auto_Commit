@echo off
echo ===================================================
echo    AUTO COMMIT WITH COPILOT SETUP
echo ===================================================
echo.

REM Check admin rights
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Please run this script as Administrator to install the required tools.
    echo Right-click on auto-commit-setup.bat and select "Run as administrator".
    pause
    exit /b 1
)

REM Check if VS Code is installed
where code >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo VS Code not found. Please install VS Code first.
    echo Do you want to download VS Code? (Y/N)
    set /p download_vscode=
    if /i "%download_vscode%"=="Y" (
        echo Opening VS Code download page...
        start https://code.visualstudio.com/download
        echo After installing VS Code, please run this script again.
        pause
        exit /b 1
    ) else (
        echo Installation cancelled.
        pause
        exit /b 1
    )
)

REM Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js not found. Node.js is required.
    echo Do you want to download Node.js? (Y/N)
    set /p download_node=
    if /i "%download_node%"=="Y" (
        echo Opening Node.js download page...
        start https://nodejs.org/
        echo After installing Node.js, please run this script again.
        pause
        exit /b 1
    ) else (
        echo Installation cancelled.
        pause
        exit /b 1
    )
)

REM Check if npm is installed
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo npm not found. Node.js is required.
    echo Do you want to download Node.js? (Y/N)
    set /p download_npm=
    if /i "%download_npm%"=="Y" (
        echo Opening Node.js download page...
        start https://nodejs.org/
        echo After installing Node.js, please run this script again.
        pause
        exit /b 1
    ) else (
        echo Installation cancelled.
        pause
        exit /b 1
    )
)

REM Check if Inno Setup is installed
where iscc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Inno Setup not found. Inno Setup is required to create the installer.
    echo Do you want to download Inno Setup? (Y/N)
    set /p download_inno=
    if /i "%download_inno%"=="Y" (
        echo Opening Inno Setup download page...
        start https://jrsoftware.org/isdl.php
        echo After installing Inno Setup, please run this script again.
        pause
        exit /b 1
    ) else (
        echo Will skip creating the EXE installer.
        set skip_exe=1
    )
) else (
    set skip_exe=0
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

REM Package the extension
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

REM Return to the root directory
cd ..

REM Create the EXE installer if Inno Setup is installed
if %skip_exe% EQU 0 (
    echo.
    echo === Creating EXE installer ===
    echo Creating EXE installer...
    iscc create-installer.iss
    if %ERRORLEVEL% NEQ 0 (
        echo Could not create the EXE installer. Please check for errors and try again.
        pause
    ) else (
        echo EXE installer created successfully at: %CD%\Auto-Commit-Installer.exe
    )
)

REM Install the extension
echo.
echo === Installing extension ===
echo Do you want to install the extension in VS Code? (Y/N)
set /p install_extension=
if /i "%install_extension%"=="Y" (
    echo Installing extension...
    code --install-extension "extension\auto-commit-copilot-0.0.1.vsix"
    if %ERRORLEVEL% NEQ 0 (
        echo Could not install the extension. Please try again later.
        pause
    ) else (
        echo Extension installed successfully!
        echo Please restart VS Code if it is running.
    )
)

echo.
echo === Setup completed ===
echo.
echo Files created:
echo - VSIX: extension\auto-commit-copilot-0.0.1.vsix
if %skip_exe% EQU 0 echo - EXE: Auto-Commit-Installer.exe
echo.
echo To use the extension:
echo 1. Make changes to your project
echo 2. Stage the changes you want to commit
echo 3. Press Ctrl+Space to automatically generate a commit message and perform the commit
echo.
echo Do you want to open VS Code now? (Y/N)
set /p open_vscode=
if /i "%open_vscode%"=="Y" (
    echo Opening VS Code...
    start code
)

echo.
echo Thank you for using Auto Commit with Copilot!
echo.
pause 