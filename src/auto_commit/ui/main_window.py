from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTableWidget, QTableWidgetItem, QLabel,
                           QStatusBar, QSystemTrayIcon, QMenu, QStyle, QApplication,
                           QFrame, QHeaderView)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon, QFont, QColor
from datetime import datetime
import sys
import os

class CustomTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #262626;
                color: #ffffff;
                border: none;
                gridline-color: transparent;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333333;
            }
            QTableWidget::item:selected {
                background-color: #2d5a88;
            }
            QHeaderView::section {
                background-color: #252525;
                color: #ffffff;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #3daee9;
                font-weight: bold;
            }
        """)

class CustomButton(QPushButton):
    def __init__(self, text, color="#3daee9"):
        super().__init__(text)
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #555555;
                color: #888888;
            }}
        """)

    def _lighten_color(self, color, factor=120):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, c + factor) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def _darken_color(self, color, factor=30):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, c - factor) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Auto Commit")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QStatusBar {
                background-color: #252525;
                color: #ffffff;
                border-top: 1px solid #333333;
            }
        """)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #252525; border-radius: 8px;")
        header_layout = QVBoxLayout(header_frame)
        
        # Title
        title = QLabel("Auto Commit")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #3daee9;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("color: #ffd700; font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.status_label)
        
        layout.addWidget(header_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = CustomButton("Start Watching", "#2ecc71")
        self.stop_button = CustomButton("Stop Watching", "#e74c3c")
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # Table
        self.table = CustomTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File", "Status"])
        layout.addWidget(self.table)
        
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # System Tray
        self.setup_system_tray()
        
        # Connections
        self.start_button.clicked.connect(self.start_watching)
        self.stop_button.clicked.connect(self.stop_watching)
        
        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table)
        
    def setup_system_tray(self):
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.app.quit)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def add_change(self, file_path: str, change_type: str, status: str = "committed"):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        type_item = QTableWidgetItem(change_type)
        file_item = QTableWidgetItem(str(file_path))
        status_item = QTableWidgetItem(status)
        
        # Set colors based on change type
        if change_type == "CREATED":
            type_item.setForeground(QColor("#2ecc71"))  # Green
        elif change_type == "MODIFIED":
            type_item.setForeground(QColor("#f1c40f"))  # Yellow
        elif change_type == "DELETED":
            type_item.setForeground(QColor("#e74c3c"))  # Red
            
        items = [time_item, type_item, file_item, status_item]
        for col, item in enumerate(items):
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, col, item)
        
        self.table.scrollToBottom()
        
    def start_watching(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Status: Watching")
        self.status_label.setStyleSheet("color: #2ecc71; font-size: 16px;")
        self.timer.start(1000)
        
    def stop_watching(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("color: #e74c3c; font-size: 16px;")
        self.timer.stop()
        
    def update_table(self):
        """Cập nhật bảng và xử lý lỗi"""
        try:
            # Cập nhật status bar
            total_changes = self.table.rowCount()
            self.status_bar.showMessage(f"Total changes: {total_changes}")
            
            # Giới hạn số lượng hàng trong bảng để tránh quá tải
            MAX_ROWS = 1000
            if total_changes > MAX_ROWS:
                # Xóa các hàng cũ nhất
                for _ in range(total_changes - MAX_ROWS):
                    self.table.removeRow(0)
            
            # Xử lý các sự kiện Qt
            QApplication.processEvents()
            
        except Exception as e:
            print(f"Error updating table: {str(e)}")
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def closeEvent(self, event):
        """Xử lý sự kiện đóng window"""
        try:
            # Dừng timer trước khi đóng
            if self.timer.isActive():
                self.timer.stop()
            
            # Ẩn window thay vì đóng
            self.hide()
            self.tray.showMessage(
                "Auto Commit",
                "Application minimized to tray",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            event.ignore()
            
        except Exception as e:
            print(f"Error closing window: {str(e)}")
            event.accept()

    def cleanup(self):
        """Dọn dẹp resources trước khi đóng"""
        try:
            if self.timer.isActive():
                self.timer.stop()
            if self.tray is not None:
                self.tray.hide()
        except Exception as e:
            print(f"Error during cleanup: {str(e)}") 