from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTableWidget, QTableWidgetItem, QLabel,
                           QStatusBar, QSystemTrayIcon, QMenu, QStyle)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
from datetime import datetime
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Commit")
        self.setMinimumSize(800, 600)
        
        # Thiết lập style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3daee9;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4dc4ff;
            }
            QTableWidget {
                background-color: #363636;
                color: #ffffff;
                gridline-color: #4a4a4a;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #4a4a4a;
            }
            QStatusBar {
                color: #ffffff;
            }
        """)
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("Auto Commit")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3daee9;")
        header.addWidget(title)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Watching")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        header.addLayout(button_layout)
        layout.addLayout(header)
        
        # Status
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("color: #ffd700;")
        layout.addWidget(self.status_label)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "Type", "File", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # System Tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(app.quit)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()
        
        # Connections
        self.start_button.clicked.connect(self.start_watching)
        self.stop_button.clicked.connect(self.stop_watching)
        
        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table)
        
    def add_change(self, file_path: str, change_type: str, status: str = "committed"):
        """Add a new change to the table"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        type_item = QTableWidgetItem(change_type)
        file_item = QTableWidgetItem(str(file_path))
        status_item = QTableWidgetItem(status)
        
        # Set colors based on change type
        if change_type == "CREATED":
            type_item.setForeground(Qt.GlobalColor.green)
        elif change_type == "MODIFIED":
            type_item.setForeground(Qt.GlobalColor.yellow)
        elif change_type == "DELETED":
            type_item.setForeground(Qt.GlobalColor.red)
            
        self.table.setItem(row, 0, time_item)
        self.table.setItem(row, 1, type_item)
        self.table.setItem(row, 2, file_item)
        self.table.setItem(row, 3, status_item)
        
        # Scroll to bottom
        self.table.scrollToBottom()
        
    def start_watching(self):
        """Start watching for changes"""
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("Status: Watching")
        self.status_label.setStyleSheet("color: #00ff00;")
        self.timer.start(1000)  # Update every second
        
    def stop_watching(self):
        """Stop watching for changes"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("color: #ff0000;")
        self.timer.stop()
        
    def update_table(self):
        """Update table with new changes"""
        # This will be connected to the file watcher
        pass
        
    def closeEvent(self, event):
        """Handle window close event"""
        self.hide()
        self.tray.showMessage(
            "Auto Commit",
            "Application minimized to tray",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
        event.ignore() 