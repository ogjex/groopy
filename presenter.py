from __future__ import annotations
from typing import Protocol
from group_editor import GroupEditor
from PyQt6.QtWidgets import *

class GroupWindow(Protocol):
    def initUI(self, presenter: Presenter) -> None:
        ...
    def show(self) -> None:
        ...

class Presenter(object):
    def __init__(self, group_editor: GroupEditor, main_window: GroupWindow):
        self.main_window = main_window
        self.group_editor = group_editor

    def handle_save_colors(self):
        pass
        #button_colors = self.main_gui.getColors()
        #self.button_editor.saveColors(button_colors)
        
    def handle_open_csv_file(self, filename):
        pass
        #self.button_editor.read_csv_file(filename)
        #self.main_gui.loadButtonColors(self.button_editor.get_button_colors())

    def handle_save_csv_file(self, filename, button_colors):
        pass
        #self.button_editor.save_csv_file(filename, button_colors)

    def run(self) -> None:
        self.main_window.initUI(self)
        self.main_window.show()