
from PyQt6.QtWidgets import QApplication
from ui.group_window import GroupWindow
from group_editor import GroupEditor
from presenter import Presenter

def main():
    app = QApplication([])
    
    group_window = GroupWindow()
    group_editor = GroupEditor()
    presenter = Presenter(group_editor, group_window)
    presenter.run()

    group_data = [
        ("Group 1", ["Alice", "Bob", "Charlie"]),
        ("Group 2", ["David", "Eve", "Frank"]),
        ("Group 3", ["Grace", "Henry", "Ivy"]),
        ("Group 4", ["Jack", "Kate", "Liam"]),
        ("Group 5", ["Mary", "Nathan", "Olivia"]),
        ("Group 6", ["Peter", "Queen", "Robert"])
    ]
    group_window.import_group_widgets(group_data)

    app.exec()

if __name__ == "__main__":
    main()