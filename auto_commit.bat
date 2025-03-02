@echo off
echo === Auto Commit Tool ===
echo.

REM Kiểm tra xem có thay đổi nào chưa được staged không
git status --porcelain | findstr "^?? ^M ^A ^D" > nul
if %ERRORLEVEL% EQU 0 (
    echo Phát hiện các file chưa được staged:
    git status --porcelain
    
    set /p STAGE_ALL=Bạn có muốn stage tất cả các thay đổi không? (Y/N): 
    if /i "%STAGE_ALL%"=="Y" (
        git add .
        echo Đã stage tất cả các thay đổi.
    ) else (
        echo Vui lòng stage các thay đổi thủ công trước khi chạy lại script này.
        echo Ví dụ: git add <tên_file>
        exit /b 1
    )
)

REM Chạy script Python để tạo commit message và commit
python auto_commit.py

REM Kiểm tra xem commit có thành công không
if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Commit thành công ===
    
    set /p PUSH=Bạn có muốn push lên remote repository không? (Y/N): 
    if /i "%PUSH%"=="Y" (
        git push
        echo Đã push lên remote repository.
    ) else (
        echo Bạn có thể push thủ công sau bằng lệnh: git push
    )
) else (
    echo.
    echo === Commit thất bại ===
    echo Vui lòng kiểm tra lỗi và thử lại.
)

echo.
echo === Hoàn tất === 