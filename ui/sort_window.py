import sys
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QCheckBox, QPushButton, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from collections import OrderedDict

from typing import Protocol

class Presenter(Protocol):
    def handle_checkbox_order(self, checkboxes) -> None:
        ...
class SortWindow(QWidget):
    def __init__(self, presenter: Presenter):
        super().__init__()
        self.setStyleSheet("background-color: gray")
        self.setMinimumWidth(200) 
        self.setMaximumWidth(200)
        self.presenter = presenter

        # Set up the main layout
        self.sort_label = QLabel("Sort Groups")
        self.sort_label.setMaximumHeight(50)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.sort_label)

 # Create the top checkbox to check/uncheck all
        self.top_checkbox = QCheckBox("Select All")
        self.top_checkbox.stateChanged.connect(self.toggle_all_checkboxes)
        self.layout.addWidget(self.top_checkbox)

        # Create the QListWidget to hold the checkboxes
        self.checkbox_list = QListWidget()
        self.layout.addWidget(self.checkbox_list)

        # Add checkboxes to the QListWidget
        self.checkbox_dict = OrderedDict()
        for i in range(5):
            checkbox = QCheckBox(f"Option {i+1}")
            list_item = QListWidgetItem(self.checkbox_list)
            self.checkbox_list.setItemWidget(list_item, checkbox)
            self.checkbox_dict[checkbox.text()] = (checkbox, list_item)

        # Create the buttons
        self.sort_button = QPushButton("Sort Groups")
        self.clear_button = QPushButton("Clear Groups")
        self.layout.addWidget(self.sort_button)
        self.layout.addWidget(self.clear_button)

        # Connect the buttons to their functions
        self.sort_button.clicked.connect(self.sort_groups)
        self.clear_button.clicked.connect(self.clear_checkboxes)

        # Set the layout
        self.setLayout(self.layout)

        # Set the maximum height based on the content
        self.adjust_max_height()

    def toggle_all_checkboxes(self, state):
        for checkbox, _ in self.checkbox_dict.values():
            checkbox.setChecked(state == Qt.CheckState.Checked)

    def clear_checkboxes(self):
        self.top_checkbox.setChecked(False)
        for checkbox, _ in self.checkbox_dict.values():
            checkbox.setChecked(False)

    def get_checkbox_values(self):
        # Return a list of tuples with checkbox labels and their checked states
        return [(label, checkbox.isChecked()) for label, (checkbox, _) in self.checkbox_dict.items()]

    def sort_groups(self):
        # Send the ordered checkbox states to the Presenter
        ordered_checkbox_states = self.get_checkbox_values()
        self.presenter.process_checkbox_order(ordered_checkbox_states)

    def adjust_max_height(self):
        # Calculate the required height
        padding = 50
        total_height =  self.sort_label.sizeHint().height()
        total_height += self.top_checkbox.sizeHint().height()
        total_height += sum(checkbox.sizeHint().height() for checkbox, _ in self.checkbox_dict.values())
        total_height += self.sort_button.sizeHint().height()
        total_height += self.clear_button.sizeHint().height()
        total_height += padding

        # Set the maximum height
        self.setMaximumHeight(total_height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortWindow()
    window.show()
    sys.exit(app.exec())