from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QWidget
)
from ui.group_widget import GroupWidget
from typing import Protocol, List

class Presenter(Protocol):
    def handle_open_group_file(self, filename) -> None:
        ...
    def handle_save_group_file(self, filename) -> None:
        ...
class GroupWindow(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self, presenter:Presenter):
        self.presenter = presenter

        self.blayout = QHBoxLayout()
        self.group_widgets = [] 

        save_button = QPushButton("Save", self)
        save_button.setFixedSize(50, 50)  # Set fixed size for buttons
        self.blayout.addWidget(save_button)
        
        load_button = QPushButton("Open", self)
        load_button.setFixedSize(50, 50)  # Set fixed size for buttons
        self.blayout.addWidget(load_button)
        
        self.setLayout(self.blayout)
        # Connect button click signal to color change function
        save_button.clicked.connect(self.save_groups_file)
        load_button.clicked.connect(self.load_groups_file)

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

    def save_groups_file(self):
        # Open file dialog to select a json file        
        fileName, _ = QFileDialog.getSaveFileName(self,"Save Json File", "","Json Files (*.json)")
        if fileName:
            groups_data = self.get_groups_data()
            self.presenter.handle_save_group_file(fileName, groups_data)

    def load_groups_file(self):
        # Open file dialog to select a json file
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Json File", "", "Json Files (*.json)")
        if fileName:
            # Clear existing group widgets
            self.clear_group_widgets()
            
            # Load new groups from file
            self.presenter.handle_open_group_file(fileName)

    def get_groups_data(self) -> List[list]:
        """
        Get the data of all group widgets.
        """
        groups_data = []
        for group_widget in self.group_widgets:
            group_data = group_widget.get_group_data()
            groups_data.append(group_data)
        return groups_data

    def keyPressEvent(self, event):
        key_actions = {
            Qt.Key.Key_Escape: self.close,
            Qt.Key.Key_P: self.printGroupsData,
            # Add more key-function mappings as needed
        }

        if event.key() in key_actions:
            action = key_actions[event.key()]
            if callable(action):
                action()

    def printGroupsData(self):
        """
        Print data using the getData method of each GroupWidget.
        """
        for group_widget in self.group_widgets:
            print(group_widget.get_item_data())