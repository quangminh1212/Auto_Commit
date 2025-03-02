# Script để chạy extension Auto Commit với Copilot trong chế độ debug

# Di chuyển đến thư mục extension
Set-Location -Path ".\extension"

# Biên dịch TypeScript
Write-Host "Đang biên dịch TypeScript..." -ForegroundColor Cyan
npm run compile

# Chạy extension trong chế độ debug
Write-Host "Đang chuẩn bị chạy extension trong chế độ debug..." -ForegroundColor Cyan
Write-Host "Để chạy extension trong chế độ debug:" -ForegroundColor Yellow
Write-Host "1. Mở thư mục extension trong VS Code" -ForegroundColor White
Write-Host "2. Nhấn F5 để bắt đầu phiên debug" -ForegroundColor White
Write-Host "3. Trong cửa sổ VS Code mới, sử dụng phím tắt Ctrl+Alt+C hoặc menu ngữ cảnh để chạy lệnh Auto Commit với Copilot" -ForegroundColor White

# Hỏi người dùng có muốn mở VS Code không
$openVSCode = Read-Host "Bạn có muốn mở VS Code với thư mục extension không? (y/n)"
if ($openVSCode -eq "y" -or $openVSCode -eq "Y") {
    Write-Host "Đang mở VS Code..." -ForegroundColor Cyan
    code .
}

# Trở về thư mục gốc
Set-Location -Path ".." 