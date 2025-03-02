import os
import sys
import json
import requests
import subprocess
import logging
import platform
import time
from datetime import datetime

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("auto_commit.log", mode="a")  # Thêm file log
    ]
)
logger = logging.getLogger('auto_commit')

# Cấu hình API Gemini
API_KEY = "YOUR_GEMINI_API_KEY"  # Thay thế bằng API key của bạn
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Kích thước tối đa của diff content để gửi đến API (để tránh vượt quá giới hạn)
MAX_DIFF_SIZE = 3000

# Biến toàn cục để kiểm soát chế độ mô phỏng
SIMULATION_MODE = False

def check_git_installed():
    """Kiểm tra xem Git đã được cài đặt chưa"""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("Git chưa được cài đặt hoặc không có trong PATH.")
        
        # Hỏi người dùng có muốn tiếp tục ở chế độ mô phỏng không
        print("\nGit không được tìm thấy trên hệ thống của bạn.")
        print("Bạn có thể:")
        print("1. Cài đặt Git từ https://git-scm.com/downloads")
        print("2. Tiếp tục ở chế độ mô phỏng (để kiểm tra chức năng)")
        
        choice = input("Bạn muốn tiếp tục ở chế độ mô phỏng không? (Y/N): ")
        if choice.lower() == 'y':
            global SIMULATION_MODE
            SIMULATION_MODE = True
            logger.info("Đã kích hoạt chế độ mô phỏng Git.")
            return True
        else:
            logger.error("Vui lòng cài đặt Git và thử lại.")
            return False

