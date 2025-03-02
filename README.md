# Auto Commit với Copilot

Dự án này cung cấp hai phương pháp để tự động hóa quy trình commit trong VS Code với Copilot:
1. Sử dụng script PowerShell với phím tắt
2. Sử dụng extension VS Code

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

### Cài đặt

#### Sử dụng script tự động
1. Chạy script `run-extension.ps1` để đóng gói và cài đặt extension:
   ```
   .\run-extension.ps1
   ```
2. Làm theo hướng dẫn trên màn hình để cài đặt extension

#### Từ VSIX
1. Đóng gói extension theo hướng dẫn trong file `extension/HƯỚNG_DẪN.md`
2. Mở VS Code
3. Nhấn F1 hoặc Ctrl+Shift+P để mở Command Palette
4. Gõ "Extensions: Install from VSIX" và chọn file VSIX đã tạo

#### Từ mã nguồn (chế độ debug)
1. Chạy script `debug-extension.ps1` để chuẩn bị và chạy extension trong chế độ debug:
   ```
   .\debug-extension.ps1
   ```
2. Làm theo hướng dẫn trên màn hình để chạy extension trong chế độ debug

### Cách sử dụng

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Sử dụng một trong các cách sau:
   - Nhấn phím tắt `Ctrl+Alt+C` (Windows/Linux) hoặc `Cmd+Alt+C` (Mac)
   - Nhấn chuột phải trong editor và chọn "Auto Commit với Copilot" từ menu ngữ cảnh
   - Mở Command Palette (Ctrl+Shift+P) và gõ "Auto Commit với Copilot"

### Yêu cầu

- Visual Studio Code 1.60.0 trở lên
- GitHub Copilot extension đã được cài đặt và cấu hình
- Node.js và npm

## Phát triển

### Môi trường ảo

Dự án này sử dụng môi trường ảo để quản lý dependencies:

1. Cài đặt virtualenv (nếu chưa có):
   ```
   python -m pip install virtualenv
   ```

2. Tạo môi trường ảo:
   ```
   python -m virtualenv venv
   ```

3. Kích hoạt môi trường ảo:
   - Windows (PowerShell):
     ```
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```
     .\venv\Scripts\activate.bat
     ```
   - Linux/Mac:
     ```
     source venv/bin/activate
     ```

4. Cài đặt dependencies cho extension:
   ```
   cd extension
   npm install
   ```

## Tùy chỉnh

- Phương pháp 1: Bạn có thể chỉnh sửa file `scripts/auto-commit.ps1` để thay đổi hành vi của script hoặc thay đổi phím tắt trong file `.vscode/keybindings.json`.
- Phương pháp 2: Bạn có thể chỉnh sửa mã nguồn của extension trong thư mục `extension/src`. 