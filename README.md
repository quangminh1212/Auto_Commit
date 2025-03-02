# Auto Commit với Copilot

Dự án này cung cấp hai phương pháp để tự động hóa quy trình commit trong VS Code với Copilot:
1. Sử dụng script PowerShell với phím tắt
2. Sử dụng extension VS Code

## Cài đặt nhanh (Một bước duy nhất)

Để cài đặt và thiết lập tất cả mọi thứ chỉ với một bước duy nhất, chạy file `auto-commit-setup.bat`:

```
.\auto-commit-setup.bat
```

Script này sẽ tự động:
1. Kiểm tra và hướng dẫn cài đặt các công cụ cần thiết (VS Code, Node.js, Inno Setup)
2. Cài đặt vsce và các dependencies
3. Biên dịch TypeScript
4. Đóng gói extension thành file VSIX
5. Tạo file cài đặt EXE (nếu Inno Setup đã được cài đặt)
6. Cài đặt extension vào VS Code (nếu bạn chọn)

> **Lưu ý**: Nên chạy script với quyền Administrator để đảm bảo quá trình cài đặt diễn ra suôn sẻ.

## Phương pháp 1: Script PowerShell

### Tính năng

Khi nhấn phím tắt `Ctrl+Alt+C`, script sẽ tự động:
1. Mở panel Source Control
2. Gọi lệnh Generate Commit Message with Copilot
3. Thực hiện commit

### Cài đặt

1. Đảm bảo bạn đã cài đặt VS Code và GitHub Copilot
2. Clone repository này
3. Mở dự án trong VS Code
4. Phím tắt `Ctrl+Alt+C` đã được cấu hình trong file `.vscode/keybindings.json`

### Cách sử dụng

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Nhấn `Ctrl+Alt+C` để tự động tạo commit message và thực hiện commit

### Yêu cầu

- Visual Studio Code
- GitHub Copilot
- PowerShell

## Phương pháp 2: Extension VS Code

### Tính năng

Extension này cung cấp một lệnh và phím tắt để tự động:
1. Mở panel Source Control
2. Gọi lệnh Generate Commit Message with Copilot
3. Thực hiện commit

### Cách sử dụng

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Sử dụng một trong các cách sau:
   - Nhấn phím tắt `Ctrl+Space` (Windows/Linux) hoặc `Cmd+Space` (Mac)
   - Nhấn chuột phải trong editor và chọn "Auto Commit với Copilot" từ menu ngữ cảnh
   - Mở Command Palette (Ctrl+Shift+P) và gõ "Auto Commit với Copilot"

### Yêu cầu

- Visual Studio Code 1.60.0 trở lên
- GitHub Copilot extension đã được cài đặt và cấu hình
- Node.js và npm

## Gỡ cài đặt extension

1. Mở VS Code
2. Nhấn Ctrl+Shift+X để mở Extensions view
3. Tìm "Auto Commit với Copilot" trong danh sách các extension đã cài đặt
4. Nhấn nút "Uninstall"

## Tùy chỉnh

- Phương pháp 1: Bạn có thể chỉnh sửa file `scripts/auto-commit.ps1` để thay đổi hành vi của script hoặc thay đổi phím tắt trong file `.vscode/keybindings.json`.
- Phương pháp 2: Bạn có thể chỉnh sửa mã nguồn của extension trong thư mục `extension/src`.

## Hướng dẫn chi tiết

Xem file `HƯỚNG_DẪN_SỬ_DỤNG.md` để biết thêm chi tiết về cách sử dụng các script và công cụ. 