import sys
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QLabel, QWidget, QVBoxLayout, QMessageBox, QPushButton
)

from typing import Protocol
from ui.sort_list_widget import SortListWidget

class Presenter(Protocol):
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
        self.setMinimumWidth(350) 
        self.setMaximumWidth(350)
        self.presenter = presenter

        # Set up the main layout
        self.lbl_sort = QLabel("Sort Groups")
        self.lbl_sort.setMaximumHeight(50)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_sort)

        # Add dropdowns for minimum group size, maximum group size, and max total number of groups
        self.inp_minimum_group_size = QComboBox()
        self.inp_maximum_group_size = QComboBox()
        self.inp_max_total_groups = QComboBox()
        for i in range(1, 41):
            self.inp_minimum_group_size.addItem(str(i))
            self.inp_maximum_group_size.addItem(str(i))
            self.inp_max_total_groups.addItem(str(i))
        self.layout.addWidget(QLabel("Minimum group size:"))
        self.layout.addWidget(self.inp_minimum_group_size)
        self.layout.addWidget(QLabel("Maximum group size:"))
        self.layout.addWidget(self.inp_maximum_group_size)
        self.layout.addWidget(QLabel("Max total number of groups:"))
        self.layout.addWidget(self.inp_max_total_groups)

        # Load initial values from presenter
        self.set_combobox_values()

        # Connect the combo boxes to their respective slots
        self.inp_minimum_group_size.currentIndexChanged.connect(self.on_min_group_size_changed)
        self.inp_maximum_group_size.currentIndexChanged.connect(self.on_max_group_size_changed)
        self.inp_max_total_groups.currentIndexChanged.connect(self.on_max_total_groups_changed)

        # create the SortListWidget
        drag_widget_dict = {
        "Gender": (True, "Spread"),
        "Education": (False, "Spread"),
        "Experience": (True, "Spread"),
        "Location": (True, "Focus")
        }
        self.sl_widget = SortListWidget("Sort Priority", presenter, drag_widget_dict)
        self.layout.addWidget(self.sl_widget)
        # Create the buttons
        self.btn_sort = QPushButton("Sort Groups")
        self.btn_clear_group = QPushButton("Clear Groups")
        self.layout.addWidget(self.btn_sort)

        # Set the layout
        self.setLayout(self.layout)

        # Set the maximum height based on the content
        self.adjust_max_height()

    def adjust_max_height(self):
        # Calculate the required height
        total_height = sum(widget.sizeHint().height() for widget in [
            self.inp_minimum_group_size,
            self.inp_maximum_group_size,
            self.inp_max_total_groups,
            #self.top_checkbox,
            self.btn_sort,
            self.btn_clear_group,
        ])
        #total_height += sum(checkbox.sizeHint().height() for checkbox in self.checkbox_dict.values())

        total_height += 480  # Adjust this value as needed

        # Set the maximum height
        self.setMaximumHeight(total_height)
        
    def set_combobox_values(self):
        min_group_size = self.presenter.load_initial_min_group_size_value()
        max_group_size = self.presenter.load_initial_max_group_size_value()
        max_total_groups = self.presenter.load_initial_max_total_groups_value()

        self.inp_minimum_group_size.setCurrentIndex(min_group_size - 1)
        self.inp_maximum_group_size.setCurrentIndex(max_group_size - 1)
        self.inp_max_total_groups.setCurrentIndex(max_total_groups - 1)

    def sort_groups(self):
        pass
        # Send the ordered checkbox states to the Presenter
        #ordered_checkbox_states = self.get_checkbox_values()
        #self.presenter.process_checkbox_order(ordered_checkbox_states)

    def get_min_group_size(self) -> int:
        """
        Return the minimum group size entered by the user.
        """
        return int(self.inp_minimum_group_size.currentText())

    def get_max_group_size(self) -> int:
        """
        Return the maximum group size entered by the user.
        """
        return int(self.inp_maximum_group_size.currentText())

    def get_max_total_groups(self) -> int:
        """
        Return the maximum total number of groups entered by the user.
        """
        return int(self.inp_max_total_groups.currentText())

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