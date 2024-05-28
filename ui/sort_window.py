import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt

class SortWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main layout
        self.setWindowTitle("Sort Window")
        self.layout = QVBoxLayout()

        # Create the top checkbox to check/uncheck all
        self.top_checkbox = QCheckBox("Select All")
        self.top_checkbox.stateChanged.connect(self.toggle_all_checkboxes)
        self.layout.addWidget(self.top_checkbox)

        # Create the QListWidget to hold the checkboxes
        self.checkbox_list = QListWidget()
        self.layout.addWidget(self.checkbox_list)

        # Add checkboxes to the QListWidget
        self.checkbox_dict = {}
        for i in range(5):
            checkbox = QCheckBox(f"Option {i+1}")
            list_item = QListWidgetItem(self.checkbox_list)
            self.checkbox_list.setItemWidget(list_item, checkbox)
            self.checkbox_dict[checkbox.text()] = checkbox

        # Create the buttons
        self.sort_button = QPushButton("Sort Groups")
        self.clear_button = QPushButton("Clear Groups")
        self.layout.addWidget(self.sort_button)
        self.layout.addWidget(self.clear_button)

        # Connect the clear button to its function
        self.clear_button.clicked.connect(self.clear_checkboxes)

        # Set the layout
        self.setLayout(self.layout)

    def toggle_all_checkboxes(self, state):
        for checkbox in self.checkbox_dict.values():
            checkbox.setChecked(state == Qt.CheckState.Checked)

    def clear_checkboxes(self):
        self.top_checkbox.setChecked(False)
        for checkbox in self.checkbox_dict.values():
            checkbox.setChecked(False)

    def get_checked_checkboxes(self):
        return {label: checkbox.isChecked() for label, checkbox in self.checkbox_dict.items()}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortWindow()
    window.show()
    sys.exit(app.exec())