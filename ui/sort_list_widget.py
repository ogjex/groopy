from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QDropEvent
from ui.drag_widget_container import DragWidgetContainer
from ui.drag_widget import DragSortWidget
from typing import Protocol, Dict

class Presenter(Protocol):
    def handle_checked_list_widget_data(self, list: list):
        ...
    def handle_sort_order_changed(self, list: list):
        ...

class SortListWidget(DragWidgetContainer):

    def __init__(self, title: str, presenter: Presenter, drag_widget_dict: Dict[str, str], id=0, parent=None):
        super().__init__(title, id, parent)
        self.presenter = presenter
        self.drag_widget_dict = drag_widget_dict
        self.init_ui()
        self.populate_drag_widgets()
        #self.on_order_changed.connect(self.sort_order_changed)
        # need to add buttons here and connect
        # need to add a way to read in previous sort order values from workspace preferences

    def init_ui(self):
        super().init_ui()        
        #self.dragwidget_layout.setSpacing(1)

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

    def dropEvent(self, e: QDropEvent):
        self.handle_common_drop_event(e)

    def emit_order_changed(self, src_widget: QWidget, target_widget_id: int):
        """
        Override the emit_order_changed method to customize the signal data.
        """
        list_data = self.get_checked_sort_list_data()
        print(f"{list_data}")
        #self.presenter.handle_checked_list_widget_data(list_data)
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
            widget = self.get_drag_sort_widget_at_index(index)
            if widget:
                data.append(widget.get_data())
        return data

    def get_checked_sort_list_data(self) -> list:
        checked_data = []
        for index in range(self.dragwidget_layout.count()):
            widget = self.get_drag_sort_widget_at_index(index)
            if widget and widget.is_checked():
                checked_data.append(widget.get_data())
        return checked_data

    def get_drag_sort_widget_at_index(self, index) -> list:
        widget_item = self.dragwidget_layout.itemAt(index)
        if widget_item:
            widget = widget_item.widget()
            if isinstance(widget, DragSortWidget):
                return widget
        return None