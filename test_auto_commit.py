import unittest
import os
import sys
import json
import subprocess
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from io import StringIO

# Import các hàm từ auto_commit.py
from auto_commit import get_git_diff, generate_commit_message, create_commit, main

class TestAutoCommit(unittest.TestCase):
    """Test các chức năng của auto_commit.py"""
    
    def setUp(self):
        """Thiết lập môi trường test"""
        # Tạo thư mục tạm thời để test git
        self.test_dir = tempfile.mkdtemp()
        self.old_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Khởi tạo git repository
        subprocess.run(["git", "init"], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        
        # Tạo một file test
        with open("test_file.txt", "w") as f:
            f.write("Initial content")
        
        # Thêm và commit file ban đầu
        subprocess.run(["git", "add", "test_file.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, stdout=subprocess.DEVNULL)
    
    def tearDown(self):
        """Dọn dẹp sau khi test"""
        os.chdir(self.old_dir)
        shutil.rmtree(self.test_dir)
    
    def test_get_git_diff_no_changes(self):
        """Test khi không có thay đổi nào"""
        result = get_git_diff()
        self.assertIsNone(result)
    
    def test_get_git_diff_with_changes(self):
        """Test khi có thay đổi"""
        # Thay đổi nội dung file
        with open("test_file.txt", "w") as f:
            f.write("Modified content")
        
        # Stage thay đổi
        subprocess.run(["git", "add", "test_file.txt"], check=True)
        
        # Kiểm tra diff
        result = get_git_diff()
        self.assertIsNotNone(result)
        self.assertIn("test_file.txt", result["staged_files"])
        self.assertIn("Modified content", result["diff_content"])
    
    @patch("auto_commit.requests.post")
    def test_generate_commit_message(self, mock_post):
        """Test tạo commit message với API Gemini"""
        # Mock response từ API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "feat: add new feature"
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Tạo diff_info giả
        diff_info = {
            "staged_files": ["test_file.txt"],
            "diff_content": "diff --git a/test_file.txt b/test_file.txt\nModified content"
        }
        
        # Kiểm tra kết quả
        result = generate_commit_message(diff_info)
        self.assertEqual(result, "feat: add new feature")
    
    @patch("auto_commit.subprocess.run")
    def test_create_commit(self, mock_run):
        """Test tạo commit"""
        # Mock subprocess.run
        mock_run.return_value = MagicMock(returncode=0)
        
        # Kiểm tra kết quả
        result = create_commit("feat: add new feature")
        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "feat: add new feature"], 
            check=True
        )
    
    @patch("auto_commit.get_git_diff")
    @patch("auto_commit.generate_commit_message")
    @patch("auto_commit.create_commit")
    def test_main_success(self, mock_create_commit, mock_generate_message, mock_get_diff):
        """Test luồng chính khi thành công"""
        # Mock các hàm
        mock_get_diff.return_value = {
            "staged_files": ["test_file.txt"],
            "diff_content": "diff content"
        }
        mock_generate_message.return_value = "feat: add new feature"
        mock_create_commit.return_value = True
        
        # Chạy hàm main
        with patch("sys.stdout", new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
        
        # Kiểm tra các hàm đã được gọi
        mock_get_diff.assert_called_once()
        mock_generate_message.assert_called_once()
        mock_create_commit.assert_called_once_with("feat: add new feature")
    
    @patch("auto_commit.get_git_diff")
    def test_main_no_changes(self, mock_get_diff):
        """Test luồng chính khi không có thay đổi"""
        # Mock hàm get_git_diff
        mock_get_diff.return_value = None
        
        # Chạy hàm main
        with patch("sys.stdout", new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
        
        # Kiểm tra output
        self.assertIn("Không có thay đổi nào để commit", output)

def run_tests():
    """Chạy tất cả các test"""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

def optimize_code():
    """Tối ưu mã nguồn dựa trên kết quả test"""
    print("Đang tối ưu mã nguồn...")
    # Đây là nơi bạn có thể thêm logic tối ưu mã nguồn
    # Ví dụ: phân tích hiệu suất, tối ưu thuật toán, v.v.
    
    # Trong ví dụ này, chúng ta sẽ kiểm tra xem API key đã được cấu hình chưa
    from auto_commit import API_KEY
    if API_KEY == "YOUR_GEMINI_API_KEY":
        print("Cảnh báo: API key chưa được cấu hình. Vui lòng cập nhật API_KEY trong auto_commit.py")
    
    # Kiểm tra các thư viện cần thiết đã được cài đặt chưa
    try:
        import requests
        print("Thư viện requests đã được cài đặt.")
    except ImportError:
        print("Cảnh báo: Thư viện requests chưa được cài đặt. Vui lòng chạy 'pip install requests'")

if __name__ == "__main__":
    print("=== Bắt đầu kiểm tra và tối ưu auto_commit ===")
    print("\n1. Chạy các test case:")
    run_tests()
    
    print("\n2. Tối ưu mã nguồn:")
    optimize_code()
    
    print("\n=== Hoàn tất kiểm tra và tối ưu ===")
    print("Bạn có thể chạy file này bất cứ lúc nào để kiểm tra và tối ưu ứng dụng.") 