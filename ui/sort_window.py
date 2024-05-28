import sys
from PyQt6.QtWidgets import (
    QApplication, QLineEdit, QLabel, QWidget, QVBoxLayout, QCheckBox, QPushButton, QListWidget, QListWidgetItem
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
        self.setMinimumWidth(200) 
        self.setMaximumWidth(200)
        self.presenter = presenter

        # Set up the main layout
        self.sort_label = QLabel("Sort Groups")
        self.sort_label.setMaximumHeight(50)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.sort_label)

        # Add input fields for minimum group size, maximum group size, and max total number of groups
        self.minimum_group_size_input = QLineEdit()
        self.maximum_group_size_input = QLineEdit()
        self.max_total_groups_input = QLineEdit()
        self.layout.addWidget(QLabel("Minimum group size:"))
        self.layout.addWidget(self.minimum_group_size_input)
        self.layout.addWidget(QLabel("Maximum group size:"))
        self.layout.addWidget(self.maximum_group_size_input)
        self.layout.addWidget(QLabel("Max total number of groups:"))
        self.layout.addWidget(self.max_total_groups_input)

        # Create the top checkbox to check/uncheck all
        self.top_checkbox = QCheckBox("Select All")
        self.top_checkbox.stateChanged.connect(self.toggle_all_checkboxes)  # Correct connection
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
            self.checkbox_dict[checkbox.text()] = checkbox

        # Create the buttons
        self.sort_button = QPushButton("Sort Groups")
        self.clear_button = QPushButton("Clear Groups")
        self.layout.addWidget(self.sort_button)
        self.layout.addWidget(self.clear_button)

        # Connect the buttons to their functions
        self.sort_button.clicked.connect(self.sort_groups)
        #self.clear_button.clicked.connect(self.clear_checkboxes)

        # Set the layout
        self.setLayout(self.layout)

        # Set the maximum height based on the content
        self.adjust_max_height()

    def toggle_all_checkboxes(self):
        if self.top_checkbox.isChecked():
            self.change_checkboxes(True)
        else:
            self.change_checkboxes(False)

    def change_checkboxes(self, value:bool):
        for checkbox in self.checkbox_dict.values():
            checkbox.setChecked(value)

    def get_checkbox_values(self):
        # Return a list of tuples with checkbox labels and their checked states
        return [(label, checkbox.isChecked()) for label, (checkbox, _) in self.checkbox_dict.items()]

    def get_min_group_size(self) -> int:
        """
        Return the minimum group size entered by the user.
        """
        return int(self.minimum_group_size_input.text())

    def get_max_group_size(self) -> int:
        """
        Return the maximum group size entered by the user.
        """
        return int(self.maximum_group_size_input.text())

    def get_max_total_groups(self) -> int:
        """
        Return the maximum total number of groups entered by the user.
        """
        return int(self.max_total_groups_input.text())

    def sort_groups(self):
        # Send the ordered checkbox states to the Presenter
        ordered_checkbox_states = self.get_checkbox_values()
        self.presenter.process_checkbox_order(ordered_checkbox_states)

    def adjust_max_height(self):
        # Calculate the required height
        total_height = sum(widget.sizeHint().height() for widget in [
            self.minimum_group_size_input,
            self.maximum_group_size_input,
            self.max_total_groups_input,
            self.top_checkbox,
            self.sort_button,
            self.clear_button,
        ])
        total_height += sum(checkbox.sizeHint().height() for checkbox in self.checkbox_dict.values())

        total_height += 180  # Adjust this value as needed

        # Set the maximum height
        self.setMaximumHeight(total_height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortWindow()
    window.show()
    sys.exit(app.exec())