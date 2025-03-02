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
        logging.FileHandler("auto_commit.log", mode="a", encoding="utf-8")  # Thêm encoding utf-8
    ]
)
logger = logging.getLogger('auto_commit')

# Cấu hình API Gemini
API_KEY = "AIzaSyBkOqbY_bvU2TYOCiZSLQX5z56w9hWxlww"  # API key đã được cập nhật
API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"  # URL API đã được cập nhật

# Kích thước tối đa của diff content để gửi đến API (để tránh vượt quá giới hạn)
MAX_DIFF_SIZE = 3000

# Biến toàn cục để kiểm soát chế độ mô phỏng
SIMULATION_MODE = True  # Đã thay đổi thành True để chạy ở chế độ mô phỏng

def check_git_installed():
    """Kiểm tra xem Git đã được cài đặt chưa"""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("Git chua duoc cai dat hoac khong co trong PATH.")
        
        # Hỏi người dùng có muốn tiếp tục ở chế độ mô phỏng không
        print("\nGit khong duoc tim thay tren he thong cua ban.")
        print("Ban co the:")
        print("1. Cai dat Git tu https://git-scm.com/downloads")
        print("2. Tiep tuc o che do mo phong (de kiem tra chuc nang)")
        
        choice = input("Ban muon tiep tuc o che do mo phong khong? (Y/N): ")
        if choice.lower() == 'y':
            global SIMULATION_MODE
            SIMULATION_MODE = True
            logger.info("Da kich hoat che do mo phong Git.")
            return True
        else:
            logger.error("Vui long cai dat Git va thu lai.")
            return False

def check_api_key():
    """Kiểm tra xem API key đã được cấu hình chưa"""
    global API_KEY
    if API_KEY == "YOUR_GEMINI_API_KEY":
        logger.warning("API key chua duoc cau hinh.")
        
        # Hỏi người dùng có muốn nhập API key không
        api_key = input("Nhap API key cua Gemini (de trong de bo qua): ")
        if api_key.strip():
            # Cập nhật API key trong file
            try:
                with open(__file__, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                content = content.replace('API_KEY = "YOUR_GEMINI_API_KEY"', f'API_KEY = "{api_key}"')
                
                with open(__file__, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # Cập nhật biến toàn cục
                API_KEY = api_key
                
                logger.info("API key da duoc cap nhat.")
                return True
            except Exception as e:
                logger.error(f"Loi khi cap nhat API key: {e}")
                return False
        else:
            logger.error("API key khong duoc cung cap. Qua trinh commit co the that bai.")
            return False
    return True

def get_git_diff():
    """Lấy thông tin về các thay đổi trong git"""
    if SIMULATION_MODE:
        # Mô phỏng dữ liệu git diff trong chế độ mô phỏng
        logger.info("Dang mo phong git diff...")
        
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
            logger.info("Khong tim thay file nao de mo phong staged changes.")
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
            logger.info("Khong co file nao duoc staged de commit.")
            return None
            
        # Lấy nội dung thay đổi
        diff_content = subprocess.check_output(
            ["git", "diff", "--staged"], 
            text=True
        ).strip()
        
        # Giới hạn kích thước diff_content để tránh vượt quá giới hạn của API
        if len(diff_content) > MAX_DIFF_SIZE:
            logger.warning(f"Noi dung diff qua lon ({len(diff_content)} ky tu), se duoc cat ngan.")
            diff_content = diff_content[:MAX_DIFF_SIZE] + "\n... (noi dung con lai da bi cat bot)"
        
        return {
            "staged_files": staged_files.split("\n"),
            "diff_content": diff_content
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"Loi khi lay thong tin git: {e}")
        return None

def generate_commit_message(diff_info):
    """Tạo commit message bằng API Gemini"""
    if not diff_info:
        return None
    
    if not check_api_key():
        # Nếu không có API key, tạo commit message mặc định
        logger.warning("Su dung commit message mac dinh do khong co API key.")
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
        logger.info("Dang goi API Gemini de tao commit message...")
        
        # Thêm thông báo đang xử lý
        print("Dang tao commit message bang AI, vui long doi...")
        
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
                    logger.info("Da tao commit message thanh cong.")
                    return commit_message
                elif response.status_code == 429:  # Rate limit
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        logger.warning(f"API rate limit, thu lai sau {wait_time} giay...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Da vuot qua so lan thu lai. Loi: {response.status_code}")
                        logger.error(response.text)
                        return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                else:
                    logger.error(f"Loi khi goi API Gemini: {response.status_code}")
                    logger.error(response.text)
                    return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    logger.warning(f"Loi ket noi, thu lai sau {wait_time} giay: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Da vuot qua so lan thu lai. Loi: {e}")
                    return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    except (KeyError, IndexError) as e:
        logger.error(f"Loi khi xu ly ket qua tu API Gemini: {e}")
        return f"chore: auto commit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def create_commit(commit_message):
    """Tạo commit với message đã tạo"""
    if not commit_message:
        return False
    
    if SIMULATION_MODE:
        # Mô phỏng tạo commit trong chế độ mô phỏng
        logger.info("Dang mo phong tao commit...")
        print(f"\nMo phong commit voi message:\n{commit_message}")
        
        # Tạo file giả lập lịch sử commit
        commit_history_file = "commit_history.txt"
        try:
            with open(commit_history_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {commit_message}\n")
            logger.info(f"Da luu commit message vao {commit_history_file}")
        except Exception as e:
            logger.error(f"Loi khi luu commit history: {e}")
        
        return True
        
    try:
        logger.info("Dang tao commit...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        logger.info(f"Da tao commit thanh cong voi message:\n{commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Loi khi tao commit: {e}")
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
    logger.info("Bat dau qua trinh auto commit...")
    
    # Ghi thông tin hệ thống vào log
    system_info = get_system_info()
    logger.info(f"Thong tin he thong: {json.dumps(system_info, ensure_ascii=True)}")
    
    # Kiểm tra Git đã được cài đặt chưa
    if not check_git_installed():
        return
    
    # Kiểm tra xem có file nào được staged không
    diff_info = get_git_diff()
    if not diff_info:
        logger.info("Khong co thay doi nao de commit.")
        return
    
    # Tạo commit message
    commit_message = generate_commit_message(diff_info)
    if not commit_message:
        logger.error("Khong the tao commit message.")
        return
    
    # Tạo commit
    success = create_commit(commit_message)
    
    if success and not SIMULATION_MODE:
        # Hỏi người dùng có muốn push không
        push_choice = input("\nBan co muon push len remote repository khong? (Y/N): ")
        if push_choice.lower() == 'y':
            try:
                logger.info("Dang push len remote repository...")
                subprocess.run(["git", "push"], check=True)
                logger.info("Da push len remote repository thanh cong.")
            except subprocess.CalledProcessError as e:
                logger.error(f"Loi khi push len remote repository: {e}")
                print("Ban co the push thu cong sau bang lenh: git push")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Qua trinh da bi huy boi nguoi dung.")
    except Exception as e:
        logger.exception(f"Da xay ra loi khong mong muon: {e}")
    finally:
        # Thông báo kết thúc
        print("\n=== Hoan tat ===")
        if SIMULATION_MODE:
            print("Luu y: Ung dung da chay o che do mo phong. De su dung day du tinh nang, vui long cai dat Git.") 