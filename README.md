# Auto Commit Tool

Công cụ tự động tạo commit message theo chuẩn Conventional Commits sử dụng API của Google Gemini.

## Tính năng

- Tự động phát hiện các thay đổi trong repository
- Tạo commit message theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/) dựa trên nội dung thay đổi
- Sử dụng AI (Google Gemini) để phân tích thay đổi và tạo commit message phù hợp
- Hỗ trợ tự động push lên remote repository

## Yêu cầu

- Python 3.6 trở lên
- Git đã được cài đặt và cấu hình
- API key của Google Gemini

## Cài đặt

1. Clone repository này:
   ```
   git clone <repository_url>
   cd auto-commit-tool
   ```

2. Cài đặt các thư viện Python cần thiết:
   ```
   pip install requests
   ```

3. Cấu hình API key:
   - Đăng ký và lấy API key từ [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Mở file `auto_commit.py` và thay thế `YOUR_GEMINI_API_KEY` bằng API key của bạn

## Cách sử dụng

1. Thực hiện các thay đổi trong dự án của bạn

2. Chạy file batch để tự động commit:
   ```
   auto_commit.bat
   ```

3. Nếu có các file chưa được staged, công cụ sẽ hỏi bạn có muốn stage tất cả không
   - Chọn Y để stage tất cả các thay đổi
   - Chọn N để thoát và stage thủ công

4. Công cụ sẽ tự động tạo commit message dựa trên các thay đổi và thực hiện commit

5. Sau khi commit thành công, công cụ sẽ hỏi bạn có muốn push lên remote repository không

## Cấu trúc Conventional Commits

Commit message được tạo theo chuẩn Conventional Commits với định dạng:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Trong đó:
- **type**: Loại thay đổi (feat, fix, docs, style, refactor, perf, test, chore)
- **scope**: Phạm vi thay đổi (tùy chọn)
- **description**: Mô tả ngắn gọn về thay đổi
- **body**: Mô tả chi tiết hơn (tùy chọn)
- **footer**: Thông tin bổ sung như breaking changes, closed issues (tùy chọn)

## Tùy chỉnh

Bạn có thể tùy chỉnh prompt trong file `auto_commit.py` để thay đổi cách AI tạo commit message.

## Giấy phép

MIT 