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

    # Get the screen dimensions
    screen = app.primaryScreen()
    screen_geometry = screen.geometry()
    screen_width = screen_geometry.width()
    
    # Calculate the X coordinate for centering the window horizontally
    x_coordinate = (screen_width - main_window.window_width) // 2
    
    # Y coordinate is 0 to place the window at the top of the screen
    y_coordinate = 0
    
    # Move the window to the desired position
    main_window.move(x_coordinate, y_coordinate)    

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
        ("Group 8", ["Stan", "Chao", "Missy"]),
        ("Group 9", ["Helle", "Finn", "Dave"]),
        ("Group 10", ["John", "Jane", "Hunny"])
    ]
    
    main_window.import_group_widgets(groups_data)
    

    sys.exit(app.exec())

if __name__ == "__main__":
    main()