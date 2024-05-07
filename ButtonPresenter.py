from __future__ import annotations
from typing import Protocol
from buttonEditor import ButtonEditor
from PyQt6.QtWidgets import *

class ColorButtonWidget(Protocol):
    def initUI(self, presenter: Presenter) -> None:
        ...
    def show(self) -> None:
        ...

class Presenter(object):
    def __init__(self, button_editor: ButtonEditor, button_widget: ColorButtonWidget):
        self.main_gui = button_widget
        self.button_editor = button_editor

    def handle_save_colors(self):
        button_colors = self.main_gui.getColors()
        self.button_editor.saveColors(button_colors)
        
    def handle_open_csv_file(self, filename):
        self.button_editor.read_csv_file(filename)
        self.main_gui.setButtonColors(self.button_editor.get_button_colors())

    def handle_save_csv_file(self, filename, button_colors):
        self.button_editor.save_csv_file(filename, button_colors)

    def run(self) -> None:
        self.main_gui.initUI(self)
        self.main_gui.show()

