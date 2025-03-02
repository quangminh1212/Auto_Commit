# Script để chạy extension trong môi trường phát triển

# Biên dịch TypeScript
Write-Host "Đang biên dịch TypeScript..." -ForegroundColor Cyan
npm run compile

# Chạy extension trong chế độ debug
Write-Host "Đang chạy extension trong chế độ debug..." -ForegroundColor Cyan
Write-Host "Nhấn F5 trong VS Code để bắt đầu phiên debug" -ForegroundColor Yellow

# Hướng dẫn
Write-Host "`nHướng dẫn sử dụng:" -ForegroundColor Green
Write-Host "1. Mở VS Code với thư mục extension này" -ForegroundColor White
Write-Host "2. Nhấn F5 để bắt đầu phiên debug" -ForegroundColor White
Write-Host "3. Trong cửa sổ VS Code mới, sử dụng phím tắt Ctrl+Alt+C hoặc menu ngữ cảnh để chạy lệnh Auto Commit với Copilot" -ForegroundColor White 