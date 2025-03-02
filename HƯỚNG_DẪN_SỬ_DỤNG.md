# Hướng dẫn sử dụng Auto Commit với Copilot

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

## Sử dụng extension

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Nhấn phím tắt `Ctrl+Space` để tự động:
   - Mở panel Source Control
   - Tạo commit message với Copilot
   - Thực hiện commit

## Gỡ cài đặt extension

### Cách 1: Sử dụng script

Chạy file `uninstall-extension.bat` để gỡ cài đặt extension:
```
.\uninstall-extension.bat
```

### Cách 2: Từ VS Code

1. Mở VS Code
2. Nhấn Ctrl+Shift+X để mở Extensions view
3. Tìm "Auto Commit với Copilot" trong danh sách các extension đã cài đặt
4. Nhấn nút "Uninstall"

## Phương pháp thay thế: Script PowerShell

Ngoài extension, dự án này còn cung cấp một script PowerShell để tự động hóa quy trình commit.

### Tính năng

Khi nhấn phím tắt `Ctrl+Alt+C`, script sẽ tự động:
1. Mở panel Source Control
2. Gọi lệnh Generate Commit Message with Copilot
3. Thực hiện commit

### Cách sử dụng

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Nhấn `Ctrl+Alt+C` để tự động tạo commit message và thực hiện commit

### Yêu cầu

- Visual Studio Code
- GitHub Copilot
- PowerShell

## Cấu trúc dự án

- `auto-commit-setup.bat`: Script chính để cài đặt và thiết lập tất cả
- `uninstall-extension.bat`: Script để gỡ cài đặt extension
- `create-installer.iss`: File cấu hình Inno Setup để tạo file cài đặt EXE
- `install-extension.bat`: Script để cài đặt extension từ file VSIX
- `extension/`: Thư mục chứa mã nguồn của extension
  - `src/`: Mã nguồn TypeScript
  - `package.json`: Cấu hình extension
- `scripts/`: Thư mục chứa các script PowerShell

## Tùy chỉnh

- **Script PowerShell**: Bạn có thể chỉnh sửa file `scripts/auto-commit.ps1` để thay đổi hành vi của script hoặc thay đổi phím tắt trong file `.vscode/keybindings.json`.
- **Extension**: Bạn có thể chỉnh sửa mã nguồn của extension trong thư mục `extension/src`. 