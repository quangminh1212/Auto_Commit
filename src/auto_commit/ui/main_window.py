from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
                           QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện đơn giản"""
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
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File"])
        
        # Cấu hình bảng
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        # Timer cập nhật
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table)
        self.is_watching = False

    def add_change(self, file_path: str, change_type: str):
        """Thêm thay đổi vào bảng"""
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
        
        # Cuộn xuống dòng mới nhất
        self.table.scrollToBottom()

        # Giới hạn số dòng
        MAX_ROWS = 1000
        while self.table.rowCount() > MAX_ROWS:
            self.table.removeRow(0)

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