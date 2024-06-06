from PyQt6.QtWidgets import (
    QHBoxLayout,
    QGridLayout,
    QWidget
)
from typing import Protocol, List

from ui.group_widget import GroupWidget

class Presenter(Protocol):
    def handle_open_group_file(self, filename) -> None:
        ...
    def handle_save_group_file(self, filename, groups_data) -> None:
        ...
class GroupWindow(QWidget):
    def __init__(self, presenter: Presenter):
        super().__init__()
        self.presenter = presenter
        self.grid_layout = QGridLayout()
        self.group_widgets = [] 
        self.setLayout(self.grid_layout)

    def import_group_widgets(self, groups_data):
        for l in groups_data:
            new_group = GroupWidget(l[0],l[1], self.presenter)
            self.grid_layout.addWidget(new_group)
            self.group_widgets.append(new_group)
        self.update_layout()

    def import_group_widgets(self, groups_data):
        for group_id, title, participants in groups_data:
            new_group = GroupWidget(group_id, title, participants, self.presenter)
            self.grid_layout.addWidget(new_group)
            self.group_widgets.append(new_group)
        self.update_layout()

    def clear_group_widgets(self):
        # Remove all GroupWidget instances from the layout
        for group_widget in self.group_widgets:
            self.grid_layout.removeWidget(group_widget)
            group_widget.deleteLater()  # Optional: Ensure proper cleanup of the widget
        self.group_widgets.clear()  # Clear the list to prevent memory leaks

    def update_layout(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                self.grid_layout.removeWidget(widget)
        
        # Calculate how many widgets fit in one row
        max_width = self.width()        
        widget_width = self.group_widgets[0].sizeHint().width()
        widgets_per_row = max_width // widget_width        
    
        if widgets_per_row < 1:
            widgets_per_row = 1
        
        # Add widgets to the grid layout
        for index, widget in enumerate(self.group_widgets):
            row = index // widgets_per_row
            col = index % widgets_per_row
            self.grid_layout.addWidget(widget, row, col)

    def get_groups_data(self) -> List[list]:
        """
        Get the data of all group widgets.
        """
        groups_data = []
        for group_widget in self.group_widgets:
            group_data = group_widget.get_group_data()
            groups_data.append(group_data)
        return groups_data
    
    def set_widget_heights(self, min_height: int, max_height: int):
        """
        Set the minimum and maximum height for all group widgets.
        """
        for group_widget in self.group_widgets:
            group_widget.setMinimumHeight(min_height)
            group_widget.setMaximumHeight(max_height)

    def printGroupsData(self):
        """
        Print data using the getData method of each GroupWidget.
        """
        for group_widget in self.group_widgets:
            print(group_widget.get_item_data())