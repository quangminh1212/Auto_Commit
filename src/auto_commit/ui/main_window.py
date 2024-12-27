from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
                           QApplication, QHBoxLayout, QCheckBox, QSpinBox, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QKeyEvent
from datetime import datetime
from auto_commit.core.git import CommitAnalyzer, ChangeType

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication): 
        super().__init__()
        # Khởi tạo các thuộc tính
        self.app = app
        self.auto_commit = False
        self.commit_delay = 30
        self.changes_to_commit = []
        self.alt_press_time = None
        self.is_watching = False
        self.commit_analyzer = CommitAnalyzer()

        # Khởi tạo UI và timers
        self.setup_ui()
        self.init_timers()

    def init_timers(self):
        """Khởi tạo các timers"""
        # Timer cho việc kiểm tra phím Alt
        self.check_alt_timer = QTimer()
        self.check_alt_timer.timeout.connect(self.check_alt_press)
        self.check_alt_timer.start(100)

        # Timer cho auto commit
        self.auto_commit_timer = QTimer()
        self.auto_commit_timer.timeout.connect(self.auto_commit_changes)

    def setup_header(self, layout):
        """Thiết lập phần header với settings"""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 8px;
            }
            QCheckBox {
                color: #3daee9;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 1px solid #3daee9;
            }
            QCheckBox::indicator:checked {
                background-color: #3daee9;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #363636;
                color: #3daee9;
                border: 1px solid #3daee9;
                border-radius: 3px;
                padding: 4px 8px;
                min-width: 60px;
                max-width: 80px;
            }
            .help-text {
                color: #888888;
                font-style: italic;
                font-size: 12px;
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(15)

        # Auto Commit checkbox
        self.auto_commit_checkbox = QCheckBox("Auto Commit")
        self.auto_commit_checkbox.setChecked(self.auto_commit)
        self.auto_commit_checkbox.stateChanged.connect(self.toggle_auto_commit)
        header_layout.addWidget(self.auto_commit_checkbox)

        # Commit Delay
        delay_label = QLabel("Commit Delay:")
        header_layout.addWidget(delay_label)
        
        self.delay_input = QLineEdit()
        self.delay_input.setText(f"{self.commit_delay}s")
        self.delay_input.setFixedWidth(60)
        self.delay_input.textChanged.connect(self.on_delay_changed)
        header_layout.addWidget(self.delay_input)
        
        header_layout.addStretch()

        # Help text ở dưới
        help_container = QWidget()
        help_layout = QVBoxLayout(help_container)
        help_layout.setContentsMargins(0, 5, 0, 0)
        
        help_text = QLabel("Hold Alt for 1 second to commit manually")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_text.setStyleSheet("color: #888888; font-style: italic; font-size: 12px;")
        help_layout.addWidget(help_text)

        # Tạo container chung
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(header)
        container_layout.addWidget(help_container)

        layout.addWidget(container)

    def on_delay_changed(self, text):
        """Xử lý khi thay đổi giá trị delay"""
        try:
            # Loại bỏ 's' nếu có
            value = text.replace('s', '')
            delay = int(value)
            if 1 <= delay <= 3600:  # Giới hạn từ 1-3600 giây
                self.commit_delay = delay
                if self.auto_commit and hasattr(self, 'auto_commit_timer'):
                    self.auto_commit_timer.setInterval(delay * 1000)
            
            # Tự động thêm 's' vào cuối nếu chưa có
            if not text.endswith('s'):
                self.delay_input.setText(f"{value}s")
                # Di chuyển con trỏ về trước 's'
                self.delay_input.setCursorPosition(len(value))
                
        except ValueError:
            # Nếu giá trị không hợp lệ, reset về giá trị cũ
            self.delay_input.setText(f"{self.commit_delay}s")

    def setup_ui(self):
        """Thiết lập giao diện chính"""
        self.setWindowTitle("Auto Commit")
        self.setMinimumSize(800, 600)
        
        # Widget chính
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Thêm header
        self.setup_header(layout)

        # Status bar
        status_bar = QWidget()
        status_bar.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
        """)
        
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 0, 10, 0)
        
        self.status = QLabel("Status: Idle")
        status_layout.addWidget(self.status)
        status_layout.addStretch()
        
        self.start_btn = QPushButton("Start Watching")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton[watching="true"] {
                background-color: #e74c3c;
            }
            QPushButton[watching="true"]:hover {
                background-color: #c0392b;
            }
        """)
        self.start_btn.clicked.connect(self.start_watching)
        status_layout.addWidget(self.start_btn)
        
        layout.addWidget(status_bar)

        # Table setup giữ nguyên như cũ
        self.setup_table(layout)

    def start_watching(self):
        """Bắt đầu theo dõi"""
        if not self.is_watching:
            self.is_watching = True
            self.start_btn.setText("Stop Watching")
            self.status.setText("Status: Watching")
            self.status.setStyleSheet("color: #2ecc71;")
            if self.auto_commit:
                self.auto_commit_timer.start(self.commit_delay * 1000)
        else:
            self.stop_watching()

    def stop_watching(self):
        """Dừng theo dõi"""
        self.is_watching = False
        self.start_btn.setText("Start Watching")
        self.status.setText("Status: Stopped")
        self.status.setStyleSheet("color: #e74c3c;")
        if self.auto_commit_timer.isActive():
            self.auto_commit_timer.stop()

    def toggle_auto_commit(self, state):
        """Bật/tắt auto commit"""
        self.auto_commit = bool(state)
        if self.auto_commit and self.is_watching:
            self.auto_commit_timer.start(self.commit_delay * 1000)
            self.status.setText("Status: Auto Commit Enabled")
        else:
            self.auto_commit_timer.stop()
            self.status.setText("Status: Manual Commit Mode")

    def change_commit_delay(self, value):
        """Thay đổi thời gian delay commit"""
        self.commit_delay = value
        if self.auto_commit and self.auto_commit_timer.isActive():
            self.auto_commit_timer.setInterval(value * 1000)

    def auto_commit_changes(self):
        """Tự động commit theo timer"""
        if self.auto_commit and self.changes_to_commit:
            self.commit_changes()

    def commit_changes(self):
        """Thực hiện commit các thay đổi"""
        if self.changes_to_commit:
            self.status.setText("Status: Committing changes...")
            
            # Tạo commit messages thông minh
            commit_messages = self.commit_analyzer.generate_commit_messages()
            
            # Hiển thị commit messages
            for msg in commit_messages:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(datetime.now().strftime("%H:%M:%S")))
                self.table.setItem(row, 1, QTableWidgetItem("COMMIT"))
                self.table.setItem(row, 2, QTableWidgetItem(msg))
                self.table.setItem(row, 3, QTableWidgetItem("committed"))
            
            # Cập nhật status các thay đổi
            for change in self.changes_to_commit:
                self.add_change(change['file'], change['type'], "committed")
            
            self.changes_to_commit.clear()
            self.commit_analyzer.clear()
            self.status.setText("Status: Changes committed")

    def add_change(self, file_path: str, change_type: str, status: str = "pending"):
        """Thêm thay đổi vào bảng"""
        if status == "pending":
            self.changes_to_commit.append({
                'file': file_path,
                'type': change_type
            })
            self.commit_analyzer.add_change(file_path, ChangeType(change_type.lower()))

        row = self.table.rowCount()
        self.table.insertRow(row)

        items = [
            (datetime.now().strftime("%H:%M:%S"), Qt.AlignmentFlag.AlignCenter),
            (change_type, Qt.AlignmentFlag.AlignCenter),
            (str(file_path), Qt.AlignmentFlag.AlignLeft),
            (status, Qt.AlignmentFlag.AlignCenter)
        ]

        for col, (text, alignment) in enumerate(items):
            item = QTableWidgetItem(text)
            item.setTextAlignment(alignment)
            
            if col == 1:  # Type column
                color = {
                    "CREATED": QColor("#2ecc71"),
                    "MODIFIED": QColor("#f1c40f"),
                    "DELETED": QColor("#e74c3c")
                }.get(change_type, QColor("#ffffff"))
                item.setForeground(color)
                
            self.table.setItem(row, col, item)

        self.table.scrollToBottom()

        # Giới hạn số dòng
        while self.table.rowCount() > 1000:
            self.table.removeRow(0)

    def check_alt_press(self):
        """Kiểm tra phím Alt"""
        if self.alt_press_time:
            duration = (datetime.now() - self.alt_press_time).total_seconds()
            if duration >= 1.0:
                self.commit_changes()
                self.alt_press_time = None

    def keyPressEvent(self, event: QKeyEvent):
        """Xử lý nhấn phím"""
        if event.key() == Qt.Key.Key_Alt and not self.auto_commit:
            if not self.alt_press_time:
                self.alt_press_time = datetime.now()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        """Xử lý thả phím"""
        if event.key() == Qt.Key.Key_Alt:
            self.alt_press_time = None
        super().keyReleaseEvent(event)

    def closeEvent(self, event):
        """Xử lý đóng cửa sổ"""
        self.check_alt_timer.stop()
        self.auto_commit_timer.stop()
        event.accept()

    def setup_table(self, layout):
        """Thiết lập bảng theo dõi thay đổi"""
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File", "Status"])
        
        # Style cho table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252526;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                gridline-color: #3d3d3d;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
                color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: #2d5a88;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                padding: 8px;
                border: none;
                color: #ffffff;
                font-weight: bold;
            }
            QTableWidget::item:alternate {
                background-color: #2d2d2d;
            }
        """)
        
        # Cấu hình header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Time
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)          # File
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Status
        
        # Ẩn vertical header
        self.table.verticalHeader().setVisible(False)
        
        # Bật alternating row colors
        self.table.setAlternatingRowColors(True)
        
        # Chọn cả dòng
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Thêm vào layout
        layout.addWidget(self.table)