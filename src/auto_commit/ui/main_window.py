from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
                           QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QKeyEvent
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app 
        self.setup_ui() 
        self.alt_press_time = None
        self.changes_to_commit = []
        self.commit_timer = QTimer()
        self.commit_timer.timeout.connect(self.check_alt_press)
        self.commit_timer.start(100)  # Kiểm tra mỗi 100ms

    def keyPressEvent(self, event: QKeyEvent):
        """Xử lý sự kiện nhấn phím"""
        if event.key() == Qt.Key.Key_Alt:
            if not self.alt_press_time:
                self.alt_press_time = datetime.now()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        """Xử lý sự kiện thả phím"""
        if event.key() == Qt.Key.Key_Alt:
            self.alt_press_time = None
        super().keyReleaseEvent(event)

    def check_alt_press(self):
        """Kiểm tra thời gian nhấn giữ Alt"""
        if self.alt_press_time:
            duration = (datetime.now() - self.alt_press_time).total_seconds()
            if duration >= 1.0:  # Nếu nhấn giữ >= 1 giây
                self.commit_changes()
                self.alt_press_time = None

    def commit_changes(self):
        """Thực hiện commit các thay đổi"""
        if self.changes_to_commit:
            self.status.setText("Status: Committing changes...")
            self.status.setStyleSheet("color: #f1c40f")  # Màu vàng
            
            # Thực hiện commit
            for change in self.changes_to_commit:
                self.add_change(change['file'], change['type'], "committed")
            
            # Xóa danh sách thay đổi đã commit
            self.changes_to_commit.clear()
            
            self.status.setText("Status: Changes committed")
            self.status.setStyleSheet("color: #2ecc71")  # Màu xanh

    def add_change(self, file_path: str, change_type: str, status: str = "pending"):
        """Thêm thay đổi vào bảng và danh sách chờ commit"""
        if status == "pending":
            self.changes_to_commit.append({
                'file': file_path,
                'type': change_type
            })

        row = self.table.rowCount()
        self.table.insertRow(row)

        # Thời gian
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Loại thay đổi
        type_item = QTableWidgetItem(change_type)
        type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Tên file
        file_item = QTableWidgetItem(str(file_path))
        
        # Status
        status_item = QTableWidgetItem(status)
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Màu sắc theo loại thay đổi
        color = {
            "CREATED": QColor("#2ecc71"),
            "MODIFIED": QColor("#f1c40f"),
            "DELETED": QColor("#e74c3c")
        }.get(change_type, QColor("#ffffff"))
        
        type_item.setForeground(color)

        # Thêm vào bảng
        self.table.setItem(row, 0, time_item)
        self.table.setItem(row, 1, type_item)
        self.table.setItem(row, 2, file_item)
        self.table.setItem(row, 3, status_item)
        
        # Cuộn xuống dòng mới nhất
        self.table.scrollToBottom()

        # Giới hạn số dòng
        MAX_ROWS = 1000
        while self.table.rowCount() > MAX_ROWS:
            self.table.removeRow(0)

    def setup_ui(self):
        """Thiết lập giao diện"""
        # Cấu hình cửa sổ
        self.setWindowTitle("Auto Commit")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton {
                background-color: #3daee9;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                min-width: 120px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #4dc4ff;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QTableWidget {
                background-color: #333333;
                color: #ffffff;
                gridline-color: #444444;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px;
                border: none;
            }
        """)

        # Widget chính
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Tiêu đề
        title = QLabel("Auto Commit")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: #3daee9; font-weight: bold;")
        layout.addWidget(title)

        # Trạng thái
        self.status = QLabel("Status: Idle")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

        # Nút điều khiển
        self.start_btn = QPushButton("Start Watching")
        self.start_btn.clicked.connect(self.start_watching)
        layout.addWidget(self.start_btn)

        # Bảng theo dõi
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File", "Status"])
        
        # Cấu hình bảng
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # Timer cập nhật
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table)
        self.is_watching = False

        # Thêm hướng dẫn
        help_label = QLabel("Hold Alt for 1 second to commit changes")
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_label.setStyleSheet("color: #888888; font-size: 12px;")
        layout.addWidget(help_label)

    def start_watching(self):
        """Bắt đầu/dừng theo dõi"""
        if not self.is_watching:
            self.is_watching = True
            self.start_btn.setText("Stop Watching")
            self.status.setText("Status: Watching")
            self.status.setStyleSheet("color: #2ecc71")
            self.timer.start(1000)
        else:
            self.is_watching = False
            self.start_btn.setText("Start Watching")
            self.status.setText("Status: Stopped")
            self.status.setStyleSheet("color: #e74c3c")
            self.timer.stop()

    def update_table(self):
        """Cập nhật bảng"""
        try:
            QApplication.processEvents()
        except Exception as e:
            print(f"Error updating: {e}")

    def closeEvent(self, event):
        """Xử lý đóng cửa sổ"""
        if self.timer.isActive():
            self.timer.stop()
        event.accept() 