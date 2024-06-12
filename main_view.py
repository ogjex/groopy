import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from group_editor import GroupEditor
from person_editor import PersonEditor
from group_sorter import GroupSorter
from workspace_preference_handler import WorkspacePreferenceHandler
from presenter import Presenter

def main():
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    
    
    # Instantiate PersonEditor
    person_editor = PersonEditor()
    group_editor = GroupEditor(person_editor)
    group_sorter = GroupSorter()
    ws_handler = WorkspacePreferenceHandler()    

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

    presenter = Presenter(group_sorter, group_editor, person_editor, main_window, ws_handler)
    
    # Prepare sample data as dictionaries for details window
    #sample_persons = person_editor.create_persons_sample()
    #sample_persons_data = person_editor.get_persons_data_as_dict(sample_persons)
    
    persons = person_editor.read_persons_from_csv("persons.csv")
    persons_as_dict = person_editor.get_persons_data_as_dict(persons)
    person_editor.save_csv()

    presenter.run()
    presenter.handle_set_field_values(persons_as_dict)

    # can the groups_data also be used for grouping_module?
    group_editor.create_group_data_sample()
    presenter.handle_import_group_widgets()
    #groups_data = group_editor.groups
    #main_window.import_group_widgets(groups_data)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()