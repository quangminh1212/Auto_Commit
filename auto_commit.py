import os
import sys
import json
import requests
import subprocess
from datetime import datetime

# Cấu hình API Gemini
API_KEY = "YOUR_GEMINI_API_KEY"  # Thay thế bằng API key của bạn
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def get_git_diff():
    """Lấy thông tin về các thay đổi trong git"""
    try:
        # Lấy danh sách các file đã thay đổi
        staged_files = subprocess.check_output(
            ["git", "diff", "--staged", "--name-only"], 
            text=True
        ).strip()
        
        if not staged_files:
            print("Không có file nào được staged để commit.")
            return None
            
        # Lấy nội dung thay đổi
        diff_content = subprocess.check_output(
            ["git", "diff", "--staged"], 
            text=True
        ).strip()
        
        return {
            "staged_files": staged_files.split("\n"),
            "diff_content": diff_content
        }
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi lấy thông tin git: {e}")
        return None

def generate_commit_message(diff_info):
    """Tạo commit message bằng API Gemini"""
    if not diff_info:
        return None
        
    # Chuẩn bị prompt cho Gemini
    prompt = f"""
    Hãy tạo một commit message theo chuẩn Conventional Commits dựa trên các thay đổi sau:
    
    Files đã thay đổi:
    {', '.join(diff_info['staged_files'])}
    
    Nội dung thay đổi:
    {diff_info['diff_content'][:3000]}  # Giới hạn kích thước để tránh vượt quá giới hạn của API
    
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
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            commit_message = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            return commit_message
        else:
            print(f"Lỗi khi gọi API Gemini: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Lỗi khi gọi API Gemini: {e}")
        return None

def create_commit(commit_message):
    """Tạo commit với message đã tạo"""
    if not commit_message:
        return False
        
    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"Đã tạo commit thành công với message:\n{commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi tạo commit: {e}")
        return False

def main():
    # Kiểm tra xem có file nào được staged không
    diff_info = get_git_diff()
    if not diff_info:
        print("Không có thay đổi nào để commit.")
        return
    
    # Tạo commit message
    commit_message = generate_commit_message(diff_info)
    if not commit_message:
        print("Không thể tạo commit message.")
        return
    
    # Tạo commit
    create_commit(commit_message)

if __name__ == "__main__":
    main() 