def check_api_key():
    """Kiểm tra xem API key đã được cấu hình chưa"""
    if API_KEY == "YOUR_GEMINI_API_KEY":
        logger.warning("API key chưa được cấu hình.")
        
        # Hỏi người dùng có muốn nhập API key không
        api_key = input("Nhập API key của Gemini (để trống để bỏ qua): ")
        if api_key.strip():
            # Cập nhật API key trong file
            try:
                with open(__file__, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                content = content.replace('API_KEY = "YOUR_GEMINI_API_KEY"', f'API_KEY = "{api_key}"')
                
                with open(__file__, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # Cập nhật biến toàn cục
                global API_KEY
                API_KEY = api_key
                
                logger.info("API key đã được cập nhật.")
                return True
            except Exception as e:
                logger.error(f"Lỗi khi cập nhật API key: {e}")
                return False
        else:
            logger.error("API key không được cung cấp. Quá trình commit có thể thất bại.")
            return False
    return True

def get_git_diff():
    """Lấy thông tin về các thay đổi trong git"""
    if SIMULATION_MODE:
        # Mô phỏng dữ liệu git diff trong chế độ mô phỏng
        logger.info("Đang mô phỏng git diff...")
        
        # Tạo danh sách các file trong thư mục hiện tại
        files = []
        for root, _, filenames in os.walk('.'):
            for filename in filenames:
                if not filename.startswith('.git') and not filename.endswith('.log'):
                    file_path = os.path.join(root, filename).replace('\\', '/')
                    if file_path.startswith('./'):
                        file_path = file_path[2:]
                    files.append(file_path)
        
        if not files:
            logger.info("Không tìm thấy file nào để mô phỏng staged changes.")
            return None
        
        # Tạo nội dung diff giả
        diff_content = "Simulated diff content:\n\n"
        for file in files[:5]:  # Giới hạn số lượng file để tránh quá nhiều dữ liệu
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read(500)  # Chỉ đọc 500 ký tự đầu tiên
                diff_content += f"--- a/{file}\n+++ b/{file}\n@@ -1,10 +1,10 @@\n{content}\n\n"
            except Exception:
                diff_content += f"Binary file {file} changed\n\n"
        
        return {
            "staged_files": files[:5],
            "diff_content": diff_content
        }
    
    try:
        # Kiểm tra xem có phải là git repository không
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Lấy danh sách các file đã thay đổi
        staged_files = subprocess.check_output(
            ["git", "diff", "--staged", "--name-only"], 
            text=True
        ).strip()
        
        if not staged_files:
            logger.info("Không có file nào được staged để commit.")
            return None
            
        # Lấy nội dung thay đổi
        diff_content = subprocess.check_output(
            ["git", "diff", "--staged"], 
            text=True
        ).strip()
        
        # Giới hạn kích thước diff_content để tránh vượt quá giới hạn của API
        if len(diff_content) > MAX_DIFF_SIZE:
            logger.warning(f"Nội dung diff quá lớn ({len(diff_content)} ký tự), sẽ được cắt ngắn.")
            diff_content = diff_content[:MAX_DIFF_SIZE] + "\n... (nội dung còn lại đã bị cắt bớt)"
        
        return {
            "staged_files": staged_files.split("\n"),
            "diff_content": diff_content
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"Lỗi khi lấy thông tin git: {e}")
        return None

def generate_commit_message(diff_info):
    """Tạo commit message bằng API Gemini"""
    if not diff_info:
        return None
    
    if not check_api_key():
        # Nếu không có API key, tạo commit message mặc định
        logger.warning("Sử dụng commit message mặc định do không có API key.")
        return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
    # Chuẩn bị prompt cho Gemini
    prompt = f"""
    Hãy tạo một commit message theo chuẩn Conventional Commits dựa trên các thay đổi sau:
    
    Files đã thay đổi:
    {', '.join(diff_info['staged_files'])}
    
    Nội dung thay đổi:
    {diff_info['diff_content']}
    
    Commit message nên tuân theo định dạng:
    <type>[optional scope]: <description>
    
    [optional body]
    
    [optional footer(s)]
    
    Trong đó:
    - type: feat (tính năng mới), fix (sửa lỗi), docs (tài liệu), style (định dạng), refactor (tái cấu trúc), perf (hiệu suất), test (kiểm thử), chore (công việc thường xuyên)
    - scope: phạm vi thay đổi (tùy chọn)
    - description: mô tả ngắn gọn về thay đổi
    - body: mô tả chi tiết hơn (tùy chọn)
    - footer: thông tin bổ sung như breaking changes, closed issues (tùy chọn)
    
    Chỉ trả về commit message, không cần giải thích thêm.
    """
    
    # Gọi API Gemini
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        }
    }
    
    try:
        logger.info("Đang gọi API Gemini để tạo commit message...")
        
        # Thêm thông báo đang xử lý
        print("Đang tạo commit message bằng AI, vui lòng đợi...")
        
        # Thử gọi API với số lần thử lại
        max_retries = 3
        retry_delay = 2  # Giây
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{API_URL}?key={API_KEY}",
                    headers=headers,
                    json=data,
                    timeout=30  # Thêm timeout để tránh treo
                )
                
                if response.status_code == 200:
                    result = response.json()
                    commit_message = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                    logger.info("Đã tạo commit message thành công.")
                    return commit_message
                elif response.status_code == 429:  # Rate limit
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        logger.warning(f"API rate limit, thử lại sau {wait_time} giây...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Đã vượt quá số lần thử lại. Lỗi: {response.status_code}")
                        logger.error(response.text)
                        return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                else:
                    logger.error(f"Lỗi khi gọi API Gemini: {response.status_code}")
                    logger.error(response.text)
                    return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    logger.warning(f"Lỗi kết nối, thử lại sau {wait_time} giây: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Đã vượt quá số lần thử lại. Lỗi: {e}")
                    return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    except (KeyError, IndexError) as e:
        logger.error(f"Lỗi khi xử lý kết quả từ API Gemini: {e}")
        return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def create_commit(commit_message):
    """Tạo commit với message đã tạo"""
    if not commit_message:
        return False
    
    if SIMULATION_MODE:
        # Mô phỏng tạo commit trong chế độ mô phỏng
        logger.info("Đang mô phỏng tạo commit...")
        print(f"\nMô phỏng commit với message:\n{commit_message}")
        
        # Tạo file giả lập lịch sử commit
        commit_history_file = "commit_history.txt"
        try:
            with open(commit_history_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {commit_message}\n")
            logger.info(f"Đã lưu commit message vào {commit_history_file}")
        except Exception as e:
            logger.error(f"Lỗi khi lưu commit history: {e}")
        
        return True
        
    try:
        logger.info("Đang tạo commit...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        logger.info(f"Đã tạo commit thành công với message:\n{commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Lỗi khi tạo commit: {e}")
        return False

def get_system_info():
    """Lấy thông tin hệ thống để gỡ lỗi"""
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "cwd": os.getcwd(),
    }
    
    # Kiểm tra Git
    try:
        git_version = subprocess.check_output(["git", "--version"], text=True).strip()
        info["git_version"] = git_version
    except:
        info["git_version"] = "Not installed or not in PATH"
    
    return info

def main():
    """Hàm chính của ứng dụng"""
    logger.info("Bắt đầu quá trình auto commit...")
    
    # Ghi thông tin hệ thống vào log
    system_info = get_system_info()
    logger.info(f"Thông tin hệ thống: {json.dumps(system_info, ensure_ascii=False)}")
    
    # Kiểm tra Git đã được cài đặt chưa
    if not check_git_installed():
        return
    
    # Kiểm tra xem có file nào được staged không
    diff_info = get_git_diff()
    if not diff_info:
        logger.info("Không có thay đổi nào để commit.")
        return
    
    # Tạo commit message
    commit_message = generate_commit_message(diff_info)
    if not commit_message:
        logger.error("Không thể tạo commit message.")
        return
    
    # Tạo commit
    success = create_commit(commit_message)
    
    if success and not SIMULATION_MODE:
        # Hỏi người dùng có muốn push không
        push_choice = input("\nBạn có muốn push lên remote repository không? (Y/N): ")
        if push_choice.lower() == 'y':
            try:
                logger.info("Đang push lên remote repository...")
                subprocess.run(["git", "push"], check=True)
                logger.info("Đã push lên remote repository thành công.")
            except subprocess.CalledProcessError as e:
                logger.error(f"Lỗi khi push lên remote repository: {e}")
                print("Bạn có thể push thủ công sau bằng lệnh: git push")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Quá trình đã bị hủy bởi người dùng.")
    except Exception as e:
        logger.exception(f"Đã xảy ra lỗi không mong muốn: {e}")
    finally:
        # Thông báo kết thúc
        print("\n=== Hoàn tất ===")
        if SIMULATION_MODE:
            print("Lưu ý: Ứng dụng đã chạy ở chế độ mô phỏng. Để sử dụng đầy đủ tính năng, vui lòng cài đặt Git.") 