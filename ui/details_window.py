from PyQt6.QtWidgets import (
    QLabel,
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
        self.setGeometry(100, 100, 400, 300)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Create labels for CSV structure fields
        self.field_names = ['Name', 'Gender', 'Education', 'Experience', 'Career Preference', 'Desirables', 'Undesirables']
        self.field_labels = []

        for field_name in self.field_names:
            label = QLabel(field_name)
            self.field_labels.append(label)
            self.main_layout.addWidget(label)

    def set_field_values(self, persons_data: List[dict]):
        for field_index, field_name in enumerate(self.field_names):
            values = [str(person_data.get(field_name.lower(), "")) for person_data in persons_data]
            label_text = f"{field_name}:\n" + "\n".join(values)
            self.field_labels[field_index].setText(label_text)