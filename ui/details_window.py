from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)
from typing import Protocol, List

class Presenter(Protocol):
    def handle_open_persons_file(self, filename) -> None:
        ...
    def handle_view_group(self) -> None:
        ...
    
class DetailsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Structure Details")
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Create a horizontal layout for headers
        self.headers_layout = QHBoxLayout()

        # Create labels for CSV structure fields
        self.field_names = ['Name', 'Gender', 'Education', 'Experience', 'Career Preference', 'Desirables', 'Undesirables']
        self.field_labels = []

        # Set background color and font color for header labels
        header_background_color = QColor(50, 50, 50)  # Darkest grey
        header_font_color = QColor(200, 200, 200)     # Light grey

        for field_name in self.field_names:
            label = QLabel(field_name)
            label.setAutoFillBackground(True)
            palette = label.palette()
            palette.setColor(label.backgroundRole(), header_background_color)
            label.setPalette(palette)
            label.setStyleSheet("color: rgb({}, {}, {});".format(header_font_color.red(), header_font_color.green(), header_font_color.blue()))
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))  # Adjust font weight if necessary
            self.field_labels.append(label)
            self.headers_layout.addWidget(label)

        # Add the headers layout to the main layout
        self.main_layout.addLayout(self.headers_layout)

    def set_field_values(self, persons_data: List[dict]):
        # Create a vertical layout for values
        values_layout = QVBoxLayout()

        # Iterate over each person's data
        for index, person_data in enumerate(persons_data):
            # Create a horizontal layout for each person's data
            person_layout = QHBoxLayout()

            # Set background color for alternating rows
            if index % 2 == 0:
                row_color = QColor(240, 240, 240)  # Light grey
            else:
                row_color = QColor(255, 255, 255)  # White

            # Iterate over each field name
            for field_name in self.field_names:
                # Get the value for the field name from person_data
                value = person_data.get(field_name.lower(), "")
                # Create a label for the value
                label = QLabel(str(value))
                # Set background color for the label
                label.setAutoFillBackground(True)
                palette = label.palette()
                palette.setColor(label.backgroundRole(), row_color)
                label.setPalette(palette)
                # Add the label to the person layout
                person_layout.addWidget(label)

            # Add the person layout to the vertical layout for values
            values_layout.addLayout(person_layout)

        # Add the vertical layout for values to the main layout
        self.main_layout.addLayout(values_layout)
    
    def keyPressEvent(self, event):
        key_actions = {
            Qt.Key.Key_Escape: self.close,
            # Add more key-function mappings as needed
        }

        if event.key() in key_actions:
            action = key_actions[event.key()]
            if callable(action):
                action()
