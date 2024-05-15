from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFileDialog,
    QWidget
)
from typing import Protocol, List

from ui.group_widget import GroupWidget

class Presenter(Protocol):
    def handle_open_group_file(self, filename) -> None:
        ...
    def handle_save_group_file(self, filename) -> None:
        ...
class GroupWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.blayout = QHBoxLayout()
        self.group_widgets = [] 
        self.setLayout(self.blayout)

    def import_group_widgets(self, groups_data):
        for l in groups_data:
            new_group = GroupWidget(l[0],l[1])
            self.blayout.addWidget(new_group)
            self.group_widgets.append(new_group)

    def clear_group_widgets(self):
        # Remove all GroupWidget instances from the layout
        for group_widget in self.group_widgets:
            self.blayout.removeWidget(group_widget)
            group_widget.deleteLater()  # Optional: Ensure proper cleanup of the widget
        self.group_widgets.clear()  # Clear the list to prevent memory leaks

    def save_groups_file(self, presenter: Presenter):
        # Open file dialog to select a json file        
        fileName, _ = QFileDialog.getSaveFileName(self,"Save Json File", "","Json Files (*.json)")
        if fileName:
            groups_data = self.get_groups_data()
            presenter.handle_save_group_file(fileName, groups_data)

    def load_groups_file(self, presenter: Presenter):
        # Open file dialog to select a json file
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Json File", "", "Json Files (*.json)")
        if fileName:
            # Clear existing group widgets
            self.clear_group_widgets()
            
            # Load new groups from file
            presenter.handle_open_group_file(fileName)

    def get_groups_data(self) -> List[list]:
        """
        Get the data of all group widgets.
        """
        groups_data = []
        for group_widget in self.group_widgets:
            group_data = group_widget.get_group_data()
            groups_data.append(group_data)
        return groups_data
    
    def printGroupsData(self):
        """
        Print data using the getData method of each GroupWidget.
        """
        for group_widget in self.group_widgets:
            print(group_widget.get_item_data())