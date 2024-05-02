from PyQt6.QtCore import QMimeData, Qt, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QFrame,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

class DragTargetIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(25, 5, 25, 5)
        self.setStyleSheet(
            "QLabel { background-color: #ccc; border: 1px solid black; }"
        )

class GroupWidget(QWidget):
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
        self.participants_frame.setFrameShape(QFrame.StyledPanel)
        self.participants_layout = QVBoxLayout(self.participants_frame)
        layout.addWidget(self.participants_frame)
        
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
        label = DragItem(participant)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setMargin(2)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(100, 20)
        label.setScaledContents(True)
        label.setContentsMargins(5, 0, 5, 0)
        label.setAutoFillBackground(True)
        self.participants_layout.addWidget(label)
        
class DragItem(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(25, 5, 25, 5)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        # Store data separately from display label, but use label for default.
        self.data = self.text()

    def set_data(self, data):
        self.data = data

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            # Render at x2 pixel ratio to avoid blur on Retina screens.
            pixmap = QPixmap(self.size().width() * 2, self.size().height() * 2)
            pixmap.setDevicePixelRatio(2)
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)
            self.show() # Show this widget again, if it's dropped outside.

class DragWidgetController(QWidget):
    """
    Generic list sorting handler.
    """

    orderChanged = pyqtSignal(list)

    def __init__(self,  groupWidgetList:list[GroupWidget], *args, orientation=Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        # Store the orientation for drag checks later.
        self.orientation = orientation

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()

        # Add the drag target indicator. This is invisible by default,
        # we show it and move it around while the drag is active.
        self._drag_target_indicator = DragTargetIndicator()
        self.blayout.addWidget(self._drag_target_indicator)
        self._drag_target_indicator.hide()

        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dragLeaveEvent(self, e):
        self._drag_target_indicator.hide()
        e.accept()

    def dragMoveEvent(self, e):
        # Find the correct location of the drop target, so we can move it there.
        index = self._find_drop_location(e)
        if index is not None:
            # Inserting moves the item if its already in the layout.
            self.blayout.insertWidget(index, self._drag_target_indicator)
            # Hide the item being dragged.
            e.source().hide()
            # Show the target.
            self._drag_target_indicator.show()
        e.accept()

    def dropEvent(self, e):
        widget = e.source()
        # Use drop target location for destination, then remove it.
        self._drag_target_indicator.hide()
        index = self.blayout.indexOf(self._drag_target_indicator)
        if index is not None:
            self.blayout.insertWidget(index, widget)
            self.orderChanged.emit(self.get_item_data())
            widget.show()
            self.blayout.activate()
        e.accept()

    def _find_drop_location(self, e):
        pos = e.position()
        spacing = self.blayout.spacing() / 2

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()

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

    def add_item(self, item):
        self.blayout.addWidget(item)

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if w != self._drag_target_indicator:
                # The target indicator has no data.
                data.append(w.data)
        return data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dragController = DragWidgetController(orientation=Qt.Orientation.Vertical)

        # Create GroupWidgets
        groups_data = [
            ("Group 1", ["Alice", "Bob", "Charlie"]),
            ("Group 2", ["David", "Eve", "Frank"]),
            ("Group 3", ["Grace", "Henry", "Ivy"]),
            ("Group 4", ["Jack", "Kate", "Liam"]),
            ("Group 5", ["Mary", "Nathan", "Olivia"]),
            ("Group 6", ["Peter", "Queen", "Robert"])
        ]

        for n, l in enumerate(["A", "B", "C", "D"]):
            item = DragItem(l)
            item.set_data(n)  # Store the data.
            self.dragController.add_item(item)

        # Print out the changed order.
        self.dragController.orderChanged.connect(print)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.dragController)
        layout.addStretch(1)
        container.setLayout(layout)

        self.setCentralWidget(container)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


app = QApplication([])
w = MainWindow()
w.show()

app.exec()