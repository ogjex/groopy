from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QFrame,
    QPushButton
)
from typing import Protocol, List
class Presenter(Protocol):
    def handle_open_workspace(self, filename):
        ...

    def handle_save_workspace(self):
        ...

    def handle_save_as_workspace(self, filename):
        ...

    def handle_open_group_file(self, filename):
        ...
    
    def handle_new_group_layout():
        raise NotImplementedError("This function is not yet implemented.")

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

        # Connect button click signals to change functions
        open_button.clicked.connect(self.open_workspace)
        save_button.clicked.connect(self.save_workspace)
        save_as_button.clicked.connect(self.save_as_workspace)
        import_group_button.clicked.connect(self.open_group)        
        new_group_layout_button.clicked.connect(self.new_group_layout)

    def open_workspace(self):
        raise NotImplementedError("This function is not yet implemented.")

    def save_workspace(self):
        raise NotImplementedError("This function is not yet implemented.")

    def save_as_workspace(self):
        raise NotImplementedError("This function is not yet implemented.")

    def open_group(self) ->str:
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Json File", "", "Json Files (*.json)")
        if fileName:
            # Load new groups from file
            self.presenter.handle_open_group_file(fileName)
    
    def new_group_layout():
        raise NotImplementedError("This function is not yet implemented.")
