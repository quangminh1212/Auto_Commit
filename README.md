# Auto Commit

Một công cụ tự động theo dõi và commit các thay đổi trong repository Git.

## 🌟 Tính năng

- 🔄 Tự động theo dõi thay đổi file trong thời gian thực
- 📝 Tự động tạo commit với message chuẩn hóa
- 🎨 Phân loại commit theo loại file
- 🚀 Tự động push lên GitHub (tùy chọn)
- 🎯 Bỏ qua các file không cần thiết (git, cache, etc.)
- 🌈 Giao diện dòng lệnh với thông báo màu sắc

## 📋 Yêu cầu

- Python 3.8 trở lên
- Git đã được cài đặt và cấu hình
- (Tùy chọn) GitHub token cho tính năng tự động push

## 🚀 Cài đặt

1. Clone repository:
```

2. Tạo và kích hoạt môi trường ảo:
```

3. Cài đặt package:
```

## ⚙️ Cấu hình

Tạo hoặc chỉnh sửa file `config/settings.yaml`:

```yaml
# Repository settings
repo_path: "."          # Đường dẫn đến repository
watch_path: "."         # Đường dẫn cần theo dõi
github_token: ""        # GitHub token (tùy chọn)

# Commit settings
commit_delay: 30        # Độ trễ giữa các commit (giây)
```

## 🎮 Sử dụng

1. Chạy chương trình:
```bash
python run.py
```

2. Hoặc với file cấu hình tùy chỉnh:
```bash
python run.py --config path/to/config.yaml
```

3. Bật chế độ verbose:
```bash
python run.py --verbose
```

## 🏷️ Quy ước Commit

Commit messages được tạo tự động theo format:
- `feat: ` cho file Python
- `docs: ` cho file Markdown
- `config: ` cho file YAML/JSON
- `chore: ` cho các file khác

Ví dụ:
- `feat: add user_service.py`
- `docs: update README.md`
- `config: modify settings.yaml`

## 🔍 Cấu trúc dự án

```
auto-commit/
├── src/
│   └── auto_commit/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── git.py
│       │   └── watcher.py
│       └── config/
│           ├── __init__.py
│           └── settings.py
├── config/
│   └── settings.yaml
├── tests/
├── pyproject.toml
└── README.md
```

## 🐛 Xử lý sự cố

1. **Lỗi Permission**: Đảm bảo bạn có quyền ghi vào repository

2. **Lỗi Git**: Kiểm tra cấu hình git:
```bash
git config --list
```

3. **Lỗi GitHub**: Kiểm tra token có đúng và còn hạn

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy:
1. Fork dự án
2. Tạo branch mới
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📝 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 👥 Tác giả

- Tên của bạn - [GitHub](link_github_của_bạn)

## 🙏 Cảm ơn

- [Watchdog](https://github.com/gorakhargosh/watchdog)
- [GitPython](https://github.com/gitpython-developers/GitPython)
- [PyGithub](https://github.com/PyGithub/PyGithub)
- [Rich](https://github.com/Textualize/rich)
- [Typer](https://github.com/tiangolo/typer)
```

Commit message: `docs: add comprehensive project documentation to README`