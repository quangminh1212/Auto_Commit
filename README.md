# Auto Commit VSCode Extension

Extension VS Code tự động tạo commit cho các thay đổi trong Git repository

## Tính năng

- Tự động theo dõi thay đổi file trong workspace
- Tạo commit message dựa trên loại file
- Tùy chọn tự động push
- Hiển thị trạng thái trên thanh status bar
- Cấu hình linh hoạt

## Cài đặt

1. Mở VS Code
2. Mở Extensions (Ctrl+Shift+X)
3. Tìm "Auto Commit"
4. Click Install

## Sử dụng

1. Mở Command Palette (Ctrl+Shift+P)
2. Gõ "Auto Commit" để xem các lệnh có sẵn:
   - Enable Auto Commit: Bật tự động commit
   - Disable Auto Commit: Tắt tự động commit

## Cấu hình

Mở Settings (Ctrl+,) và tìm "Auto Commit" để điều chỉnh:
- Delay time trước khi tạo commit
- Bật/tắt tự động push
- Các tùy chọn khác

## License

MIT License

.
├── config/
│   └── settings.yaml
├── src/
│   ├── core/
│   │   ├── file_watcher.py
│   │   └── git_handler.py
│   ├── utils/
│   │   └── config.py
│   └── main.py
├��─ requirements.txt
└── run.py