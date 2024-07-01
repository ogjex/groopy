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
        
    def handle_open_group_file(self, file_path):
        self.main_window.clear_group_widgets()
        groups_data = self.group_editor.read_groups_from_json(file_path)
        self.handle_import_group_widgets()

    def handle_save_workspace(self, file_path):
        raise NotImplementedError("This function is not yet implemented.")

    def handle_save_group_file(self, file_path):
        self.group_editor.save_groups_to_json(file_path, self.person_editor.person_csv_filename)

    def handle_import_group_widgets(self):
        groups_data = self.group_editor.prep_groups_for_view()
        self.main_window.import_group_widgets(groups_data)

    def handle_clear_group_layout(self):
        self.main_window.clear_group_widgets()

    def handle_set_field_values(self, data):
        self.main_window.update_details_window(data)

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

    def handle_sort_groups(self, strategies: dict[str, str]) -> None:
        print("Gathered strategies:", strategies)
        self.group_sorter.set_people_to_sort(self.person_editor.persons)
        self.group_sorter.distribute_people_to_groups(strategies)
        self.handle_clear_group_layout()
        self.handle_import_group_widgets
        # Debugging: Print the gathered strategies

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

