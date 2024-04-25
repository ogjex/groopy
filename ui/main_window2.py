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

        # Menu bar
        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("File")
        view_menu = menu_bar.addMenu("View")

        # Workspace
        workspace = QFrame()
        workspace.setStyleSheet("background-color: lightblue;")
        workspace.setMaximumWidth(300)

        # Content
        content = QFrame()
        content.setStyleSheet("background-color: blue;")
        
        # Filter bar

        filter_bar = QFrame()
        filter_bar.setStyleSheet("background-color: gray;")
        filter_bar.setMaximumWidth(300)

        # Details window
        details_window = QFrame()
        details_window.setStyleSheet("background-color: lightgreen;")

        menubar_layout = QVBoxLayout()
        menubar_layout.addWidget(menu_bar)        
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(menubar_layout)
        content_layout = QHBoxLayout()
        content_layout.addWidget(workspace)

        main_content_layout = QVBoxLayout()
        
        overview_filter_layout = QHBoxLayout()
        overview_filter_layout.addWidget(content)
        overview_filter_layout.addWidget(filter_bar)

        main_content_layout.addLayout(overview_filter_layout)
        details_window_layout = QVBoxLayout()
        details_window_layout.addWidget(QLabel("Details"))
        details_window_layout.addWidget(details_window)

        main_content_layout.addLayout(overview_filter_layout)
        main_content_layout.addLayout(details_window_layout)
        
        content_layout.addLayout(main_content_layout)
        main_layout.addLayout(content_layout)
        main_widget.setLayout(main_layout)

        '''window = QWidget()
        queryLabel = QLabel(()
            QApplication.translate("nestedlayouts", "Query:"))
        queryEdit = QLineEdit()
        resultView = QTableView()
        queryLayout = QHBoxLayout()
        queryLayout.addWidget(queryLabel)
        queryLayout.addWidget(queryEdit)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(queryLayout)
        mainLayout.addWidget(resultView)
        window.setLayout(mainLayout)'''

        '''# Create the nested layouts
        main_layout = QVBoxLayout()
        content_layout = QVBoxLayout()
        content_filter = QHBoxLayout()


        main_layout.addWidget(menu_bar)


        # Add widgets to layouts
        workspace_layout = QVBoxLayout()
        workspace_layout.addWidget(QLabel("Workspace"))
        workspace_layout.addWidget(QPushButton("Button 1"))
        workspace_layout.addWidget(QPushButton("Button 2"))
        workspace.setLayout(workspace_layout)
        
                

        workspace_content_layout.addWidget(workspace)

        # Main content
        group_overview = QTabWidget()
        content_filter.addWidget(group_overview)
        main_layout.addLayout(workspace_content_layout)

        # Add tabs to main content
        tab1 = QWidget()
        tab2 = QWidget()
        group_overview.addTab(tab1, "Tab 1")
        group_overview.addTab(tab2, "Tab 2")

        # Add the layouts to the main layout
        '''

        '''main_layout.addLayout(workspace_content_layout)
        main_layout.addLayout(content_layout)
        main_layout.addLayout(content_filter)
        main_widget.setLayout(main_layout)'''
        

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
