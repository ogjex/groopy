from PyQt6.QtWidgets import (
    QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy, QScrollArea, QSizeGrip
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

class DetailsWindow(QWidget):
    def __init__(self, presenter=None):
        super().__init__()
        self.presenter = presenter
        self.setGeometry(100, 100, 600, 400)

        # Create a scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Create a widget to contain the main layout
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create a horizontal layout for headers
        self.headers_layout = QHBoxLayout()
        self.headers_layout.setContentsMargins(0, 0, 0, 0)
        self.headers_layout.setSpacing(0)

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
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
            label.setMaximumHeight(50)
            self.field_labels.append(label)
            self.headers_layout.addWidget(label)

        # Add the headers layout to the main layout
        self.main_layout.addLayout(self.headers_layout)

        # Add a QSizeGrip to the bottom-right corner
        self.size_grip = QSizeGrip(self)
        grip_layout = QHBoxLayout()
        grip_layout.addStretch()
        grip_layout.addWidget(self.size_grip)
        self.main_layout.addLayout(grip_layout)

    def set_field_values(self, persons_data):
        # Clear previous data
        for i in reversed(range(self.main_layout.count())):
            layout_item = self.main_layout.itemAt(i)
            if layout_item.widget() and layout_item.widget() is not self.size_grip:
                layout_item.widget().deleteLater()

        # Create a vertical layout for values
        values_layout = QVBoxLayout()
        values_layout.setContentsMargins(0, 0, 0, 0)
        values_layout.setSpacing(0)

        # Iterate over each person's data
        for index, person_data in enumerate(persons_data):
            # Create a horizontal layout for each person's data
            person_layout = QHBoxLayout()
            person_layout.setContentsMargins(0, 0, 0, 0)
            person_layout.setSpacing(0)

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
                label.setContentsMargins(0, 0, 0, 0)
                label.setAutoFillBackground(True)
                palette = label.palette()
                palette.setColor(label.backgroundRole(), row_color)
                label.setPalette(palette)
                label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
                person_layout.addWidget(label)

            # Add the person layout to the vertical layout for values
            values_layout.addLayout(person_layout)

        # Add the vertical layout for values to the main layout, above the size grip
        self.main_layout.insertLayout(self.main_layout.count() - 1, values_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scroll_area.setGeometry(0, 0, self.width(), self.height() - self.size_grip.height())
        self.size_grip.move(self.width() - self.size_grip.width(), self.height() - self.size_grip.height())
