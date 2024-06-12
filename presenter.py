from __future__ import annotations
from typing import Protocol
from group_editor import GroupEditor
from person_editor import PersonEditor
from group_sorter import GroupSorter
from workspace_preference_handler import WorkspacePreferenceHandler

class MainWindow(Protocol):
    def initUI(self, presenter: Presenter) -> None:
        ...
    def show(self) -> None:
        ...
    def import_group_widgets(self, groups) -> None:
        ...
    def get_groups_data(self) -> None:
        ...
    def update_details_window(self, data) -> None:
        ...
    def clear_group_widgets(self) -> None:
        ...
    def update_sort_window_values(self) -> None:
        ...        
class Presenter(object):
    def __init__(self, group_sorter: GroupSorter, group_editor: GroupEditor, person_editor: PersonEditor, main_window: MainWindow, handler: WorkspacePreferenceHandler):
        self.group_sorter = group_sorter
        self.group_editor = group_editor
        self.person_editor = person_editor
        self.main_window = main_window
        self.handler = handler
        self.group_sort_methods = {
            "Option 1": self.method1,
            "Option 2": self.method2,
            "Option 3": self.method3,
            "Option 4": self.method4,
            "Option 5": self.method5
        }
        
    def handle_open_group_file(self, file_path):
        self.main_window.clear_group_widgets()
        new_groups = self.group_editor.read_groups_from_json(file_path)
        self.main_window.import_group_widgets(new_groups)

    def handle_save_workspace(self, file_path):
        raise NotImplementedError("This function is not yet implemented.")
        #groups_data = self.main_window.get_groups_data()
        #self.group_editor.create_groups_from_data(groups_data)
        #self.group_editor.save_groups_to_json(file_path)

    def handle_save_group_file(self, file_path):
        groups_data = self.main_window.get_groups_data()
        self.group_editor.create_groups_from_data(groups_data)
        self.group_editor.save_groups_to_json(file_path)

    def handle_import_group_widgets(self):
        groups_data = self.group_editor.prep_groups_for_view()
        self.main_window.import_group_widgets(groups_data)

    def handle_clear_group_layout(self):
        self.main_window.clear_group_widgets()

    def handle_set_field_values(self, data):
        self.main_window.update_details_window(data)

    def handle_checkbox_order(self, checkbox_states):
        print("Processing checkbox order:")
        for label, state in checkbox_states:
            print(f"{label}: {'Checked' if state else 'Unchecked'}")
            if state:
                # Call the corresponding method if the checkbox is checked
                self.group_sort_methods[label]()

    def method1(self):
        print("Executing Method 1")

    def method2(self):
        print("Executing Method 2")

    def method3(self):
        print("Executing Method 3")

    def method4(self):
        print("Executing Method 4")

    def method5(self):
        print("Executing Method 5")

    def handle_print_group_widget_data(self, list):
        print(f"{list}")

    def handle_participant_order_changed(self, data:tuple):
        participant_id = data[0]
        target_group_id = data[1]
        self.group_editor.move_person_to_group(participant_id, target_group_id)
        self.group_editor.print_groups()

    def handle_min_group_size_changed(self, min_group_size: int) -> None:
        self.group_sorter.set_min_group_size(min_group_size)

    def handle_max_group_size_changed(self, max_group_size: int) -> None:
        self.group_sorter.set_max_group_size(max_group_size)

    def handle_max_total_groups_changed(self, max_total_groups: int) -> None:
        self.group_sorter.set_max_num_groups(max_total_groups)
    
    def load_initial_min_group_size_value(self) -> int:
        return self.handler.get_min_group_size()

    def load_initial_max_group_size_value(self) -> int:
        return self.handler.get_max_group_size()
    
    def load_initial_max_total_groups_value(self) -> int:
        return self.handler.get_max_num_groups()
    
    def update_sort_window_values(self):
        self.main_window.update_sort_window_values()

    def run(self) -> None:
        # Load preferences
        self.handler.load_preferences()

        # Initialize and show the main window
        self.main_window.initUI(self)
        self.main_window.show()

        # Set group sorter values based on loaded preferences
        self.group_sorter.set_min_group_size(self.handler.min_group_size)
        self.group_sorter.set_max_group_size(self.handler.max_group_size)
        self.group_sorter.set_max_groups_per_person(self.handler.max_groups_per_person)
        self.group_sorter.set_max_num_groups(self.handler.max_num_groups)

