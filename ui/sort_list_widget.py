from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QCheckBox, 
    QLabel
)
from PyQt6.QtGui import QDropEvent
from ui.drag_widget_container import DragWidgetContainer
from ui.drag_widget import DragSortWidget
from typing import Protocol, Dict, Tuple

class Presenter(Protocol):
    def handle_checked_list_widget_data(self, list: list):
        ...
    def handle_sort_order_changed(self, list: list):
        ...

class SortListWidget(DragWidgetContainer):
    def __init__(self, title: str, presenter: Presenter, drag_widget_dict: Dict[str, Tuple[bool, str]], id=0, parent=None):
        super().__init__(title, id, parent)
        self.presenter = presenter
        self.drag_widget_dict = drag_widget_dict
        self.init_ui()
        self.populate_drag_widgets()

    def init_ui(self):
        super().init_ui()

        # Header frame
        self.header_frame = QFrame()
        self.header_layout = QHBoxLayout(self.header_frame)
        
        self.cb_checkall = QCheckBox("Select All")
        self.cb_checkall.stateChanged.connect(self.toggle_all_checkboxes)
        self.header_layout.addWidget(self.cb_checkall)

        self.header_layout.addWidget(self.cb_checkall)
        self.header_layout.addStretch(1)  # To center "Spread" and "Focus"
    
        # Call parent layout to add widgets in the right order
        self.layout.addWidget(self.header_frame)
        self.layout.addWidget(self.dragwidget_frame)
        self.setLayout(self.layout)
        self.dragwidget_frame.show()

    def populate_drag_widgets(self):
        for label, (checkbox_state, radio_option) in self.drag_widget_dict.items():
            self.add_sort_list_widget(label, checkbox_state, radio_option)

    def add_sort_list_widget(self, label: str, checkbox_state: bool, radio_option: str):
        frame = QFrame()
        frame_layout = QHBoxLayout(frame)
        
        drag_sort_widget = DragSortWidget(label, label, checkbox_state, radio_option)
        frame_layout.addWidget(drag_sort_widget)
        
        self.drag_widget_dict[label] = drag_sort_widget
        self.dragwidget_layout.addWidget(frame)
        self.update_height()

    def clear_sort_list_widgets(self):
        while self.dragwidget_layout.count() > 0:
            item = self.dragwidget_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.drag_widget_dict.clear()
        self.update_height()

    def update_sort_list_widgets(self, new_preferences: Dict[str, Tuple[bool, str]]):
        self.clear_sort_list_widgets()
        self.drag_widget_dict = new_preferences
        self.populate_drag_widgets()
    
    def toggle_all_checkboxes(self):
        if self.cb_checkall.isChecked():
            self.change_checkboxes(True)
        else:
            self.change_checkboxes(False)

    def change_checkboxes(self, value: bool):
        for index in range(self.dragwidget_layout.count()):
            item = self.dragwidget_layout.itemAt(index)
            if self.is_valid_drag_sort_widget_frame(item):
                frame_widget = item.widget()
                self.change_checkboxes_in_frame(frame_widget, value)

    def is_valid_drag_sort_widget_frame(self, item):
        return item and isinstance(item.widget(), QFrame)

    def change_checkboxes_in_frame(self, frame_widget, value):
        frame_layout = frame_widget.layout()
        if not frame_layout:
            return

        for i in range(frame_layout.count()):
            widget = frame_layout.itemAt(i).widget()
            if isinstance(widget, DragSortWidget):
                self.set_checkbox_value(widget, value)

    def set_checkbox_value(self, widget, value):
        widget.checkbox.setChecked(value)                            
    
    def dropEvent(self, e: QDropEvent):
        self.handle_common_drop_event(e)

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