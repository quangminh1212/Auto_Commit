from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
                           QApplication, QHBoxLayout, QCheckBox, QSpinBox, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QKeyEvent
from datetime import datetime
from auto_commit.core.git import CommitAnalyzer, ChangeType, CommitMessageBuilder
from pathlib import Path

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
        """Thiết lập phần header với settings và controls"""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #3daee9;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #43b8ff;
            }
            QPushButton:pressed {
                background-color: #3498db;
            }
            QPushButton#commit-all {
                background-color: #2ecc71;
            }
            QPushButton#commit-all:hover {
                background-color: #27ae60;
            }
            QPushButton[toggled="true"] {
                background-color: #e74c3c;
            }
            QPushButton[toggled="true"]:hover {
                background-color: #c0392b;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #363636;
                color: #3daee9;
                border: 1px solid #3daee9;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(15)

        # Controls container
        controls = QHBoxLayout()
        controls.setSpacing(10)

        # Auto Commit Toggle Button
        self.auto_commit_btn = QPushButton("Auto Commit: OFF")
        self.auto_commit_btn.setCheckable(True)
        self.auto_commit_btn.clicked.connect(self.toggle_auto_commit)
        controls.addWidget(self.auto_commit_btn)

        # Commit Delay
        delay_container = QHBoxLayout()
        delay_label = QLabel("Delay:")
        self.delay_input = QLineEdit()
        self.delay_input.setText(f"{self.commit_delay}s")
        self.delay_input.setFixedWidth(60)
        self.delay_input.textChanged.connect(self.on_delay_changed)
        
        delay_container.addWidget(delay_label)
        delay_container.addWidget(self.delay_input)
        controls.addLayout(delay_container)

        # Commit All Button
        self.commit_all_btn = QPushButton("Commit All")
        self.commit_all_btn.setObjectName("commit-all")
        self.commit_all_btn.clicked.connect(self.commit_all_changes)
        controls.addWidget(self.commit_all_btn)

        header_layout.addLayout(controls)
        header_layout.addStretch()

        # Help text
        help_text = QLabel("Hold Alt for 1 second to commit manually")
        help_text.setStyleSheet("color: #888888; font-style: italic;")
        header_layout.addWidget(help_text)

        layout.addWidget(header)

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

    def toggle_auto_commit(self):
        """Toggle chế độ auto commit"""
        self.auto_commit = self.auto_commit_btn.isChecked()
        self.auto_commit_btn.setText(f"Auto Commit: {'ON' if self.auto_commit else 'OFF'}")
        self.auto_commit_btn.setProperty("toggled", self.auto_commit)
        self.auto_commit_btn.style().unpolish(self.auto_commit_btn)
        self.auto_commit_btn.style().polish(self.auto_commit_btn)
        
        if self.auto_commit:
            self.auto_commit_timer.start(self.commit_delay * 1000)
            self.status.setText("Status: Auto commit enabled")
        else:
            self.auto_commit_timer.stop()
            self.status.setText("Status: Auto commit disabled (Manual commit available)")
            
        # Cập nhật trạng thái nút Commit All
        self.commit_all_btn.setEnabled(True)
        self.commit_all_btn.setToolTip(
            "Click to commit all changes immediately" if not self.auto_commit
            else "Auto commit is ON - Manual commit still available"
        )

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
        """Thực hiện commit với phân tích chi tiết"""
        if not self.changes_to_commit:
            return

        try:
            self.status.setText("Status: Analyzing changes...")
            
            # Tạo commit message builder
            builder = CommitMessageBuilder()
            
            # Phân tích changes
            changes = [(c['file'], c['type']) for c in self.changes_to_commit]
            details = builder.analyze_changes(changes)
            
            # Tạo commit message
            message = builder.build_message(details)
            
            # Hiển thị trong bảng
            self._add_commit_entry(message)
            
            # Cập nhật status
            for change in self.changes_to_commit:
                self._update_file_status(change['file'], "committed")
            
            self.changes_to_commit.clear()
            self.status.setText("Status: Changes committed successfully")
            
        except Exception as e:
            self.status.setText(f"Error: {str(e)}")
            print(f"Commit error: {str(e)}")

    def _get_file_category(self, file_path: str, ext: str) -> str:
        """Phân loại file dựa trên extension và đường dẫn"""
        # Source code
        if ext in {'.py', '.js', '.ts', '.java', '.cpp', '.cs'}:
            if 'test' in file_path.lower():
                return 'test'
            return 'source'
            
        # UI/Frontend
        if ext in {'.html', '.css', '.scss', '.vue', '.jsx', '.tsx'}:
            return 'ui'
            
        # Config files
        if ext in {'.json', '.yaml', '.yml', '.toml', '.ini', '.env'}:
            return 'config'
            
        # Documentation
        if ext in {'.md', '.rst', '.txt', '.doc', '.pdf'}:
            return 'docs'
            
        # Build/Deploy
        if any(p in file_path for p in ['build', 'deploy', 'ci', 'docker']):
            return 'build'
            
        return 'other'

    def _analyze_changes_impact(self, changes: list) -> dict:
        """Phân tích mức độ ảnh hưởng của các thay đổi"""
        impact = {
            'breaking': False,
            'scope': set(),
            'components': set(),
            'dependencies_changed': False,
            'security_related': False,
            'database_changes': False,
            'api_changes': False
        }
        
        for file_path, change_type in changes:
            # Kiểm tra breaking changes
            if change_type == 'DELETED':
                impact['breaking'] = True
            
            # Phân tích components
            parts = Path(file_path).parts
            if len(parts) > 1:
                impact['components'].add(parts[0])
            
            # Kiểm tra dependencies
            if any(dep in file_path for dep in [
                'requirements.txt', 'package.json', 'go.mod', 'pom.xml'
            ]):
                impact['dependencies_changed'] = True
            
            # Kiểm tra security
            if any(sec in file_path.lower() for sec in [
                'security', 'auth', 'password', 'crypto', 'secret'
            ]):
                impact['security_related'] = True
            
            # Kiểm tra database
            if any(db in file_path.lower() for db in [
                'migration', 'schema', 'database', 'model'
            ]):
                impact['database_changes'] = True
            
            # Kiểm tra API
            if any(api in file_path.lower() for api in [
                'api', 'endpoint', 'route', 'controller'
            ]):
                impact['api_changes'] = True
        
        return impact

    def _generate_detailed_commit_message(self, category: str, changes: list, impact: dict) -> str:
        """Tạo commit message chi tiết"""
        # Xác định commit type
        commit_type = {
            'source': 'feat' if any(t == 'CREATED' for _, t in changes) else 'fix',
            'test': 'test',
            'ui': 'style',
            'config': 'chore',
            'docs': 'docs',
            'build': 'build'
        }.get(category, 'chore')

        # Tạo scope
        scope = None
        if impact['components']:
            scope = ','.join(sorted(impact['components']))
        elif category != 'other':
            scope = category

        # Tạo subject line
        if len(changes) == 1:
            file_path, change_type = changes[0]
            action = {
                'CREATED': 'add',
                'MODIFIED': 'update',
                'DELETED': 'remove'
            }[change_type]
            subject = f"{action} {Path(file_path).name}"
        else:
            subject = f"update {len(changes)} {category} files"

        # Tạo message chính
        message = f"{commit_type}"
        if scope:
            message += f"({scope})"
        message += f": {subject}"

        # Thêm body với chi tiết
        body = []
        
        # Liệt kê các thay đổi
        if len(changes) > 1:
            body.append("\nChanges:")
            for file_path, change_type in changes:
                action = {
                    'CREATED': 'Add',
                    'MODIFIED': 'Update',
                    'DELETED': 'Remove'
                }[change_type]
                body.append(f"- {action} {file_path}")

        # Thêm impact analysis
        impacts = []
        if impact['breaking']:
            impacts.append("BREAKING CHANGE: This includes file deletions")
        if impact['dependencies_changed']:
            impacts.append("Dependencies were modified")
        if impact['security_related']:
            impacts.append("Security-related changes")
        if impact['database_changes']:
            impacts.append("Database schema changes")
        if impact['api_changes']:
            impacts.append("API modifications")

        if impacts:
            body.append("\nImpact:")
            body.extend(f"- {impact}" for impact in impacts)

        if body:
            message += '\n' + '\n'.join(body)

        return message

    def _add_commit_entry(self, message: str, highlight: bool = False):
        """Thêm commit entry vào bảng với tùy chọn highlight"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Time column
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Type column với highlight nếu là manual commit
        type_item = QTableWidgetItem("COMMIT")
        type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if highlight:
            type_item.setForeground(QColor("#e74c3c"))  # Đỏ cho manual commit
            type_item.setToolTip("Manual commit")
        else:
            type_item.setForeground(QColor("#2ecc71"))  # Xanh cho auto commit
            type_item.setToolTip("Auto commit")
        
        # Message column
        message_item = QTableWidgetItem(message)
        if highlight:
            message_item.setBackground(QColor("#2d2d2d"))
        
        # Status column
        status_item = QTableWidgetItem("committed")
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.table.setItem(row, 0, time_item)
        self.table.setItem(row, 1, type_item)
        self.table.setItem(row, 2, message_item)
        self.table.setItem(row, 3, status_item)
        
        self.table.scrollToBottom()

    def _update_file_status(self, file_path: str, status: str):
        """Cập nhật trạng thái của file trong bảng"""
        for row in range(self.table.rowCount()):
            if self.table.item(row, 2).text() == file_path:
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 3, status_item)

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
        """Kiểm tra phím Alt để commit thủ công"""
        if not self.alt_press_time:
            return
            
        # Tính thời gian giữ phím Alt
        duration = (datetime.now() - self.alt_press_time).total_seconds()
        
        # Nếu giữ đủ 1 giây và có thay đổi, thực hiện commit
        if duration >= 1 and self.changes_to_commit:
            self.commit_all_changes()
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

    def commit_all_changes(self):
        """Commit tất cả thay đổi ngay lập tức"""
        if not self.changes_to_commit:
            self.status.setText("Status: No changes to commit")
            return
            
        try:
            self.status.setText("Status: Committing all changes...")
            
            # Tạo commit message builder
            builder = CommitMessageBuilder()
            
            # Phân tích changes
            changes = [(c['file'], c['type']) for c in self.changes_to_commit]
            details = builder.analyze_changes(changes)
            
            # Tạo commit message
            message = builder.build_message(details)
            
            # Hiển thị trong bảng với highlight
            self._add_commit_entry(message, highlight=True)
            
            # Cập nhật status
            for change in self.changes_to_commit:
                self._update_file_status(change['file'], "committed")
            
            self.changes_to_commit.clear()
            self.status.setText("Status: All changes committed successfully")
            
        except Exception as e:
            self.status.setText(f"Error: {str(e)}")
            print(f"Commit error: {str(e)}")