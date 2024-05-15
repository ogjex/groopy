import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from group_editor import GroupEditor
from presenter import Presenter

def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    
    group_editor = GroupEditor()

    # Center the window on the screen
    window_width = main_window.frameGeometry().width()
    window_height = main_window.frameGeometry().height()
    screen = app.primaryScreen()
    screen_width = screen.size().width()
    screen_height = screen.size().height()
    main_window.move((screen_width - window_width) // 2, (screen_height - window_height) // 2)
    
    presenter = Presenter(group_editor, main_window)
    presenter.run()
    
    groups_data = [
        ("Group 1", ["Alice", "Bob", "Charlie"]),
        ("Group 2", ["David", "Eve", "Frank"]),
        ("Group 3", ["Grace", "Henry", "Ivy"]),
        ("Group 4", ["Jack", "Kate", "Liam"]),
        ("Group 5", ["Mary", "Nathan", "Olivia"]),
        ("Group 6", ["Peter", "Queen", "Robert"])
    ]
    
    main_window.import_group_widgets(groups_data)
    

    sys.exit(app.exec())

if __name__ == "__main__":
    main()