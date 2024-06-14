from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QFrame
from ui.drag_widget_container import DragWidgetContainer
from ui.drag_widget import DragLabel

from typing import Protocol, List, Tuple

class Presenter(Protocol):
    def handle_print_group_widget_data(self, list: list):
        ...
    def handle_participant_order_changed(self, tuple):
        ...
class GroupWidget(DragWidgetContainer):

    def __init__(self, group_id: int, title:str, participants: List[Tuple[int, str]], presenter: Presenter, parent=None):
        super().__init__(title, group_id, parent)
        self.participants = participants
        self.presenter = presenter
        self.expanded = True
        self.init_ui()
        self.on_order_changed.connect(self.slot_participant_order_changed)
        
    def populate_drag_widgets(self):
        for person_id, person_name in self.participants:
           self.add_participant(person_id, person_name) 

    def add_participant(self, person_id: int, person_name: str):
        label = DragLabel(person_id, person_name)
        label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        label.setMargin(2)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(100, 20)
        label.setScaledContents(True)
        label.setContentsMargins(5, 0, 5, 0)
        label.setAutoFillBackground(True)
        label.data = (person_id, person_name)
        self.dragwidget_layout.addWidget(label)

    def calculate_height(self):
        # Calculate the new height based on the number of participants
        new_height = self.title_label.height() + self.dragwidget_frame.contentsMargins().top() + self.dragwidget_frame.contentsMargins().bottom()
        for i in range(self.dragwidget_layout.count()):
            widget = self.dragwidget_layout.itemAt(i).widget()
            if widget and widget != self._drag_target_indicator:
                new_height += widget.sizeHint().height() + self.dragwidget_layout.spacing()
        
        # Ensure the height is at least double the sum of title label height and drag target indicator height
        min_height = self.title_label.height() + self._drag_target_indicator.sizeHint().height() * 4
        new_height = max(new_height, min_height)
        
        return new_height

    def emit_order_changed(self, src_widget: DragLabel, target_widget_id: int):
        """
        Override the emit_order_changed method to customize the signal data.
        """
        participant_id = src_widget.get_person_id()
        self.on_order_changed.emit((participant_id, target_widget_id))
    
    def add_item(self, item):
        self.dragwidget_layout.addWidget(item)
        self.update_height()

    def get_group_data(self) -> list:
        """
        Get the data of this group widget.
        """
        return [self.id, self.title, self.get_item_data()]

    def get_item_data(self) -> list:
        data = []
        for n in range(self.dragwidget_layout.count()):
            # Get the widget at each index in turn.
            w = self.dragwidget_layout.itemAt(n).widget()
            if w != self._drag_target_indicator:
                # The target indicator has no data.
                data.append((w.person_id, w.person_name))
        return data

    @pyqtSlot(tuple)
    def slot_participant_order_changed(self, data: Tuple[int, int, int]):
        self.presenter.handle_participant_order_changed(data)