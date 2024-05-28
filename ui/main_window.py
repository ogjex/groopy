
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QMenuBar
from PyQt6.QtCore import Qt

from typing import Protocol
from ui.group_window import GroupWindow
from ui.details_window import DetailsWindow
from ui.workspace_window import WorkspaceWindow
from ui.sort_window import SortWindow

from presenter import Presenter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1680, 1050)
        self.setWindowTitle("Gettin' Groopy")

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

    def initUI(self, presenter: Presenter):
        self.presenter = presenter
            
        # Menu bar
        menu_bar = QMenuBar()
        menu_bar.setMaximumHeight(50)
        font = menu_bar.font()
        font.setPointSize(10)  # Adjust the font size as needed
        menu_bar.setFont(font)

        file_menu = menu_bar.addMenu("File")
        view_menu = menu_bar.addMenu("View")

        # Content
        # Create the window for groups
        self.group_window = GroupWindow(self.presenter)
        self.details_window = DetailsWindow(self.presenter)
        self.workspace_window = WorkspaceWindow(self.presenter)
        self.workspace_window.setMaximumWidth(150)
        self.sort_window = SortWindow(self.presenter)

        menubar_layout = QVBoxLayout()
        menubar_layout.addWidget(menu_bar)        
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(menubar_layout)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.workspace_window)

        main_content_layout = QVBoxLayout()
        
        overview_filter_layout = QHBoxLayout()
        overview_filter_layout.addWidget(self.group_window)
        overview_filter_layout.addWidget(self.sort_window)

        details_window_layout = QVBoxLayout()
        details_label = QLabel("Details")
        details_label.setMaximumHeight(50)
        details_window_layout.addWidget(details_label)
        details_window_layout.addWidget(self.details_window)

        main_content_layout.addLayout(overview_filter_layout)
        main_content_layout.addLayout(details_window_layout)
        
        content_layout.addLayout(main_content_layout)
        main_layout.addLayout(content_layout)
        self.main_widget.setLayout(main_layout)

    # Define functions for group_window
    def clear_group_widgets(self):
        self.group_window.clear_group_widgets()

    def import_group_widgets(self, groups_data):
        self.group_window.import_group_widgets(groups_data)

    def get_groups_data(self) -> list:
        groups_data = self.group_window.get_groups_data()
        return groups_data

    # Define functions for details_window
    def update_details_window(self, data) -> None:
        self.details_window.set_field_values(data)

    # Define global Keypress events
    def keyPressEvent(self, event):
        key_actions = {
            Qt.Key.Key_Escape: self.close,
            Qt.Key.Key_P: self.group_window.printGroupsData,
            # Add more key-function mappings as needed
        }

        if event.key() in key_actions:
            action = key_actions[event.key()]
            if callable(action):
                action()

