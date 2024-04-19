import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenuBar, QAction, QVBoxLayout, QHBoxLayout, QTabWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the menu bar
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("File")
        view_menu = menu_bar.addMenu("View")
        self.setMenuBar(menu_bar)

        # Create the workspace (left side)
        workspace = QWidget()
        workspace.setMaximumWidth(300)  # Set maximum width
        # Add text and buttons to the workspace as needed

        # Create the vertical bar (right side)
        vertical_bar = QWidget()
        vertical_bar.setMaximumWidth(300)  # Set maximum width
        # Add any widgets you need for the vertical bar

        # Create the main content (center)
        main_content = QTabWidget()
        # Add tabs to the main content as needed
        tab1 = QWidget()
        tab2 = QWidget()
        main_content.addTab(tab1, "Tab 1")
        main_content.addTab(tab2, "Tab 2")

        # Create the details window (bottom)
        details_window = QWidget()
        # Add any widgets you need for the details window

        # Set up the main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(workspace)
        main_layout.addWidget(main_content)
        main_layout.addWidget(vertical_bar)
        main_layout.addWidget(details_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
