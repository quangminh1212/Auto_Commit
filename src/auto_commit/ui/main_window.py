from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QLabel, QHeaderView,
                           QApplication, QHBoxLayout, QCheckBox, QSpinBox, QLineEdit,
                           QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QFileSystemWatcher
from PyQt6.QtGui import QColor, QKeyEvent
from datetime import datetime
from pathlib import Path
from auto_commit.core.git import CommitMessageBuilder
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Commit")
        
        # Khởi tạo các biến trước khi setup UI 
        self.auto_commit = False
        self.commit_delay = 30
        self.changes_to_commit = []
        self.alt_press_time = None 
        self.is_watching = False  # Thêm thuộc tính is_watching
        
        # Khởi tạo các thành phần UI
        self.status = None
        self.table = None
        self.delay_input = None
        self.auto_commit_btn = None
        self.commit_all_btn = None
        
        # Tạo QTimer cho auto commit
        self.auto_commit_timer = QTimer(self)
        self.auto_commit_timer.timeout.connect(self.commit_all_changes)
        
        # Tạo QTimer cho việc kiểm tra phím Alt
        self.check_alt_timer = QTimer(self)
        self.check_alt_timer.timeout.connect(self.check_alt_press)
        self.check_alt_timer.start(100)  # Kiểm tra mỗi 100ms
        
        # Khởi tạo file watcher trước khi setup UI
        self.watcher = QFileSystemWatcher(self)
        
        # Setup UI (sẽ khởi tạo các thành phần UI)
        self.setup_ui()
        
        # Kết nối signals sau khi setup UI hoàn tất
        self.watcher.fileChanged.connect(self.on_file_changed)
        self.watcher.directoryChanged.connect(self.on_directory_changed)

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
        self.commit_all_btn.clicked.connect(self.on_commit_button_clicked)   
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
        """Thiết lập giao diện người dùng"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Setup header  
        self.setup_header(layout) 
        
        # Status bar   
        self.status = QLabel("Status: No changes to commit")
        self.status.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.status)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: white;
                gridline-color: #2d2d2d;
                border: none;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: white;
                padding: 5px;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        layout.addWidget(self.table)
        
        # Start Watching button
        self.watch_btn = QPushButton("Start Watching")
        self.watch_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton[watching="true"] {
                background-color: #c0392b;
            }
            QPushButton[watching="true"]:hover {
                background-color: #e74c3c;
            }
        """)
        self.watch_btn.clicked.connect(self.toggle_watching)
        layout.addWidget(self.watch_btn)

    def toggle_watching(self):
        """Toggle watching status"""
        if not self.is_watching:
            self.start_watching()
            self.watch_btn.setText("Stop Watching")
            self.watch_btn.setProperty("watching", True)
        else:
            self.stop_watching()
            self.watch_btn.setText("Start Watching")
            self.watch_btn.setProperty("watching", False)
        
        self.watch_btn.style().unpolish(self.watch_btn)
        self.watch_btn.style().polish(self.watch_btn)

    def start_watching(self):
        """Bắt đầu theo dõi thay đổi"""
        try:
            import os
            
            # Lấy thư mục hiện tại
            current_dir = os.getcwd()
            
            # Thêm thư mục vào watcher
            self.watcher.addPath(current_dir)
            
            # Thêm tất cả các file trong thư mục
            for root, _, files in os.walk(current_dir):
                if '.git' in root:  # Bỏ qua thư mục .git
                    continue
                    
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self._should_ignore_file(Path(file_path)):
                        self.watcher.addPath(file_path)
            
            self.is_watching = True
            self.status.setText("Status: Watching for changes...")
            
        except Exception as e:
            self.status.setText(f"Error starting watch: {str(e)}")
            print(f"Watch error: {str(e)}")

    def stop_watching(self):
        """Dừng theo dõi thay đổi"""
        try:
            # Xóa tất cả paths đang theo dõi
            self.watcher.removePaths(self.watcher.files())
            self.watcher.removePaths(self.watcher.directories())
            
            self.is_watching = False
            self.status.setText("Status: Watching stopped")
            
        except Exception as e:
            self.status.setText(f"Error stopping watch: {str(e)}")
            print(f"Stop watch error: {str(e)}")

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
        """Xử lý khi đóng ứng dụng"""
        try:
            # Dừng các timers
            if hasattr(self, 'auto_commit_timer'):
                self.auto_commit_timer.stop()
            
            if hasattr(self, 'check_alt_timer'):
                self.check_alt_timer.stop()
            
            # Dừng watching
            if self.is_watching:
                self.stop_watching()
            
            # Commit các thay đổi cuối cùng nếu có
            if self.changes_to_commit:
                reply = QMessageBox.question(
                    self,
                    'Uncommitted Changes',
                    'There are uncommitted changes. Do you want to commit them before closing?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.commit_all_changes()
            
            event.accept()
            
        except Exception as e:
            print(f"Close event error: {str(e)}")
            event.accept()  # Vẫn đóng ứng dụng ngay cả khi có lỗi

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

    def on_commit_button_clicked(self):
        """Xử lý khi nhấn nút commit"""
        try:
            if not self.changes_to_commit:
                self.status.setText("Status: No changes to commit")
                return

            self.status.setText("Status: Committing changes...")
            self.commit_all_changes()
            
        except Exception as e:
            self.status.setText(f"Error: {str(e)}")
            print(f"Commit button error: {str(e)}")

    def commit_all_changes(self):
        """Commit tất cả thay đổi ngay lập tức"""
        if not self.changes_to_commit:
            self.status.setText("Status: No changes to commit")
            return
            
        try:
            self.status.setText("Status: Preparing commit...")
            
            # Tạo commit message builder
            builder = CommitMessageBuilder()
            
            # Chuẩn bị danh sách changes
            changes = []
            for change in self.changes_to_commit:
                if 'file' in change and 'type' in change:  # Kiểm tra keys tồn tại
                    changes.append((change['file'], change['type']))
            
            # Kiểm tra changes không rỗng
            if not changes:
                self.status.setText("Status: No valid changes to commit")
                return
                
            # Phân tích changes và tạo message
            try:
                details = builder.analyze_changes(changes)
                if not details:
                    raise ValueError("Could not analyze changes")
                    
                message = builder.build_message(details)
                if not message:
                    raise ValueError("Could not build commit message")
            except Exception as e:
                raise Exception(f"Error preparing commit: {str(e)}")
            
            # Thực hiện git commit
            try:
                self._execute_git_commit(message)
            except Exception as e:
                raise Exception(f"Git commit failed: {str(e)}")
            
            # Cập nhật UI
            self._add_commit_entry(message, highlight=True)
            
            # Cập nhật status cho từng file
            for change in self.changes_to_commit:
                if 'file' in change:
                    self._update_file_status(change['file'], "committed")
            
            # Clear changes và cập nhật status
            self.changes_to_commit.clear()
            self.status.setText("Status: Changes committed successfully")
            
        except Exception as e:
            error_msg = str(e)
            self.status.setText(f"Error: {error_msg}")
            print(f"Commit error: {error_msg}")
            
            # Hiển thị error dialog
            QMessageBox.critical(
                self,
                "Commit Error",
                f"Failed to commit changes:\n{error_msg}",
                QMessageBox.StandardButton.Ok
            )

    def _execute_git_commit(self, message: str):
        """Thực hiện git commit với message"""
        import subprocess
        import os
        
        if not message:
            raise ValueError("Commit message cannot be empty")
            
        try:
            # Đảm bảo đang ở trong git repository
            repo_path = os.getcwd()
            if not os.path.exists(os.path.join(repo_path, '.git')):
                raise Exception("Not a git repository")
            
            # Add tất cả changes
            add_result = subprocess.run(
                ['git', 'add', '.'],
                cwd=repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            if add_result.returncode != 0:
                raise Exception(f"Git add failed: {add_result.stderr}")
            
            # Thực hiện commit
            commit_result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            if commit_result.returncode != 0:
                raise Exception(f"Git commit failed: {commit_result.stderr}")
                
            print("Git commit output:", commit_result.stdout)
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git command failed: {e.stderr}")
        except Exception as e:
            raise Exception(f"Git operation failed: {str(e)}")

    def on_file_changed(self, path: str):
        """Xử lý khi file thay đổi"""
        try:
            file_path = Path(path)
            
            # Bỏ qua các file không cần theo dõi
            if self._should_ignore_file(file_path):
                return
                
            # Xác định loại thay đổi
            change_type = self._determine_change_type(file_path)
            
            # Thêm vào danh sách changes
            self.changes_to_commit.append({
                'file': str(file_path),
                'type': change_type,
                'time': datetime.now()
            })
            
            # Cập nhật UI
            self._add_change_entry(str(file_path), change_type)
            self.status.setText(f"Status: Detected change in {file_path.name}")
            
        except Exception as e:
            self.status.setText(f"Error: {str(e)}")
            print(f"File change error: {str(e)}")

    def on_directory_changed(self, path: str):
        """Xử lý khi thư mục thay đổi"""
        try:
            dir_path = Path(path)
            
            # Quét các file mới trong thư mục
            for file_path in dir_path.glob('*'):
                if not self._should_ignore_file(file_path):
                    # Thêm file mới vào watcher
                    self.watcher.addPath(str(file_path))
                    
            self.status.setText(f"Status: Directory {dir_path.name} updated")
            
        except Exception as e:
            self.status.setText(f"Error: {str(e)}")
            print(f"Directory change error: {str(e)}")

    def _should_ignore_file(self, file_path: Path) -> bool:
        """Kiểm tra có nên bỏ qua file không"""
        ignore_patterns = [
            r'\.git',
            r'__pycache__',
            r'\.pyc$',
            r'\.pyo$',
            r'\.pyd$',
            r'\.so$',
            r'\.dll$',
            r'\.dylib$',
            r'\.log$',
            r'\.tmp$',
            r'\.swp$'
        ]
        
        file_str = str(file_path).lower()
        return any(re.search(pattern, file_str) for pattern in ignore_patterns)

    def _determine_change_type(self, file_path: Path) -> str:
        """Xác định loại thay đổi của file"""
        if not file_path.exists():
            return 'DELETED'
        elif str(file_path) not in [c['file'] for c in self.changes_to_commit]:
            return 'CREATED'
        else:
            return 'MODIFIED'

    def _add_change_entry(self, file_path: str, change_type: str):
        """Thêm entry vào bảng changes"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        type_item = QTableWidgetItem(change_type)
        type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Màu sắc theo loại thay đổi
        if change_type == 'CREATED':
            type_item.setForeground(QColor("#2ecc71"))  # Xanh lá
        elif change_type == 'DELETED':
            type_item.setForeground(QColor("#e74c3c"))  # Đỏ
        else:
            type_item.setForeground(QColor("#3498db"))  # Xanh dương
        
        file_item = QTableWidgetItem(file_path)
        status_item = QTableWidgetItem("pending")
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.table.setItem(row, 0, time_item)
        self.table.setItem(row, 1, type_item)
        self.table.setItem(row, 2, file_item)
        self.table.setItem(row, 3, status_item)
        
        self.table.scrollToBottom()