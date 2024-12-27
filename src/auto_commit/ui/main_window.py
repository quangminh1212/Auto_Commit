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
        self.app = app
        self.auto_commit = False
        self.commit_delay = 30
        self.changes_to_commit = []
        self.alt_press_time = None
        self.is_watching = False
        self.commit_analyzer = CommitAnalyzer()
        self.setup_ui()
        
        # Khởi tạo timers
        self.check_alt_timer = QTimer()
        self.check_alt_timer.timeout.connect(self.check_alt_press)
        self.check_alt_timer.start(100)

        self.auto_commit_timer = QTimer()
        self.auto_commit_timer.timeout.connect(self.auto_commit_changes)

    def setup_ui(self):
        """Thiết lập giao diện"""
        self.setWindowTitle("Auto Commit")
        self.setMinimumSize(800, 600)
        
        # Widget chính
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Tiêu đề
        title = QLabel("Auto Commit")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3daee9;")
        layout.addWidget(title)

        # Settings panel
        settings_panel = QWidget()
        settings_layout = QVBoxLayout(settings_panel)
        settings_panel.setStyleSheet("""
            QWidget {
                background-color: #333333;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: white;
            }
            QCheckBox {
                color: white;
            }
            QSpinBox {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
            }
        """)

        # Auto commit settings
        auto_commit_layout = QHBoxLayout()
        self.auto_commit_checkbox = QCheckBox("Auto Commit")
        self.auto_commit_checkbox.setChecked(self.auto_commit)
        self.auto_commit_checkbox.stateChanged.connect(self.toggle_auto_commit)
        auto_commit_layout.addWidget(self.auto_commit_checkbox)

        # Commit delay settings
        delay_label = QLabel("Commit Delay (seconds):")
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 3600)
        self.delay_spinbox.setValue(self.commit_delay)
        self.delay_spinbox.valueChanged.connect(self.change_commit_delay)
        auto_commit_layout.addWidget(delay_label)
        auto_commit_layout.addWidget(self.delay_spinbox)
        
        settings_layout.addLayout(auto_commit_layout)
        
        # Manual commit help
        manual_commit_label = QLabel("Hold Alt for 1 second to commit manually")
        manual_commit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual_commit_label.setStyleSheet("color: #888888; font-size: 12px;")
        settings_layout.addWidget(manual_commit_label)
        
        layout.addWidget(settings_panel)

        # Status
        self.status = QLabel("Status: Idle")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

        # Start/Stop button
        self.start_btn = QPushButton("Start Watching")
        self.start_btn.clicked.connect(self.start_watching)
        layout.addWidget(self.start_btn)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File", "Status"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def toggle_auto_commit(self, state):
        """Bật/tắt auto commit"""
        self.auto_commit = bool(state)
        if self.auto_commit:
            self.auto_commit_timer.start(self.commit_delay * 1000)
            self.status.setText("Status: Auto Commit Enabled")
        else:
            self.auto_commit_timer.stop()
            self.status.setText("Status: Manual Commit Mode")

    def change_commit_delay(self, value):
        """Thay đổi thời gian delay commit"""
        self.commit_delay = value
        if self.auto_commit:
            self.auto_commit_timer.setInterval(value * 1000)

    def auto_commit_changes(self):
        """Tự động commit theo timer"""
        if self.auto_commit and self.changes_to_commit:
            self.commit_changes()

    def commit_changes(self):
        """Thực hiện commit các thay đổi"""
        if self.changes_to_commit:
            self.status.setText("Status: Analyzing changes...")
            
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
            self.commit_analyzer.add_change(
                file_path, 
                ChangeType(change_type.lower())
            )

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