# Script để tự động mở Source Control, tạo commit message với Copilot và thực hiện commit
# Sử dụng VS Code CLI để thực hiện các lệnh

# Đường dẫn đến VS Code CLI
$vscodePath = "code"

try {
    # Kiểm tra xem VS Code CLI có hoạt động không
    $codeVersion = & $vscodePath --version
    if (-not $?) {
        throw "Không thể kết nối với VS Code CLI. Hãy đảm bảo VS Code đã được cài đặt và thêm vào PATH."
    }

    # 1. Mở panel Source Control
    Write-Host "Đang mở Source Control panel..." -ForegroundColor Cyan
    & $vscodePath --command workbench.view.scm

    # Chờ một chút để panel Source Control được mở hoàn toàn
    Start-Sleep -Seconds 1

    # 2. Gọi lệnh Generate Commit Message with Copilot
    Write-Host "Đang tạo commit message với Copilot..." -ForegroundColor Cyan
    & $vscodePath --command github.copilot.generateCommitMessage

    # Chờ một chút để Copilot tạo commit message
    Start-Sleep -Seconds 3

    # 3. Thực hiện commit
    Write-Host "Đang thực hiện commit..." -ForegroundColor Cyan
    & $vscodePath --command git.commit

    Write-Host "Hoàn thành quy trình commit!" -ForegroundColor Green
}
catch {
    Write-Host "Lỗi: $_" -ForegroundColor Red
    Write-Host "Không thể hoàn thành quy trình commit. Vui lòng kiểm tra lại cài đặt và thử lại." -ForegroundColor Red
    exit 1
}

# Hiển thị thông báo hoàn thành
Write-Host "`nĐể sử dụng lại tính năng này, nhấn Ctrl+Alt+C hoặc chạy task 'Auto Commit với Copilot' từ VS Code." -ForegroundColor Yellow 