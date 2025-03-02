# Auto Commit

Ứng dụng tự động tạo commit message bằng Gemini API.

## Tính năng

- Tự động tạo commit message theo chuẩn Conventional Commits dựa trên các thay đổi trong Git
- Giao diện đồ họa dễ sử dụng
- Hỗ trợ chọn repository
- Cấu hình API key và các thông số khác
- Xem thông tin diff và commit
- Tự động push lên remote repository (tùy chọn)

## Cài đặt

1. Cài đặt Python 3.8 trở lên
2. Cài đặt Git
3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Cách sử dụng

### Chạy ứng dụng giao diện đồ họa

```bash
python auto_commit_gui.py
```

### Chạy ứng dụng dòng lệnh

```bash
python auto_commit.py
```

## Cấu hình

Bạn có thể cấu hình các thông số sau trong ứng dụng:

- **API Key Gemini**: API key để sử dụng Gemini API
- **Kích thước tối đa của diff**: Giới hạn kích thước dữ liệu diff gửi đến API
- **Số lần thử lại tối đa**: Số lần thử lại khi gọi API bị lỗi
- **Thời gian chờ giữa các lần thử lại**: Thời gian chờ (giây) giữa các lần thử lại
- **Chế độ mô phỏng**: Chạy ứng dụng ở chế độ mô phỏng (không cần Git)

## Quy trình làm việc

1. Mở ứng dụng
2. Chọn repository (hoặc sử dụng repository hiện tại)
3. Cấu hình API key và các thông số khác (nếu cần)
4. Stage các thay đổi bằng Git (`git add .` hoặc `git add <file>`)
5. Nhấn "Tạo commit message" để tạo commit message bằng AI
6. Kiểm tra và chỉnh sửa commit message nếu cần
7. Nhấn "Commit" để tạo commit
8. Chọn "Auto push" nếu muốn tự động push lên remote repository

## Lưu ý

- Bạn cần có API key của Gemini để sử dụng tính năng tạo commit message bằng AI
- Nếu không có API key, ứng dụng sẽ sử dụng commit message mặc định
- Ứng dụng yêu cầu Git được cài đặt và có trong PATH

## Giấy phép

MIT 