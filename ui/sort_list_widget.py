import sys
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QApplication, QListWidgetItem, QListWidget, QVBoxLayout, QLabel, QWidget
from ui.drag_widget_container import DragWidgetContainer
from ui.drag_widget import DragSortWidget
from typing import Protocol, Tuple, Dict

class Presenter(Protocol):
    def handle_print_list_widget_data(self, list: list):
        ...
    def handle_sort_order_changed(self, tuple):
        ...

class SortListWidget(DragWidgetContainer):
    def __init__(self, title: str, presenter: Presenter, drag_widget_dict: Dict[str, str], id=0, parent=None):
        super().__init__(title, id, parent)
        self.presenter = presenter
        self.drag_widget_dict = drag_widget_dict
        self.init_ui()
        self.populate_drag_widgets()
        self.on_order_changed.connect(self.slot_sort_order_changed)

    def populate_drag_widgets(self):
        for label, var_name in list(self.drag_widget_dict.items()):
            self.add_sort_list_widget(label, var_name)

    def add_sort_list_widget(self, label: str, var_name: str):
        drag_sort_widget = DragSortWidget(label, var_name)
        self.drag_widget_dict[var_name] = drag_sort_widget
        self.dragwidget_layout.addWidget(drag_sort_widget)
        self.update_height()

    def remove_sort_list_widget(self, var_name: str):
        widget = self.drag_widget_dict.pop(var_name, None)
        if widget:
            self.layout.removeWidget(widget)
            widget.deleteLater()
            self.update_height()

    def clear_checkboxes(self):
        for widget in self.drag_widget_dict.values():
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.drag_widget_dict.clear()
        self.update_height()

    def emit_order_changed(self, src_widget: QWidget, target_widget_id: int):
        pass
        """
        Override the emit_order_changed method to customize the signal data.
        """
        '''# Find the corresponding QListWidgetItem for the src_widget
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if self.list_widget.itemWidget(item) == src_widget:
                self.on_order_changed.emit((src_widget, index, target_widget_id))
                break'''

    def calculate_height(self):
        # Calculate the new height based on the number of widgets
        new_height = self.title_label.height() + 50  # Initial height including title label and padding
        for index in range(self.dragwidget_layout.count()):
            widget = self.dragwidget_layout.itemAt(index).widget()
            if widget:
                new_height += widget.sizeHint().height() + self.dragwidget_layout.spacing()
        
        return new_height    
    
    def get_sort_list_data(self):
        data = []
        for index in range(self.dragwidget_layout.count()):
            widget = self.dragwidget_layout.itemAt(index).widget()
            if widget:
                data.append(widget.get_data())
        return data

    @pyqtSlot(tuple)
    def slot_sort_order_changed(self, data: Tuple[int, int, int]):
        self.presenter.handle_sort_order_changed(data)