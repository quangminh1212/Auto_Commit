# Script để tự động mở Source Control, tạo commit message với Copilot và thực hiện commit
# Sử dụng VS Code CLI để thực hiện các lệnh

# Đường dẫn đến VS Code CLI
$vscodePath = "code"

# 1. Mở panel Source Control
Write-Host "Đang mở Source Control panel..."
& $vscodePath --command workbench.view.scm

# Chờ một chút để panel Source Control được mở hoàn toàn
Start-Sleep -Seconds 1

# 2. Gọi lệnh Generate Commit Message with Copilot
Write-Host "Đang tạo commit message với Copilot..."
& $vscodePath --command github.copilot.generateCommitMessage

# Chờ một chút để Copilot tạo commit message
Start-Sleep -Seconds 3

# 3. Thực hiện commit
Write-Host "Đang thực hiện commit..."
& $vscodePath --command git.commit

Write-Host "Hoàn thành quy trình commit!" 