import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from group_editor import GroupEditor
from person_editor import PersonEditor
from presenter import Presenter

def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    
    group_editor = GroupEditor()
    # Instantiate PersonEditor
    person_editor = PersonEditor()

    # Center the window on the screen
    window_width = main_window.frameGeometry().width()
    window_height = main_window.frameGeometry().height()
    screen = app.primaryScreen()
    screen_width = screen.size().width()
    screen_height = screen.size().height()
    main_window.move((screen_width - window_width) // 2, (screen_height - window_height) // 2)
    
    presenter = Presenter(group_editor, person_editor, main_window)
    
    # Prepare sample data as dictionaries
    sample_persons = person_editor.create_persons_sample()
    sample_persons_data = person_editor.get_persons_data_as_dict(sample_persons)
    
    presenter.run()
    presenter.handle_set_field_values(sample_persons_data)

    groups_data = [
        ("Group 1", ["Alice", "Bob", "Charlie"]),
        ("Group 2", ["David", "Eve", "Frank"]),
        ("Group 3", ["Grace", "Henry", "Ivy"]),
        ("Group 4", ["Jack", "Kate", "Liam"]),
        ("Group 5", ["Mary", "Nathan", "Olivia"]),
        ("Group 6", ["Peter", "Queen", "Robert"]),
        ("Group 7", ["Henry", "Norton", "Moose"]),
        ("Group 8", ["Stan", "Chao", "Missy"])
    ]
    
    main_window.import_group_widgets(groups_data)
    

    sys.exit(app.exec())

if __name__ == "__main__":
    main()