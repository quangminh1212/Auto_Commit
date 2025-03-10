@echo off
setlocal enabledelayedexpansion

echo Auto-Commit Tool
echo ===============

:: Check for parameters
set TEST_MODE=0
set OPEN_COPILOT=0

:parse_args
if "%1"=="" goto end_parse_args
if /i "%1"=="-test" set TEST_MODE=1
if /i "%1"=="--test" set TEST_MODE=1
if /i "%1"=="-t" set TEST_MODE=1
if /i "%1"=="-copilot" set OPEN_COPILOT=1
if /i "%1"=="--copilot" set OPEN_COPILOT=1
if /i "%1"=="-c" set OPEN_COPILOT=1
if /i "%1"=="-help" goto show_help
if /i "%1"=="--help" goto show_help
if /i "%1"=="-h" goto show_help
shift
goto parse_args
:end_parse_args

:: Open GitHub Copilot if requested
if %OPEN_COPILOT%==1 (
    echo Opening GitHub Copilot agent...
    start "" code --command github.copilot.show
    exit /b 0
)

:: Check if git is installed
git --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Git is not installed or not in PATH.
    exit /b 1
)

:: Check for changes
echo Checking for changes...
git status --porcelain > changes.tmp
set /p CHANGES=<changes.tmp
del changes.tmp

if "!CHANGES!"=="" (
    echo No changes detected. Nothing to commit.
    exit /b 0
)

:: Get a list of changed files
git diff --name-only > changed_files.tmp
echo Changed files:
type changed_files.tmp
echo.

:: Generate a simple commit message based on changes
echo Generating commit message...
set COMMIT_MSG="Auto-commit: Updated files at %date% %time%"

:: Execute or simulate commit based on test mode
if %TEST_MODE%==1 (
    echo TEST MODE: Would commit the following changes with message: !COMMIT_MSG!
    echo.
    git status
    echo.
    echo No actual commit was made. Run without -test parameter to perform actual commit.
) else (
    echo Committing changes with message: !COMMIT_MSG!
    git add .
    git commit -m !COMMIT_MSG!
    echo Commit completed successfully.
)

goto end

:show_help
echo.
echo Usage: auto-commit.bat [options]
echo.
echo Options:
echo   -t, --test       Test mode - shows what would happen without making changes
echo   -c, --copilot    Open GitHub Copilot agent in VS Code
echo   -h, --help       Show this help message
echo.
exit /b 0

:end
pause