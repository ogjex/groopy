from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QFrame,
    QPushButton,
    QMessageBox
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
    def handle_save_group_file(self, filename):
        ...
    def handle_clear_group_layout(self):
        ...
    def handle_new_group_layout(self):
        ...

class WorkspaceWindow(QWidget):
    def __init__(self, presenter = Presenter):
        super().__init__()
        self.presenter = presenter
        self.workspace_path = ""
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
        
# Create a vertical layout for the buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)  # Set vertical spacing between buttons

        open_button = QPushButton("Open", self)
        open_button.setFixedSize(workspace_button_width, workspace_button_height)
        buttons_layout.addWidget(open_button)

        save_button = QPushButton("Save", self)
        save_button.setFixedSize(workspace_button_width, workspace_button_height)
        buttons_layout.addWidget(save_button)

        save_as_button = QPushButton("Save as", self)
        save_as_button.setFixedSize(workspace_button_width, workspace_button_height)
        buttons_layout.addWidget(save_as_button)

        import_group_button = QPushButton("Import group", self)
        import_group_button.setFixedSize(workspace_button_width, workspace_button_height)
        buttons_layout.addWidget(import_group_button)

        clear_group_layout_button = QPushButton("Clear layout", self)
        clear_group_layout_button.setFixedSize(workspace_button_width, workspace_button_height)
        buttons_layout.addWidget(clear_group_layout_button)

        new_group_layout_button = QPushButton("New layout", self)
        new_group_layout_button.setFixedSize(workspace_button_width, workspace_button_height)
        buttons_layout.addWidget(new_group_layout_button)

        # Add a spacer item at the bottom to keep buttons at the top
        buttons_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Add the buttons layout to the main layout
        workspace_layout.addLayout(buttons_layout)

        # Connect button click signals to change functions
        open_button.clicked.connect(self.open_workspace)
        save_button.clicked.connect(self.save_workspace)
        save_as_button.clicked.connect(self.save_as_workspace)
        import_group_button.clicked.connect(self.open_group)        
        clear_group_layout_button.clicked.connect(self.open_clear_group_layout)
        new_group_layout_button.clicked.connect(self.new_group_layout)

    def set_workspace_path(self, file_path: str):
        self.workspace_path = file_path

    def is_workspace_path_set(self) -> bool:
        return bool(self.workspace_path)

    def open_workspace(self):
        raise NotImplementedError("This function is not yet implemented.")

    def save_workspace(self):
        if not self.is_workspace_path_set():
            self.save_as_workspace()
        else:
            self.presenter.handle_save_group_file(self.workspace_path)

    def save_as_workspace(self):
        # currently calls save group but needs to fuse with a future workspace_handler
        file_path, _ = QFileDialog.getSaveFileName(self,"Save Json File", "","Json Files (*.json)")
        if file_path:
            self.presenter.handle_save_group_file(file_path)
            self.set_workspace_path(file_path)

    def open_group(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Json File", "", "Json Files (*.json)")
        if file_path:
            # Load new groups from file
            self.presenter.handle_open_group_file(file_path)
    
    def open_clear_group_layout(self) -> None:
        reply = QMessageBox.warning(
            self,
            'Warning',
            'This clears your current layout. Do you wish to proceed?',
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )

        if reply == QMessageBox.StandardButton.Ok:
            self.presenter.handle_clear_group_layout()
        else:
            return

    def new_group_layout(self):
        raise NotImplementedError("This function is not yet implemented.")
