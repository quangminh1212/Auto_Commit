# Script để chạy extension Auto Commit với Copilot

# Di chuyển đến thư mục extension
Set-Location -Path ".\extension"

# Biên dịch TypeScript
Write-Host "Đang biên dịch TypeScript..." -ForegroundColor Cyan
npm run compile

# Đóng gói extension
Write-Host "Đang đóng gói extension..." -ForegroundColor Cyan
try {
    $vsixFile = npx @vscode/vsce package 2>&1 | Select-String -Pattern "Created: (.+\.vsix)" | ForEach-Object { $_.Matches.Groups[1].Value }
    
    if ($vsixFile -and (Test-Path $vsixFile)) {
        Write-Host "Extension đã được đóng gói thành công: $vsixFile" -ForegroundColor Green
        
        # Hướng dẫn cài đặt
        Write-Host "`nHướng dẫn cài đặt:" -ForegroundColor Yellow
        Write-Host "1. Mở VS Code" -ForegroundColor White
        Write-Host "2. Nhấn F1 hoặc Ctrl+Shift+P để mở Command Palette" -ForegroundColor White
        Write-Host "3. Gõ 'Extensions: Install from VSIX' và chọn file $vsixFile" -ForegroundColor White
        Write-Host "4. Sau khi cài đặt, sử dụng phím tắt Ctrl+Alt+C hoặc menu ngữ cảnh để chạy lệnh Auto Commit với Copilot" -ForegroundColor White
    } else {
        Write-Host "Không thể đóng gói extension. Vui lòng kiểm tra lại cài đặt." -ForegroundColor Red
    }
} catch {
    Write-Host "Lỗi khi đóng gói extension: $_" -ForegroundColor Red
}

# Trở về thư mục gốc
Set-Location -Path ".." 