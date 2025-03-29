from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QDialog, QLineEdit, QLabel, QWidget
from PySide6.QtCore import Signal

class CustomDialog(QDialog):
    # Define a signal to send data from the dialog to the main window
    dataSubmitted = Signal(str)  

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Data")

        self.layout = QVBoxLayout()
        self.input_field = QLineEdit(self)
        self.submit_button = QPushButton("Submit")

        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

        # Connect button click to send_data method
        self.submit_button.clicked.connect(self.send_data)

    def send_data(self):
        text = self.input_field.text()
        if text:
            self.dataSubmitted.emit(text)  # Emit the signal with the data
            self.accept()  # Close the dialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.button = QPushButton("Open Dialog")
        self.label = QLabel("No data received")

        self.button.clicked.connect(self.open_dialog)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        self.central_widget.setLayout(self.layout)

    def open_dialog(self):
        dialog = CustomDialog()
        dialog.dataSubmitted.connect(self.update_label)  # Connect signal to slot
        dialog.exec()

    def update_label(self, text):
        self.label.setText(f"Received: {text}")


# Run the application
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
