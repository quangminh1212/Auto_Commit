import sys
from PyQt6.QtWidgets import QApplication
from auto_commit.ui.main_window import MainWindow
from auto_commit.core.git import CommitMessageBuilder

def main():
    app = QApplication(sys.argv)
    
    # Sử dụng CommitMessageBuilder thay vì CommitAnalyzer
    commit_builder = CommitMessageBuilder()
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 