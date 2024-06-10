import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from group_editor import GroupEditor
from person_editor import PersonEditor
from grouping_module import GroupingModule
from presenter import Presenter

def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    
    group_editor = GroupEditor()
    # Instantiate PersonEditor
    person_editor = PersonEditor()
    
    grouping_module = GroupingModule()
    grouping_module.set_group(sample_persons)
    #grouping_module.set_people_to_sort(sample_persons)

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

    presenter = Presenter(grouping_module, group_editor, person_editor, main_window)
    
    sample_persons = person_editor.create_persons_sample()
    sample_persons_data = person_editor.get_persons_data_as_dict(sample_persons)

    presenter.run()
    presenter.handle_set_field_values(sample_persons_data)

    groups_data = group_editor.create_group_data_sample()
    
    # Prepare sample data as dictionaries    
    
    main_window.import_group_widgets(groups_data)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()