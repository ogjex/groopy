import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QFrame, QPushButton, QLabel, QMenuBar, QAction
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(1366, 768)
        self.setWindowTitle("Resizable Window")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Menu bar
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("File")
        view_menu = menu_bar.addMenu("View")
        main_layout.addWidget(menu_bar)

        # Workspace
        workspace = QFrame()
        workspace.setStyleSheet("background-color: lightblue;")
        workspace.setMaximumWidth(300)
        workspace_layout = QVBoxLayout()
        workspace.setLayout(workspace_layout)
        workspace_layout.addWidget(QLabel("Workspace"))
        workspace_layout.addWidget(QPushButton("Button 1"))
        workspace_layout.addWidget(QPushButton("Button 2"))
        main_layout.addWidget(workspace)

        # Vertical bar
        vertical_bar = QFrame()
        vertical_bar.setStyleSheet("background-color: gray;")
        vertical_bar.setMaximumWidth(300)
        main_layout.addWidget(vertical_bar)

        # Main content
        main_content = QTabWidget()
        main_layout.addWidget(main_content)

        # Details window
        details_window = QFrame()
        details_window.setStyleSheet("background-color: lightgreen;")
        details_window_layout = QVBoxLayout()
        details_window.setLayout(details_window_layout)
        details_window_layout.addWidget(QLabel("Details"))
        main_layout.addWidget(details_window)

        # Add tabs to main content
        tab1 = QWidget()
        tab2 = QWidget()
        main_content.addTab(tab1, "Tab 1")
        main_content.addTab(tab2, "Tab 2")

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
