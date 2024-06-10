from __future__ import annotations
from typing import Protocol
from group_editor import GroupEditor
from person_editor import PersonEditor
from group_sorter import GroupSorter

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
    def clear_group_widgets() -> None:
        ...
class Presenter(object):
    def __init__(self, group_sorter: GroupSorter, group_editor: GroupEditor, person_editor: PersonEditor, main_window: MainWindow):
        self.group_sorter = group_sorter
        self.group_editor = group_editor
        self.person_editor = person_editor
        self.main_window = main_window
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
        #print(f"Received data: {data}")
        #self.main_window.print_group_widgets()

    def run(self) -> None:
        self.main_window.initUI(self)
        self.main_window.show()