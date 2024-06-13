from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QCheckBox

class DragWidget(QWidget):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super().__init__(parent, flags)

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

class DragLabel(QLabel, DragWidget):
    def __init__(self, person_id: int, person_name: str, parent=None):
        super().__init__(str(person_name), parent)  # Ensure text is a string
        self.person_id = person_id
        self.person_name = person_name
        # The size needs refactoring, so a drag label creates a target indicator that can be used for itself
        self.setContentsMargins(25, 5, 25, 5)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("border: 1px solid black;")
        # Store data separately from display label, but use label for default.
        self.data = (self.person_id, self.person_name)

    
    def set_data(self, data):
        self.data = data

class DragCheckbox(QCheckBox, DragWidget):
    def __init__(self, value: str, parent=None):
        QCheckBox.__init__(self, value, parent)
        DragWidget.__init__(self, parent)
        self.value = value
        self.setContentsMargins(25, 5, 25, 5)

class DragTargetIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(25, 5, 25, 5)
        self.setStyleSheet(
            "QLabel { background-color: #ccc; border: 1px solid black; }"
        )