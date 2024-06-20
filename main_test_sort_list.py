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
    # Populate the drag widgets with a dictionary
    drag_widget_dict = {
        "Item 1": (True, "Spread"),
        "Item 2": (False, "Focus"),
        "Item 3": (True, "Spread")
    }
    widget = SortListWidget("Test Title", presenter, drag_widget_dict)

    widget.show()
    widget.toggle_checkbox_values()  # Toggle checkbox values
    sys.exit(app.exec())

