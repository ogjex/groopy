from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget,
)
from group_widget import GroupWidget

class Window(QWidget):
    def __init__(self):
        super().__init__()

        groups_data = [
            ("Group 1", ["Alice", "Bob", "Charlie"]),
            ("Group 2", ["David", "Eve", "Frank"]),
            ("Group 3", ["Grace", "Henry", "Ivy"]),
            ("Group 4", ["Jack", "Kate", "Liam"]),
            ("Group 5", ["Mary", "Nathan", "Olivia"]),
            ("Group 6", ["Peter", "Queen", "Robert"])
        ]


        self.blayout = QHBoxLayout()
        self.group_widgets = [] 

        for l in groups_data:
            new_group = GroupWidget(l[0],l[1])
            self.blayout.addWidget(new_group)
            self.group_widgets.append(new_group)

        self.setLayout(self.blayout)

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
        
app = QApplication([])
w = Window()
w.show()

app.exec()