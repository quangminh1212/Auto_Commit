# Hướng dẫn đóng gói và cài đặt extension

## Chuẩn bị

1. Cài đặt Node.js và npm từ [nodejs.org](https://nodejs.org/)
2. Cài đặt Visual Studio Code Extension Manager (vsce):
   ```
   npm install -g @vscode/vsce
   ```

## Đóng gói extension

1. Mở terminal và di chuyển đến thư mục extension:
   ```
   cd extension
   ```

2. Cài đặt các dependencies:
   ```
   npm install
   ```

3. Biên dịch TypeScript:
   ```
   npm run compile
   ```

4. Đóng gói extension thành file VSIX:
   ```
   vsce package
   ```
   Lệnh này sẽ tạo ra một file `auto-commit-copilot-0.0.1.vsix` trong thư mục extension.

## Cài đặt extension

### Cách 1: Cài đặt từ file VSIX

1. Mở VS Code
2. Nhấn F1 hoặc Ctrl+Shift+P để mở Command Palette
3. Gõ "Extensions: Install from VSIX" và chọn file VSIX đã tạo

### Cách 2: Cài đặt từ mã nguồn (để phát triển)

1. Mở thư mục extension trong VS Code
2. Nhấn F5 để chạy extension trong chế độ debug

## Sử dụng extension

Sau khi cài đặt, bạn có thể sử dụng extension bằng cách:

1. Nhấn phím tắt `Ctrl+Alt+C` (Windows/Linux) hoặc `Cmd+Alt+C` (Mac)
2. Nhấn chuột phải trong editor và chọn "Auto Commit với Copilot" từ menu ngữ cảnh
3. Mở Command Palette (Ctrl+Shift+P) và gõ "Auto Commit với Copilot"

## Gỡ cài đặt extension

1. Mở VS Code
2. Nhấn Ctrl+Shift+X để mở Extensions view
3. Tìm "Auto Commit với Copilot" trong danh sách các extension đã cài đặt
4. Nhấn nút "Uninstall" 