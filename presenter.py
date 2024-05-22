from __future__ import annotations
from typing import Protocol
from group_editor import GroupEditor
from person_editor import PersonEditor

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
    def __init__(self, group_editor: GroupEditor, person_editor: PersonEditor, main_window: MainWindow):
        self.main_window = main_window
        self.group_editor = group_editor
        self.person_editor = person_editor
        
    def handle_open_group_file(self, file_path):
        self.main_window.clear_group_widgets()
        new_groups = self.group_editor.read_groups_from_json(file_path)
        self.main_window.import_group_widgets(new_groups)

    def handle_save_workspace(self, file_path):
        groups_data = self.main_window.get_groups_data()
        self.group_editor.create_groups_from_data(groups_data)
        self.group_editor.save_groups_to_json(file_path)

    def handle_save_group_file(self, file_path):
        groups_data = self.main_window.get_groups_data()
        self.group_editor.create_groups_from_data(groups_data)
        self.group_editor.save_groups_to_json(file_path)

    def handle_set_field_values(self, data):
        self.main_window.update_details_window(data)

    def run(self) -> None:
        self.main_window.initUI(self)
        self.main_window.show()