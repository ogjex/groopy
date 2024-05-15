import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QFrame, QPushButton, QLabel, QMenuBar, QAction
from PyQt5.QtCore import Qt

from typing import Protocol
from ui.group_window import GroupWindow

class Presenter(Protocol):
    def handle_open_group_file(self, filename) -> None:
        ...
    def handle_save_group_file(self, filename) -> None:
        ...

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
    def initUI(self, presenter: Presenter):
        self.presenter:Presenter
            
        self.setMinimumSize(1366, 768)
        self.setWindowTitle("Gettin' Groopy")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Menu bar
        menu_bar = QMenuBar()
        font = menu_bar.font()
        font.setPointSize(10)  # Adjust the font size as needed
        menu_bar.setFont(font)

        file_menu = menu_bar.addMenu("File")
        view_menu = menu_bar.addMenu("View")

        # Workspace
        workspace = QFrame()
        workspace.setStyleSheet("background-color: lightblue;")
        workspace.setMaximumWidth(300)
        # Add widgets to layouts
        workspace_layout = QVBoxLayout()
        
        workspace_label = QLabel("Workspace")
        workspace_label.setMaximumHeight(30)
        workspace_layout.addWidget(workspace_label)
        
        save_button = QPushButton("Save", self)
        save_button.setFixedSize(50, 50)  # Set fixed size for buttons
        workspace_layout.addWidget(save_button)
        
        load_button = QPushButton("Open", self)
        load_button.setFixedSize(50, 50)  # Set fixed size for buttons
        workspace_layout.addWidget(load_button)

        # Connect button click signal to color change function
        save_button.clicked.connect(self.save_groups_file)
        load_button.clicked.connect(self.load_groups_file)
        
        workspace.setLayout(workspace_layout)

        # Content
        # Create the window for groups
        self.group_window = GroupWindow()
        # Add tabs to the main content as needed
        
        # Filter bar
        filter_bar = QFrame()
        filter_bar.setStyleSheet("background-color: gray;")
        filter_bar.setMinimumWidth(300) 
        filter_bar.setMaximumWidth(300)

        # Details window
        details_label = QLabel("Details")
        details_window = QFrame()
        details_window.setStyleSheet("background-color: lightgreen;")
        details_window.setMinimumHeight(100)         

        menubar_layout = QVBoxLayout()
        menubar_layout.addWidget(menu_bar)        
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(menubar_layout)

        content_layout = QHBoxLayout()
        content_layout.addWidget(workspace)

        main_content_layout = QVBoxLayout()
        
        overview_filter_layout = QHBoxLayout()
        overview_filter_layout.addWidget(self.group_window)
        overview_filter_layout.addWidget(filter_bar)

        details_window_layout = QVBoxLayout()
        details_window_layout.addWidget(details_label)
        details_window_layout.addWidget(details_window)

        main_content_layout.addLayout(overview_filter_layout)
        main_content_layout.addLayout(details_window_layout)
        
        content_layout.addLayout(main_content_layout)
        main_layout.addLayout(content_layout)
        main_widget.setLayout(main_layout)

    # Define functions for group_window
    def save_groups_file(self, presenter):
        self.group_window.save_groups_file(presenter)

    def load_groups_file(self, presenter):
        self.group_window.load_groups_file(presenter)

    # Define keypress events globally
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Center the window on the screen
    window_width = window.frameGeometry().width()
    window_height = window.frameGeometry().height()
    screen = app.primaryScreen()
    screen_width = screen.size().width()
    screen_height = screen.size().height()
    window.move((screen_width - window_width) // 2, (screen_height - window_height) // 2)
    
    window.show()
    sys.exit(app.exec_())
