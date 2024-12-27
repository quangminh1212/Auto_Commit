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

    def setup_ui(self):
        """Thiết lập giao diện"""
        self.setWindowTitle("Auto Commit")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: transparent;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2d5a88;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #366ba1;
            }
            QPushButton:pressed {
                background-color: #244a70;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
            QTableWidget {
                background-color: #252526;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                gridline-color: #3d3d3d;
                selection-background-color: #2d5a88;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #3d3d3d;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4d4d4d;
            }
        """)

        # Widget chính với margins
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header với logo và tiêu đề
        header = QHBoxLayout()
        title = QLabel("Auto Commit")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #3daee9;
            padding: 10px;
        """)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        # Settings panel với style mới
        settings_panel = QWidget()
        settings_panel.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 15px;
            }
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #3daee9;
            }
            QCheckBox::indicator:checked {
                background-color: #3daee9;
            }
            QSpinBox {
                background-color: #363636;
                color: white;
                border: 2px solid #3daee9;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        settings_layout = QVBoxLayout(settings_panel)

        # Auto commit controls
        controls = QHBoxLayout()
        controls.setSpacing(20)

        self.auto_commit_checkbox = QCheckBox("Auto Commit")
        self.auto_commit_checkbox.setChecked(self.auto_commit)
        self.auto_commit_checkbox.stateChanged.connect(self.toggle_auto_commit)

        delay_container = QHBoxLayout()
        delay_label = QLabel("Commit Delay (seconds):")
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 3600)
        self.delay_spinbox.setValue(self.commit_delay)
        self.delay_spinbox.valueChanged.connect(self.change_commit_delay)
        
        delay_container.addWidget(delay_label)
        delay_container.addWidget(self.delay_spinbox)
        delay_container.addStretch()

        controls.addWidget(self.auto_commit_checkbox)
        controls.addLayout(delay_container)
        controls.addStretch()
        settings_layout.addLayout(controls)

        # Manual commit help
        help_text = QLabel("Hold Alt for 1 second to commit manually")
        help_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_text.setStyleSheet("color: #888888; font-style: italic;")
        settings_layout.addWidget(help_text)

        layout.addWidget(settings_panel)

        # Status with icon
        status_container = QHBoxLayout()
        self.status = QLabel("Status: Idle")
        self.status.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            background-color: #2d2d2d;
        """)
        status_container.addWidget(self.status)
        status_container.addStretch()
        
        # Start/Stop button với icon
        self.start_btn = QPushButton("Start Watching")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
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
        status_container.addWidget(self.start_btn)
        
        layout.addLayout(status_container)

        # Table với style mới
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File", "Status"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252526;
                alternate-background-color: #2d2d2d;
            }
            QTableWidget::item {
                color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: #2d5a88;
            }
        """)
        
        layout.addWidget(self.table)

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