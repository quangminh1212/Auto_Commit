@echo off
setlocal enabledelayedexpansion

echo Auto-Commit Tool
echo ===============

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

:: Commit changes
echo Committing changes with message: !COMMIT_MSG!
git add .
git commit -m !COMMIT_MSG!

echo Commit completed successfully.
pause