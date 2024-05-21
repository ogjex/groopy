from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QFrame,
    QPushButton
)
class Presenter(Protocol):
    pass
class WorkspaceWindow(QWidget):
    def __init__(self, presenter = Presenter):
        super().__init__()
        self.presenter = presenter
        self.setGeometry(100, 100, 100, 300)

        workspace_layout = QVBoxLayout()
        self.setLayout(workspace_layout)
                # Workspace
        workspace = QFrame()
        workspace.setStyleSheet("background-color: lightblue;")
        workspace.setMaximumWidth(300)
        
        workspace_button_width = 100
        workspace_button_height = 50
        # Add widgets to layouts
        
        workspace_label = QLabel("Workspace")
        workspace_label.setMaximumHeight(30)
        workspace_layout.addWidget(workspace_label)
        
        open_button = QPushButton("Open", self)
        open_button.setFixedSize(workspace_button_width, workspace_button_height)  # Set fixed size for buttons
        workspace_layout.addWidget(open_button)
        
        save_button = QPushButton("Save", self)
        save_button.setFixedSize(workspace_button_width, workspace_button_height)
        workspace_layout.addWidget(save_button)
        
        save_as_button = QPushButton("Save as", self)
        save_as_button.setFixedSize(workspace_button_width, workspace_button_height)
        workspace_layout.addWidget(save_as_button)

        import_group_button = QPushButton("Import group", self)
        import_group_button.setFixedSize(workspace_button_width, workspace_button_height)
        workspace_layout.addWidget(import_group_button)

        clear_group_layout_button = QPushButton("Clear layout", self)
        clear_group_layout_button.setFixedSize(workspace_button_width, workspace_button_height)
        workspace_layout.addWidget(clear_group_layout_button)
        
        new_group_layout_button = QPushButton("New layout", self)
        new_group_layout_button.setFixedSize(workspace_button_width, workspace_button_height)
        workspace_layout.addWidget(new_group_layout_button)