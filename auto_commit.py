import os
import sys
import json
import requests
import subprocess
import logging
from datetime import datetime

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('auto_commit')

# Cấu hình API Gemini
API_KEY = "YOUR_GEMINI_API_KEY"  # Thay thế bằng API key của bạn
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Kích thước tối đa của diff content để gửi đến API (để tránh vượt quá giới hạn)
MAX_DIFF_SIZE = 3000

def check_git_installed():
    """Kiểm tra xem Git đã được cài đặt chưa"""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.error("Git chưa được cài đặt hoặc không có trong PATH. Vui lòng cài đặt Git.")
        return False

def check_api_key():
    """Kiểm tra xem API key đã được cấu hình chưa"""
    if API_KEY == "YOUR_GEMINI_API_KEY":
        logger.error("API key chưa được cấu hình. Vui lòng cập nhật API_KEY trong file auto_commit.py.")
        return False
    return True

def get_git_diff():
    """Lấy thông tin về các thay đổi trong git"""
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
        return None
        
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
        else:
            logger.error(f"Lỗi khi gọi API Gemini: {response.status_code}")
            logger.error(response.text)
            return None
    except requests.RequestException as e:
        logger.error(f"Lỗi khi gọi API Gemini: {e}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Lỗi khi xử lý kết quả từ API Gemini: {e}")
        return None

def create_commit(commit_message):
    """Tạo commit với message đã tạo"""
    if not commit_message:
        return False
        
    try:
        logger.info("Đang tạo commit...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        logger.info(f"Đã tạo commit thành công với message:\n{commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Lỗi khi tạo commit: {e}")
        return False

def main():
    """Hàm chính của ứng dụng"""
    logger.info("Bắt đầu quá trình auto commit...")
    
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
    create_commit(commit_message)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Quá trình đã bị hủy bởi người dùng.")
    except Exception as e:
        logger.exception(f"Đã xảy ra lỗi không mong muốn: {e}") 