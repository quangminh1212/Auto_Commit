@echo off
echo ===================================================
echo    AUTO COMMIT WITH COPILOT SETUP
echo ===================================================
echo.

REM Create log file
echo Setup started at %date% %time% > setup_log.txt
echo ===================================================>> setup_log.txt

REM Check admin rights
echo Checking admin rights...
echo Checking admin rights... >> setup_log.txt
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Admin rights check failed. Error code: %ERRORLEVEL% >> setup_log.txt
    echo Please run this script as Administrator to install the required tools.
    echo Right-click on auto-commit-setup.bat and select "Run as administrator".
    pause
    exit /b 1
) else (
    echo Admin rights confirmed >> setup_log.txt
)

REM Check if VS Code is installed - with timeout
echo Checking if VS Code is installed...
echo Checking if VS Code is installed... >> setup_log.txt

REM Use a temporary file to store the result
echo @echo off > check_vscode.bat
echo where code ^>nul 2^>^&1 >> check_vscode.bat
echo echo %%ERRORLEVEL%% ^> vscode_result.txt >> check_vscode.bat

REM Run the check with a timeout
start /wait /b cmd /c check_vscode.bat
timeout /t 5 /nobreak > nul

REM Check if the result file exists
if not exist vscode_result.txt (
    echo VS Code check timed out >> setup_log.txt
    echo VS Code check timed out. Assuming VS Code is not installed.
    set VSCODE_CHECK=1
) else (
    set /p VSCODE_CHECK=<vscode_result.txt
    del vscode_result.txt
)

REM Clean up
del check_vscode.bat

if %VSCODE_CHECK% NEQ 0 (
    echo VS Code not found. Error code: %VSCODE_CHECK% >> setup_log.txt
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
) else (
    echo VS Code found >> setup_log.txt
)

REM Check if Node.js is installed - with timeout
echo Checking if Node.js is installed...
echo Checking if Node.js is installed... >> setup_log.txt

REM Use a temporary file to store the result
echo @echo off > check_node.bat
echo where node ^>nul 2^>^&1 >> check_node.bat
echo echo %%ERRORLEVEL%% ^> node_result.txt >> check_node.bat

REM Run the check with a timeout
start /wait /b cmd /c check_node.bat
timeout /t 5 /nobreak > nul

REM Check if the result file exists
if not exist node_result.txt (
    echo Node.js check timed out >> setup_log.txt
    echo Node.js check timed out. Assuming Node.js is not installed.
    set NODE_CHECK=1
) else (
    set /p NODE_CHECK=<node_result.txt
    del node_result.txt
)

REM Clean up
del check_node.bat

if %NODE_CHECK% NEQ 0 (
    echo Node.js not found. Error code: %NODE_CHECK% >> setup_log.txt
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
) else (
    echo Node.js found >> setup_log.txt
    node --version >> setup_log.txt 2>nul
)

REM Check if npm is installed - with timeout
echo Checking if npm is installed...
echo Checking if npm is installed... >> setup_log.txt

REM Use a temporary file to store the result
echo @echo off > check_npm.bat
echo where npm ^>nul 2^>^&1 >> check_npm.bat
echo echo %%ERRORLEVEL%% ^> npm_result.txt >> check_npm.bat

REM Run the check with a timeout
start /wait /b cmd /c check_npm.bat
timeout /t 5 /nobreak > nul

REM Check if the result file exists
if not exist npm_result.txt (
    echo npm check timed out >> setup_log.txt
    echo npm check timed out. Assuming npm is not installed.
    set NPM_CHECK=1
) else (
    set /p NPM_CHECK=<npm_result.txt
    del npm_result.txt
)

REM Clean up
del check_npm.bat

if %NPM_CHECK% NEQ 0 (
    echo npm not found. Error code: %NPM_CHECK% >> setup_log.txt
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
) else (
    echo npm found >> setup_log.txt
    npm --version >> setup_log.txt 2>nul
)

REM Check if Inno Setup is installed - with timeout
echo Checking if Inno Setup is installed...
echo Checking if Inno Setup is installed... >> setup_log.txt

REM Use a temporary file to store the result
echo @echo off > check_inno.bat
echo where iscc ^>nul 2^>^&1 >> check_inno.bat
echo echo %%ERRORLEVEL%% ^> inno_result.txt >> check_inno.bat

REM Run the check with a timeout
start /wait /b cmd /c check_inno.bat
timeout /t 5 /nobreak > nul

REM Check if the result file exists
if not exist inno_result.txt (
    echo Inno Setup check timed out >> setup_log.txt
    echo Inno Setup check timed out. Assuming Inno Setup is not installed.
    set INNO_CHECK=1
) else (
    set /p INNO_CHECK=<inno_result.txt
    del inno_result.txt
)

