# Auto_Commit

Ứng dụng tự động tạo commit cho các thay đổi trong Git repository

## Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.x
- **Thư viện chính:**
  - watchdog: Theo dõi thay đổi file system
  - GitPython: Tương tác với Git
  - PyYAML: Đọc file cấu hình YAML
  - PyGithub: Tương tác với GitHub API
  - logging: Ghi log hệ thống
  - schedule: Lập lịch tự động

## Tính năng chi tiết

### Quản lý File
- Theo dõi thay đổi real-time trong thư mục được chỉ định
- Phát hiện file mới, file bị xóa, file được sửa đổi
- Lọc file theo pattern (gitignore)

### Xử lý Git
- Tự động git add cho files thay đổi
- Tạo commit message theo template
- Hỗ trợ multiple repositories
- Push tự động lên remote repository

### Tích hợp GitHub
- Xác thực qua GitHub API
- Tạo/Cập nhật Pull Request
- Quản lý branch

### Cấu hình & Quản lý
- Cấu hình qua file YAML
- Ghi log chi tiết
- Lập lịch commit tự động
- Thông báo qua email/webhook

## Tính năng

- Tự động theo dõi thay đổi trong thư mục được chỉ định
- Tự động tạo commit message dựa trên loại thay đổi
- Hỗ trợ đồng bộ với GitHub
- Cấu hình linh hoạt thông qua file settings.yaml
- Ghi log đầy đủ các hoạt động

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/your-username/Auto_Commit.git
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Cấu hình trong file `config/settings.yaml`

## Sử dụng

1. Chạy ứng dụng:
```bash
python src/main.py
```

2. Ứng dụng sẽ tự động:
- Theo dõi các thay đổi trong thư mục
- Tạo commit khi phát hiện thay đổi
- Push lên GitHub (nếu được cấu hình)

## Cấu trúc dự án

```
Auto_Commit/
├── src/
│   ├── core/           # Core functionality
│   ├── utils/          # Utility modules
│   └── main.py         # Entry point
├── tests/              # Unit tests
├── config/             # Configuration files
└── requirements.txt    # Dependencies
```

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.

## License

MIT License