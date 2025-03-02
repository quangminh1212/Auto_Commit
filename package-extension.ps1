# Script để đóng gói extension Auto Commit với Copilot

# Di chuyển đến thư mục extension
Set-Location -Path ".\extension"

# Biên dịch TypeScript
Write-Host "Đang biên dịch TypeScript..." -ForegroundColor Cyan
npm run compile

# Đóng gói extension với tham số bổ sung để bỏ qua cảnh báo
Write-Host "Đang đóng gói extension..." -ForegroundColor Cyan
npx @vscode/vsce package --no-dependencies --no-git-tag-version --allow-missing-repository --skip-license

# Trở về thư mục gốc
Set-Location -Path ".."

Write-Host "`nExtension đã được đóng gói thành công!" -ForegroundColor Green
Write-Host "Bạn có thể tìm thấy file VSIX tại: extension\auto-commit-copilot-0.0.1.vsix" -ForegroundColor Yellow 