REM Clean up
del check_inno.bat

if %INNO_CHECK% NEQ 0 (
    echo Inno Setup not found. Error code: %INNO_CHECK% >> setup_log.txt
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
        echo Will skip creating the EXE installer >> setup_log.txt
    )
) else (
    set skip_exe=0
    echo Inno Setup found >> setup_log.txt
)

REM Install vsce
echo.
echo === Installing vsce ===
echo Installing vsce... >> setup_log.txt
echo Installing vsce...
call npm install -g @vscode/vsce 2>> setup_log.txt
if %ERRORLEVEL% NEQ 0 (
    echo Could not install vsce. Error code: %ERRORLEVEL% >> setup_log.txt
    echo Could not install vsce. Please try again later.
    pause
    exit /b 1
) else (
    echo vsce installed successfully >> setup_log.txt
)

REM Check if extension directory exists
echo Checking if extension directory exists...
echo Checking if extension directory exists... >> setup_log.txt
if not exist "extension" (
    echo Extension directory not found >> setup_log.txt
    echo Extension directory not found. Please make sure you are running this script from the correct location.
    pause
    exit /b 1
) else (
    echo Extension directory found >> setup_log.txt
)

REM Install dependencies for the extension
echo.
echo === Installing extension dependencies ===
echo Installing extension dependencies... >> setup_log.txt
cd extension
echo Current directory: %CD% >> ..\setup_log.txt
echo Installing dependencies...
call npm install 2>> ..\setup_log.txt
if %ERRORLEVEL% NEQ 0 (
    echo Could not install dependencies. Error code: %ERRORLEVEL% >> ..\setup_log.txt
    echo Could not install dependencies. Please try again later.
    cd ..
    pause
    exit /b 1
) else (
    echo Dependencies installed successfully >> ..\setup_log.txt
)

REM Compile TypeScript
echo.
echo === Compiling TypeScript ===
echo Compiling TypeScript... >> ..\setup_log.txt
echo Compiling TypeScript...
call npm run compile 2>> ..\setup_log.txt
if %ERRORLEVEL% NEQ 0 (
    echo Could not compile TypeScript. Error code: %ERRORLEVEL% >> ..\setup_log.txt
    echo Could not compile TypeScript. Please check for errors and try again.
    cd ..
    pause
    exit /b 1
) else (
    echo TypeScript compiled successfully >> ..\setup_log.txt
)

REM Package the extension
echo.
echo === Packaging extension ===
echo Packaging extension... >> ..\setup_log.txt
echo Packaging extension...
call npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license 2>> ..\setup_log.txt
if %ERRORLEVEL% NEQ 0 (
    echo Could not package the extension. Error code: %ERRORLEVEL% >> ..\setup_log.txt
    echo Could not package the extension. Please check for errors and try again.
    cd ..
    pause
    exit /b 1
) else (
    echo Extension packaged successfully >> ..\setup_log.txt
)

REM Return to the root directory
cd ..
echo Returned to root directory: %CD% >> setup_log.txt

REM Create the EXE installer if Inno Setup is installed
if %skip_exe% EQU 0 (
    echo.
    echo === Creating EXE installer ===
    echo Creating EXE installer... >> setup_log.txt
    echo Creating EXE installer...
    iscc create-installer.iss 2>> setup_log.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Could not create the EXE installer. Error code: %ERRORLEVEL% >> setup_log.txt
        echo Could not create the EXE installer. Please check for errors and try again.
        pause
    ) else (
        echo EXE installer created successfully at: %CD%\Auto-Commit-Installer.exe
        echo EXE installer created successfully >> setup_log.txt
    )
)

REM Install the extension
echo.
echo === Installing extension ===
echo Do you want to install the extension in VS Code? (Y/N)
set /p install_extension=
echo User chose to install extension: %install_extension% >> setup_log.txt
if /i "%install_extension%"=="Y" (
    echo Installing extension...
    echo Installing extension... >> setup_log.txt
    code --install-extension "extension\auto-commit-copilot-0.0.1.vsix" 2>> setup_log.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Could not install the extension. Error code: %ERRORLEVEL% >> setup_log.txt
        echo Could not install the extension. Please try again later.
        pause
    ) else (
        echo Extension installed successfully!
        echo Extension installed successfully >> setup_log.txt
        echo Please restart VS Code if it is running.
    )
)

echo.
echo === Setup completed ===
echo Setup completed at %date% %time% >> setup_log.txt
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
echo User chose to open VS Code: %open_vscode% >> setup_log.txt
if /i "%open_vscode%"=="Y" (
    echo Opening VS Code...
    start code
)

echo.
echo Thank you for using Auto Commit with Copilot!
echo If you encountered any issues, please check the setup_log.txt file for details.
echo.
pause