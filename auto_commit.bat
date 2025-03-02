@echo off
echo === Auto Commit Tool ===
echo.

REM Kiểm tra xem Python đã được cài đặt chưa
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Lỗi: Python chưa được cài đặt. Vui lòng cài đặt Python trước khi chạy script này.
    exit /b 1
)

REM Kiểm tra xem Git đã được cài đặt chưa
git --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Lỗi: Git chưa được cài đặt. Vui lòng cài đặt Git trước khi chạy script này.
    exit /b 1
)

REM Kiểm tra xem có phải là git repository không
git rev-parse --is-inside-work-tree > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Lỗi: Thư mục hiện tại không phải là git repository.
    exit /b 1
)

REM Kiểm tra xem API key đã được cấu hình chưa
findstr /C:"YOUR_GEMINI_API_KEY" auto_commit.py > nul
if %ERRORLEVEL% EQU 0 (
    echo Cảnh báo: API key chưa được cấu hình.
    set /p API_KEY=Nhập API key của Gemini (để trống để bỏ qua): 
    
    if not "%API_KEY%"=="" (
        echo Đang cập nhật API key...
        powershell -Command "(Get-Content auto_commit.py) -replace 'YOUR_GEMINI_API_KEY', '%API_KEY%' | Set-Content auto_commit.py"
        echo API key đã được cập nhật.
    ) else (
        echo API key không được cung cấp. Quá trình commit có thể thất bại.
    )
)

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

REM Kiểm tra xem có thay đổi nào đã được staged không
git diff --staged --quiet
if %ERRORLEVEL% NEQ 0 (
    REM Có thay đổi đã được staged
    
    REM Hỏi người dùng có muốn chạy test trước khi commit không
    set /p RUN_TEST=Bạn có muốn chạy test trước khi commit không? (Y/N, mặc định là N): 
    if /i "%RUN_TEST%"=="Y" (
        echo Đang chạy test...
        python test_auto_commit.py
        
        if %ERRORLEVEL% NEQ 0 (
            echo Test thất bại. Bạn có muốn tiếp tục commit không?
            set /p CONTINUE=Tiếp tục commit mặc dù test thất bại? (Y/N): 
            if /i not "%CONTINUE%"=="Y" (
                echo Đã hủy quá trình commit.
                exit /b 1
            )
        ) else (
            echo Test thành công.
        )
    )
    
    REM Chạy script Python để tạo commit message và commit
    echo Đang tạo commit message và commit...
    python auto_commit.py
    
    REM Kiểm tra xem commit có thành công không
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo === Commit thành công ===
        
        set /p PUSH=Bạn có muốn push lên remote repository không? (Y/N): 
        if /i "%PUSH%"=="Y" (
            echo Đang push lên remote repository...
            git push
            
            if %ERRORLEVEL% EQU 0 (
                echo Đã push lên remote repository thành công.
            ) else (
                echo Lỗi khi push lên remote repository.
                echo Bạn có thể push thủ công sau bằng lệnh: git push
            )
        ) else (
            echo Bạn có thể push thủ công sau bằng lệnh: git push
        )
    ) else (
        echo.
        echo === Commit thất bại ===
        echo Vui lòng kiểm tra lỗi và thử lại.
    )
) else (
    echo Không có thay đổi nào được staged để commit.
    echo Vui lòng thực hiện một số thay đổi và stage chúng trước khi chạy lại script này.
    echo Ví dụ: git add <tên_file>
)

echo.
echo === Hoàn tất === 