# Auto Commit Tool

Công cụ tự động tạo commit message theo chuẩn Conventional Commits sử dụng API của Google Gemini.

## Tính năng

- Tự động phát hiện các thay đổi trong repository
- Tạo commit message theo chuẩn [Conventional Commits](https://www.conventionalcommits.org/) dựa trên nội dung thay đổi
- Sử dụng AI (Google Gemini) để phân tích thay đổi và tạo commit message phù hợp
- Hỗ trợ tự động push lên remote repository
- Tự động test và tối ưu mã nguồn
- Xử lý lỗi mạnh mẽ và logging chi tiết
- Kiểm tra tự động các yêu cầu hệ thống
- Chế độ mô phỏng khi Git không được cài đặt
- Tự động cài đặt các thư viện cần thiết
- Tự động thử lại khi gặp lỗi kết nối API

## Yêu cầu

- Python 3.6 trở lên
- Git đã được cài đặt và cấu hình (tùy chọn, có thể chạy ở chế độ mô phỏng)
- API key của Google Gemini (tùy chọn, có thể sử dụng commit message mặc định)

## Cài đặt

1. Clone repository này:
   ```
   git clone <repository_url>
   cd auto-commit-tool
   ```

2. Cài đặt các thư viện Python cần thiết:
   ```
   pip install -r requirements.txt
   ```
   Hoặc chạy trực tiếp `auto_commit.bat` hoặc `test_and_optimize.bat`, các thư viện sẽ được cài đặt tự động.

3. Cấu hình API key:
   - Đăng ký và lấy API key từ [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Mở file `auto_commit.py` và thay thế `YOUR_GEMINI_API_KEY` bằng API key của bạn
   - Hoặc chạy `auto_commit.bat` và nhập API key khi được yêu cầu

## Cách sử dụng

1. Thực hiện các thay đổi trong dự án của bạn

2. Chạy file batch để tự động commit:
   ```
   auto_commit.bat
   ```

3. Nếu Git không được cài đặt, bạn sẽ được hỏi có muốn tiếp tục ở chế độ mô phỏng không
   - Chọn Y để tiếp tục ở chế độ mô phỏng
   - Chọn N để thoát và cài đặt Git

4. Nếu có các file chưa được staged, công cụ sẽ hỏi bạn có muốn stage tất cả không
   - Chọn Y để stage tất cả các thay đổi
   - Chọn N để thoát và stage thủ công

5. Công cụ sẽ hỏi bạn có muốn chạy test trước khi commit không
   - Chọn Y để chạy test
   - Chọn N để bỏ qua test

6. Công cụ sẽ tự động tạo commit message dựa trên các thay đổi và thực hiện commit

7. Sau khi commit thành công, công cụ sẽ hỏi bạn có muốn push lên remote repository không

## Chế độ mô phỏng

Khi Git không được cài đặt hoặc thư mục hiện tại không phải là git repository, công cụ có thể chạy ở chế độ mô phỏng:

- Mô phỏng các thay đổi dựa trên các file trong thư mục hiện tại
- Tạo commit message bằng API Gemini (nếu có API key) hoặc sử dụng message mặc định
- Lưu commit message vào file `commit_history.txt` thay vì thực hiện commit thật
- Vẫn chạy được các test và tối ưu

Chế độ mô phỏng giúp bạn:
- Kiểm tra chức năng của công cụ mà không cần cài đặt Git
- Thử nghiệm tạo commit message trước khi áp dụng vào repository thật
- Học cách sử dụng công cụ trong môi trường an toàn

## Test và Tối ưu

Công cụ này cung cấp tính năng tự động test và tối ưu:

1. Chạy file batch để test và tối ưu:
   ```
   test_and_optimize.bat
   ```

2. Quá trình này sẽ:
   - Kiểm tra các yêu cầu hệ thống (Python, Git)
   - Cài đặt các thư viện cần thiết
   - Chạy các test case để đảm bảo tất cả các chức năng hoạt động đúng
   - Tối ưu mã nguồn dựa trên kết quả test
   - Kiểm tra và cập nhật API key nếu cần

3. Bạn cũng có thể chạy test trước mỗi lần commit bằng cách chọn Y khi được hỏi trong quá trình commit

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

## Cấu trúc dự án

- `auto_commit.py`: Script Python chính để tạo commit message và thực hiện commit
- `auto_commit.bat`: File batch để chạy quá trình commit
- `test_auto_commit.py`: Script Python để test các chức năng
- `test_and_optimize.bat`: File batch để chạy test và tối ưu
- `requirements.txt`: Danh sách các thư viện Python cần thiết
- `auto_commit.log`: File log ghi lại các hoạt động của ứng dụng
- `commit_history.txt`: Lịch sử commit trong chế độ mô phỏng

## Tùy chỉnh

Bạn có thể tùy chỉnh các tham số trong file `auto_commit.py`:

- `MAX_DIFF_SIZE`: Kích thước tối đa của diff content để gửi đến API (mặc định: 3000 ký tự)
- `SIMULATION_MODE`: Bật/tắt chế độ mô phỏng thủ công (mặc định: False)
- Prompt cho Gemini: Bạn có thể thay đổi prompt để tạo commit message theo ý muốn

## Xử lý lỗi

Công cụ này bao gồm xử lý lỗi mạnh mẽ:

- Kiểm tra tự động các yêu cầu hệ thống (Python, Git)
- Kiểm tra API key đã được cấu hình chưa
- Xử lý các lỗi khi gọi API Gemini với cơ chế thử lại
- Logging chi tiết vào file `auto_commit.log` để dễ dàng gỡ lỗi
- Chế độ mô phỏng khi không có Git
- Tự động cài đặt các thư viện cần thiết

## Giấy phép

MIT 