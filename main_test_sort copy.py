import sys
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication

from ui.sort_list_widget import SortListWidget
from typing import Protocol, Tuple, Dict

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