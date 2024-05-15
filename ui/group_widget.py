from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QWidget,
)
from ui.drag_widget import DragLabel, DragTargetIndicator

class GroupWidget(QWidget):

    orderChanged = pyqtSignal(list)

    def __init__(self, title, participants, parent=None):
        super().__init__(parent)
        
        self.title = title
        self.participants = participants
        self.expanded = True
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Create a title label
        self.title_label = QLabel(self.title)
        layout.addWidget(self.title_label)
        
        # Create a frame for participants
        self.participants_frame = QFrame()
        self.participants_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.participants_frame.setFrameShadow(QFrame.Shadow.Sunken)  # Set the shadow of the frame
        self.participants_layout = QVBoxLayout(self.participants_frame)
        layout.addWidget(self.participants_frame)

        self.orientation=Qt.Orientation.Vertical
        self._drag_target_indicator = DragTargetIndicator()
        self.participants_layout.addWidget(self._drag_target_indicator)
        self._drag_target_indicator.hide()
        
        self.setLayout(layout)
        
        # Hide participants initially
        self.participants_frame.show()
        
        # Populate participants
        self.populateParticipants()
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
    def populateParticipants(self):
        for participant in self.participants:
           self.addParticipant(participant) 

    def addParticipant(self, participant):
        label = DragLabel(participant)
        label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        label.setMargin(2)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(100, 20)
        label.setScaledContents(True)
        label.setContentsMargins(5, 0, 5, 0)
        label.setAutoFillBackground(True)
        self.participants_layout.addWidget(label)

    def dragEnterEvent(self, e):
        e.accept()
    
    def dragMoveEvent(self, e):
        # Find the correct location of the drop target, so we can move it there.
        index = self._find_drop_location(e)
        if index is not None:
            # Inserting moves the item if its alreaady in the layout.
            self.participants_layout.insertWidget(index, self._drag_target_indicator)
            # Hide the item being dragged.
            e.source().hide()
            # Show the target.
            self._drag_target_indicator.show()
        e.accept()

    def dropEvent(self, e):
        widget = e.source()
        self._drag_target_indicator.hide()
        index = self.participants_layout.indexOf(self._drag_target_indicator)
        if index is not None:
            self.participants_layout.insertWidget(index, widget)
            self.orderChanged.emit(self.get_item_data())
            widget.show()
            self.participants_layout.activate()
        e.accept()    

    def _find_drop_location(self, e):
        pos = e.position()
        spacing = self.participants_layout.spacing() / 2

        for n in range(self.participants_layout.count()):
            # Get the widget at each index in turn.
            w = self.participants_layout.itemAt(n).widget()

            if self.orientation == Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = (
                    pos.y() >= w.y() - spacing
                    and pos.y() <= w.y() + w.size().height() + spacing
                )
            else:
                # Drag drop horizontally.
                drop_here = (
                    pos.x() >= w.x() - spacing
                    and pos.x() <= w.x() + w.size().width() + spacing
                )

            if drop_here:
                # Drop over this target.
                break

        return n

    def dragLeaveEvent(self, e):
        self._drag_target_indicator.hide()
        e.accept()

    def add_item(self, item):
        self.participants_layout.addWidget(item)

    def get_group_data(self) -> list:
        """
        Get the data of this group widget.
        """
        return [self.title, self.get_item_data()]

    def get_item_data(self):
        data = []
        for n in range(self.participants_layout.count()):
            # Get the widget at each index in turn.
            w = self.participants_layout.itemAt(n).widget()
            if w != self._drag_target_indicator:
                # The target indicator has no data.
                data.append(w.data)
        return data
