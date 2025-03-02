# Auto Commit với Copilot

Extension VS Code giúp tự động hóa quy trình commit với GitHub Copilot.

## Tính năng

Extension này cung cấp một lệnh và phím tắt để tự động:
1. Mở panel Source Control
2. Gọi lệnh Generate Commit Message with Copilot
3. Thực hiện commit

## Cài đặt

### Từ VSIX
1. Tải file VSIX từ trang Releases
2. Mở VS Code
3. Nhấn F1 hoặc Ctrl+Shift+P để mở Command Palette
4. Gõ "Extensions: Install from VSIX" và chọn file VSIX đã tải

### Từ mã nguồn
1. Clone repository này
2. Mở thư mục extension trong terminal
3. Chạy `npm install` để cài đặt các dependencies
4. Chạy `npm run compile` để biên dịch TypeScript
5. Nhấn F5 để chạy extension trong chế độ debug

## Sử dụng

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Sử dụng một trong các cách sau:
   - Nhấn phím tắt `Ctrl+Alt+C` (Windows/Linux) hoặc `Cmd+Alt+C` (Mac)
   - Nhấn chuột phải trong editor và chọn "Auto Commit với Copilot" từ menu ngữ cảnh
   - Mở Command Palette (Ctrl+Shift+P) và gõ "Auto Commit với Copilot"

## Yêu cầu

- Visual Studio Code 1.60.0 trở lên
- GitHub Copilot extension đã được cài đặt và cấu hình 