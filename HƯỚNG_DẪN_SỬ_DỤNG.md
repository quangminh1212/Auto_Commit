# Hướng dẫn sử dụng Auto Commit với Copilot

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

## Cài đặt nhanh

Để cài đặt extension một cách nhanh chóng, chạy file `quick-install.bat`:

```
.\quick-install.bat
```

Script này sẽ:
1. Kiểm tra xem VS Code đã được cài đặt chưa
2. Tạo file VSIX nếu cần
3. Cài đặt extension vào VS Code

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

Có bốn cách để cài đặt extension:

### Cách 1: Cài đặt nhanh

Chạy file `quick-install.bat` để cài đặt extension một cách nhanh chóng:
```
.\quick-install.bat
```

### Cách 2: Từ file VSIX

1. Mở VS Code
2. Nhấn F1 hoặc Ctrl+Shift+P để mở Command Palette
3. Gõ "Extensions: Install from VSIX" và chọn file VSIX đã tạo

### Cách 3: Từ file EXE

1. Chạy file `Auto-Commit-Installer.exe`
2. Làm theo hướng dẫn trên màn hình để cài đặt extension

### Cách 4: Từ Command Line

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

## Phát triển extension

### Chạy extension trong chế độ debug

Để chạy extension trong chế độ debug, chạy file `debug-extension.bat`:

```
.\debug-extension.bat
```

Script này sẽ:
1. Biên dịch TypeScript
2. Mở VS Code với extension trong chế độ debug
3. Bạn có thể nhấn F5 trong VS Code để bắt đầu debug extension

### Chỉnh sửa mã nguồn

1. Mở thư mục extension trong VS Code:
   ```
   code extension
   ```
2. Chỉnh sửa mã nguồn trong thư mục `src`
3. Biên dịch TypeScript bằng cách chạy `npm run compile` hoặc nhấn Ctrl+Shift+B
4. Chạy extension trong chế độ debug bằng cách nhấn F5

## Các file script

- `run-all.bat`: Chạy tất cả các bước từ cài đặt công cụ đến tạo file cài đặt
- `setup-tools.bat`: Cài đặt tất cả các công cụ cần thiết
- `package-extension.bat`: Đóng gói extension thành file VSIX
- `build-installer.bat`: Tạo file cài đặt EXE
- `quick-install.bat`: Cài đặt extension một cách nhanh chóng
- `run-extension.bat`: Chạy extension
- `debug-extension.bat`: Chạy extension trong chế độ debug
- `uninstall-extension.bat`: Gỡ cài đặt extension
- `install-extension.bat`: Cài đặt extension từ file VSIX

## Cấu trúc dự án

- `extension/`: Thư mục chứa mã nguồn của extension
  - `src/`: Mã nguồn TypeScript
  - `package.json`: Cấu hình extension
- `scripts/`: Thư mục chứa các script PowerShell
- `create-installer.iss`: File cấu hình Inno Setup để tạo file cài đặt EXE
- `*.bat`: Các file batch để tự động hóa các tác vụ 