import sys
import pytest
from PyQt6.QtWidgets import QApplication
from unittest.mock import Mock
# setting path
sys.path.append('../groopy')
from ui.sort_list_widget import SortListWidget
from ui.sort_window import SortWindow, Presenter  # Replace with the actual module name

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def mock_presenter():
    presenter = Mock(spec=Presenter)
    presenter.load_initial_min_group_size_value.return_value = 1
    presenter.load_initial_max_group_size_value.return_value = 10
    presenter.load_initial_max_total_groups_value.return_value = 5
    return presenter

@pytest.fixture
def sort_window(mock_presenter):
    return SortWindow(presenter=mock_presenter)

def test_gather_strategies(app, sort_window):
    # Configure SortListWidget with sample data
    sort_window.sl_widget.clear_sort_list_widgets()
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
        if widget and widget.label in ["Gender", "Education", "Location"]:
            widget.checkbox.setChecked(True)

    # Change radio buttons
    for i in range(sort_window.sl_widget.dragwidget_layout.count()):
        widget = sort_window.sl_widget.get_drag_sort_widget_at_index(i)
        if widget and widget.label == "Gender":
            widget.radio_spread.setChecked(True)
        elif widget and widget.label == "Education":
            widget.radio_focus.setChecked(True)

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
