from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSizePolicy
)

class WorkspaceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workspace window")
        self.setGeometry(100, 100, 200, 400)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def keyPressEvent(self, event):
        key_actions = {
            Qt.Key.Key_Escape: self.close,
            # Add more key-function mappings as needed
        }

        if event.key() in key_actions:
            action = key_actions[event.key()]
            if callable(action):
                action()
