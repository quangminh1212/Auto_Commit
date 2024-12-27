from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
                           QApplication, QHBoxLayout, QCheckBox, QSpinBox)
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
                padding: 15px;
            }
            QLabel {
                color: #3daee9;
                font-size: 24px;
                font-weight: bold;
            }
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #3daee9;
            }
            QCheckBox::indicator:checked {
                background-color: #3daee9;
            }
            QSpinBox {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #3daee9;
                border-radius: 4px;
                padding: 5px;
                min-width: 60px;
                max-width: 80px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background: #404040;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #505050;
            }
            .help-text {
                color: #888888;
                font-style: italic;
                font-size: 12px;
            }
        """)

        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(10)

        # Title và controls trong một hàng
        title_row = QHBoxLayout()
        
        # Auto Commit controls
        controls = QHBoxLayout()
        controls.setSpacing(15)

        self.auto_commit_checkbox = QCheckBox("Auto Commit")
        self.auto_commit_checkbox.setChecked(self.auto_commit)
        self.auto_commit_checkbox.stateChanged.connect(self.toggle_auto_commit)
        controls.addWidget(self.auto_commit_checkbox)

        # Delay settings với label
        delay_widget = QWidget()
        delay_layout = QHBoxLayout(delay_widget)
        delay_layout.setContentsMargins(0, 0, 0, 0)
        delay_layout.setSpacing(8)
        
        delay_label = QLabel("Commit Delay:")
        delay_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        delay_layout.addWidget(delay_label)
        
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 3600)
        self.delay_spinbox.setValue(self.commit_delay)
        self.delay_spinbox.setSuffix("s")
        self.delay_spinbox.valueChanged.connect(self.change_commit_delay)
        delay_layout.addWidget(self.delay_spinbox)
        
        controls.addWidget(delay_widget)
        controls.addStretch()
        
        title_row.addLayout(controls)
        header_layout.addLayout(title_row)

        # Help text
        help_text = QLabel("Hold Alt for 1 second to commit manually")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_text.setProperty("class", "help-text")
        header_layout.addWidget(help_text)

        layout.addWidget(header)

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