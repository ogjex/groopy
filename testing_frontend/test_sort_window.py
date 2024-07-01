import sys
import pytest
from PyQt6.QtWidgets import QApplication
from unittest.mock import Mock
# setting path
sys.path.append('../groopy')
from ui.sort_list_widget import SortListWidget
from ui.sort_window import SortWindow, Presenter  # Replace with the actual module name
class MockPresenter:
    def handle_min_group_size_changed(self, new_value: int) -> None:
        pass
    def handle_max_group_size_changed(self, new_value: int) -> None:
        pass
    def handle_max_total_groups_changed(self, new_value: int) -> None:        
        pass
    def load_initial_min_group_size_value(self) -> int:
        return 1
    def load_initial_max_group_size_value(self) -> int:
        return 40
    def load_initial_max_total_groups_value(self) -> int:
        return 40
    def handle_sort_groups(self, strategies: dict) -> None:
        pass

@pytest.fixture
def app(qtbot):
    app = QApplication([])
    qtbot.addWidget(app)
    return app

def test_gather_strategies(qtbot):
    presenter = MockPresenter()  # Mock presenter
    sort_window = SortWindow(presenter)
    qtbot.addWidget(sort_window)

    # Sample data for SortListWidget
    sample_data = {
        "Gender": (True, "Spread"),
        "Education": (True, "Focus"),
        "Experience": (False, "Spread"),
        "Location": (True, "Focus")
    }
    sort_window.sl_widget.update_sort_list_widgets(sample_data)

    # Check some checkboxes
    for i in range(sort_window.sl_widget.dragwidget_layout.count()):
        widget = sort_window.sl_widget.get_drag_sort_widget_at_index(i)
        if widget and widget.label.text() in ["Gender", "Education", "Location"]:
            widget.checkbox.setChecked(True)

    # Change radio buttons
    for i in range(sort_window.sl_widget.dragwidget_layout.count()):
        widget = sort_window.sl_widget.get_drag_sort_widget_at_index(i)
        if widget and widget.label.text() == "Gender":
            widget.radio1.setChecked(True)
        elif widget and widget.label.text() == "Education":
            widget.radio2.setChecked(True)

    # Gather strategies and check the output
    expected_strategies = {
        "Gender": "Spread",
        "Education": "Focus",
        "Location": "Focus"
    }
    
    # Debugging: Print the strategies before the assertion
    actual_strategies = sort_window.gather_strategies()
    print("Expected strategies:", expected_strategies)
    print("Actual strategies:", actual_strategies)

    assert actual_strategies == expected_strategies
