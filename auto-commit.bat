@echo off
setlocal enabledelayedexpansion

echo Auto Commit Tool - v1.0.0
echo ===========================

:: Check if git is installed
where git >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git and try again.
    goto :end
)

:: Read command line arguments
set "REPO_PATH="
set "FREQUENCY=1h"
set "COMMIT_MESSAGE=Auto commit: %date% %time%"
set "COMMAND=start"

:parse_args
if "%~1"=="" goto process_command
if /i "%~1"=="--path" (
    set "REPO_PATH=%~2"
    shift
) else if /i "%~1"=="-p" (
    set "REPO_PATH=%~2"
    shift
) else if /i "%~1"=="--frequency" (
    set "FREQUENCY=%~2"
    shift
) else if /i "%~1"=="-f" (
    set "FREQUENCY=%~2"
    shift
) else if /i "%~1"=="--message" (
    set "COMMIT_MESSAGE=%~2"
    shift
) else if /i "%~1"=="-m" (
    set "COMMIT_MESSAGE=%~2"
    shift
) else if /i "%~1"=="start" (
    set "COMMAND=start"
) else if /i "%~1"=="stop" (
    set "COMMAND=stop"
) else if /i "%~1"=="status" (
    set "COMMAND=status"
) else if /i "%~1"=="help" (
    set "COMMAND=help"
)
shift
goto parse_args

:process_command
if /i "%COMMAND%"=="help" (
    call :show_help
    goto :end
)

:: If no repo path provided, use current directory
if "%REPO_PATH%"=="" (
    set "REPO_PATH=%CD%"
)

:: Check if provided path is a git repository
if not exist "%REPO_PATH%\.git" (
    echo ERROR: The path '%REPO_PATH%' is not a git repository.
    echo Please initialize a git repository first or specify a valid path.
    goto :end
)

:: Process the command
if /i "%COMMAND%"=="start" (
    call :start_auto_commit
) else if /i "%COMMAND%"=="stop" (
    call :stop_auto_commit
) else if /i "%COMMAND%"=="status" (
    call :show_status
)

goto :end

:start_auto_commit
echo Starting Auto Commit for repository: %REPO_PATH%
echo Commit frequency: %FREQUENCY%
echo Commit message template: %COMMIT_MESSAGE%
echo.

:: Parse frequency to minutes
set "MINUTES="
if "%FREQUENCY:~-1%"=="m" (
    set "MINUTES=%FREQUENCY:~0,-1%"
) else if "%FREQUENCY:~-1%"=="h" (
    set /a "MINUTES=%FREQUENCY:~0,-1% * 60"
) else if "%FREQUENCY:~-1%"=="d" (
    set /a "MINUTES=%FREQUENCY:~0,-1% * 60 * 24"
) else (
    set "MINUTES=%FREQUENCY%"
)

echo Starting auto-commit cycle every %MINUTES% minutes...
echo Press Ctrl+C to stop.
echo.

:commit_loop
cd /d "%REPO_PATH%"
git add .
git commit -m "%COMMIT_MESSAGE%"

echo Auto-committed at %time% - Waiting %MINUTES% minutes for next commit...
timeout /t %MINUTES% /nobreak
goto :commit_loop

:stop_auto_commit
echo Function not implemented yet.
goto :end

:show_status
echo Function not implemented yet.
goto :end

:show_help
echo USAGE: auto-commit [COMMAND] [OPTIONS]
echo.
echo Commands:
echo   start      Start auto-commit for a repository
echo   stop       Stop auto-commit process
echo   status     Show status of auto-commit processes
echo   help       Show this help message
echo.
echo Options:
echo   --path, -p       Path to the git repository (default: current directory)
echo   --frequency, -f  Commit frequency (e.g., 30m, 1h, 1d) (default: 1h)
echo   --message, -m    Commit message template (default: "Auto commit: %%date%% %%time%%")
echo.
echo Examples:
echo   auto-commit start
echo   auto-commit start --path C:\projects\myrepo --frequency 2h
echo   auto-commit stop
goto :end

:end
endlocal 