from PyQt6.QtCore import Qt, pyqtSlot
from ui.drag_widget_container import DragWidgetContainer
from ui.drag_widget import DragCheckBox
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from typing import Protocol, Tuple, Dict

class Presenter(Protocol):
    def handle_print_list_widget_data(self, list: list):
        ...
    def handle_sort_order_changed(self, tuple):
        ...
class SortListWidget(DragWidgetContainer):

    def __init__(self, title: str, presenter: Presenter, id=0, parent=None):
        super().__init__(title, id, parent)
        self.presenter = presenter
        self.drag_widget_dict = Dict
        self.init_ui()
        self.on_order_changed.connect(self.slot_sort_order_changed)
        
    def init_ui():
        ...

    def populate_drag_widgets(self, drag_widget_dict):
        for label, var_name, in drag_widget_dict:
           self.add_checkbox(label, var_name) 

    def add_checkbox(self, label: str, var_name: str):
        if label in self.checkbox_dict:
            return
        checkbox = DragCheckBox(label)
        list_item = QListWidgetItem(self.checkbox_list)
        self.checkbox_list.setItemWidget(list_item, checkbox)
        self.checkbox_dict[var_name] = checkbox
        self.adjust_max_height()

    '''def remove_checkbox(self, var_name: str):
        if var_name not in self.checkbox_dict:
            return
        checkbox = self.checkbox_dict.pop(var_name)
        for i in range(self.checkbox_list.count()):
            item = self.checkbox_list.item(i)
            widget = self.checkbox_list.itemWidget(item)
            if widget == checkbox:
                self.checkbox_list.takeItem(i)
                break
        self.adjust_max_height()

    def clear_checkboxes(self):
        self.checkbox_dict.clear()
        self.checkbox_list.clear()
        self.adjust_max_height()

    def set_checkboxes(self, checkboxes: list):
        self.clear_checkboxes()
        for label, var_name in checkboxes:
            self.add_checkbox(label, var_name)

    def set_checkboxes_test(self):
        checkboxes = [("Gender", "gender"), ("Education", "education"), ("Career Preference", "career_preference")]
        self.set_checkboxes(checkboxes)'''

    '''def calculate_height(self):
        # Calculate the new height based on the number of participants
        new_height = self.title_label.height() + self.dragwidget_frame.contentsMargins().top() + self.dragwidget_frame.contentsMargins().bottom()
        for i in range(self.dragwidget_layout.count()):
            widget = self.dragwidget_layout.itemAt(i).widget()
            if widget and widget != self._drag_target_indicator:
                new_height += widget.sizeHint().height() + self.dragwidget_layout.spacing()
        
        # Ensure the height is at least double the sum of title label height and drag target indicator height
        min_height = self.title_label.height() + self._drag_target_indicator.sizeHint().height() * 4
        new_height = max(new_height, min_height)
        
        return new_height'''

    def emit_order_changed(self, src_widget: DragCheckBox, target_widget_id: int):
        """
        Override the emit_order_changed method to customize the signal data.
        """
        self.on_order_changed.emit((participant_id, target_widget_id))

    '''def get_group_data(self) -> list:
        """
        Get the data of this group widget.
        """
        return [self.id, self.title, self.get_item_data()]

    def get_item_data(self) -> list:
        data = []
        for n in range(self.dragwidget_layout.count()):
            # Get the widget at each index in turn.
            w = self.dragwidget_layout.itemAt(n).widget()
            if w != self._drag_target_indicator:
                # The target indicator has no data.
                data.append((w.person_id, w.person_name))
        return data'''

    @pyqtSlot(tuple)
    def slot_sort_order_changed(self, data: Tuple[int, int, int]):
        self.presenter.handle_sort_order_changed(data)