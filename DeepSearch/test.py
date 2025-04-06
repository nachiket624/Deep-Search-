import sys
import json
import os
import hashlib
import shutil
import tempfile
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox


# Determine the application's base directory (handles both normal & EXE modes)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # PyInstaller temporary directory
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "user_config.json")

def hash_text(text):
    """Generate SHA-256 hash of the input text (username or password)."""
    return hashlib.sha256(text.encode()).hexdigest()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup - First Time Login")
        self.setGeometry(100, 100, 300, 200)

        # UI Elements
        self.label_username = QLabel("Set Username:")
        self.input_username = QLineEdit(self)

        self.label_password = QLabel("Set Password:")
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)  # Hide password input

        self.button_save = QPushButton("Save & Continue")
        self.button_save.clicked.connect(self.save_credentials)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_save)
        self.setLayout(layout)

    def save_credentials(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if username and password:
            hashed_username = hash_text(username)  # Hash the username
            hashed_password = hash_text(password)  # Hash the password

            # Save hashed credentials
            with open(CONFIG_FILE, "w") as f:
                json.dump({"username": hashed_username, "password": hashed_password}, f)

            QMessageBox.information(self, "Success", "Credentials saved securely! Restarting...")
            self.close()
            main_app()  # Launch the main application
        else:
            QMessageBox.warning(self, "Error", "Username and password cannot be empty.")

def verify_login(username, password):
    """Verify if entered credentials match the stored credentials."""
    if not os.path.exists(CONFIG_FILE):
        return False  # No stored credentials yet

    with open(CONFIG_FILE, "r") as f:
        stored_data = json.load(f)

    stored_hashed_username = stored_data.get("username")
    stored_hashed_password = stored_data.get("password")

    return stored_hashed_username == hash_text(username) and stored_hashed_password == hash_text(password)

def main_app():
    """Main application window after first-time setup."""
    QMessageBox.information(None, "Welcome", "Launching main application...")

def check_first_time():
    """Check if credentials already exist."""
    return os.path.exists(CONFIG_FILE)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if check_first_time():
        main_app()  # Skip login if credentials exist
    else:
        window = LoginWindow()
        window.show()

    sys.exit(app.exec())
