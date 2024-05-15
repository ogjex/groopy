from __future__ import annotations
from typing import Protocol
from group_editor import GroupEditor

class MainWindow(Protocol):
    def initUI(self, presenter: Presenter) -> None:
        ...
    def show(self) -> None:
        ...
    def import_group_widgets(self, groups) -> None:
        ...

class Presenter(object):
    def __init__(self, group_editor: GroupEditor, main_window: MainWindow):
        self.main_window = main_window
        self.group_editor = group_editor
        
    def handle_open_group_file(self, filename):
        new_groups = self.group_editor.read_groups_from_json(filename)
        self.main_window.import_group_widgets(new_groups)

    def handle_save_group_file(self, filename, groups_data):
        #save_groups = self.main_window.get_groups_data()
        self.group_editor.create_groups_from_data(groups_data)
        self.group_editor.save_groups_to_json(filename)

    def run(self) -> None:
        self.main_window.initUI(self)
        self.main_window.show()