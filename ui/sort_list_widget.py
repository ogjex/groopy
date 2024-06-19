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
    def __init__(self, title: str, presenter: Presenter, id=0, parent=None):
        super().__init__(title, id, parent)
        self.presenter = presenter
        self.drag_widget_dict = {}  # Store drag widgets with var_name as key
        self.init_ui()
        self.on_order_changed.connect(self.slot_sort_order_changed)

    def init_ui(self):
        self.dragwidget_layout = QVBoxLayout(self)
        
        # Create a title label
        self.title_label = QLabel(self.title)
        self.title_label.setMaximumHeight(50)
        self.dragwidget_layout.addWidget(self.title_label)
        
        # Create a QListWidget for sorting
        self.list_widget = QListWidget()
        self.dragwidget_layout.addWidget(self.list_widget)
        
        self.set_orientation(Qt.Orientation.Vertical)
        self.set_drag_target_indicator()
                
        self.setLayout(self.dragwidget_layout)

    def populate_drag_widgets(self, drag_widget_dict: Dict[str, str]):
        for label, var_name in drag_widget_dict.items():
            self.add_sort_list_widget(label, var_name)

    def add_sort_list_widget(self, label: str, var_name: str):
        item = QListWidgetItem(self.list_widget)
        drag_sort_widget = DragSortWidget(label, var_name)
        item.setSizeHint(drag_sort_widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, drag_sort_widget)
        self.drag_widget_dict[var_name] = drag_sort_widget

    def remove_sort_list_widget(self, var_name: str):
        widget = self.drag_widget_dict.pop(var_name, None)
        if widget:
            for index in range(self.list_widget.count()):
                item = self.list_widget.item(index)
                if self.list_widget.itemWidget(item) == widget:
                    self.list_widget.takeItem(index)
                    break

    def clear_checkboxes(self):
        self.drag_widget_dict.clear()
        self.list_widget.clear()

    def emit_order_changed(self, src_widget: QWidget, target_widget_id: int):
        """
        Override the emit_order_changed method to customize the signal data.
        """
        item_index = self.list_widget.indexFromItem(src_widget)
        self.on_order_changed.emit((src_widget, item_index.row(), target_widget_id))

    def get_sort_list_data(self):
        data = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            widget = self.list_widget.itemWidget(item)
            if widget:
                data.append(widget.get_data())
        return data

    @pyqtSlot(tuple)
    def slot_sort_order_changed(self, data: Tuple[int, int, int]):
        self.presenter.handle_sort_order_changed(data)

# Test the SortListWidget
if __name__ == "__main__":
    app = QApplication([])

    class TestPresenter:
        def handle_print_list_widget_data(self, list: list):
            print(list)
        def handle_sort_order_changed(self, data: Tuple[int, int, int]):
            print(f"Order changed: {data}")

    presenter = TestPresenter()
    widget = SortListWidget("Test Title", presenter)
    
    widget.populate_drag_widgets({
        "Item 1": "var1",
        "Item 2": "var2",
        "Item 3": "var3"
    })

    widget.show()
    sys.exit(app.exec())