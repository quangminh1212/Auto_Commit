# Auto Commit với Copilot

Dự án này cung cấp hai phương pháp để tự động hóa quy trình commit trong VS Code với Copilot:
1. Sử dụng script PowerShell với phím tắt
2. Sử dụng extension VS Code

## Cài đặt và cấu hình tự động

Để thực hiện tất cả các bước từ cài đặt công cụ đến tạo file cài đặt và cài đặt extension, chạy file `run-all.bat`:

```
.\run-all.bat
```

Script này sẽ:
1. Cài đặt tất cả các công cụ cần thiết
2. Đóng gói extension thành file VSIX
3. Tạo file cài đặt EXE
4. Hỏi bạn có muốn cài đặt extension không

## Cài đặt nhanh

Để cài đặt extension một cách nhanh chóng, chỉ cần chạy file `quick-install.bat`:
```
.\quick-install.bat
```

Script này sẽ tự động đóng gói và cài đặt extension vào VS Code của bạn.

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

#### Cài đặt nhanh
Chạy file `quick-install.bat` để cài đặt extension một cách nhanh chóng:
```
.\quick-install.bat
```

#### Sử dụng file Executable (EXE)
1. Chạy file `build-installer.bat` để tạo file cài đặt:
   ```
   .\build-installer.bat
   ```
2. Chạy file `Auto-Commit-Installer.exe` và làm theo hướng dẫn để cài đặt extension
3. Khởi động lại VS Code sau khi cài đặt

#### Sử dụng file VSIX
1. Chạy file `package-extension.bat` để đóng gói extension:
   ```
   .\package-extension.bat
   ```
2. Mở VS Code
3. Nhấn F1 hoặc Ctrl+Shift+P để mở Command Palette
4. Gõ "Extensions: Install from VSIX" và chọn file `extension\auto-commit-copilot-0.0.1.vsix`

#### Từ mã nguồn (chế độ debug)
1. Chạy script `debug-extension.bat` để chuẩn bị và chạy extension trong chế độ debug:
   ```
   .\debug-extension.bat
   ```
2. Làm theo hướng dẫn trên màn hình để chạy extension trong chế độ debug

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

## Phát triển

### Cài đặt công cụ

Chạy file `setup-tools.bat` để cài đặt các công cụ cần thiết:
```
.\setup-tools.bat
```

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

## Hướng dẫn chi tiết

Xem file `HƯỚNG_DẪN_SỬ_DỤNG.md` để biết thêm chi tiết về cách sử dụng các script và công cụ. 