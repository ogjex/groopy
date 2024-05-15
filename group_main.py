from PyQt6.QtWidgets import QApplication
from ui.group_window import GroupWindow
from presenter import Presenter

def main():
    app = QApplication([])
    
    group_window = GroupWindow()
    presenter = Presenter()
    group_window.initUI(presenter)

    group_data = [
        ("Group 1", ["Alice", "Bob", "Charlie"]),
        ("Group 2", ["David", "Eve", "Frank"]),
        ("Group 3", ["Grace", "Henry", "Ivy"]),
        ("Group 4", ["Jack", "Kate", "Liam"]),
        ("Group 5", ["Mary", "Nathan", "Olivia"]),
        ("Group 6", ["Peter", "Queen", "Robert"])
    ]
    group_window.import_group_widgets(group_data)

    group_window.show()
    app.exec()

if __name__ == "__main__":
    main()