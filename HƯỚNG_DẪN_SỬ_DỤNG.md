# Hướng dẫn sử dụng Auto Commit với Copilot

## Cài đặt công cụ

Trước khi bắt đầu, bạn cần cài đặt các công cụ cần thiết:

1. Chạy file `setup-tools.bat` để cài đặt các công cụ cần thiết:
   ```
   .\setup-tools.bat
   ```

   Script này sẽ:
   - Kiểm tra và cài đặt Node.js và npm (nếu chưa có)
   - Cài đặt vsce (VS Code Extension Manager)
   - Hướng dẫn cài đặt Inno Setup (nếu chưa có)
   - Cài đặt dependencies cho extension

## Đóng gói extension

Có hai cách để đóng gói extension:

### Cách 1: Chỉ đóng gói thành file VSIX

Chạy file `package-extension.bat` để đóng gói extension thành file VSIX:
```
.\package-extension.bat
```

File VSIX sẽ được tạo tại: `extension\auto-commit-copilot-0.0.1.vsix`

### Cách 2: Tạo file cài đặt EXE

Chạy file `build-installer.bat` để tạo file cài đặt EXE:
```
.\build-installer.bat
```

File EXE sẽ được tạo tại: `Auto-Commit-Installer.exe`

## Cài đặt extension

Có ba cách để cài đặt extension:

### Cách 1: Từ file VSIX

1. Mở VS Code
2. Nhấn F1 hoặc Ctrl+Shift+P để mở Command Palette
3. Gõ "Extensions: Install from VSIX" và chọn file VSIX đã tạo

### Cách 2: Từ file EXE

1. Chạy file `Auto-Commit-Installer.exe`
2. Làm theo hướng dẫn trên màn hình để cài đặt extension

### Cách 3: Từ Command Line

Chạy lệnh sau để cài đặt extension:
```
code --install-extension extension\auto-commit-copilot-0.0.1.vsix
```

## Sử dụng extension

1. Thực hiện các thay đổi trong dự án của bạn
2. Stage các thay đổi bạn muốn commit
3. Nhấn phím tắt `Ctrl+Space` để tự động:
   - Mở panel Source Control
   - Tạo commit message với Copilot
   - Thực hiện commit

## Gỡ cài đặt extension

1. Mở VS Code
2. Nhấn Ctrl+Shift+X để mở Extensions view
3. Tìm "Auto Commit với Copilot" trong danh sách các extension đã cài đặt
4. Nhấn nút "Uninstall"

## Phát triển extension

Nếu bạn muốn phát triển extension:

1. Mở thư mục extension trong VS Code:
   ```
   code extension
   ```

2. Chỉnh sửa mã nguồn trong thư mục `src`

3. Nhấn F5 để chạy extension trong chế độ debug 