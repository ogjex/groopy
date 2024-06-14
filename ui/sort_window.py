import sys
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QLabel, QWidget, QVBoxLayout, QCheckBox, QPushButton, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from collections import OrderedDict

from typing import Protocol
from ui.drag_widget import DragCheckBox

class Presenter(Protocol):
    def handle_checkbox_order(self, checkboxes: list) -> None:
        ...
    def handle_min_group_size_changed(self, new_value: int) -> None:
        ...
    def handle_max_group_size_changed(self, new_value: int) -> None:
        ...
    def handle_max_total_groups_changed(self, new_value: int) -> None:
        ...
    def load_initial_min_group_size_value(self) -> int:
        ...
    def load_initial_max_group_size_value(self) -> int:
        ...
    def load_initial_max_total_groups_value(self) -> int:
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

        # Add dropdowns for minimum group size, maximum group size, and max total number of groups
        self.minimum_group_size_input = QComboBox()
        self.maximum_group_size_input = QComboBox()
        self.max_total_groups_input = QComboBox()
        for i in range(1, 41):
            self.minimum_group_size_input.addItem(str(i))
            self.maximum_group_size_input.addItem(str(i))
            self.max_total_groups_input.addItem(str(i))
        self.layout.addWidget(QLabel("Minimum group size:"))
        self.layout.addWidget(self.minimum_group_size_input)
        self.layout.addWidget(QLabel("Maximum group size:"))
        self.layout.addWidget(self.maximum_group_size_input)
        self.layout.addWidget(QLabel("Max total number of groups:"))
        self.layout.addWidget(self.max_total_groups_input)

        # Load initial values from presenter
        self.set_combobox_values()

        # Connect the combo boxes to their respective slots
        self.minimum_group_size_input.currentIndexChanged.connect(self.on_min_group_size_changed)
        self.maximum_group_size_input.currentIndexChanged.connect(self.on_max_group_size_changed)
        self.max_total_groups_input.currentIndexChanged.connect(self.on_max_total_groups_changed)

        # Create the top checkbox to check/uncheck all
        self.top_checkbox = QCheckBox("Select All")
        self.top_checkbox.stateChanged.connect(self.toggle_all_checkboxes)
        self.layout.addWidget(self.top_checkbox)

        # Create the QListWidget to hold the checkboxes
        self.checkbox_list = QListWidget()
        self.layout.addWidget(self.checkbox_list)

        # Add checkboxes to the QListWidget
        self.checkbox_dict = OrderedDict()

        '''for i in range(5):
            checkbox = QCheckBox(f"Option {i+1}")
            list_item = QListWidgetItem(self.checkbox_list)
            self.checkbox_list.setItemWidget(list_item, checkbox)
            self.checkbox_dict[checkbox.text()] = checkbox'''

        # Create the buttons
        self.sort_button = QPushButton("Sort Groups")
        self.clear_button = QPushButton("Clear Groups")
        self.layout.addWidget(self.sort_button)
        self.layout.addWidget(self.clear_button)

        # Connect the buttons to their functions
        #self.sort_button.clicked.connect(self.set_checkboxes_test)
        #self.clear_button.clicked.connect(self.clear_checkboxes)

        # Set the layout
        self.setLayout(self.layout)

        # Set the maximum height based on the content
        self.adjust_max_height()

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
        
    def set_combobox_values(self):
        min_group_size = self.presenter.load_initial_min_group_size_value()
        max_group_size = self.presenter.load_initial_max_group_size_value()
        max_total_groups = self.presenter.load_initial_max_total_groups_value()

        self.minimum_group_size_input.setCurrentIndex(min_group_size - 1)
        self.maximum_group_size_input.setCurrentIndex(max_group_size - 1)
        self.max_total_groups_input.setCurrentIndex(max_total_groups - 1)

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

    def sort_groups(self):
        # Send the ordered checkbox states to the Presenter
        ordered_checkbox_states = self.get_checkbox_values()
        self.presenter.process_checkbox_order(ordered_checkbox_states)


    def get_min_group_size(self) -> int:
        """
        Return the minimum group size entered by the user.
        """
        return int(self.minimum_group_size_input.currentText())

    def get_max_group_size(self) -> int:
        """
        Return the maximum group size entered by the user.
        """
        return int(self.maximum_group_size_input.currentText())

    def get_max_total_groups(self) -> int:
        """
        Return the maximum total number of groups entered by the user.
        """
        return int(self.max_total_groups_input.currentText())

    def on_min_group_size_changed(self):
        min_group_size = self.get_min_group_size()
        self.presenter.handle_min_group_size_changed(min_group_size)

    def on_max_group_size_changed(self):
        max_group_size = self.get_max_group_size()
        self.presenter.handle_max_group_size_changed(max_group_size)

    def on_max_total_groups_changed(self):
        max_total_groups = self.get_max_total_groups()
        self.presenter.handle_max_total_groups_changed(max_total_groups)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SortWindow(presenter=None)  # Replace with an actual presenter instance
    window.show()
    sys.exit(app.exec())