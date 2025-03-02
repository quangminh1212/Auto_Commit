# Auto Commit với Copilot

Dự án này cung cấp một phím tắt để tự động hóa quy trình commit trong VS Code với Copilot.

## Tính năng

Khi nhấn phím tắt `Ctrl+Alt+C`, script sẽ tự động:
1. Mở panel Source Control
2. Gọi lệnh Generate Commit Message with Copilot
3. Thực hiện commit

## Cài đặt

1. Đảm bảo bạn đã cài đặt VS Code và GitHub Copilot
2. Clone repository này
3. Mở dự án trong VS Code
4. Phím tắt `Ctrl+Alt+C` đã được cấu hình trong file `.vscode/keybindings.json`

## Cách sử dụng

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Nhấn `Ctrl+Alt+C` để tự động tạo commit message và thực hiện commit

## Tùy chỉnh

Bạn có thể chỉnh sửa file `scripts/auto-commit.ps1` để thay đổi hành vi của script hoặc thay đổi phím tắt trong file `.vscode/keybindings.json`.

## Yêu cầu

- Visual Studio Code
- GitHub Copilot
- PowerShell 