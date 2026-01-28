"""
Desktop Application - Offline Course Player

PyQt6-based desktop GUI for managing the Flask video learning platform.
Features:
- Start/Stop server controls
- Native folder picker for content selection
- Server log display
- Auto-start on launch if folder configured

Author: Course Platform Team
Version: 1.0
"""

import sys
import os
import webbrowser
from typing import Optional

# Ensure proper path for imports
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFileDialog, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette

from config import get_static_folder, set_static_folder, get_effective_static_folder
from server import FlaskServerWrapper


class LogSignal(QObject):
    """Signal class for thread-safe log updates."""
    log_message = pyqtSignal(str)


class OfflineCoursePlayerApp(QMainWindow):
    """Main application window for Offline Course Player."""
    
    def __init__(self):
        super().__init__()
        self.server = FlaskServerWrapper()
        self.log_signal = LogSignal()
        self.log_signal.log_message.connect(self._append_log)
        
        self.setup_ui()
        self.update_status()
        
        # Auto-start if folder is configured
        QTimer.singleShot(500, self.auto_start_if_ready)
    
    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Offline Course Player")
        self.setMinimumSize(550, 450)
        self.resize(600, 500)
        
        # Try to set icon if available
        icon_path = os.path.join(APP_DIR, "icons", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header_label = QLabel("📚 Offline Course Player")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setStyleSheet("background-color: #444;")
        layout.addWidget(separator1)
        
        # Status section
        status_layout = QHBoxLayout()
        
        status_title = QLabel("Server Status:")
        status_title.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(status_title)
        
        self.status_label = QLabel("● Stopped")
        self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Folder section
        folder_layout = QHBoxLayout()
        
        folder_title = QLabel("Content Folder:")
        folder_title.setStyleSheet("font-weight: bold;")
        folder_layout.addWidget(folder_title)
        
        self.folder_label = QLabel("Not selected")
        self.folder_label.setStyleSheet("color: #aaa;")
        self.folder_label.setWordWrap(True)
        folder_layout.addWidget(self.folder_label, 1)
        
        self.folder_btn = QPushButton("📁 Select Folder")
        self.folder_btn.clicked.connect(self.select_folder)
        self.folder_btn.setFixedWidth(130)
        folder_layout.addWidget(self.folder_btn)
        
        layout.addLayout(folder_layout)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Start Server")
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setFixedHeight(40)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #666;
            }
        """)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop Server")
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setFixedHeight(40)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #666;
            }
        """)
        btn_layout.addWidget(self.stop_btn)
        
        self.browser_btn = QPushButton("🌐 Open Browser")
        self.browser_btn.clicked.connect(self.open_browser)
        self.browser_btn.setFixedHeight(40)
        self.browser_btn.setEnabled(False)
        self.browser_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #666;
            }
        """)
        btn_layout.addWidget(self.browser_btn)
        
        layout.addLayout(btn_layout)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("background-color: #444;")
        layout.addWidget(separator2)
        
        # Log section
        log_label = QLabel("Server Logs:")
        log_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.log_text, 1)
        
        # Update folder display
        self.update_folder_display()
    
    def apply_dark_theme(self):
        """Apply dark theme to the application."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(100, 100, 200))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ddd;
            }
            QPushButton {
                background-color: #444;
                color: #ddd;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
    
    def update_folder_display(self):
        """Update the folder path display."""
        folder = get_static_folder()
        if folder:
            # Shorten path for display if too long
            display_path = folder
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]
            self.folder_label.setText(display_path)
            self.folder_label.setStyleSheet("color: #8bc34a;")
            self.folder_label.setToolTip(folder)
        else:
            self.folder_label.setText("Not selected - Click 'Select Folder' to choose content location")
            self.folder_label.setStyleSheet("color: #ff9800;")
            self.folder_label.setToolTip("")
    
    def update_status(self):
        """Update server status display."""
        if self.server.is_server_running():
            self.status_label.setText("● Running")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.browser_btn.setEnabled(True)
        else:
            self.status_label.setText("● Stopped")
            self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.browser_btn.setEnabled(False)
    
    def _append_log(self, message: str):
        """Append message to log display (thread-safe via signal)."""
        self.log_text.append(message)
        # Scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def log(self, message: str):
        """Log a message (thread-safe)."""
        self.log_signal.log_message.emit(message)
    
    def select_folder(self):
        """Open folder picker dialog."""
        current = get_static_folder() or os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Course Content Folder",
            current,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            if set_static_folder(folder):
                self.log(f"[APP] Content folder set to: {folder}")
                self.update_folder_display()
                
                # Restart server if running to pick up new folder
                if self.server.is_server_running():
                    self.log("[APP] Restarting server to apply new folder...")
                    self.stop_server()
                    QTimer.singleShot(500, self.start_server)
            else:
                QMessageBox.warning(
                    self,
                    "Invalid Folder",
                    "The selected folder is not accessible. Please choose another folder."
                )
    
    def auto_start_if_ready(self):
        """Auto-start server if folder is configured."""
        folder = get_effective_static_folder()
        if folder:
            self.log("[APP] Content folder found, auto-starting server...")
            self.start_server()
        else:
            self.log("[APP] No content folder configured. Please select a folder.")
    
    def start_server(self):
        """Start the Flask server."""
        folder = get_effective_static_folder()
        if not folder:
            QMessageBox.warning(
                self,
                "No Folder Selected",
                "Please select a content folder before starting the server."
            )
            return
        
        self.log("[APP] Starting server...")
        
        # Set server log callback
        self.server.log_callback = self.log
        
        if self.server.start():
            self.update_status()
            # Auto-open browser after short delay
            QTimer.singleShot(1000, self.open_browser)
        else:
            self.log("[APP] Failed to start server")
            self.update_status()
    
    def stop_server(self):
        """Stop the Flask server."""
        self.log("[APP] Stopping server...")
        self.server.stop()
        self.update_status()
    
    def open_browser(self):
        """Open the web browser to the app URL."""
        url = "http://127.0.0.1:5000"
        self.log(f"[APP] Opening browser: {url}")
        webbrowser.open(url)
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.server.is_server_running():
            self.log("[APP] Closing application, stopping server...")
            self.server.stop()
        event.accept()


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Offline Course Player")
    
    window = OfflineCoursePlayerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
