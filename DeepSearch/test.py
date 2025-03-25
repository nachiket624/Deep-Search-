from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt

app = QApplication([])

# Create Table
table = QTableWidget(3, 2)
table.setWordWrap(True)  # Enable word wrap
table.setHorizontalHeaderLabels(["Column 1", "Column 2"])
table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Make cells read-only
table.setTextElideMode(Qt.ElideNone)  # Prevent text truncation

# Add Long Text Items
long_text = "This is a long text that should wrap inside the QTableWidget cell."
for row in range(3):
    for col in range(2):
        item = QTableWidgetItem(long_text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Prevent editing
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align text properly
        table.setItem(row, col, item)

# Adjust Row Heights
table.resizeRowsToContents()

# Show Table
table.show()
app.exec()
